"""MCP Tool definitions for SpecMem.

Defines the tools exposed by the SpecMem MCP server following
the Model Context Protocol specification.
"""

from typing import Any


# Tool definitions following MCP specification
TOOLS: list[dict[str, Any]] = [
    {
        "name": "specmem_query",
        "description": "Query specifications by natural language. Returns relevant specs matching the query.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Natural language query to search specifications",
                },
                "top_k": {
                    "type": "integer",
                    "default": 10,
                    "description": "Maximum number of results to return",
                },
                "include_legacy": {
                    "type": "boolean",
                    "default": False,
                    "description": "Whether to include legacy/deprecated specs",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "specmem_impact",
        "description": "Get specs and tests affected by file changes. Analyzes the SpecImpact graph to find related specifications.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "files": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of file paths to analyze",
                },
                "depth": {
                    "type": "integer",
                    "default": 2,
                    "description": "Maximum traversal depth for transitive relationships",
                },
            },
            "required": ["files"],
        },
    },
    {
        "name": "specmem_context",
        "description": "Get optimized context bundle for files. Returns specs, designs, and tests relevant to the given files within a token budget.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "files": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of file paths to get context for",
                },
                "token_budget": {
                    "type": "integer",
                    "default": 4000,
                    "description": "Maximum tokens for the context bundle",
                },
            },
            "required": ["files"],
        },
    },
    {
        "name": "specmem_tldr",
        "description": "Get TL;DR summary of key specifications. Returns a concise summary prioritizing pinned specs.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "token_budget": {
                    "type": "integer",
                    "default": 500,
                    "description": "Maximum tokens for the summary",
                },
            },
        },
    },
    {
        "name": "specmem_coverage",
        "description": "Get spec coverage analysis. Analyzes gaps between acceptance criteria and existing tests.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "feature": {
                    "type": "string",
                    "description": "Optional feature name to analyze (analyzes all if not provided)",
                },
            },
        },
    },
    {
        "name": "specmem_validate",
        "description": "Validate specifications for quality issues. Checks for contradictions, missing criteria, and other problems.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "spec_id": {
                    "type": "string",
                    "description": "Optional spec ID to validate (validates all if not provided)",
                },
            },
        },
    },
]


def get_tool_by_name(name: str) -> dict[str, Any] | None:
    """Get a tool definition by name.

    Args:
        name: The tool name to look up

    Returns:
        Tool definition dict or None if not found
    """
    for tool in TOOLS:
        if tool["name"] == name:
            return tool
    return None


def get_tool_names() -> list[str]:
    """Get list of all tool names.

    Returns:
        List of tool name strings
    """
    return [tool["name"] for tool in TOOLS]
