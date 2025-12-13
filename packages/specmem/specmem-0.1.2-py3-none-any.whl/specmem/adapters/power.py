"""Kiro Power adapter for SpecMem.

Parses Kiro Power configurations (POWER.md, steering files, mcp.json)
and converts them to SpecBlock format for inclusion in spec memory.
"""

import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from specmem.adapters.base import SpecAdapter
from specmem.core.specir import SpecBlock, SpecStatus, SpecType


logger = logging.getLogger(__name__)


@dataclass
class ToolInfo:
    """Information about an MCP tool."""

    name: str
    description: str
    input_schema: dict = field(default_factory=dict)


@dataclass
class PowerInfo:
    """Information about an installed Kiro Power."""

    name: str
    path: Path
    description: str = ""
    tools: list[ToolInfo] = field(default_factory=list)
    steering_files: list[Path] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    version: str | None = None


class PowerAdapter(SpecAdapter):
    """Adapter for Kiro Power configurations.

    Detects and parses:
    - .kiro/powers/*/POWER.md - Power documentation
    - .kiro/powers/*/steering/*.md - Steering files
    - .kiro/powers/*/mcp.json - MCP configuration (for tool metadata)
    """

    @property
    def name(self) -> str:
        return "KiroPower"

    def detect(self, repo_path: str) -> bool:
        """Check if any Powers are installed in the repository."""
        powers_dir = Path(repo_path) / ".kiro" / "powers"
        if not powers_dir.exists():
            return False

        # Check for any Power directories with POWER.md
        for power_dir in powers_dir.iterdir():
            if power_dir.is_dir():
                power_md = power_dir / "POWER.md"
                if power_md.exists():
                    return True

        return False

    def load(self, repo_path: str) -> list[SpecBlock]:
        """Load and parse all Power configurations."""
        blocks: list[SpecBlock] = []
        powers_dir = Path(repo_path) / ".kiro" / "powers"

        if not powers_dir.exists():
            return blocks

        for power_dir in powers_dir.iterdir():
            if not power_dir.is_dir():
                continue

            try:
                power_info = self._load_power_info(power_dir)
                if power_info:
                    # Parse POWER.md
                    power_md = power_dir / "POWER.md"
                    if power_md.exists():
                        blocks.extend(self._parse_power_md(power_md, power_info))

                    # Parse steering files
                    blocks.extend(self._parse_steering_files(power_dir, power_info))

            except Exception as e:
                logger.warning(f"Failed to load Power from {power_dir}: {e}")

        logger.info(f"Loaded {len(blocks)} SpecBlocks from Kiro Powers")
        return blocks

    def _load_power_info(self, power_dir: Path) -> PowerInfo | None:
        """Load Power information from directory."""
        power_md = power_dir / "POWER.md"
        mcp_json = power_dir / "mcp.json"

        if not power_md.exists():
            return None

        # Extract name from directory
        name = power_dir.name

        # Try to get more info from mcp.json
        description = ""
        keywords: list[str] = []
        tools: list[ToolInfo] = []
        version = None

        if mcp_json.exists():
            try:
                mcp_config = self._parse_mcp_config(mcp_json)
                name = mcp_config.get("displayName", mcp_config.get("name", name))
                description = mcp_config.get("description", "")
                keywords = mcp_config.get("keywords", [])
                version = mcp_config.get("version")

                # Extract tool info if available
                for tool_def in mcp_config.get("tools", []):
                    tools.append(
                        ToolInfo(
                            name=tool_def.get("name", ""),
                            description=tool_def.get("description", ""),
                            input_schema=tool_def.get("inputSchema", {}),
                        )
                    )
            except Exception as e:
                logger.warning(f"Failed to parse mcp.json for {power_dir}: {e}")

        # Find steering files
        steering_dir = power_dir / "steering"
        steering_files: list[Path] = []
        if steering_dir.exists():
            steering_files = list(steering_dir.glob("*.md"))

        return PowerInfo(
            name=name,
            path=power_dir,
            description=description,
            tools=tools,
            steering_files=steering_files,
            keywords=keywords,
            version=version,
        )

    def _parse_power_md(self, file_path: Path, power_info: PowerInfo) -> list[SpecBlock]:
        """Parse POWER.md file into SpecBlocks."""
        blocks: list[SpecBlock] = []
        source = str(file_path)

        try:
            content = file_path.read_text()
        except Exception as e:
            logger.warning(f"Failed to read {file_path}: {e}")
            return blocks

        # Create main Power block with overview
        block_id = SpecBlock.generate_id(source, f"power_{power_info.name}_overview")
        tags = ["power", power_info.name.lower().replace(" ", "_")]
        tags.extend(power_info.keywords)

        # Extract description from content if not in mcp.json
        description = power_info.description
        if not description:
            # Try to extract from first paragraph
            lines = content.split("\n")
            for line in lines:
                line = line.strip()
                if line and not line.startswith("#"):
                    description = line[:200]
                    break

        overview_text = f"[Power: {power_info.name}]\n{description}"
        if power_info.version:
            overview_text += f"\nVersion: {power_info.version}"

        blocks.append(
            SpecBlock(
                id=block_id,
                type=SpecType.KNOWLEDGE,
                text=overview_text,
                source=source,
                status=SpecStatus.ACTIVE,
                tags=tags,
                pinned=True,  # Power overviews are important context
            )
        )

        # Extract sections from POWER.md
        section_blocks = self._extract_markdown_sections(content, source, power_info)
        blocks.extend(section_blocks)

        # Create blocks for tools
        for tool in power_info.tools:
            tool_block_id = SpecBlock.generate_id(
                source, f"power_{power_info.name}_tool_{tool.name}"
            )
            tool_text = f"[Tool: {tool.name}]\n{tool.description}"

            blocks.append(
                SpecBlock(
                    id=tool_block_id,
                    type=SpecType.DESIGN,
                    text=tool_text,
                    source=source,
                    status=SpecStatus.ACTIVE,
                    tags=["power", "tool", tool.name, power_info.name.lower()],
                )
            )

        return blocks

    def _parse_steering_files(self, power_dir: Path, power_info: PowerInfo) -> list[SpecBlock]:
        """Parse steering files into SpecBlocks."""
        blocks: list[SpecBlock] = []
        steering_dir = power_dir / "steering"

        if not steering_dir.exists():
            return blocks

        for steering_file in steering_dir.glob("*.md"):
            try:
                content = steering_file.read_text()
                source = str(steering_file)

                # Create block for steering file
                block_id = SpecBlock.generate_id(
                    source, f"power_{power_info.name}_steering_{steering_file.stem}"
                )

                # Extract title from first heading or filename
                title = steering_file.stem.replace("-", " ").replace("_", " ").title()
                lines = content.split("\n")
                for line in lines:
                    if line.startswith("#"):
                        title = line.lstrip("#").strip()
                        break

                # Truncate content if too long
                text = f"[Steering: {title}]\n{content}"
                if len(text) > 1000:
                    text = text[:1000] + "..."

                blocks.append(
                    SpecBlock(
                        id=block_id,
                        type=SpecType.TASK,  # Steering files are workflow guides
                        text=text,
                        source=source,
                        status=SpecStatus.ACTIVE,
                        tags=["power", "steering", power_info.name.lower(), steering_file.stem],
                    )
                )

            except Exception as e:
                logger.warning(f"Failed to parse steering file {steering_file}: {e}")

        return blocks

    def _parse_mcp_config(self, file_path: Path) -> dict[str, Any]:
        """Parse mcp.json configuration file."""
        try:
            content = file_path.read_text()
            return json.loads(content)
        except Exception as e:
            logger.warning(f"Failed to parse {file_path}: {e}")
            return {}

    def _extract_markdown_sections(
        self, content: str, source: str, power_info: PowerInfo
    ) -> list[SpecBlock]:
        """Extract sections from markdown content."""
        blocks: list[SpecBlock] = []

        # Split by headers (## level)
        section_pattern = r"##\s+(.+?)\n(.*?)(?=##\s|\Z)"
        matches = re.findall(section_pattern, content, re.DOTALL)

        for title, body in matches:
            title = title.strip()
            body = body.strip()

            if not body or len(body) < 20:
                continue

            # Skip certain sections
            if title.lower() in ("table of contents", "toc", "contents"):
                continue

            block_id = SpecBlock.generate_id(source, f"power_{power_info.name}_section_{title}")

            # Truncate body if too long
            text = f"[{title}]\n{body}"
            if len(text) > 800:
                text = text[:800] + "..."

            # Determine type based on section title
            spec_type = SpecType.KNOWLEDGE
            if any(kw in title.lower() for kw in ["usage", "example", "workflow", "guide"]):
                spec_type = SpecType.TASK
            elif any(kw in title.lower() for kw in ["architecture", "design", "tool"]):
                spec_type = SpecType.DESIGN

            blocks.append(
                SpecBlock(
                    id=block_id,
                    type=spec_type,
                    text=text,
                    source=source,
                    status=SpecStatus.ACTIVE,
                    tags=["power", power_info.name.lower(), title.lower().replace(" ", "_")[:30]],
                )
            )

        return blocks
