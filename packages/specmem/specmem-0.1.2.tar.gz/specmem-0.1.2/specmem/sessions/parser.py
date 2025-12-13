"""Kiro session file parser.

Parses Kiro session files into normalized Session data structures.
"""

import json
from pathlib import Path
from typing import Any

from specmem.sessions.exceptions import SessionParseError
from specmem.sessions.models import (
    MessageRole,
    Session,
    SessionMessage,
    normalize_timestamp,
)


class KiroSessionParser:
    """Parses Kiro session files into normalized Session objects.

    Handles the Kiro session file format including:
    - sessions.json index files
    - Individual session JSON files with history arrays
    - Content arrays with text and tool_use items
    """

    def parse_sessions_index(self, index_path: Path) -> list[dict[str, Any]]:
        """Parse sessions.json index file.

        Args:
            index_path: Path to sessions.json file.

        Returns:
            List of session metadata dictionaries with keys:
            - sessionId: Unique session identifier
            - title: Human-readable session title
            - dateCreated: Creation timestamp
            - workspaceDirectory: Associated workspace path

        Raises:
            SessionParseError: If file is invalid or missing required fields.
        """
        try:
            content = index_path.read_text()
            data = json.loads(content)
        except json.JSONDecodeError as e:
            raise SessionParseError(index_path, f"Invalid JSON: {e}") from e
        except Exception as e:
            raise SessionParseError(index_path, str(e)) from e

        # Handle both array format and object with sessions key
        if isinstance(data, list):
            sessions = data
        elif isinstance(data, dict) and "sessions" in data:
            sessions = data["sessions"]
        else:
            raise SessionParseError(index_path, "Expected array or object with 'sessions' key")

        # Validate required fields
        for i, session in enumerate(sessions):
            if not isinstance(session, dict):
                raise SessionParseError(index_path, f"Session {i} is not an object")
            if "sessionId" not in session:
                raise SessionParseError(index_path, f"Session {i} missing 'sessionId'")

        return sessions

    def parse_session_file(self, session_path: Path) -> Session:
        """Parse individual session JSON file.

        Args:
            session_path: Path to session JSON file.

        Returns:
            Normalized Session object with messages.

        Raises:
            SessionParseError: If file is invalid or missing required fields.
        """
        try:
            content = session_path.read_text()
            data = json.loads(content)
        except json.JSONDecodeError as e:
            raise SessionParseError(session_path, f"Invalid JSON: {e}") from e
        except Exception as e:
            raise SessionParseError(session_path, str(e)) from e

        if not isinstance(data, dict):
            raise SessionParseError(session_path, "Expected JSON object")

        # Extract session metadata
        session_id = data.get("sessionId", session_path.stem)
        title = data.get("title", "Untitled Session")
        workspace_directory = data.get("workspaceDirectory", "")
        date_created = data.get("dateCreated")

        # Parse timestamp
        date_created_ms = normalize_timestamp(date_created) or 0

        # Parse messages from history array
        history = data.get("history", [])
        messages = self._parse_messages(history, session_path)

        return Session(
            session_id=session_id,
            title=title,
            workspace_directory=workspace_directory,
            date_created_ms=date_created_ms,
            messages=messages,
            metadata=data.get("metadata", {}),
            session_path=session_path,
        )

    def _parse_messages(self, history: list[Any], session_path: Path) -> list[SessionMessage]:
        """Parse message history array.

        Args:
            history: List of message objects from session file.
            session_path: Path to session file (for error messages).

        Returns:
            List of normalized SessionMessage objects.
        """
        messages = []

        for i, msg in enumerate(history):
            if not isinstance(msg, dict):
                continue  # Skip invalid messages

            role_str = msg.get("role", "user")
            try:
                role = SessionMessage.normalize_role(role_str)
            except ValueError:
                role = MessageRole.USER  # Default to user for unknown roles

            # Flatten content
            raw_content = msg.get("content", "")
            content = self.flatten_content(raw_content)

            # Extract tool calls
            tool_calls = self.extract_tool_calls(msg)

            # Parse timestamp if present
            timestamp = msg.get("timestamp")
            timestamp_ms = normalize_timestamp(timestamp) if timestamp else None

            messages.append(
                SessionMessage(
                    role=role,
                    content=content,
                    timestamp_ms=timestamp_ms,
                    tool_calls=tool_calls if tool_calls else None,
                    raw_content=raw_content,
                )
            )

        return messages

    def flatten_content(self, content: Any) -> str:
        """Flatten content arrays into readable text.

        Handles various content formats:
        - Plain string
        - Array of text objects: [{"type": "text", "text": "..."}]
        - Array with tool_use: [{"type": "tool_use", "name": "...", ...}]
        - Mixed arrays

        Args:
            content: Content in any supported format.

        Returns:
            Flattened string representation.
        """
        if content is None:
            return ""

        if isinstance(content, str):
            return content

        if isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, str):
                    parts.append(item)
                elif isinstance(item, dict):
                    item_type = item.get("type", "")

                    if item_type == "text":
                        text = item.get("text", "")
                        if text:
                            parts.append(text)

                    elif item_type == "tool_use":
                        tool_name = item.get("name", "unknown_tool")
                        tool_input = item.get("input", {})
                        # Format tool call as readable text
                        parts.append(f"[Tool: {tool_name}]")
                        if isinstance(tool_input, dict):
                            for key, value in tool_input.items():
                                if isinstance(value, str) and len(value) < 100:
                                    parts.append(f"  {key}: {value}")

                    elif item_type == "tool_result":
                        result = item.get("content", "")
                        if isinstance(result, str) and result:
                            # Truncate long results
                            if len(result) > 500:
                                result = result[:500] + "..."
                            parts.append(f"[Result: {result}]")

                    else:
                        # Unknown type, try to extract text
                        text = item.get("text", "")
                        if text:
                            parts.append(text)

            return "\n".join(parts)

        # Fallback: convert to string
        return str(content)

    def extract_tool_calls(self, message: dict[str, Any]) -> list[dict[str, Any]]:
        """Extract tool call information from message.

        Args:
            message: Message dictionary.

        Returns:
            List of tool call dictionaries with name, input, and id.
        """
        tool_calls = []

        content = message.get("content", [])
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get("type") == "tool_use":
                    tool_calls.append(
                        {
                            "name": item.get("name", "unknown"),
                            "input": item.get("input", {}),
                            "id": item.get("id", ""),
                        }
                    )

        return tool_calls
