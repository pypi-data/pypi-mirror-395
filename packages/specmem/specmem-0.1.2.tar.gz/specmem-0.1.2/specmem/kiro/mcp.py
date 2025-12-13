"""MCP configuration parser for Kiro configuration."""

from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Any

from specmem.kiro.models import MCPServerInfo, MCPToolInfo


if TYPE_CHECKING:
    from pathlib import Path


logger = logging.getLogger(__name__)


class MCPConfigParser:
    """Parses MCP server configuration from mcp.json."""

    def parse(self, config_path: Path) -> list[MCPServerInfo]:
        """Parse mcp.json configuration file.

        Args:
            config_path: Path to mcp.json file

        Returns:
            List of MCPServerInfo objects
        """
        if not config_path.exists():
            return []

        try:
            content = config_path.read_text(encoding="utf-8")
            data = json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse mcp.json: {e}")
            return []
        except Exception as e:
            logger.warning(f"Failed to read mcp.json: {e}")
            return []

        servers = []
        mcp_servers = data.get("mcpServers", {})

        for name, config in mcp_servers.items():
            if not isinstance(config, dict):
                logger.warning(f"Invalid server config for '{name}'")
                continue

            server = MCPServerInfo(
                name=name,
                command=config.get("command", ""),
                args=config.get("args", []),
                env=config.get("env", {}),
                disabled=config.get("disabled", False),
                auto_approve=config.get("autoApprove", []),
            )
            servers.append(server)
            logger.debug(f"Parsed MCP server: {name}")

        return servers

    def get_tools(self, servers: list[MCPServerInfo]) -> list[MCPToolInfo]:
        """Extract tool information from servers.

        Note: Tool metadata is typically not in mcp.json directly,
        but we can infer from autoApprove lists and server names.

        Args:
            servers: List of parsed server configurations

        Returns:
            List of MCPToolInfo objects
        """
        tools = []

        for server in servers:
            if server.disabled:
                continue

            # Create tool entries from autoApprove list
            for tool_name in server.auto_approve:
                tool = MCPToolInfo(
                    server_name=server.name,
                    tool_name=tool_name,
                    description=f"Auto-approved tool from {server.name}",
                    auto_approved=True,
                )
                tools.append(tool)

            # Also create a generic entry for the server itself
            tool = MCPToolInfo(
                server_name=server.name,
                tool_name=f"{server.name}_server",
                description=f"MCP server: {server.command} {' '.join(server.args)}",
                auto_approved=False,
            )
            tools.append(tool)

        return tools

    def get_enabled_servers(self, servers: list[MCPServerInfo]) -> list[MCPServerInfo]:
        """Get only enabled servers.

        Args:
            servers: List of all server configurations

        Returns:
            List of enabled servers only
        """
        return [s for s in servers if not s.disabled]

    def get_disabled_servers(self, servers: list[MCPServerInfo]) -> list[MCPServerInfo]:
        """Get only disabled servers.

        Args:
            servers: List of all server configurations

        Returns:
            List of disabled servers only
        """
        return [s for s in servers if s.disabled]

    def serialize(self, servers: list[MCPServerInfo]) -> str:
        """Serialize servers back to mcp.json format.

        Args:
            servers: List of server configurations

        Returns:
            JSON string
        """
        mcp_servers: dict[str, Any] = {}

        for server in servers:
            config: dict[str, Any] = {
                "command": server.command,
            }
            if server.args:
                config["args"] = server.args
            if server.env:
                config["env"] = server.env
            if server.disabled:
                config["disabled"] = server.disabled
            if server.auto_approve:
                config["autoApprove"] = server.auto_approve

            mcp_servers[server.name] = config

        return json.dumps({"mcpServers": mcp_servers}, indent=2)
