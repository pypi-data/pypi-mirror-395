"""Data models for Kiro session search.

Provides normalized data structures for sessions, messages, search results,
and session-spec links that can be used across different agent adapters.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any


class MessageRole(str, Enum):
    """Standard message roles across all adapters."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass
class SessionMessage:
    """A single message in a session conversation.

    Attributes:
        role: The role of the message sender (user, assistant, system)
        content: The flattened text content of the message
        timestamp_ms: Unix timestamp in milliseconds (optional)
        tool_calls: List of tool call information (optional)
        raw_content: Original unflattened content for reference
    """

    role: MessageRole
    content: str
    timestamp_ms: int | None = None
    tool_calls: list[dict[str, Any]] | None = None
    raw_content: Any = None

    @classmethod
    def normalize_role(cls, role: str) -> MessageRole:
        """Normalize a role string to a standard MessageRole.

        Args:
            role: Role string from any adapter (e.g., "user", "assistant", "system")

        Returns:
            Normalized MessageRole enum value

        Raises:
            ValueError: If role cannot be normalized
        """
        role_lower = role.lower().strip()

        # Direct mappings
        if role_lower in ("user", "human"):
            return MessageRole.USER
        elif role_lower in ("assistant", "ai", "bot", "agent"):
            return MessageRole.ASSISTANT
        elif role_lower in ("system", "tool"):
            return MessageRole.SYSTEM
        else:
            raise ValueError(f"Unknown role: {role}")


@dataclass
class Session:
    """Normalized session data model.

    Represents a complete conversation session with metadata and messages.

    Attributes:
        session_id: Unique identifier for the session
        title: Human-readable title for the session
        workspace_directory: Path to the workspace this session is associated with
        date_created_ms: Unix timestamp in milliseconds when session was created
        messages: List of messages in the session
        metadata: Additional metadata from the source adapter
        session_path: Path to the session file (optional)
    """

    session_id: str
    title: str
    workspace_directory: str
    date_created_ms: int
    messages: list[SessionMessage] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    session_path: Path | None = None

    @property
    def message_count(self) -> int:
        """Return the number of messages in the session."""
        return len(self.messages)

    @property
    def date_created(self) -> datetime:
        """Return the creation date as a datetime object."""
        return datetime.fromtimestamp(self.date_created_ms / 1000)

    def to_dict(self) -> dict[str, Any]:
        """Convert session to dictionary for serialization."""
        return {
            "session_id": self.session_id,
            "title": self.title,
            "workspace_directory": self.workspace_directory,
            "date_created_ms": self.date_created_ms,
            "message_count": self.message_count,
            "messages": [
                {
                    "role": msg.role.value,
                    "content": msg.content,
                    "timestamp_ms": msg.timestamp_ms,
                }
                for msg in self.messages
            ],
            "metadata": self.metadata,
        }


@dataclass
class SessionConfig:
    """Session search configuration.

    Attributes:
        sessions_path: Path to the Kiro sessions directory
        workspace_only: If True, only search sessions for current workspace
        enabled: Whether session search is enabled
    """

    sessions_path: Path | None = None
    workspace_only: bool = False
    enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Convert config to dictionary for serialization."""
        return {
            "path": str(self.sessions_path) if self.sessions_path else None,
            "workspace_only": self.workspace_only,
            "enabled": self.enabled,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SessionConfig":
        """Create config from dictionary."""
        path = data.get("path")
        return cls(
            sessions_path=Path(path) if path else None,
            workspace_only=data.get("workspace_only", False),
            enabled=data.get("enabled", False),
        )


@dataclass
class SearchFilters:
    """Filters for session search.

    Attributes:
        workspace: Filter to specific workspace path
        since_ms: Only include sessions created after this timestamp
        until_ms: Only include sessions created before this timestamp
        limit: Maximum number of results to return
    """

    workspace: Path | None = None
    since_ms: int | None = None
    until_ms: int | None = None
    limit: int = 10


@dataclass
class SearchResult:
    """A single search result.

    Attributes:
        session: The matched session
        score: Relevance score (0.0 to 1.0)
        matched_message_indices: Indices of messages that matched the query
    """

    session: Session
    score: float
    matched_message_indices: list[int] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert result to dictionary for serialization."""
        return {
            "session": self.session.to_dict(),
            "score": self.score,
            "matched_message_indices": self.matched_message_indices,
        }


@dataclass
class SessionSpecLink:
    """Link between a session and a specification.

    Attributes:
        session_id: ID of the linked session
        spec_id: ID of the linked specification
        confidence: Confidence score for the link (0.0 to 1.0)
        link_type: Type of link (file_ref, semantic, manual)
    """

    session_id: str
    spec_id: str
    confidence: float
    link_type: str  # "file_ref" | "semantic" | "manual"

    def to_dict(self) -> dict[str, Any]:
        """Convert link to dictionary for serialization."""
        return {
            "session_id": self.session_id,
            "spec_id": self.spec_id,
            "confidence": self.confidence,
            "link_type": self.link_type,
        }


def normalize_timestamp(timestamp: str | int | float | None) -> int | None:
    """Normalize a timestamp to Unix milliseconds.

    Args:
        timestamp: Timestamp in various formats:
            - ISO 8601 string (e.g., "2025-01-15T10:30:00Z")
            - Unix seconds (int or float)
            - Unix milliseconds (int)
            - None

    Returns:
        Unix timestamp in milliseconds, or None if input is None

    Raises:
        ValueError: If timestamp format is not recognized
    """
    if timestamp is None:
        return None

    if isinstance(timestamp, str):
        # Parse ISO 8601 format
        try:
            # Handle various ISO formats
            ts = timestamp.replace("Z", "+00:00")
            dt = datetime.fromisoformat(ts)
            return int(dt.timestamp() * 1000)
        except ValueError as e:
            raise ValueError(f"Invalid timestamp format: {timestamp}") from e

    if isinstance(timestamp, float):
        # Assume seconds if small, milliseconds if large
        if timestamp < 1e12:
            return int(timestamp * 1000)
        else:
            return int(timestamp)

    if isinstance(timestamp, int):
        # Assume seconds if small, milliseconds if large
        if timestamp < 1e12:
            return timestamp * 1000
        else:
            return timestamp

    raise ValueError(f"Unsupported timestamp type: {type(timestamp)}")
