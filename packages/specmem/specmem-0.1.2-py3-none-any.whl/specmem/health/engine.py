"""Health Score Engine implementation."""

import logging
from datetime import datetime, timedelta
from pathlib import Path

from specmem.health.models import (
    DEFAULT_WEIGHTS,
    HealthScore,
    ScoreBreakdown,
    ScoreCategory,
)


logger = logging.getLogger(__name__)


class HealthScoreEngine:
    """Engine for calculating project specification health scores.

    The health score is a weighted average of four categories:
    - Coverage: How well acceptance criteria are covered by tests
    - Validation: How many validation issues exist in specs
    - Freshness: How recently specs have been updated
    - Completeness: How complete the spec structure is
    """

    def __init__(
        self,
        workspace_path: Path,
        weights: dict[ScoreCategory, float] | None = None,
    ):
        """Initialize the health score engine.

        Args:
            workspace_path: Path to the workspace root
            weights: Optional custom weights for categories (must sum to 1)
        """
        self.workspace_path = workspace_path
        self.weights = weights or DEFAULT_WEIGHTS

    def calculate(self) -> HealthScore:
        """Calculate the overall health score for the project.

        Returns:
            HealthScore with overall score, grade, breakdown, and suggestions
        """
        breakdown = []

        # Calculate each category score
        coverage_score = self._calculate_coverage_score()
        breakdown.append(coverage_score)

        validation_score = self._calculate_validation_score()
        breakdown.append(validation_score)

        freshness_score = self._calculate_freshness_score()
        breakdown.append(freshness_score)

        completeness_score = self._calculate_completeness_score()
        breakdown.append(completeness_score)

        # Calculate weighted overall score
        overall = sum(item.weighted_score() for item in breakdown)

        # Get letter grade
        grade = HealthScore.score_to_grade(overall)

        # Generate suggestions for improvement
        suggestions = self._generate_suggestions(breakdown, grade)

        # Count specs and features
        spec_count, feature_count = self._count_specs()

        return HealthScore(
            overall_score=overall,
            letter_grade=grade,
            breakdown=breakdown,
            suggestions=suggestions,
            spec_count=spec_count,
            feature_count=feature_count,
        )

    def _calculate_coverage_score(self) -> ScoreBreakdown:
        """Calculate coverage score based on test coverage of acceptance criteria."""
        try:
            from specmem.coverage.engine import CoverageEngine

            engine = CoverageEngine(self.workspace_path)
            result = engine.analyze_coverage()

            score = result.coverage_percentage
            details = f"{result.covered_criteria}/{result.total_criteria} criteria covered"

        except Exception as e:
            logger.warning(f"Coverage calculation failed: {e}")
            score = 100.0  # Default to 100 if no criteria exist
            details = "No acceptance criteria found"

        return ScoreBreakdown(
            category=ScoreCategory.COVERAGE,
            score=score,
            weight=self.weights[ScoreCategory.COVERAGE],
            details=details,
        )

    def _calculate_validation_score(self) -> ScoreBreakdown:
        """Calculate validation score based on spec quality issues."""
        try:
            from specmem.validator.engine import SpecValidator

            validator = SpecValidator(self.workspace_path)
            results = validator.validate_all()

            # Count issues by severity
            errors = sum(1 for r in results for i in r.issues if i.severity == "error")
            warnings = sum(1 for r in results for i in r.issues if i.severity == "warning")

            # Score: start at 100, subtract for issues
            # Errors: -10 each, Warnings: -3 each
            penalty = (errors * 10) + (warnings * 3)
            score = max(0, 100 - penalty)
            details = f"{errors} errors, {warnings} warnings"

        except Exception as e:
            logger.warning(f"Validation calculation failed: {e}")
            score = 100.0
            details = "Validation not available"

        return ScoreBreakdown(
            category=ScoreCategory.VALIDATION,
            score=score,
            weight=self.weights[ScoreCategory.VALIDATION],
            details=details,
        )

    def _calculate_freshness_score(self) -> ScoreBreakdown:
        """Calculate freshness score based on spec file modification times."""
        specs_dir = self.workspace_path / ".kiro" / "specs"

        if not specs_dir.exists():
            return ScoreBreakdown(
                category=ScoreCategory.FRESHNESS,
                score=100.0,
                weight=self.weights[ScoreCategory.FRESHNESS],
                details="No specs directory found",
            )

        now = datetime.now()
        stale_threshold = timedelta(days=30)
        very_stale_threshold = timedelta(days=90)

        total_files = 0
        fresh_files = 0
        stale_files = 0
        very_stale_files = 0

        for spec_file in specs_dir.rglob("*.md"):
            total_files += 1
            mtime = datetime.fromtimestamp(spec_file.stat().st_mtime)
            age = now - mtime

            if age < stale_threshold:
                fresh_files += 1
            elif age < very_stale_threshold:
                stale_files += 1
            else:
                very_stale_files += 1

        if total_files == 0:
            return ScoreBreakdown(
                category=ScoreCategory.FRESHNESS,
                score=100.0,
                weight=self.weights[ScoreCategory.FRESHNESS],
                details="No spec files found",
            )

        # Score: 100% fresh = 100, stale = -20 each, very stale = -40 each
        fresh_ratio = fresh_files / total_files
        stale_penalty = (stale_files / total_files) * 20
        very_stale_penalty = (very_stale_files / total_files) * 40

        score = max(0, (fresh_ratio * 100) - stale_penalty - very_stale_penalty)
        details = f"{fresh_files} fresh, {stale_files} stale, {very_stale_files} very stale"

        return ScoreBreakdown(
            category=ScoreCategory.FRESHNESS,
            score=score,
            weight=self.weights[ScoreCategory.FRESHNESS],
            details=details,
        )

    def _calculate_completeness_score(self) -> ScoreBreakdown:
        """Calculate completeness score based on spec structure."""
        specs_dir = self.workspace_path / ".kiro" / "specs"

        if not specs_dir.exists():
            return ScoreBreakdown(
                category=ScoreCategory.COMPLETENESS,
                score=0.0,
                weight=self.weights[ScoreCategory.COMPLETENESS],
                details="No specs directory found",
            )

        total_features = 0
        complete_features = 0
        missing_parts: list[str] = []

        for feature_dir in specs_dir.iterdir():
            if not feature_dir.is_dir():
                continue

            total_features += 1
            has_requirements = (feature_dir / "requirements.md").exists()
            has_design = (feature_dir / "design.md").exists()
            has_tasks = (feature_dir / "tasks.md").exists()

            if has_requirements and has_design and has_tasks:
                complete_features += 1
            else:
                missing = []
                if not has_requirements:
                    missing.append("requirements")
                if not has_design:
                    missing.append("design")
                if not has_tasks:
                    missing.append("tasks")
                missing_parts.append(f"{feature_dir.name}: {', '.join(missing)}")

        if total_features == 0:
            return ScoreBreakdown(
                category=ScoreCategory.COMPLETENESS,
                score=0.0,
                weight=self.weights[ScoreCategory.COMPLETENESS],
                details="No feature specs found",
            )

        score = (complete_features / total_features) * 100
        details = f"{complete_features}/{total_features} features complete"

        return ScoreBreakdown(
            category=ScoreCategory.COMPLETENESS,
            score=score,
            weight=self.weights[ScoreCategory.COMPLETENESS],
            details=details,
        )

    def _generate_suggestions(self, breakdown: list[ScoreBreakdown], grade: str) -> list[str]:
        """Generate actionable suggestions based on scores."""
        suggestions = []

        # Only generate suggestions if grade is below B
        if grade in ("A", "B"):
            return suggestions

        for item in breakdown:
            if item.score < 80:
                if item.category == ScoreCategory.COVERAGE:
                    suggestions.append(
                        f"Improve test coverage: {item.details}. "
                        "Run 'specmem cov' to see uncovered criteria."
                    )
                elif item.category == ScoreCategory.VALIDATION:
                    suggestions.append(
                        f"Fix validation issues: {item.details}. "
                        "Run 'specmem validate' to see details."
                    )
                elif item.category == ScoreCategory.FRESHNESS:
                    suggestions.append(
                        f"Update stale specs: {item.details}. "
                        "Review and update specs that haven't changed in 30+ days."
                    )
                elif item.category == ScoreCategory.COMPLETENESS:
                    suggestions.append(
                        f"Complete spec structure: {item.details}. "
                        "Ensure each feature has requirements.md, design.md, and tasks.md."
                    )

        return suggestions

    def _count_specs(self) -> tuple[int, int]:
        """Count total specs and features."""
        specs_dir = self.workspace_path / ".kiro" / "specs"

        if not specs_dir.exists():
            return 0, 0

        spec_count = len(list(specs_dir.rglob("*.md")))
        feature_count = sum(1 for d in specs_dir.iterdir() if d.is_dir())

        return spec_count, feature_count
