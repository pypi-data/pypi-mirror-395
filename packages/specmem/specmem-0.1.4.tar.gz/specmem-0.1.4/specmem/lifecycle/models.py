"""Data models for spec lifecycle management."""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Literal


@dataclass
class SpecHealthScore:
    """Health score for a specification.

    Attributes:
        spec_id: Unique identifier for the spec
        spec_path: Path to the spec file
        score: Health score between 0.0 and 1.0
        code_references: Number of code files referencing this spec
        last_modified: When the spec was last modified
        query_count: Number of times this spec has been queried
        is_orphaned: True if spec has no code references
        is_stale: True if spec hasn't been updated recently
        compression_ratio: Ratio of compressed to original size (if compressed)
        recommendations: List of recommended actions for this spec
    """

    spec_id: str
    spec_path: Path
    score: float
    code_references: int
    last_modified: datetime
    query_count: int = 0
    is_orphaned: bool = False
    is_stale: bool = False
    compression_ratio: float | None = None
    recommendations: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate score is within bounds."""
        if not 0.0 <= self.score <= 1.0:
            raise ValueError(f"Score must be between 0.0 and 1.0, got {self.score}")


@dataclass
class PruneResult:
    """Result of a prune operation on a spec.

    Attributes:
        spec_id: Unique identifier for the spec
        spec_path: Original path to the spec file
        action: What action was taken (archived, deleted, or skipped)
        archive_path: Path where spec was archived (if archived)
        reason: Explanation of why this action was taken
    """

    spec_id: str
    spec_path: Path
    action: Literal["archived", "deleted", "skipped"]
    archive_path: Path | None = None
    reason: str = ""


@dataclass
class GeneratedSpec:
    """A spec generated from source code.

    Attributes:
        source_files: List of source files used to generate this spec
        spec_name: Name of the generated spec
        spec_path: Path where the spec was written
        content: The generated spec content
        adapter_format: Format used (kiro, speckit, etc.)
        metadata: Additional metadata about the generation
    """

    source_files: list[Path]
    spec_name: str
    spec_path: Path
    content: str
    adapter_format: str = "kiro"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Ensure auto-generated marker is in metadata."""
        if "auto_generated" not in self.metadata:
            self.metadata["auto_generated"] = True
        if "generated_at" not in self.metadata:
            self.metadata["generated_at"] = datetime.now().isoformat()


@dataclass
class CompressedSpec:
    """A compressed version of a spec.

    Attributes:
        spec_id: Unique identifier for the spec
        original_path: Path to the original spec file
        original_size: Size of original content in bytes
        compressed_content: The compressed spec content
        compressed_size: Size of compressed content in bytes
        compression_ratio: Ratio of compressed to original size
        preserved_criteria: List of acceptance criteria preserved
    """

    spec_id: str
    original_path: Path
    original_size: int
    compressed_content: str
    compressed_size: int
    compression_ratio: float
    preserved_criteria: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Calculate compression ratio if not provided."""
        if self.original_size > 0:
            calculated_ratio = self.compressed_size / self.original_size
            if abs(calculated_ratio - self.compression_ratio) > 0.01:
                self.compression_ratio = calculated_ratio


@dataclass
class ArchiveMetadata:
    """Metadata stored with archived specs.

    Attributes:
        original_path: Original path of the spec before archiving
        archived_at: When the spec was archived
        reason: Why the spec was archived
        health_score: Health score at time of archiving
        code_references: Number of code references at time of archiving
        can_restore: Whether the spec can be restored
    """

    original_path: str
    archived_at: datetime
    reason: str
    health_score: float
    code_references: int
    can_restore: bool = True

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "original_path": self.original_path,
            "archived_at": self.archived_at.isoformat(),
            "reason": self.reason,
            "health_score": self.health_score,
            "code_references": self.code_references,
            "can_restore": self.can_restore,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ArchiveMetadata":
        """Create from dictionary."""
        return cls(
            original_path=data["original_path"],
            archived_at=datetime.fromisoformat(data["archived_at"]),
            reason=data["reason"],
            health_score=data["health_score"],
            code_references=data["code_references"],
            can_restore=data.get("can_restore", True),
        )


def calculate_health_score(
    code_references: int,
    days_since_modified: int,
    query_count: int,
    stale_threshold: int = 90,
) -> float:
    """Calculate health score for a spec.

    Args:
        code_references: Number of code files referencing this spec
        days_since_modified: Days since the spec was last modified
        query_count: Number of times the spec has been queried
        stale_threshold: Days after which a spec is considered stale

    Returns:
        Health score between 0.0 and 1.0
    """
    # Base score from code references (0-40 points)
    ref_score = min(code_references * 10, 40)

    # Freshness score (0-30 points)
    if days_since_modified <= 7:
        fresh_score = 30
    elif days_since_modified <= 30:
        fresh_score = 20
    elif days_since_modified <= stale_threshold:
        fresh_score = 10
    else:
        fresh_score = 0

    # Usage score (0-30 points)
    usage_score = min(query_count * 5, 30)

    # Ensure score is within bounds
    total = ref_score + fresh_score + usage_score
    return max(0.0, min(1.0, total / 100.0))
