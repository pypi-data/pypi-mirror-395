"""Data models for Health Score Engine."""

from dataclasses import dataclass, field
from enum import Enum


class ScoreCategory(str, Enum):
    """Categories for health score breakdown."""

    COVERAGE = "coverage"
    VALIDATION = "validation"
    FRESHNESS = "freshness"
    COMPLETENESS = "completeness"


@dataclass
class ScoreBreakdown:
    """Breakdown of a single score category."""

    category: ScoreCategory
    score: float  # 0-100
    weight: float  # 0-1, weights should sum to 1
    details: str = ""

    def weighted_score(self) -> float:
        """Calculate weighted contribution to overall score."""
        return self.score * self.weight


@dataclass
class HealthScore:
    """Overall health score for project specifications.

    The health score provides a comprehensive assessment of specification
    quality based on multiple factors: test coverage, validation issues,
    spec freshness, and completeness.
    """

    overall_score: float  # 0-100
    letter_grade: str  # A, B, C, D, F
    breakdown: list[ScoreBreakdown] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    spec_count: int = 0
    feature_count: int = 0

    @staticmethod
    def score_to_grade(score: float) -> str:
        """Convert numeric score to letter grade.

        Grade mapping:
        - A: 90-100
        - B: 80-89
        - C: 70-79
        - D: 60-69
        - F: 0-59
        """
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    @staticmethod
    def grade_to_color(grade: str) -> str:
        """Get color for grade display."""
        colors = {
            "A": "#10b981",  # emerald-500
            "B": "#3b82f6",  # blue-500
            "C": "#f59e0b",  # amber-500
            "D": "#f97316",  # orange-500
            "F": "#ef4444",  # red-500
        }
        return colors.get(grade, "#6b7280")  # gray-500 default

    def get_category_score(self, category: ScoreCategory) -> float | None:
        """Get score for a specific category."""
        for item in self.breakdown:
            if item.category == category:
                return item.score
        return None

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "overall_score": round(self.overall_score, 1),
            "letter_grade": self.letter_grade,
            "grade_color": self.grade_to_color(self.letter_grade),
            "breakdown": [
                {
                    "category": item.category.value,
                    "score": round(item.score, 1),
                    "weight": item.weight,
                    "weighted_score": round(item.weighted_score(), 1),
                    "details": item.details,
                }
                for item in self.breakdown
            ],
            "suggestions": self.suggestions,
            "spec_count": self.spec_count,
            "feature_count": self.feature_count,
        }


# Default weights for score categories
DEFAULT_WEIGHTS = {
    ScoreCategory.COVERAGE: 0.30,
    ScoreCategory.VALIDATION: 0.25,
    ScoreCategory.FRESHNESS: 0.20,
    ScoreCategory.COMPLETENESS: 0.25,
}
