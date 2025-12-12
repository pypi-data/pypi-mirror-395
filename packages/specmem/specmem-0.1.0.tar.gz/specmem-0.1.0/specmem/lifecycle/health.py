"""Health analyzer for spec lifecycle management."""

from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING

from specmem.lifecycle.models import SpecHealthScore, calculate_health_score


if TYPE_CHECKING:
    from specmem.impact.graph import SpecImpactGraph
    from specmem.vectordb.base import VectorStore


class HealthAnalyzer:
    """Analyzes spec health based on code references, freshness, and usage.

    The health analyzer calculates scores for specs based on:
    - Code references: How many code files reference this spec
    - Freshness: How recently the spec was modified
    - Usage: How often the spec is queried

    Specs with low health scores are candidates for pruning.
    """

    def __init__(
        self,
        impact_graph: "SpecImpactGraph | None" = None,
        vector_store: "VectorStore | None" = None,
        stale_threshold_days: int = 90,
        spec_base_path: Path | None = None,
    ) -> None:
        """Initialize the health analyzer.

        Args:
            impact_graph: The spec impact graph for code references
            vector_store: Vector store for query counts
            stale_threshold_days: Days after which a spec is considered stale
            spec_base_path: Base path for spec files
        """
        self.impact_graph = impact_graph
        self.vector_store = vector_store
        self.stale_threshold_days = stale_threshold_days
        self.spec_base_path = spec_base_path or Path(".kiro/specs")
        self._query_counts: dict[str, int] = {}

    def analyze_spec(self, spec_id: str, spec_path: Path | None = None) -> SpecHealthScore:
        """Analyze health of a single spec.

        Args:
            spec_id: Unique identifier for the spec
            spec_path: Path to the spec file (optional, will be inferred)

        Returns:
            SpecHealthScore with calculated metrics
        """
        # Determine spec path
        if spec_path is None:
            spec_path = self.spec_base_path / spec_id

        # Get code references from impact graph
        code_references = self._get_code_references(spec_id)

        # Get last modified time
        last_modified = self._get_last_modified(spec_path)

        # Calculate days since modified
        now = datetime.now(UTC)
        if last_modified.tzinfo is None:
            last_modified = last_modified.replace(tzinfo=UTC)
        days_since_modified = (now - last_modified).days

        # Get query count
        query_count = self._query_counts.get(spec_id, 0)

        # Calculate health score
        score = calculate_health_score(
            code_references=code_references,
            days_since_modified=days_since_modified,
            query_count=query_count,
            stale_threshold=self.stale_threshold_days,
        )

        # Determine status flags
        is_orphaned = code_references == 0
        is_stale = days_since_modified > self.stale_threshold_days

        # Generate recommendations
        recommendations = self._generate_recommendations(
            code_references=code_references,
            days_since_modified=days_since_modified,
            is_orphaned=is_orphaned,
            is_stale=is_stale,
        )

        return SpecHealthScore(
            spec_id=spec_id,
            spec_path=spec_path,
            score=score,
            code_references=code_references,
            last_modified=last_modified,
            query_count=query_count,
            is_orphaned=is_orphaned,
            is_stale=is_stale,
            recommendations=recommendations,
        )

    def analyze_all(self) -> list[SpecHealthScore]:
        """Analyze health of all indexed specs.

        Returns:
            List of SpecHealthScore for all specs
        """
        specs = self._discover_specs()
        return [self.analyze_spec(spec_id, spec_path) for spec_id, spec_path in specs]

    def get_orphaned_specs(self) -> list[SpecHealthScore]:
        """Get all specs with no code references.

        Returns:
            List of SpecHealthScore for orphaned specs
        """
        all_scores = self.analyze_all()
        return [s for s in all_scores if s.is_orphaned]

    def get_stale_specs(self) -> list[SpecHealthScore]:
        """Get all specs that haven't been updated recently.

        Returns:
            List of SpecHealthScore for stale specs
        """
        all_scores = self.analyze_all()
        return [s for s in all_scores if s.is_stale]

    def get_summary(self) -> dict[str, int | float]:
        """Get summary statistics for all specs.

        Returns:
            Dictionary with total, orphaned, stale counts and average score
        """
        all_scores = self.analyze_all()

        if not all_scores:
            return {
                "total_specs": 0,
                "orphaned_count": 0,
                "stale_count": 0,
                "average_score": 0.0,
            }

        orphaned = sum(1 for s in all_scores if s.is_orphaned)
        stale = sum(1 for s in all_scores if s.is_stale)
        avg_score = sum(s.score for s in all_scores) / len(all_scores)

        return {
            "total_specs": len(all_scores),
            "orphaned_count": orphaned,
            "stale_count": stale,
            "average_score": round(avg_score, 2),
        }

    def record_query(self, spec_id: str) -> None:
        """Record a query for a spec (for usage tracking).

        Args:
            spec_id: The spec that was queried
        """
        self._query_counts[spec_id] = self._query_counts.get(spec_id, 0) + 1

    def _get_code_references(self, spec_id: str) -> int:
        """Get number of code files referencing a spec."""
        if self.impact_graph is None:
            return 0

        try:
            # Try to get references from impact graph
            if hasattr(self.impact_graph, "get_code_for_spec"):
                refs = self.impact_graph.get_code_for_spec(spec_id)
                return len(refs) if refs else 0
            return 0
        except Exception:
            return 0

    def _get_last_modified(self, spec_path: Path) -> datetime:
        """Get last modified time for a spec."""
        try:
            if spec_path.exists():
                stat = spec_path.stat()
                return datetime.fromtimestamp(stat.st_mtime, tz=UTC)
            elif spec_path.is_dir():
                # For directories, find the most recent file
                latest = datetime.min.replace(tzinfo=UTC)
                for f in spec_path.rglob("*.md"):
                    mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=UTC)
                    latest = max(latest, mtime)
                return latest if latest > datetime.min.replace(tzinfo=UTC) else datetime.now(UTC)
        except Exception:
            pass
        return datetime.now(UTC)

    def _discover_specs(self) -> list[tuple[str, Path]]:
        """Discover all specs in the base path."""
        specs: list[tuple[str, Path]] = []

        if not self.spec_base_path.exists():
            return specs

        # Look for spec directories (each subdirectory is a spec)
        for item in self.spec_base_path.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                spec_id = item.name
                specs.append((spec_id, item))

        return specs

    def _generate_recommendations(
        self,
        code_references: int,
        days_since_modified: int,
        is_orphaned: bool,
        is_stale: bool,
    ) -> list[str]:
        """Generate recommendations based on spec health."""
        recommendations: list[str] = []

        if is_orphaned:
            recommendations.append("Consider archiving: no code references found")

        if is_stale:
            recommendations.append(f"Spec is stale: not modified in {days_since_modified} days")

        if code_references == 0 and not is_orphaned:
            recommendations.append("Link spec to code files for better tracking")

        if code_references > 0 and is_stale:
            recommendations.append("Review and update: code references exist but spec is outdated")

        return recommendations
