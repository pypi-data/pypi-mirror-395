"""Power Graph Builder - Builds graph nodes and edges for Kiro Powers.

Extends the SpecImpact graph to track relationships between Powers,
code files, and specifications.
"""

from __future__ import annotations

import fnmatch
import logging
import re
from pathlib import Path
from typing import TYPE_CHECKING

from specmem.impact.graph_models import EdgeType, GraphEdge, GraphNode, NodeType


if TYPE_CHECKING:
    from specmem.adapters.power import PowerInfo
    from specmem.core.specir import SpecBlock


logger = logging.getLogger(__name__)


class PowerGraphBuilder:
    """Builds graph nodes and edges for Kiro Powers.

    Creates:
    - POWER nodes for each installed Power
    - PROVIDES edges from Powers to code files matching steering patterns
    - USES edges from specs that reference Power tools
    """

    def __init__(self, workspace_path: Path | str) -> None:
        """Initialize the builder.

        Args:
            workspace_path: Path to the workspace root
        """
        self.workspace_path = Path(workspace_path)

    def build_power_nodes(self, powers: list[PowerInfo]) -> list[GraphNode]:
        """Create graph nodes for each installed Power.

        Args:
            powers: List of PowerInfo objects

        Returns:
            List of GraphNode objects for the Powers
        """
        nodes: list[GraphNode] = []

        for power in powers:
            node_id = f"power:{power.name}"
            node = GraphNode(
                id=node_id,
                type=NodeType.POWER,
                data={
                    "name": power.name,
                    "description": power.description,
                    "path": str(power.path),
                    "keywords": power.keywords,
                    "tools": [t.name for t in power.tools],
                    "version": power.version,
                },
                confidence=1.0,
                suggested=False,
            )
            nodes.append(node)
            logger.debug(f"Created Power node: {node_id}")

        return nodes

    def build_power_edges(
        self,
        power: PowerInfo,
        code_files: list[Path],
        specs: list[SpecBlock],
    ) -> list[GraphEdge]:
        """Create edges linking a Power to code and specs.

        Args:
            power: PowerInfo for the Power
            code_files: List of code file paths in the workspace
            specs: List of SpecBlocks in the workspace

        Returns:
            List of GraphEdge objects
        """
        edges: list[GraphEdge] = []
        power_node_id = f"power:{power.name}"

        # Extract code patterns from steering files
        patterns = self._extract_code_patterns_from_power(power)

        # Create PROVIDES edges to matching code files
        for code_file in code_files:
            rel_path = str(code_file.relative_to(self.workspace_path))
            for pattern in patterns:
                if self._matches_pattern(rel_path, pattern):
                    code_node_id = f"code:{rel_path}"
                    edge = GraphEdge(
                        source_id=power_node_id,
                        target_id=code_node_id,
                        relationship=EdgeType.PROVIDES,
                        confidence=0.7,  # Pattern-based matching
                        metadata={"pattern": pattern},
                    )
                    edges.append(edge)
                    logger.debug(f"Created PROVIDES edge: {power_node_id} -> {code_node_id}")
                    break  # Only one edge per file

        # Create USES edges from specs that reference Power tools
        tool_names = [t.name for t in power.tools]
        for spec in specs:
            if self._spec_references_tools(spec, tool_names):
                spec_node_id = f"spec:{spec.id}"
                edge = GraphEdge(
                    source_id=spec_node_id,
                    target_id=power_node_id,
                    relationship=EdgeType.USES,
                    confidence=0.8,
                    metadata={"tools": tool_names},
                )
                edges.append(edge)
                logger.debug(f"Created USES edge: {spec_node_id} -> {power_node_id}")

        return edges

    def _extract_code_patterns_from_power(self, power: PowerInfo) -> list[str]:
        """Extract code file patterns from Power steering files.

        Looks for patterns like:
        - `*.py`, `**/*.ts`
        - File references in code blocks
        - Explicit file patterns in steering content

        Args:
            power: PowerInfo for the Power

        Returns:
            List of glob patterns
        """
        patterns: list[str] = []

        for steering_file in power.steering_files:
            try:
                content = steering_file.read_text()
                patterns.extend(self._extract_patterns_from_content(content))
            except Exception as e:
                logger.warning(f"Failed to read steering file {steering_file}: {e}")

        # Also check keywords for language hints
        language_patterns = {
            "python": ["**/*.py"],
            "typescript": ["**/*.ts", "**/*.tsx"],
            "javascript": ["**/*.js", "**/*.jsx"],
            "rust": ["**/*.rs"],
            "go": ["**/*.go"],
        }
        for keyword in power.keywords:
            keyword_lower = keyword.lower()
            if keyword_lower in language_patterns:
                patterns.extend(language_patterns[keyword_lower])

        return list(set(patterns))  # Deduplicate

    def _extract_patterns_from_content(self, content: str) -> list[str]:
        """Extract file patterns from markdown content.

        Args:
            content: Markdown content to parse

        Returns:
            List of glob patterns found
        """
        patterns: list[str] = []

        # Match glob patterns like *.py, **/*.ts, src/**/*.js
        glob_pattern = r"[`'\"]?(\*\*?/?\*?\.[a-zA-Z]+)[`'\"]?"
        matches = re.findall(glob_pattern, content)
        patterns.extend(matches)

        # Match explicit file paths like src/auth.py
        path_pattern = r"[`'\"]([a-zA-Z0-9_/.-]+\.[a-zA-Z]+)[`'\"]"
        path_matches = re.findall(path_pattern, content)
        for path in path_matches:
            # Convert specific paths to patterns
            if "/" in path:
                # Keep directory structure but allow any file
                dir_part = "/".join(path.split("/")[:-1])
                ext = path.split(".")[-1]
                patterns.append(f"{dir_part}/**/*.{ext}")

        return patterns

    def _matches_pattern(self, file_path: str, pattern: str) -> bool:
        """Check if a file path matches a glob pattern.

        Args:
            file_path: Relative file path
            pattern: Glob pattern

        Returns:
            True if the path matches the pattern
        """
        # Handle ** patterns
        if "**" in pattern:
            # Convert ** to regex
            regex_pattern = pattern.replace(".", r"\.").replace("**", ".*").replace("*", "[^/]*")
            return bool(re.match(regex_pattern, file_path))
        else:
            return fnmatch.fnmatch(file_path, pattern)

    def _spec_references_tools(self, spec: SpecBlock, tool_names: list[str]) -> bool:
        """Check if a spec references any of the given tool names.

        Args:
            spec: SpecBlock to check
            tool_names: List of tool names to look for

        Returns:
            True if the spec references any tool
        """
        text_lower = spec.text.lower()
        for tool_name in tool_names:
            if tool_name.lower() in text_lower:
                return True
        return False

    def remove_power_nodes(
        self,
        power_name: str,
        nodes: dict[str, GraphNode],
        edges: list[GraphEdge],
    ) -> tuple[dict[str, GraphNode], list[GraphEdge]]:
        """Remove a Power's nodes and edges from the graph.

        Args:
            power_name: Name of the Power to remove
            nodes: Current graph nodes
            edges: Current graph edges

        Returns:
            Tuple of (updated nodes, updated edges)
        """
        power_node_id = f"power:{power_name}"

        # Remove the Power node
        if power_node_id in nodes:
            del nodes[power_node_id]
            logger.debug(f"Removed Power node: {power_node_id}")

        # Remove edges involving this Power
        edges = [e for e in edges if power_node_id not in (e.source_id, e.target_id)]

        return nodes, edges
