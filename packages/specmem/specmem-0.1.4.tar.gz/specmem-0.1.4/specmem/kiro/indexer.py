"""Kiro Configuration Indexer - main orchestrator."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from specmem.core.specir import SpecBlock, SpecStatus, SpecType
from specmem.kiro.hooks import HookParser
from specmem.kiro.mcp import MCPConfigParser
from specmem.kiro.models import (
    HookInfo,
    KiroConfigSummary,
    MCPServerInfo,
    MCPToolInfo,
    SteeringFile,
)
from specmem.kiro.steering import SteeringParser


if TYPE_CHECKING:
    from pathlib import Path


logger = logging.getLogger(__name__)


class KiroConfigIndexer:
    """Indexes all Kiro CLI configuration artifacts.

    Indexes:
    - Steering files (.kiro/steering/*.md)
    - MCP configuration (.kiro/settings/mcp.json)
    - Hooks (.kiro/hooks/*.json)
    """

    def __init__(self, workspace_path: Path):
        """Initialize the indexer.

        Args:
            workspace_path: Path to the workspace root
        """
        self.workspace_path = workspace_path
        self.kiro_path = workspace_path / ".kiro"

        self._steering_parser = SteeringParser()
        self._mcp_parser = MCPConfigParser()
        self._hook_parser = HookParser()

        # Cached parsed data
        self._steering_files: list[SteeringFile] = []
        self._mcp_servers: list[MCPServerInfo] = []
        self._hooks: list[HookInfo] = []

    def index_all(self) -> list[SpecBlock]:
        """Index all Kiro configuration files.

        Returns:
            List of SpecBlocks from all config sources
        """
        blocks = []
        blocks.extend(self.index_steering())
        blocks.extend(self.index_mcp_config())
        blocks.extend(self.index_hooks())

        logger.info(
            f"Indexed Kiro config: {len(self._steering_files)} steering, "
            f"{len(self._mcp_servers)} MCP servers, {len(self._hooks)} hooks"
        )
        return blocks

    def index_steering(self) -> list[SpecBlock]:
        """Index steering files from .kiro/steering/.

        Returns:
            List of SpecBlocks from steering files
        """
        steering_dir = self.kiro_path / "steering"
        self._steering_files = self._steering_parser.parse_directory(steering_dir)

        blocks = []
        for steering in self._steering_files:
            block = self._steering_to_specblock(steering)
            blocks.append(block)

        return blocks

    def index_mcp_config(self) -> list[SpecBlock]:
        """Index MCP configuration from .kiro/settings/mcp.json.

        Returns:
            List of SpecBlocks from MCP config
        """
        mcp_path = self.kiro_path / "settings" / "mcp.json"
        self._mcp_servers = self._mcp_parser.parse(mcp_path)

        blocks = []
        for server in self._mcp_servers:
            block = self._mcp_server_to_specblock(server)
            blocks.append(block)

        return blocks

    def index_hooks(self) -> list[SpecBlock]:
        """Index hooks from .kiro/hooks/.

        Returns:
            List of SpecBlocks from hooks
        """
        hooks_dir = self.kiro_path / "hooks"
        self._hooks = self._hook_parser.parse_directory(hooks_dir)

        blocks = []
        for hook in self._hooks:
            block = self._hook_to_specblock(hook)
            blocks.append(block)

        return blocks

    def get_steering_for_file(self, file_path: str) -> list[SteeringFile]:
        """Get steering files applicable to a specific file.

        Args:
            file_path: Path to check

        Returns:
            List of applicable steering files
        """
        applicable = []
        for steering in self._steering_files:
            if steering.matches_file(file_path):
                applicable.append(steering)
        return applicable

    def get_available_tools(self) -> list[MCPToolInfo]:
        """Get list of available (enabled) MCP tools.

        Returns:
            List of tools from enabled servers
        """
        enabled = self._mcp_parser.get_enabled_servers(self._mcp_servers)
        return self._mcp_parser.get_tools(enabled)

    def get_hooks_for_trigger(
        self,
        trigger: str,
        file_path: str | None = None,
    ) -> list[HookInfo]:
        """Get hooks matching a trigger type and optional file pattern.

        Args:
            trigger: Trigger type (file_save, manual, session_start)
            file_path: Optional file path to match

        Returns:
            List of matching hooks
        """
        if trigger not in ("file_save", "manual", "session_start"):
            return []
        return self._hook_parser.get_hooks_for_trigger(
            self._hooks,
            trigger,
            file_path,  # type: ignore
        )

    def get_summary(self) -> KiroConfigSummary:
        """Get summary of all Kiro configuration.

        Returns:
            KiroConfigSummary with all config data
        """
        enabled_servers = self._mcp_parser.get_enabled_servers(self._mcp_servers)
        active_hooks = self._hook_parser.get_enabled_hooks(self._hooks)
        tools = self.get_available_tools()

        return KiroConfigSummary(
            steering_files=self._steering_files,
            mcp_servers=self._mcp_servers,
            hooks=self._hooks,
            total_tools=len(tools),
            enabled_servers=len(enabled_servers),
            active_hooks=len(active_hooks),
        )

    def _steering_to_specblock(self, steering: SteeringFile) -> SpecBlock:
        """Convert steering file to SpecBlock.

        Args:
            steering: Parsed steering file

        Returns:
            SpecBlock representation
        """
        # Determine priority based on inclusion mode
        pinned = steering.inclusion == "always"

        tags = ["steering", "config", "kiro"]
        if steering.inclusion:
            tags.append(f"inclusion:{steering.inclusion}")
        if steering.file_match_pattern:
            tags.append(f"pattern:{steering.file_match_pattern}")

        block_id = SpecBlock.generate_id(str(steering.path), f"steering_{steering.path.stem}")

        return SpecBlock(
            id=block_id,
            type=SpecType.KNOWLEDGE,
            text=f"[Steering: {steering.title}] {steering.body[:500]}",
            source=str(steering.path),
            tags=tags,
            pinned=pinned,
            status=SpecStatus.ACTIVE,
        )

    def _mcp_server_to_specblock(self, server: MCPServerInfo) -> SpecBlock:
        """Convert MCP server to SpecBlock.

        Args:
            server: Parsed MCP server config

        Returns:
            SpecBlock representation
        """
        status = SpecStatus.LEGACY if server.disabled else SpecStatus.ACTIVE

        tags = ["mcp", "config", "kiro", f"server:{server.name}"]
        if server.disabled:
            tags.append("disabled")
        if server.auto_approve:
            tags.append("auto_approve")

        text = f"[MCP Server: {server.name}] {server.command} {' '.join(server.args)}"
        if server.auto_approve:
            text += f" (auto-approve: {', '.join(server.auto_approve)})"

        block_id = SpecBlock.generate_id(
            str(self.kiro_path / "settings" / "mcp.json"), f"mcp_{server.name}"
        )

        return SpecBlock(
            id=block_id,
            type=SpecType.KNOWLEDGE,
            text=text,
            source=str(self.kiro_path / "settings" / "mcp.json"),
            tags=tags,
            pinned=False,
            status=status,
        )

    def _hook_to_specblock(self, hook: HookInfo) -> SpecBlock:
        """Convert hook to SpecBlock.

        Args:
            hook: Parsed hook config

        Returns:
            SpecBlock representation
        """
        status = SpecStatus.ACTIVE if hook.enabled else SpecStatus.LEGACY

        tags = ["hook", "config", "kiro", f"trigger:{hook.trigger}"]
        if hook.file_pattern:
            tags.append(f"pattern:{hook.file_pattern}")
        if not hook.enabled:
            tags.append("disabled")

        text = f"[Hook: {hook.name}] {hook.description}"
        if hook.action:
            text += f" Action: {hook.action}"

        block_id = SpecBlock.generate_id(str(self.kiro_path / "hooks"), f"hook_{hook.name}")

        return SpecBlock(
            id=block_id,
            type=SpecType.TASK,
            text=text,
            source=str(self.kiro_path / "hooks" / f"{hook.name}.json"),
            tags=tags,
            pinned=False,
            status=status,
        )
