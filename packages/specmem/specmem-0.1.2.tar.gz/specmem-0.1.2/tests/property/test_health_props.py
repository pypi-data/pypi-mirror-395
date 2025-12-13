"""Property-based tests for Health Score Engine.

**Feature: project-polish**
"""

from hypothesis import given, settings
from hypothesis import strategies as st

from specmem.health.models import HealthScore, ScoreBreakdown, ScoreCategory


class TestHealthScoreGradeMapping:
    """Property tests for health score grade mapping.

    **Feature: project-polish, Property 1: Health Score Grade Mapping**
    **Validates: Requirements 1.2, 6.2**
    """

    @given(score=st.floats(min_value=90.0, max_value=100.0, allow_nan=False))
    @settings(max_examples=100)
    def test_grade_a_for_scores_90_to_100(self, score: float):
        """Scores 90-100 should map to grade A."""
        grade = HealthScore.score_to_grade(score)
        assert grade == "A", f"Score {score} should be A, got {grade}"

    @given(score=st.floats(min_value=80.0, max_value=89.99, allow_nan=False))
    @settings(max_examples=100)
    def test_grade_b_for_scores_80_to_89(self, score: float):
        """Scores 80-89 should map to grade B."""
        grade = HealthScore.score_to_grade(score)
        assert grade == "B", f"Score {score} should be B, got {grade}"

    @given(score=st.floats(min_value=70.0, max_value=79.99, allow_nan=False))
    @settings(max_examples=100)
    def test_grade_c_for_scores_70_to_79(self, score: float):
        """Scores 70-79 should map to grade C."""
        grade = HealthScore.score_to_grade(score)
        assert grade == "C", f"Score {score} should be C, got {grade}"

    @given(score=st.floats(min_value=60.0, max_value=69.99, allow_nan=False))
    @settings(max_examples=100)
    def test_grade_d_for_scores_60_to_69(self, score: float):
        """Scores 60-69 should map to grade D."""
        grade = HealthScore.score_to_grade(score)
        assert grade == "D", f"Score {score} should be D, got {grade}"

    @given(score=st.floats(min_value=0.0, max_value=59.99, allow_nan=False))
    @settings(max_examples=100)
    def test_grade_f_for_scores_below_60(self, score: float):
        """Scores 0-59 should map to grade F."""
        grade = HealthScore.score_to_grade(score)
        assert grade == "F", f"Score {score} should be F, got {grade}"

    @given(score=st.floats(min_value=0.0, max_value=100.0, allow_nan=False))
    @settings(max_examples=100)
    def test_grade_is_always_valid(self, score: float):
        """Any valid score should produce a valid grade."""
        grade = HealthScore.score_to_grade(score)
        assert grade in ("A", "B", "C", "D", "F")

    @given(score=st.floats(min_value=0.0, max_value=100.0, allow_nan=False))
    @settings(max_examples=100)
    def test_grade_color_is_always_valid(self, score: float):
        """Any grade should have a valid color."""
        grade = HealthScore.score_to_grade(score)
        color = HealthScore.grade_to_color(grade)
        assert color.startswith("#")
        assert len(color) == 7  # #RRGGBB format


class TestScoreBreakdown:
    """Property tests for score breakdown calculations."""

    @given(
        score=st.floats(min_value=0.0, max_value=100.0, allow_nan=False),
        weight=st.floats(min_value=0.0, max_value=1.0, allow_nan=False),
    )
    @settings(max_examples=100)
    def test_weighted_score_calculation(self, score: float, weight: float):
        """Weighted score should be score * weight."""
        breakdown = ScoreBreakdown(
            category=ScoreCategory.COVERAGE,
            score=score,
            weight=weight,
        )
        expected = score * weight
        assert abs(breakdown.weighted_score() - expected) < 0.0001


class TestHealthScoreToDict:
    """Property tests for HealthScore serialization."""

    @given(
        overall=st.floats(min_value=0.0, max_value=100.0, allow_nan=False),
    )
    @settings(max_examples=100)
    def test_to_dict_preserves_data(self, overall: float):
        """to_dict should preserve all data."""
        grade = HealthScore.score_to_grade(overall)
        health = HealthScore(
            overall_score=overall,
            letter_grade=grade,
            breakdown=[],
            suggestions=["Test suggestion"],
            spec_count=10,
            feature_count=5,
        )

        data = health.to_dict()

        assert abs(data["overall_score"] - round(overall, 1)) < 0.1
        assert data["letter_grade"] == grade
        assert data["suggestions"] == ["Test suggestion"]
        assert data["spec_count"] == 10
        assert data["feature_count"] == 5


class TestHealthScoreCalculationConsistency:
    """Property tests for health score calculation consistency.

    **Feature: project-polish, Property 2: Health Score Calculation Consistency**
    **Validates: Requirements 6.1**
    """

    @given(
        coverage=st.floats(min_value=0.0, max_value=100.0, allow_nan=False),
        validation=st.floats(min_value=0.0, max_value=100.0, allow_nan=False),
        freshness=st.floats(min_value=0.0, max_value=100.0, allow_nan=False),
        completeness=st.floats(min_value=0.0, max_value=100.0, allow_nan=False),
    )
    @settings(max_examples=100)
    def test_weighted_average_is_deterministic(
        self,
        coverage: float,
        validation: float,
        freshness: float,
        completeness: float,
    ):
        """Given the same inputs, the overall score should be the same."""
        from specmem.health.models import DEFAULT_WEIGHTS

        # Calculate expected weighted average
        expected = (
            coverage * DEFAULT_WEIGHTS[ScoreCategory.COVERAGE]
            + validation * DEFAULT_WEIGHTS[ScoreCategory.VALIDATION]
            + freshness * DEFAULT_WEIGHTS[ScoreCategory.FRESHNESS]
            + completeness * DEFAULT_WEIGHTS[ScoreCategory.COMPLETENESS]
        )

        # Create breakdown manually
        breakdown = [
            ScoreBreakdown(
                category=ScoreCategory.COVERAGE,
                score=coverage,
                weight=DEFAULT_WEIGHTS[ScoreCategory.COVERAGE],
            ),
            ScoreBreakdown(
                category=ScoreCategory.VALIDATION,
                score=validation,
                weight=DEFAULT_WEIGHTS[ScoreCategory.VALIDATION],
            ),
            ScoreBreakdown(
                category=ScoreCategory.FRESHNESS,
                score=freshness,
                weight=DEFAULT_WEIGHTS[ScoreCategory.FRESHNESS],
            ),
            ScoreBreakdown(
                category=ScoreCategory.COMPLETENESS,
                score=completeness,
                weight=DEFAULT_WEIGHTS[ScoreCategory.COMPLETENESS],
            ),
        ]

        # Calculate overall from breakdown
        overall = sum(item.weighted_score() for item in breakdown)

        assert abs(overall - expected) < 0.0001, f"Expected {expected}, got {overall}"

    @given(
        coverage=st.floats(min_value=0.0, max_value=100.0, allow_nan=False),
        validation=st.floats(min_value=0.0, max_value=100.0, allow_nan=False),
        freshness=st.floats(min_value=0.0, max_value=100.0, allow_nan=False),
        completeness=st.floats(min_value=0.0, max_value=100.0, allow_nan=False),
    )
    @settings(max_examples=100)
    def test_overall_score_in_valid_range(
        self,
        coverage: float,
        validation: float,
        freshness: float,
        completeness: float,
    ):
        """Overall score should always be between 0 and 100."""
        from specmem.health.models import DEFAULT_WEIGHTS

        breakdown = [
            ScoreBreakdown(
                category=ScoreCategory.COVERAGE,
                score=coverage,
                weight=DEFAULT_WEIGHTS[ScoreCategory.COVERAGE],
            ),
            ScoreBreakdown(
                category=ScoreCategory.VALIDATION,
                score=validation,
                weight=DEFAULT_WEIGHTS[ScoreCategory.VALIDATION],
            ),
            ScoreBreakdown(
                category=ScoreCategory.FRESHNESS,
                score=freshness,
                weight=DEFAULT_WEIGHTS[ScoreCategory.FRESHNESS],
            ),
            ScoreBreakdown(
                category=ScoreCategory.COMPLETENESS,
                score=completeness,
                weight=DEFAULT_WEIGHTS[ScoreCategory.COMPLETENESS],
            ),
        ]

        overall = sum(item.weighted_score() for item in breakdown)

        assert 0 <= overall <= 100, f"Overall score {overall} out of range"

    @given(
        coverage=st.floats(min_value=0.0, max_value=100.0, allow_nan=False),
        validation=st.floats(min_value=0.0, max_value=100.0, allow_nan=False),
        freshness=st.floats(min_value=0.0, max_value=100.0, allow_nan=False),
        completeness=st.floats(min_value=0.0, max_value=100.0, allow_nan=False),
    )
    @settings(max_examples=100)
    def test_weights_sum_to_one(
        self,
        coverage: float,
        validation: float,
        freshness: float,
        completeness: float,
    ):
        """Default weights should sum to 1.0."""
        from specmem.health.models import DEFAULT_WEIGHTS

        total_weight = sum(DEFAULT_WEIGHTS.values())
        assert abs(total_weight - 1.0) < 0.0001, f"Weights sum to {total_weight}"


class TestLowScoreSuggestions:
    """Property tests for low score suggestions.

    **Feature: project-polish, Property 3: Low Score Suggestions**
    **Validates: Requirements 6.3**
    """

    @given(
        coverage=st.floats(min_value=0.0, max_value=79.0, allow_nan=False),
        validation=st.floats(min_value=0.0, max_value=79.0, allow_nan=False),
        freshness=st.floats(min_value=0.0, max_value=79.0, allow_nan=False),
        completeness=st.floats(min_value=0.0, max_value=79.0, allow_nan=False),
    )
    @settings(max_examples=100)
    def test_low_scores_generate_suggestions(
        self,
        coverage: float,
        validation: float,
        freshness: float,
        completeness: float,
    ):
        """Scores below 80 (grade B) should generate at least one suggestion."""
        from specmem.health.engine import HealthScoreEngine
        from specmem.health.models import DEFAULT_WEIGHTS

        # Create breakdown with low scores
        breakdown = [
            ScoreBreakdown(
                category=ScoreCategory.COVERAGE,
                score=coverage,
                weight=DEFAULT_WEIGHTS[ScoreCategory.COVERAGE],
                details="test",
            ),
            ScoreBreakdown(
                category=ScoreCategory.VALIDATION,
                score=validation,
                weight=DEFAULT_WEIGHTS[ScoreCategory.VALIDATION],
                details="test",
            ),
            ScoreBreakdown(
                category=ScoreCategory.FRESHNESS,
                score=freshness,
                weight=DEFAULT_WEIGHTS[ScoreCategory.FRESHNESS],
                details="test",
            ),
            ScoreBreakdown(
                category=ScoreCategory.COMPLETENESS,
                score=completeness,
                weight=DEFAULT_WEIGHTS[ScoreCategory.COMPLETENESS],
                details="test",
            ),
        ]

        overall = sum(item.weighted_score() for item in breakdown)
        grade = HealthScore.score_to_grade(overall)

        # Use the engine's suggestion generator
        from pathlib import Path

        engine = HealthScoreEngine(Path())
        suggestions = engine._generate_suggestions(breakdown, grade)

        # If grade is below B, should have suggestions
        if grade not in ("A", "B"):
            assert len(suggestions) > 0, f"Grade {grade} should have suggestions"

    @given(
        coverage=st.floats(min_value=90.0, max_value=100.0, allow_nan=False),
        validation=st.floats(min_value=90.0, max_value=100.0, allow_nan=False),
        freshness=st.floats(min_value=90.0, max_value=100.0, allow_nan=False),
        completeness=st.floats(min_value=90.0, max_value=100.0, allow_nan=False),
    )
    @settings(max_examples=100)
    def test_high_scores_no_suggestions(
        self,
        coverage: float,
        validation: float,
        freshness: float,
        completeness: float,
    ):
        """Scores above 90 (grade A) should not generate suggestions."""
        from specmem.health.engine import HealthScoreEngine
        from specmem.health.models import DEFAULT_WEIGHTS

        breakdown = [
            ScoreBreakdown(
                category=ScoreCategory.COVERAGE,
                score=coverage,
                weight=DEFAULT_WEIGHTS[ScoreCategory.COVERAGE],
                details="test",
            ),
            ScoreBreakdown(
                category=ScoreCategory.VALIDATION,
                score=validation,
                weight=DEFAULT_WEIGHTS[ScoreCategory.VALIDATION],
                details="test",
            ),
            ScoreBreakdown(
                category=ScoreCategory.FRESHNESS,
                score=freshness,
                weight=DEFAULT_WEIGHTS[ScoreCategory.FRESHNESS],
                details="test",
            ),
            ScoreBreakdown(
                category=ScoreCategory.COMPLETENESS,
                score=completeness,
                weight=DEFAULT_WEIGHTS[ScoreCategory.COMPLETENESS],
                details="test",
            ),
        ]

        overall = sum(item.weighted_score() for item in breakdown)
        grade = HealthScore.score_to_grade(overall)

        from pathlib import Path

        engine = HealthScoreEngine(Path())
        suggestions = engine._generate_suggestions(breakdown, grade)

        # Grade A should have no suggestions
        if grade == "A":
            assert len(suggestions) == 0, "Grade A should have no suggestions"
