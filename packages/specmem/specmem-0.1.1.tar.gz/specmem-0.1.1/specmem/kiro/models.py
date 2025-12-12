"""Data models for Kiro configuration indexing."""

from __future__ import annotations

import fnmatch
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


logger = logging.getLogger(__name__)


InclusionMode = Literal["always", "fileMatch", "manual"]
TriggerType = Literal["file_save", "manual", "session_start"]


@dataclass
class SteeringFile:
    """Parsed steering file with frontmatter metadata.

    Attributes:
        path: Path to the steering file
        content: Full content of the file (including frontmatter)
        body: Content without frontmatter
        inclusion: How the steering is included (always, fileMatch, manual)
        file_match_pattern: Glob pattern for fileMatch inclusion
        title: Title extracted from content
    """

    path: Path
    content: str
    body: str
    inclusion: InclusionMode = "always"
    file_match_pattern: str | None = None
    title: str = ""

    def matches_file(self, file_path: str) -> bool:
        """Check if this steering applies to a file.

        Args:
            file_path: Path to check against the pattern

        Returns:
            True if steering applies to the file
        """
        if self.inclusion == "always":
            return True
        if self.inclusion == "manual":
            return False
        if self.inclusion == "fileMatch" and self.file_match_pattern:
            try:
                # Normalize path separators
                normalized_path = file_path.replace("\\", "/")
                pattern = self.file_match_pattern.replace("\\", "/")

                # Try matching against filename and full path
                filename = Path(file_path).name
                if fnmatch.fnmatch(filename, pattern):
                    return True
                if fnmatch.fnmatch(normalized_path, pattern):
                    return True
                # Also try with ** prefix for recursive matching
                if "**" not in pattern:
                    if fnmatch.fnmatch(normalized_path, f"**/{pattern}"):
                        return True
                return False
            except Exception as e:
                logger.warning(f"Invalid pattern '{self.file_match_pattern}': {e}")
                return False
        return False


@dataclass
class MCPServerInfo:
    """Parsed MCP server configuration.

    Attributes:
        name: Server identifier
        command: Command to run the server
        args: Command arguments
        env: Environment variables
        disabled: Whether the server is disabled
        auto_approve: List of auto-approved tool names
    """

    name: str
    command: str
    args: list[str] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    disabled: bool = False
    auto_approve: list[str] = field(default_factory=list)


@dataclass
class MCPToolInfo:
    """Information about an MCP tool.

    Attributes:
        server_name: Name of the server providing this tool
        tool_name: Name of the tool
        description: Tool description
        auto_approved: Whether the tool is auto-approved
    """

    server_name: str
    tool_name: str
    description: str = ""
    auto_approved: bool = False


@dataclass
class HookInfo:
    """Parsed hook configuration.

    Attributes:
        name: Hook identifier
        description: Hook description
        trigger: What triggers the hook
        file_pattern: Glob pattern for file-based triggers
        action: Command or action to execute
        enabled: Whether the hook is enabled
    """

    name: str
    description: str = ""
    trigger: TriggerType = "manual"
    file_pattern: str | None = None
    action: str = ""
    enabled: bool = True

    def matches_file(self, file_path: str) -> bool:
        """Check if hook's file pattern matches a file.

        Args:
            file_path: Path to check against the pattern

        Returns:
            True if pattern matches or no pattern is set
        """
        if not self.file_pattern:
            return True
        try:
            normalized_path = file_path.replace("\\", "/")
            pattern = self.file_pattern.replace("\\", "/")
            filename = Path(file_path).name

            if fnmatch.fnmatch(filename, pattern):
                return True
            if fnmatch.fnmatch(normalized_path, pattern):
                return True
            if "**" not in pattern:
                if fnmatch.fnmatch(normalized_path, f"**/{pattern}"):
                    return True
            return False
        except Exception as e:
            logger.warning(f"Invalid hook pattern '{self.file_pattern}': {e}")
            return False


@dataclass
class KiroConfigSummary:
    """Summary of all Kiro configuration.

    Attributes:
        steering_files: List of parsed steering files
        mcp_servers: List of MCP server configurations
        hooks: List of hook configurations
        total_tools: Total number of MCP tools
        enabled_servers: Number of enabled MCP servers
        active_hooks: Number of active hooks
    """

    steering_files: list[SteeringFile] = field(default_factory=list)
    mcp_servers: list[MCPServerInfo] = field(default_factory=list)
    hooks: list[HookInfo] = field(default_factory=list)
    total_tools: int = 0
    enabled_servers: int = 0
    active_hooks: int = 0
