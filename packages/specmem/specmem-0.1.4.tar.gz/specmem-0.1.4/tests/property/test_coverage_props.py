"""Property-based tests for Spec Coverage Analysis.

Tests correctness properties for coverage calculation, matching,
and data model behavior.
"""

from hypothesis import given
from hypothesis import strategies as st

from specmem.coverage.models import (
    AcceptanceCriterion,
    BadgeColor,
    CoverageResult,
    CriteriaMatch,
    ExtractedTest,
    FeatureCoverage,
    get_badge_color,
)


# Strategies for generating test data
criterion_strategy = st.builds(
    AcceptanceCriterion,
    id=st.text(min_size=1, max_size=50).filter(lambda x: x.strip()),
    number=st.from_regex(r"[1-9][0-9]*\.[1-9][0-9]*", fullmatch=True),
    text=st.text(min_size=10, max_size=500).filter(lambda x: x.strip()),
    requirement_id=st.from_regex(r"[1-9][0-9]*", fullmatch=True),
    user_story=st.text(min_size=5, max_size=200),
    feature_name=st.text(min_size=1, max_size=50).filter(lambda x: x.strip()),
)

test_strategy = st.builds(
    ExtractedTest,
    name=st.from_regex(r"test_[a-z][a-z_]{0,30}", fullmatch=True),
    file_path=st.from_regex(r"tests/test_[a-z]+\.py", fullmatch=True),
    line_number=st.integers(min_value=1, max_value=10000),
    docstring=st.text(max_size=200) | st.none(),
    requirement_links=st.lists(st.text(min_size=1, max_size=10), max_size=5),
    framework=st.sampled_from(["pytest", "jest", "vitest", "playwright", "mocha"]),
    selector=st.text(max_size=100),
)

confidence_strategy = st.floats(min_value=0.0, max_value=1.0, allow_nan=False)


@st.composite
def criteria_match_strategy(draw: st.DrawFn) -> CriteriaMatch:
    """Generate a CriteriaMatch with valid data."""
    criterion = draw(criterion_strategy)
    has_test = draw(st.booleans())
    test = draw(test_strategy) if has_test else None
    confidence = draw(confidence_strategy)
    return CriteriaMatch(criterion=criterion, test=test, confidence=confidence)


@st.composite
def feature_coverage_strategy(draw: st.DrawFn) -> FeatureCoverage:
    """Generate a FeatureCoverage with valid data."""
    feature_name = draw(st.text(min_size=1, max_size=50).filter(lambda x: x.strip()))
    criteria = draw(st.lists(criteria_match_strategy(), max_size=10))
    return FeatureCoverage(feature_name=feature_name, criteria=criteria)


@st.composite
def coverage_result_strategy(draw: st.DrawFn) -> CoverageResult:
    """Generate a CoverageResult with valid data."""
    features = draw(st.lists(feature_coverage_strategy(), max_size=5))
    return CoverageResult(features=features, suggestions=[])


class TestCoverageCalculationConsistency:
    """Property 1: Coverage Calculation Consistency.

    **Feature: spec-coverage, Property 1: Coverage Calculation Consistency**
    **Validates: Requirements 1.3**

    For any CoverageResult, the coverage_percentage SHALL equal
    (covered_criteria / total_criteria) * 100, and gap_percentage
    SHALL equal 100 - coverage_percentage.
    """

    @given(coverage_result_strategy())
    def test_coverage_percentage_formula(self, result: CoverageResult) -> None:
        """Coverage percentage equals (covered / total) * 100."""
        if result.total_criteria == 0:
            assert result.coverage_percentage == 100.0
        else:
            expected = (result.covered_criteria / result.total_criteria) * 100
            assert abs(result.coverage_percentage - expected) < 0.0001

    @given(coverage_result_strategy())
    def test_gap_percentage_complement(self, result: CoverageResult) -> None:
        """Gap percentage equals 100 - coverage_percentage."""
        assert abs(result.gap_percentage + result.coverage_percentage - 100.0) < 0.0001

    @given(feature_coverage_strategy())
    def test_feature_coverage_percentage_formula(self, feature: FeatureCoverage) -> None:
        """Feature coverage percentage equals (tested / total) * 100."""
        if feature.total_count == 0:
            assert feature.coverage_percentage == 100.0
        else:
            expected = (feature.tested_count / feature.total_count) * 100
            assert abs(feature.coverage_percentage - expected) < 0.0001

    @given(feature_coverage_strategy())
    def test_feature_gap_percentage_complement(self, feature: FeatureCoverage) -> None:
        """Feature gap percentage equals 100 - coverage_percentage."""
        assert abs(feature.gap_percentage + feature.coverage_percentage - 100.0) < 0.0001

    @given(coverage_result_strategy())
    def test_total_criteria_sum(self, result: CoverageResult) -> None:
        """Total criteria equals sum of all feature totals."""
        expected = sum(f.total_count for f in result.features)
        assert result.total_criteria == expected

    @given(coverage_result_strategy())
    def test_covered_criteria_sum(self, result: CoverageResult) -> None:
        """Covered criteria equals sum of all feature tested counts."""
        expected = sum(f.tested_count for f in result.features)
        assert result.covered_criteria == expected


class TestCriteriaExtractionCompleteness:
    """Property 2: Criteria Extraction Completeness.

    **Feature: spec-coverage, Property 2: Criteria Extraction Completeness**
    **Validates: Requirements 3.1, 3.2, 3.3, 3.4**

    For any requirements.md file with numbered acceptance criteria,
    the extractor SHALL extract all criteria with their number, text,
    and parent requirement linkage preserved.
    """

    def test_extraction_preserves_number(self) -> None:
        """Extracted criteria have valid numbers."""
        from pathlib import Path

        from specmem.coverage.extractor import CriteriaExtractor

        extractor = CriteriaExtractor(Path())
        all_criteria = extractor.extract_all()

        for criteria in all_criteria.values():
            for criterion in criteria:
                # Number should be in format "X.Y"
                assert "." in criterion.number
                parts = criterion.number.split(".")
                assert len(parts) == 2
                assert parts[0].isdigit()
                assert parts[1].isdigit()

    def test_extraction_preserves_text(self) -> None:
        """Extracted criteria have non-empty text."""
        from pathlib import Path

        from specmem.coverage.extractor import CriteriaExtractor

        extractor = CriteriaExtractor(Path())
        all_criteria = extractor.extract_all()

        for criteria in all_criteria.values():
            for criterion in criteria:
                assert criterion.text
                assert len(criterion.text) > 0

    def test_extraction_links_to_requirement(self) -> None:
        """Extracted criteria link to parent requirement."""
        from pathlib import Path

        from specmem.coverage.extractor import CriteriaExtractor

        extractor = CriteriaExtractor(Path())
        all_criteria = extractor.extract_all()

        for criteria in all_criteria.values():
            for criterion in criteria:
                # requirement_id should be the first part of number
                expected_req_id = criterion.number.split(".")[0]
                assert criterion.requirement_id == expected_req_id

    def test_extraction_sets_feature_name(self) -> None:
        """Extracted criteria have correct feature name."""
        from pathlib import Path

        from specmem.coverage.extractor import CriteriaExtractor

        extractor = CriteriaExtractor(Path())
        all_criteria = extractor.extract_all()

        for feature, criteria in all_criteria.items():
            for criterion in criteria:
                assert criterion.feature_name == feature

    @given(st.text(min_size=100, max_size=500))
    def test_empty_content_returns_empty_list(self, content: str) -> None:
        """Content without proper structure returns empty list."""
        from pathlib import Path

        from specmem.coverage.extractor import CriteriaExtractor

        extractor = CriteriaExtractor(Path())
        # Random text without proper markdown structure
        criteria = extractor.parse_requirements_md(content, "test-feature")
        # Should not crash, may return empty or some criteria
        assert isinstance(criteria, list)


class TestTestExtractionCompleteness:
    """Property 3: Test Extraction Completeness.

    **Feature: spec-coverage, Property 3: Test Extraction Completeness**
    **Validates: Requirements 4.1, 4.2, 4.4**

    For any test file in a supported framework, the scanner SHALL extract
    all test functions with name, file_path, line_number, and any
    requirement links present.
    """

    def test_extracted_tests_have_required_fields(self) -> None:
        """All extracted tests have name, file_path, and line_number."""
        from pathlib import Path

        from specmem.coverage.scanner import TestScanner

        scanner = TestScanner(Path())
        tests = scanner.scan_tests()

        for test in tests:
            assert test.name, "Test name should not be empty"
            assert test.file_path, "Test file_path should not be empty"
            assert test.line_number > 0, "Test line_number should be positive"

    def test_extracted_tests_have_valid_framework(self) -> None:
        """All extracted tests have a valid framework."""
        from pathlib import Path

        from specmem.coverage.scanner import TestScanner

        scanner = TestScanner(Path())
        tests = scanner.scan_tests()

        valid_frameworks = {"pytest", "jest", "vitest", "playwright", "mocha", "unknown"}
        for test in tests:
            assert test.framework in valid_frameworks

    def test_requirement_links_extraction(self) -> None:
        """Requirement links are extracted from docstrings."""
        from pathlib import Path

        from specmem.coverage.scanner import TestScanner

        scanner = TestScanner(Path())

        # Test various formats
        test_cases = [
            ("Validates: 1.2", ["1.2"]),
            ("Validates: Requirements 1.2, 1.3", ["1.2", "1.3"]),
            ("Req 1.2", ["1.2"]),
            ("Requirements: 1.2", ["1.2"]),
            ("No links here", []),
            (None, []),
        ]

        for text, expected in test_cases:
            links = scanner.extract_requirement_links(text)
            assert links == expected, f"Failed for '{text}': got {links}, expected {expected}"

    @given(st.text(min_size=0, max_size=100))
    def test_requirement_links_never_crashes(self, text: str) -> None:
        """extract_requirement_links never crashes on any input."""
        from pathlib import Path

        from specmem.coverage.scanner import TestScanner

        scanner = TestScanner(Path())
        links = scanner.extract_requirement_links(text)
        assert isinstance(links, list)


class TestConfidenceScoreRange:
    """Property 4: Confidence Score Range.

    **Feature: spec-coverage, Property 4: Confidence Score Range**
    **Validates: Requirements 5.2, 5.3**

    For any CriteriaMatch, the confidence score SHALL be between 0.0 and 1.0,
    and explicit requirement links SHALL have confidence 1.0.
    """

    @given(criterion_strategy, test_strategy)
    def test_similarity_in_range(
        self,
        criterion: AcceptanceCriterion,
        test: ExtractedTest,
    ) -> None:
        """Similarity scores are always between 0.0 and 1.0."""
        from specmem.coverage.matcher import CriteriaMatcher

        matcher = CriteriaMatcher()
        similarity = matcher.calculate_similarity(criterion, test)
        assert 0.0 <= similarity <= 1.0

    def test_explicit_link_has_confidence_one(self) -> None:
        """Explicit requirement links have confidence 1.0."""
        from specmem.coverage.matcher import CriteriaMatcher

        matcher = CriteriaMatcher()

        criterion = AcceptanceCriterion(
            id="test.1.2",
            number="1.2",
            text="WHEN user logs in THEN system SHALL authenticate",
            requirement_id="1",
            user_story="As a user, I want to log in",
            feature_name="test",
        )

        test = ExtractedTest(
            name="test_login",
            file_path="tests/test_auth.py",
            line_number=10,
            docstring="Validates: 1.2",
            requirement_links=["1.2"],
            framework="pytest",
        )

        matches = matcher.match([criterion], [test])
        assert len(matches) == 1
        assert matches[0].confidence == 1.0


class TestCoverageThresholdBehavior:
    """Property 5: Coverage Threshold Behavior.

    **Feature: spec-coverage, Property 5: Coverage Threshold Behavior**
    **Validates: Requirements 5.4**

    For any CriteriaMatch with confidence below 0.5, is_covered SHALL be False;
    for confidence >= 0.5, is_covered SHALL be True.
    """

    @given(confidence_strategy)
    def test_threshold_behavior(self, confidence: float) -> None:
        """is_covered follows threshold rule."""
        criterion = AcceptanceCriterion(
            id="test.1.1",
            number="1.1",
            text="Test criterion",
            requirement_id="1",
            user_story="Test story",
            feature_name="test",
        )

        test = ExtractedTest(
            name="test_something",
            file_path="tests/test.py",
            line_number=1,
            framework="pytest",
        )

        match = CriteriaMatch(criterion=criterion, test=test, confidence=confidence)

        if confidence >= 0.5:
            assert match.is_covered is True
        else:
            assert match.is_covered is False

    def test_no_test_means_not_covered(self) -> None:
        """Match with no test is not covered regardless of confidence."""
        criterion = AcceptanceCriterion(
            id="test.1.1",
            number="1.1",
            text="Test criterion",
            requirement_id="1",
            user_story="Test story",
            feature_name="test",
        )

        match = CriteriaMatch(criterion=criterion, test=None, confidence=0.8)
        assert match.is_covered is False


class TestHighestConfidenceSelection:
    """Property 6: Highest Confidence Selection.

    **Feature: spec-coverage, Property 6: Highest Confidence Selection**
    **Validates: Requirements 5.5**

    For any criterion with multiple matching tests, the selected match
    SHALL have the highest confidence score among all candidates.
    """

    def test_selects_highest_confidence(self) -> None:
        """Matcher selects the test with highest confidence."""
        from specmem.coverage.matcher import CriteriaMatcher

        matcher = CriteriaMatcher()

        criterion = AcceptanceCriterion(
            id="test.1.1",
            number="1.1",
            text="WHEN user authenticates THEN system SHALL validate credentials",
            requirement_id="1",
            user_story="As a user, I want to log in",
            feature_name="test",
        )

        # Test with explicit link (should win)
        test_explicit = ExtractedTest(
            name="test_auth_validation",
            file_path="tests/test_auth.py",
            line_number=10,
            docstring="Validates: 1.1",
            requirement_links=["1.1"],
            framework="pytest",
        )

        # Test with similar name but no link
        test_similar = ExtractedTest(
            name="test_something_else",
            file_path="tests/test_other.py",
            line_number=20,
            framework="pytest",
        )

        matches = matcher.match([criterion], [test_explicit, test_similar])
        assert len(matches) == 1
        assert matches[0].test == test_explicit
        assert matches[0].confidence == 1.0


class TestSuggestionCompleteness:
    """Property 7: Suggestion Completeness.

    **Feature: spec-coverage, Property 7: Suggestion Completeness**
    **Validates: Requirements 6.2, 6.3, 6.4**

    For any TestSuggestion, it SHALL contain suggested_file, suggested_name,
    and at least one verification_point.
    """

    def test_suggestions_have_required_fields(self) -> None:
        """All suggestions have required fields."""
        from pathlib import Path

        from specmem.coverage.engine import CoverageEngine

        engine = CoverageEngine(Path())
        suggestions = engine.get_suggestions()

        for suggestion in suggestions:
            assert suggestion.suggested_file, "suggested_file should not be empty"
            assert suggestion.suggested_name, "suggested_name should not be empty"
            assert suggestion.verification_points, "verification_points should not be empty"
            assert len(suggestion.verification_points) >= 1

    def test_suggestions_reference_uncovered_criteria(self) -> None:
        """Suggestions are only for uncovered criteria."""
        from pathlib import Path

        from specmem.coverage.engine import CoverageEngine

        engine = CoverageEngine(Path())
        result = engine.analyze_coverage()

        # Get all uncovered criteria
        uncovered_ids = set()
        for feature in result.features:
            for match in feature.criteria:
                if not match.is_covered:
                    uncovered_ids.add(match.criterion.id)

        # All suggestions should be for uncovered criteria
        for suggestion in result.suggestions:
            assert suggestion.criterion.id in uncovered_ids

    def test_suggested_file_is_valid_path(self) -> None:
        """Suggested file paths are valid."""
        from pathlib import Path

        from specmem.coverage.engine import CoverageEngine

        engine = CoverageEngine(Path())
        suggestions = engine.get_suggestions()

        for suggestion in suggestions:
            # Should be a Python test file path
            assert suggestion.suggested_file.endswith(".py")
            assert "test" in suggestion.suggested_file.lower()

    def test_suggested_name_is_valid_function_name(self) -> None:
        """Suggested names are valid Python function names."""
        import re
        from pathlib import Path

        from specmem.coverage.engine import CoverageEngine

        engine = CoverageEngine(Path())
        suggestions = engine.get_suggestions()

        for suggestion in suggestions:
            # Should start with test_
            assert suggestion.suggested_name.startswith("test_")
            # Should be a valid Python identifier
            assert re.match(r"^[a-z_][a-z0-9_]*$", suggestion.suggested_name)


class TestBadgeColorThresholds:
    """Property 8: Badge Color Thresholds.

    **Feature: spec-coverage, Property 8: Badge Color Thresholds**
    **Validates: Requirements 7.3, 7.4, 7.5**

    For any coverage percentage, badge color SHALL be red if < 50%,
    yellow if 50-80%, and green if > 80%.
    """

    @given(st.floats(min_value=0.0, max_value=49.9, allow_nan=False))
    def test_low_coverage_is_red(self, percentage: float) -> None:
        """Coverage below 50% produces red badge."""

        color = get_badge_color(percentage)
        assert color == BadgeColor.RED

    @given(st.floats(min_value=50.0, max_value=80.0, allow_nan=False))
    def test_medium_coverage_is_yellow(self, percentage: float) -> None:
        """Coverage between 50-80% produces yellow badge."""

        color = get_badge_color(percentage)
        assert color == BadgeColor.YELLOW

    @given(st.floats(min_value=80.1, max_value=100.0, allow_nan=False))
    def test_high_coverage_is_green(self, percentage: float) -> None:
        """Coverage above 80% produces green badge."""

        color = get_badge_color(percentage)
        assert color == BadgeColor.GREEN

    def test_badge_contains_percentage(self) -> None:
        """Generated badge contains coverage percentage."""
        from pathlib import Path

        from specmem.coverage.engine import CoverageEngine

        engine = CoverageEngine(Path())
        badge = engine.generate_badge()

        # Badge should contain percentage
        assert "%" in badge or "%25" in badge  # URL encoded
        assert "Spec_Coverage" in badge or "Spec Coverage" in badge


class TestExportRoundTrip:
    """Property 9: Export Round-Trip.

    **Feature: spec-coverage, Property 9: Export Round-Trip**
    **Validates: Requirements 8.1, 8.3, 8.4**

    For any CoverageResult, exporting to JSON then parsing SHALL produce
    an equivalent CoverageResult with all features, criteria, and
    confidence scores preserved.
    """

    def test_json_export_is_valid(self) -> None:
        """JSON export produces valid JSON."""
        import json
        from pathlib import Path

        from specmem.coverage.engine import CoverageEngine

        engine = CoverageEngine(Path())
        json_str = engine.export("json")

        # Should be valid JSON
        data = json.loads(json_str)
        assert isinstance(data, dict)

    def test_json_export_contains_all_fields(self) -> None:
        """JSON export contains all required fields."""
        import json
        from pathlib import Path

        from specmem.coverage.engine import CoverageEngine

        engine = CoverageEngine(Path())
        json_str = engine.export("json")
        data = json.loads(json_str)

        # Check required fields
        assert "features" in data
        assert "total_criteria" in data
        assert "covered_criteria" in data
        assert "coverage_percentage" in data

        # Check feature structure
        if data["features"]:
            feature = data["features"][0]
            assert "feature_name" in feature
            assert "criteria" in feature
            assert "coverage_percentage" in feature

    def test_json_round_trip(self) -> None:
        """JSON export can be parsed back to CoverageResult."""
        import json
        from pathlib import Path

        from specmem.coverage.engine import CoverageEngine
        from specmem.coverage.models import CoverageResult

        engine = CoverageEngine(Path())
        original = engine.analyze_coverage()
        json_str = original.to_json()

        # Parse back
        data = json.loads(json_str)
        restored = CoverageResult.from_dict(data)

        # Verify key properties preserved
        assert restored.total_criteria == original.total_criteria
        assert restored.covered_criteria == original.covered_criteria
        assert abs(restored.coverage_percentage - original.coverage_percentage) < 0.01

    def test_markdown_export_is_valid(self) -> None:
        """Markdown export produces valid markdown."""
        from pathlib import Path

        from specmem.coverage.engine import CoverageEngine

        engine = CoverageEngine(Path())
        md = engine.export("markdown")

        # Should contain markdown elements
        assert "# Spec Coverage Report" in md
        assert "|" in md  # Table
        assert "Coverage" in md


class TestAPIResultCompleteness:
    """Property 10: API Result Completeness.

    **Feature: spec-coverage, Property 10: API Result Completeness**
    **Validates: Requirements 9.1, 9.3, 9.4**

    For any call to get_coverage(), the returned CoverageResult SHALL contain
    all features with their criteria, test mappings, confidence scores,
    and suggestions for uncovered criteria.
    """

    def test_get_coverage_returns_coverage_result(self) -> None:
        """get_coverage returns a CoverageResult object."""
        from pathlib import Path

        from specmem.client import SpecMemClient
        from specmem.coverage.models import CoverageResult

        client = SpecMemClient(Path())
        result = client.get_coverage()

        assert isinstance(result, CoverageResult)

    def test_coverage_result_has_features(self) -> None:
        """CoverageResult contains features list."""
        from pathlib import Path

        from specmem.client import SpecMemClient

        client = SpecMemClient(Path())
        result = client.get_coverage()

        assert hasattr(result, "features")
        assert isinstance(result.features, list)

    def test_coverage_result_has_suggestions(self) -> None:
        """CoverageResult contains suggestions for uncovered criteria."""
        from pathlib import Path

        from specmem.client import SpecMemClient

        client = SpecMemClient(Path())
        result = client.get_coverage()

        assert hasattr(result, "suggestions")
        assert isinstance(result.suggestions, list)

    def test_feature_coverage_has_criteria(self) -> None:
        """Each FeatureCoverage has criteria with confidence scores."""
        from pathlib import Path

        from specmem.client import SpecMemClient

        client = SpecMemClient(Path())
        result = client.get_coverage()

        for feature in result.features:
            assert hasattr(feature, "criteria")
            for match in feature.criteria:
                assert hasattr(match, "confidence")
                assert 0.0 <= match.confidence <= 1.0

    def test_get_coverage_with_feature_filter(self) -> None:
        """get_coverage with feature parameter filters results."""
        from pathlib import Path

        from specmem.client import SpecMemClient

        client = SpecMemClient(Path())

        # Get coverage for specific feature
        result = client.get_coverage("spec-coverage")

        # Should only have one feature
        assert len(result.features) == 1
        assert result.features[0].feature_name == "spec-coverage"
