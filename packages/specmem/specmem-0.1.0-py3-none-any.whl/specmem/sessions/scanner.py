"""Session scanner for discovering and loading sessions.

Scans configured session directories for Kiro sessions.
"""

import base64
from collections.abc import Iterator
from pathlib import Path

from specmem.sessions.exceptions import InvalidSessionPathError
from specmem.sessions.models import Session, SessionConfig
from specmem.sessions.parser import KiroSessionParser


def encode_workspace_path(workspace_path: str) -> str:
    """Encode a workspace path to base64 for directory naming.

    Args:
        workspace_path: The workspace path to encode.

    Returns:
        Base64-encoded string safe for use as directory name.
    """
    encoded = base64.urlsafe_b64encode(workspace_path.encode("utf-8"))
    return encoded.decode("ascii")


def decode_workspace_path(encoded: str) -> str:
    """Decode a base64-encoded workspace path.

    Args:
        encoded: Base64-encoded workspace path.

    Returns:
        Decoded workspace path string.

    Raises:
        ValueError: If decoding fails.
    """
    try:
        # Handle both standard and URL-safe base64
        # Add padding if needed
        padding = 4 - len(encoded) % 4
        if padding != 4:
            encoded += "=" * padding

        decoded = base64.urlsafe_b64decode(encoded.encode("ascii"))
        return decoded.decode("utf-8")
    except Exception as e:
        raise ValueError(f"Failed to decode workspace path: {e}") from e


class SessionScanner:
    """Scans for Kiro sessions in configured directory.

    Discovers sessions by scanning the workspace-sessions directory structure
    where each subdirectory is a base64-encoded workspace path containing
    session JSON files.
    """

    def __init__(self, config: SessionConfig):
        """Initialize the scanner.

        Args:
            config: Session configuration with sessions_path.

        Raises:
            InvalidSessionPathError: If sessions_path is not configured.
        """
        if config.sessions_path is None:
            raise InvalidSessionPathError(Path(), "Sessions path not configured")
        self.config = config
        self.sessions_path = config.sessions_path
        self.parser = KiroSessionParser()

    def scan(self, workspace_filter: Path | None = None) -> list[Session]:
        """Scan for sessions, optionally filtered by workspace.

        Args:
            workspace_filter: If provided, only return sessions for this workspace.

        Returns:
            List of Session objects found.

        Raises:
            InvalidSessionPathError: If sessions directory doesn't exist.
        """
        if not self.sessions_path.exists():
            raise InvalidSessionPathError(self.sessions_path, "Directory does not exist")

        sessions = []
        for session in self._iter_sessions():
            # Apply workspace filter if specified
            if workspace_filter is not None:
                session_workspace = Path(session.workspace_directory)
                if not self._paths_match(session_workspace, workspace_filter):
                    continue

            sessions.append(session)

        return sessions

    def _iter_sessions(self) -> Iterator[Session]:
        """Iterate over all sessions in the sessions directory.

        Yields:
            Session objects for each valid session file found.
        """
        for workspace_dir in self.list_workspace_directories():
            # Try to decode workspace path from directory name
            try:
                workspace_path = decode_workspace_path(workspace_dir.name)
            except ValueError:
                # Directory name might not be base64 encoded
                workspace_path = workspace_dir.name

            # Find session files in this workspace directory
            for session_file in workspace_dir.glob("*.json"):
                if session_file.name == "sessions.json":
                    continue  # Skip index file

                try:
                    session = self.parser.parse_session_file(session_file)
                    # Override workspace if not set in file
                    if not session.workspace_directory:
                        session.workspace_directory = workspace_path
                    yield session
                except Exception:
                    # Skip invalid session files
                    continue

    def list_workspace_directories(self) -> list[Path]:
        """List all workspace directories in sessions folder.

        Returns:
            List of workspace directory paths.
        """
        if not self.sessions_path.exists():
            return []

        return [d for d in self.sessions_path.iterdir() if d.is_dir()]

    def get_session_by_id(self, session_id: str) -> Session | None:
        """Get a specific session by ID.

        Args:
            session_id: The session ID to find.

        Returns:
            Session if found, None otherwise.
        """
        for session in self._iter_sessions():
            if session.session_id == session_id:
                return session
        return None

    def _paths_match(self, path1: Path, path2: Path) -> bool:
        """Check if two paths refer to the same location.

        Args:
            path1: First path.
            path2: Second path.

        Returns:
            True if paths match (case-insensitive on Windows).
        """
        try:
            # Resolve to absolute paths for comparison
            resolved1 = path1.resolve()
            resolved2 = path2.resolve()
            return resolved1 == resolved2
        except Exception:
            # Fall back to string comparison
            return str(path1) == str(path2)

    def filter_by_workspace(self, sessions: list[Session], workspace: Path) -> list[Session]:
        """Filter sessions by workspace directory.

        Args:
            sessions: List of sessions to filter.
            workspace: Workspace path to filter by.

        Returns:
            Sessions matching the workspace.
        """
        return [s for s in sessions if self._paths_match(Path(s.workspace_directory), workspace)]
