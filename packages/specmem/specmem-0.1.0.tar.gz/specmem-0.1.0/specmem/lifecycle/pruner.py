"""Pruner engine for spec lifecycle management."""

import json
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from specmem.lifecycle.models import ArchiveMetadata, PruneResult, SpecHealthScore


if TYPE_CHECKING:
    from specmem.lifecycle.health import HealthAnalyzer
    from specmem.vectordb.base import VectorStore


class PrunerEngine:
    """Engine for pruning orphaned and stale specs.

    Supports two modes:
    - archive: Move specs to .specmem/archive/ with metadata
    - delete: Permanently remove specs

    Always supports dry-run to preview changes without making them.
    """

    def __init__(
        self,
        health_analyzer: "HealthAnalyzer",
        vector_store: "VectorStore | None" = None,
        archive_dir: Path | None = None,
    ) -> None:
        """Initialize the pruner engine.

        Args:
            health_analyzer: Health analyzer for spec analysis
            vector_store: Vector store to update after pruning
            archive_dir: Directory for archived specs
        """
        self.health_analyzer = health_analyzer
        self.vector_store = vector_store
        self.archive_dir = archive_dir or Path(".specmem/archive")

    def analyze(self) -> list[SpecHealthScore]:
        """Analyze all specs and return health scores.

        Returns:
            List of SpecHealthScore for all specs
        """
        return self.health_analyzer.analyze_all()

    def prune_orphaned(
        self,
        mode: Literal["archive", "delete"] = "archive",
        dry_run: bool = True,
        force: bool = False,
    ) -> list[PruneResult]:
        """Prune all orphaned specs (specs with no code references).

        Args:
            mode: "archive" to move to archive, "delete" to permanently remove
            dry_run: If True, only show what would be done
            force: If True, skip confirmation for delete mode

        Returns:
            List of PruneResult for each processed spec
        """
        orphaned = self.health_analyzer.get_orphaned_specs()
        return self._prune_specs(
            specs=orphaned,
            mode=mode,
            dry_run=dry_run,
            force=force,
            reason="orphaned (no code references)",
        )

    def prune_by_name(
        self,
        spec_names: list[str],
        mode: Literal["archive", "delete"] = "archive",
        dry_run: bool = True,
        force: bool = False,
    ) -> list[PruneResult]:
        """Prune specific specs by name.

        Args:
            spec_names: List of spec names/IDs to prune
            mode: "archive" to move to archive, "delete" to permanently remove
            dry_run: If True, only show what would be done
            force: If True, skip confirmation for delete mode

        Returns:
            List of PruneResult for each processed spec
        """
        results: list[PruneResult] = []

        for spec_name in spec_names:
            try:
                score = self.health_analyzer.analyze_spec(spec_name)
                result = self._prune_single_spec(
                    spec=score,
                    mode=mode,
                    dry_run=dry_run,
                    force=force,
                    reason=f"explicitly requested: {spec_name}",
                )
                results.append(result)
            except Exception as e:
                # Spec not found or error
                results.append(
                    PruneResult(
                        spec_id=spec_name,
                        spec_path=Path(spec_name),
                        action="skipped",
                        reason=f"Error: {e}",
                    )
                )

        return results

    def prune_stale(
        self,
        threshold_days: int = 90,
        mode: Literal["archive", "delete"] = "archive",
        dry_run: bool = True,
    ) -> list[PruneResult]:
        """Prune specs that haven't been updated in a while.

        Args:
            threshold_days: Days after which a spec is considered stale
            mode: "archive" to move to archive, "delete" to permanently remove
            dry_run: If True, only show what would be done

        Returns:
            List of PruneResult for each processed spec
        """
        # Update threshold in analyzer
        original_threshold = self.health_analyzer.stale_threshold_days
        self.health_analyzer.stale_threshold_days = threshold_days

        try:
            stale = self.health_analyzer.get_stale_specs()
            return self._prune_specs(
                specs=stale,
                mode=mode,
                dry_run=dry_run,
                force=False,
                reason=f"stale (not modified in {threshold_days}+ days)",
            )
        finally:
            self.health_analyzer.stale_threshold_days = original_threshold

    def _prune_specs(
        self,
        specs: list[SpecHealthScore],
        mode: Literal["archive", "delete"],
        dry_run: bool,
        force: bool,
        reason: str,
    ) -> list[PruneResult]:
        """Prune a list of specs."""
        results: list[PruneResult] = []

        for spec in specs:
            result = self._prune_single_spec(
                spec=spec,
                mode=mode,
                dry_run=dry_run,
                force=force,
                reason=reason,
            )
            results.append(result)

        return results

    def _prune_single_spec(
        self,
        spec: SpecHealthScore,
        mode: Literal["archive", "delete"],
        dry_run: bool,
        force: bool,
        reason: str,
    ) -> PruneResult:
        """Prune a single spec."""
        if dry_run:
            # Dry run - just report what would happen
            if mode == "archive":
                archive_path = self._get_archive_path(spec.spec_path)
                return PruneResult(
                    spec_id=spec.spec_id,
                    spec_path=spec.spec_path,
                    action="archived",
                    archive_path=archive_path,
                    reason=f"[DRY RUN] Would archive: {reason}",
                )
            else:
                return PruneResult(
                    spec_id=spec.spec_id,
                    spec_path=spec.spec_path,
                    action="deleted",
                    reason=f"[DRY RUN] Would delete: {reason}",
                )

        # Actual pruning
        if mode == "archive":
            return self._archive_spec(spec, reason)
        else:
            if not force:
                # In real implementation, would prompt for confirmation
                # For now, we require force flag for delete
                return PruneResult(
                    spec_id=spec.spec_id,
                    spec_path=spec.spec_path,
                    action="skipped",
                    reason="Delete requires --force flag",
                )
            return self._delete_spec(spec, reason)

    def _archive_spec(self, spec: SpecHealthScore, reason: str) -> PruneResult:
        """Archive a spec to the archive directory."""
        archive_path = self._get_archive_path(spec.spec_path)

        try:
            # Create archive directory
            archive_path.parent.mkdir(parents=True, exist_ok=True)

            # Create metadata
            metadata = ArchiveMetadata(
                original_path=str(spec.spec_path),
                archived_at=datetime.now(UTC),
                reason=reason,
                health_score=spec.score,
                code_references=spec.code_references,
                can_restore=True,
            )

            # Copy spec to archive
            if spec.spec_path.is_dir():
                shutil.copytree(spec.spec_path, archive_path)
            else:
                shutil.copy2(spec.spec_path, archive_path)

            # Write metadata
            metadata_path = (
                archive_path / ".archive_metadata.json"
                if archive_path.is_dir()
                else archive_path.with_suffix(".metadata.json")
            )
            metadata_path.write_text(json.dumps(metadata.to_dict(), indent=2))

            # Remove original
            if spec.spec_path.is_dir():
                shutil.rmtree(spec.spec_path)
            else:
                spec.spec_path.unlink()

            # Update vector store
            self._remove_from_vector_store(spec.spec_id)

            return PruneResult(
                spec_id=spec.spec_id,
                spec_path=spec.spec_path,
                action="archived",
                archive_path=archive_path,
                reason=reason,
            )
        except Exception as e:
            return PruneResult(
                spec_id=spec.spec_id,
                spec_path=spec.spec_path,
                action="skipped",
                reason=f"Archive failed: {e}",
            )

    def _delete_spec(self, spec: SpecHealthScore, reason: str) -> PruneResult:
        """Permanently delete a spec."""
        try:
            if spec.spec_path.is_dir():
                shutil.rmtree(spec.spec_path)
            else:
                spec.spec_path.unlink()

            # Update vector store
            self._remove_from_vector_store(spec.spec_id)

            return PruneResult(
                spec_id=spec.spec_id,
                spec_path=spec.spec_path,
                action="deleted",
                reason=reason,
            )
        except Exception as e:
            return PruneResult(
                spec_id=spec.spec_id,
                spec_path=spec.spec_path,
                action="skipped",
                reason=f"Delete failed: {e}",
            )

    def _get_archive_path(self, spec_path: Path) -> Path:
        """Get the archive path for a spec."""
        # Preserve directory structure under archive
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return self.archive_dir / f"{spec_path.name}_{timestamp}"

    def _remove_from_vector_store(self, spec_id: str) -> None:
        """Remove spec from vector store."""
        if self.vector_store is None:
            return

        try:
            if hasattr(self.vector_store, "delete"):
                self.vector_store.delete(spec_id)
        except Exception:
            pass  # Best effort removal
