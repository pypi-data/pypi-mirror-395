"""Coverage Engine for Spec Coverage Analysis.

Main engine that orchestrates criteria extraction, test scanning,
matching, and coverage reporting.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

from specmem.coverage.extractor import CriteriaExtractor
from specmem.coverage.matcher import CriteriaMatcher
from specmem.coverage.models import (
    AcceptanceCriterion,
    CoverageResult,
    FeatureCoverage,
    TestSuggestion,
)
from specmem.coverage.scanner import TestScanner


logger = logging.getLogger(__name__)


class CoverageEngine:
    """Main engine for spec coverage analysis.

    Orchestrates criteria extraction, test scanning, matching,
    and coverage reporting.
    """

    def __init__(self, workspace_path: Path | str) -> None:
        """Initialize the coverage engine.

        Args:
            workspace_path: Path to the workspace root
        """
        self.workspace_path = Path(workspace_path).resolve()
        self.extractor = CriteriaExtractor(workspace_path)
        self.scanner = TestScanner(workspace_path)
        self.matcher = CriteriaMatcher()

    def analyze_coverage(self) -> CoverageResult:
        """Analyze coverage for all specs.

        Returns:
            CoverageResult with all features and suggestions
        """
        # Extract all criteria
        all_criteria = self.extractor.extract_all()

        # Scan all tests
        all_tests = self.scanner.scan_tests()

        # Build feature coverage for each feature
        features: list[FeatureCoverage] = []

        for feature_name, criteria in all_criteria.items():
            feature_coverage = self._analyze_feature_criteria(feature_name, criteria, all_tests)
            features.append(feature_coverage)

        # Sort features by name
        features.sort(key=lambda f: f.feature_name)

        # Generate suggestions for uncovered criteria
        suggestions = self._generate_suggestions(features)

        return CoverageResult(features=features, suggestions=suggestions)

    def analyze_feature(self, feature_name: str) -> FeatureCoverage:
        """Analyze coverage for a specific feature.

        Args:
            feature_name: Name of the feature

        Returns:
            FeatureCoverage for the feature
        """
        # Extract criteria for this feature
        spec_path = self.workspace_path / ".kiro" / "specs" / feature_name
        criteria = self.extractor.extract_from_spec(spec_path)

        if not criteria:
            return FeatureCoverage(feature_name=feature_name, criteria=[])

        # Scan all tests
        all_tests = self.scanner.scan_tests()

        return self._analyze_feature_criteria(feature_name, criteria, all_tests)

    def _analyze_feature_criteria(
        self,
        feature_name: str,
        criteria: list[AcceptanceCriterion],
        tests: list,
    ) -> FeatureCoverage:
        """Analyze criteria for a feature against tests.

        Args:
            feature_name: Name of the feature
            criteria: List of acceptance criteria
            tests: List of extracted tests

        Returns:
            FeatureCoverage for the feature
        """
        # Match criteria to tests
        matches = self.matcher.match(criteria, tests)

        return FeatureCoverage(feature_name=feature_name, criteria=matches)

    def get_suggestions(
        self,
        feature_name: str | None = None,
    ) -> list[TestSuggestion]:
        """Get test suggestions for uncovered criteria.

        Args:
            feature_name: Optional feature to get suggestions for

        Returns:
            List of TestSuggestion objects
        """
        if feature_name:
            coverage = self.analyze_feature(feature_name)
            features = [coverage]
        else:
            result = self.analyze_coverage()
            features = result.features

        return self._generate_suggestions(features)

    def _generate_suggestions(
        self,
        features: list[FeatureCoverage],
    ) -> list[TestSuggestion]:
        """Generate test suggestions for uncovered criteria.

        Args:
            features: List of feature coverage data

        Returns:
            List of TestSuggestion objects
        """
        suggestions: list[TestSuggestion] = []

        for feature in features:
            for match in feature.criteria:
                if not match.is_covered:
                    suggestion = self._create_suggestion(match.criterion)
                    suggestions.append(suggestion)

        return suggestions

    def _create_suggestion(
        self,
        criterion: AcceptanceCriterion,
    ) -> TestSuggestion:
        """Create a test suggestion for an uncovered criterion.

        Args:
            criterion: The uncovered acceptance criterion

        Returns:
            TestSuggestion with recommended test approach
        """
        # Generate suggested test file path
        feature_name = criterion.feature_name.replace("-", "_")
        suggested_file = f"tests/test_{feature_name}.py"

        # Generate suggested test name from criterion
        suggested_name = self._generate_test_name(criterion)

        # Generate verification points from criterion text
        verification_points = self._extract_verification_points(criterion.text)

        return TestSuggestion(
            criterion=criterion,
            suggested_file=suggested_file,
            suggested_name=suggested_name,
            verification_points=verification_points,
        )

    def _generate_test_name(self, criterion: AcceptanceCriterion) -> str:
        """Generate a test function name from criterion.

        Args:
            criterion: Acceptance criterion

        Returns:
            Suggested test function name
        """
        # Extract key action from criterion text
        text = criterion.text.lower()

        # Try to extract the main action
        # Look for patterns like "WHEN X THEN Y" or "SHALL X"
        action = ""

        when_match = re.search(r"when\s+(.+?)\s+then", text)
        if when_match:
            action = when_match.group(1)
        else:
            shall_match = re.search(r"shall\s+(.+?)(?:\s+and|\s+or|$)", text)
            if shall_match:
                action = shall_match.group(1)

        if action:
            # Clean up and convert to snake_case
            action = re.sub(r"[^a-z0-9\s]", "", action)
            action = "_".join(action.split()[:5])  # Limit to 5 words
            return f"test_{action}"

        # Fallback: use criterion number
        return f"test_criterion_{criterion.number.replace('.', '_')}"

    def _extract_verification_points(self, text: str) -> list[str]:
        """Extract verification points from criterion text.

        Args:
            text: Criterion text

        Returns:
            List of verification points
        """
        points: list[str] = []

        # Extract THEN clause
        then_match = re.search(r"then\s+(.+)", text, re.IGNORECASE)
        if then_match:
            then_clause = then_match.group(1)
            # Split by "and" or "or"
            parts = re.split(r"\s+and\s+|\s+or\s+", then_clause, flags=re.IGNORECASE)
            for part in parts:
                part = part.strip()
                if part:
                    points.append(f"Verify: {part}")

        # If no THEN clause, use the whole text
        if not points:
            points.append(f"Verify: {text[:100]}...")

        return points

    def generate_badge(self) -> str:
        """Generate coverage badge markdown.

        Returns:
            Badge markdown string
        """
        result = self.analyze_coverage()
        return result.generate_badge()

    def export(self, format: str = "json") -> str:
        """Export coverage data in specified format.

        Args:
            format: Export format ("json" or "markdown")

        Returns:
            Exported data as string
        """
        result = self.analyze_coverage()

        if format == "markdown":
            return result.to_markdown()
        else:
            return result.to_json()
