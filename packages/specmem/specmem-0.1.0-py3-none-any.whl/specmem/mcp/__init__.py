"""SpecMem MCP Server - Model Context Protocol integration for Kiro Powers.

This module provides an MCP server that exposes SpecMem functionality
as tools that Kiro can invoke through the Powers system.

Tools:
- specmem_query: Query specifications by natural language
- specmem_impact: Get specs and tests affected by file changes
- specmem_context: Get optimized context bundle for files
- specmem_tldr: Get TL;DR summary of key specifications
- specmem_coverage: Get spec coverage analysis
- specmem_validate: Validate specifications for quality issues
"""

from specmem.mcp.server import SpecMemMCPServer
from specmem.mcp.tools import TOOLS, get_tool_by_name


__all__ = [
    "TOOLS",
    "SpecMemMCPServer",
    "get_tool_by_name",
]
