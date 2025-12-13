"""Data models for Spec Coverage Analysis.

Contains dataclasses for acceptance criteria, extracted tests,
coverage results, and test suggestions.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class BadgeColor(str, Enum):
    """Badge colors based on coverage percentage."""

    RED = "red"  # < 50%
    YELLOW = "yellow"  # 50-80%
    GREEN = "green"  # > 80%


def get_badge_color(coverage_percentage: float) -> BadgeColor:
    """Get badge color based on coverage percentage."""
    if coverage_percentage < 50:
        return BadgeColor.RED
    elif coverage_percentage <= 80:
        return BadgeColor.YELLOW
    else:
        return BadgeColor.GREEN


@dataclass
class AcceptanceCriterion:
    """Acceptance criterion extracted from requirements.md.

    Represents a single testable condition from a spec file.
    """

    id: str  # Unique identifier (e.g., "user-auth.1.3")
    number: str  # Criterion number (e.g., "1.3")
    text: str  # Full EARS format text
    requirement_id: str  # Parent requirement ID (e.g., "1")
    user_story: str  # Parent user story text
    feature_name: str  # Feature this belongs to

    def __post_init__(self) -> None:
        """Validate required fields."""
        if not self.id:
            raise ValueError("id cannot be empty")
        if not self.number:
            raise ValueError("number cannot be empty")
        if not self.text:
            raise ValueError("text cannot be empty")
        if not self.feature_name:
            raise ValueError("feature_name cannot be empty")

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "id": self.id,
            "number": self.number,
            "text": self.text,
            "requirement_id": self.requirement_id,
            "user_story": self.user_story,
            "feature_name": self.feature_name,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AcceptanceCriterion:
        """Deserialize from dictionary."""
        return cls(
            id=data["id"],
            number=data["number"],
            text=data["text"],
            requirement_id=data.get("requirement_id", ""),
            user_story=data.get("user_story", ""),
            feature_name=data["feature_name"],
        )


@dataclass
class ExtractedTest:
    """Test function extracted from test files.

    Represents a test that can be matched to acceptance criteria.
    """

    name: str  # Test function/method name
    file_path: str  # Path to test file
    line_number: int  # Line number in file
    docstring: str | None = None  # Test docstring or comment
    requirement_links: list[str] = field(default_factory=list)  # Explicit links
    framework: str = "unknown"  # Test framework (pytest, jest, etc.)
    selector: str = ""  # Framework-specific selector

    def __post_init__(self) -> None:
        """Validate required fields."""
        if not self.name:
            raise ValueError("name cannot be empty")
        if not self.file_path:
            raise ValueError("file_path cannot be empty")
        if self.line_number < 0:
            raise ValueError("line_number must be non-negative")

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "name": self.name,
            "file_path": self.file_path,
            "line_number": self.line_number,
            "docstring": self.docstring,
            "requirement_links": self.requirement_links,
            "framework": self.framework,
            "selector": self.selector,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ExtractedTest:
        """Deserialize from dictionary."""
        return cls(
            name=data["name"],
            file_path=data["file_path"],
            line_number=data["line_number"],
            docstring=data.get("docstring"),
            requirement_links=data.get("requirement_links", []),
            framework=data.get("framework", "unknown"),
            selector=data.get("selector", ""),
        )


@dataclass
class CriteriaMatch:
    """Match between an acceptance criterion and a test.

    Represents the result of matching a criterion to a test,
    including confidence score.
    """

    criterion: AcceptanceCriterion
    test: ExtractedTest | None  # None if uncovered
    confidence: float  # 0.0 to 1.0

    CONFIDENCE_THRESHOLD: float = 0.5

    def __post_init__(self) -> None:
        """Validate confidence range."""
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"confidence must be between 0.0 and 1.0, got {self.confidence}")

    @property
    def is_covered(self) -> bool:
        """Check if criterion is covered based on confidence threshold."""
        return self.test is not None and self.confidence >= self.CONFIDENCE_THRESHOLD

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "criterion": self.criterion.to_dict(),
            "test": self.test.to_dict() if self.test else None,
            "confidence": self.confidence,
            "is_covered": self.is_covered,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CriteriaMatch:
        """Deserialize from dictionary."""
        return cls(
            criterion=AcceptanceCriterion.from_dict(data["criterion"]),
            test=ExtractedTest.from_dict(data["test"]) if data.get("test") else None,
            confidence=data["confidence"],
        )


@dataclass
class TestSuggestion:
    """Suggestion for writing a test for an uncovered criterion.

    Provides guidance on what test to write and what to verify.
    """

    criterion: AcceptanceCriterion
    suggested_file: str  # Recommended test file path
    suggested_name: str  # Recommended test function name
    verification_points: list[str]  # What to verify in the test

    def __post_init__(self) -> None:
        """Validate required fields."""
        if not self.suggested_file:
            raise ValueError("suggested_file cannot be empty")
        if not self.suggested_name:
            raise ValueError("suggested_name cannot be empty")
        if not self.verification_points:
            raise ValueError("verification_points cannot be empty")

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "criterion": self.criterion.to_dict(),
            "suggested_file": self.suggested_file,
            "suggested_name": self.suggested_name,
            "verification_points": self.verification_points,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TestSuggestion:
        """Deserialize from dictionary."""
        return cls(
            criterion=AcceptanceCriterion.from_dict(data["criterion"]),
            suggested_file=data["suggested_file"],
            suggested_name=data["suggested_name"],
            verification_points=data["verification_points"],
        )


@dataclass
class FeatureCoverage:
    """Coverage data for a single feature.

    Contains all criteria matches and coverage statistics.
    """

    feature_name: str
    criteria: list[CriteriaMatch] = field(default_factory=list)

    @property
    def total_count(self) -> int:
        """Total number of acceptance criteria."""
        return len(self.criteria)

    @property
    def tested_count(self) -> int:
        """Number of covered criteria."""
        return sum(1 for c in self.criteria if c.is_covered)

    @property
    def coverage_percentage(self) -> float:
        """Calculate coverage percentage."""
        if self.total_count == 0:
            return 100.0
        return (self.tested_count / self.total_count) * 100

    @property
    def gap_percentage(self) -> float:
        """Calculate gap percentage."""
        return 100.0 - self.coverage_percentage

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "feature_name": self.feature_name,
            "criteria": [c.to_dict() for c in self.criteria],
            "total_count": self.total_count,
            "tested_count": self.tested_count,
            "coverage_percentage": self.coverage_percentage,
            "gap_percentage": self.gap_percentage,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FeatureCoverage:
        """Deserialize from dictionary."""
        return cls(
            feature_name=data["feature_name"],
            criteria=[CriteriaMatch.from_dict(c) for c in data.get("criteria", [])],
        )


@dataclass
class CoverageResult:
    """Overall coverage analysis result.

    Contains coverage data for all features and suggestions
    for uncovered criteria.
    """

    features: list[FeatureCoverage] = field(default_factory=list)
    suggestions: list[TestSuggestion] = field(default_factory=list)

    @property
    def total_criteria(self) -> int:
        """Total number of acceptance criteria."""
        return sum(f.total_count for f in self.features)

    @property
    def covered_criteria(self) -> int:
        """Number of covered criteria."""
        return sum(f.tested_count for f in self.features)

    @property
    def coverage_percentage(self) -> float:
        """Overall coverage percentage."""
        if self.total_criteria == 0:
            return 100.0
        return (self.covered_criteria / self.total_criteria) * 100

    @property
    def gap_percentage(self) -> float:
        """Overall gap percentage."""
        return 100.0 - self.coverage_percentage

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "features": [f.to_dict() for f in self.features],
            "suggestions": [s.to_dict() for s in self.suggestions],
            "total_criteria": self.total_criteria,
            "covered_criteria": self.covered_criteria,
            "coverage_percentage": self.coverage_percentage,
            "gap_percentage": self.gap_percentage,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CoverageResult:
        """Deserialize from dictionary."""
        return cls(
            features=[FeatureCoverage.from_dict(f) for f in data.get("features", [])],
            suggestions=[TestSuggestion.from_dict(s) for s in data.get("suggestions", [])],
        )

    def to_json(self) -> str:
        """Export as JSON string."""
        return json.dumps(self.to_dict(), indent=2)

    def to_markdown(self) -> str:
        """Export as markdown table."""
        lines = [
            "# Spec Coverage Report",
            "",
            f"**Overall Coverage:** {self.covered_criteria}/{self.total_criteria} "
            f"({self.coverage_percentage:.1f}%)",
            "",
            "## Coverage by Feature",
            "",
            "| Feature | Tested | Total | Coverage | Gap |",
            "|---------|--------|-------|----------|-----|",
        ]

        for feature in self.features:
            status = "✅" if feature.coverage_percentage >= 80 else "⚠️"
            lines.append(
                f"| {feature.feature_name} | {feature.tested_count} | "
                f"{feature.total_count} | {feature.coverage_percentage:.1f}% | "
                f"{feature.gap_percentage:.1f}% {status} |"
            )

        if self.suggestions:
            lines.extend(
                [
                    "",
                    "## Uncovered Criteria",
                    "",
                ]
            )
            for suggestion in self.suggestions:
                lines.append(f"- **{suggestion.criterion.number}**: {suggestion.criterion.text}")
                lines.append(f"  - Suggested test: `{suggestion.suggested_name}`")
                lines.append(f"  - File: `{suggestion.suggested_file}`")

        return "\n".join(lines)

    def generate_badge(self) -> str:
        """Generate coverage badge markdown."""
        color = get_badge_color(self.coverage_percentage)
        percentage = int(self.coverage_percentage)
        return (
            f"![Spec Coverage](https://img.shields.io/badge/"
            f"Spec_Coverage-{percentage}%25-{color.value})"
        )
