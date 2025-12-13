"""Session-related exceptions.

Custom exceptions for session search functionality.
"""

from pathlib import Path

from specmem.core.exceptions import SpecMemError


class SessionError(SpecMemError):
    """Base class for session-related errors."""

    pass


class SessionNotConfiguredError(SessionError):
    """Session search is not configured."""

    def __init__(self) -> None:
        super().__init__(
            "Session search is not configured.\n"
            "Run 'specmem sessions config' to set up session search.",
            code="SESSION_NOT_CONFIGURED",
        )


class InvalidSessionPathError(SessionError):
    """Configured session path is invalid."""

    def __init__(self, path: Path, reason: str) -> None:
        super().__init__(
            f"Invalid session path '{path}': {reason}",
            code="INVALID_SESSION_PATH",
            details={"path": str(path), "reason": reason},
        )


class DiscoveryFailedError(SessionError):
    """Auto-discovery failed to find valid directories."""

    def __init__(self, platform: str, checked_paths: list[str]) -> None:
        paths_str = "\n  ".join(checked_paths)
        super().__init__(
            f"Could not find Kiro sessions directory on {platform}.\n"
            f"Checked:\n  {paths_str}\n\n"
            "Please provide the path manually:\n"
            "  specmem sessions config --path /path/to/workspace-sessions",
            code="DISCOVERY_FAILED",
            details={"platform": platform, "checked_paths": checked_paths},
        )


class SessionParseError(SessionError):
    """Session file is malformed."""

    def __init__(self, path: Path, reason: str) -> None:
        super().__init__(
            f"Failed to parse session file '{path}': {reason}",
            code="SESSION_PARSE_ERROR",
            details={"path": str(path), "reason": reason},
        )


class SessionNotFoundError(SessionError):
    """Requested session ID doesn't exist."""

    def __init__(self, session_id: str) -> None:
        super().__init__(
            f"Session not found: {session_id}",
            code="SESSION_NOT_FOUND",
            details={"session_id": session_id},
        )
