"""Steering file parser for Kiro configuration."""

from __future__ import annotations

import logging
import re
from typing import TYPE_CHECKING, Any

import yaml

from specmem.kiro.models import InclusionMode, SteeringFile


if TYPE_CHECKING:
    from pathlib import Path


logger = logging.getLogger(__name__)

# Regex to match YAML frontmatter
FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


class SteeringParser:
    """Parses steering files with YAML frontmatter support."""

    def parse(self, file_path: Path) -> SteeringFile:
        """Parse a single steering file.

        Args:
            file_path: Path to the steering file

        Returns:
            Parsed SteeringFile object
        """
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            logger.warning(f"Failed to read steering file {file_path}: {e}")
            return SteeringFile(
                path=file_path,
                content="",
                body="",
                title=file_path.stem,
            )

        # Parse frontmatter
        frontmatter = self.parse_frontmatter(content)
        body = self.extract_body(content)

        # Extract metadata
        inclusion = self._get_inclusion_mode(frontmatter)
        file_match_pattern = frontmatter.get("fileMatchPattern")

        # Extract title from content
        title = self._extract_title(body, file_path)

        return SteeringFile(
            path=file_path,
            content=content,
            body=body,
            inclusion=inclusion,
            file_match_pattern=file_match_pattern,
            title=title,
        )

    def parse_frontmatter(self, content: str) -> dict[str, Any]:
        """Extract YAML frontmatter from content.

        Args:
            content: Full file content

        Returns:
            Dictionary of frontmatter values
        """
        match = FRONTMATTER_PATTERN.match(content)
        if not match:
            return {}

        try:
            frontmatter_text = match.group(1)
            parsed = yaml.safe_load(frontmatter_text)
            return parsed if isinstance(parsed, dict) else {}
        except yaml.YAMLError as e:
            logger.warning(f"Failed to parse YAML frontmatter: {e}")
            return {}

    def extract_body(self, content: str) -> str:
        """Extract content without frontmatter.

        Args:
            content: Full file content

        Returns:
            Content without frontmatter
        """
        match = FRONTMATTER_PATTERN.match(content)
        if match:
            return content[match.end() :].strip()
        return content.strip()

    def parse_directory(self, steering_dir: Path) -> list[SteeringFile]:
        """Parse all steering files in a directory.

        Args:
            steering_dir: Path to .kiro/steering/ directory

        Returns:
            List of parsed SteeringFile objects
        """
        if not steering_dir.exists():
            return []

        steering_files = []
        for file_path in steering_dir.glob("*.md"):
            if file_path.is_file():
                steering_file = self.parse(file_path)
                steering_files.append(steering_file)
                logger.debug(f"Parsed steering file: {file_path.name}")

        return steering_files

    def _get_inclusion_mode(self, frontmatter: dict[str, Any]) -> InclusionMode:
        """Get inclusion mode from frontmatter.

        Args:
            frontmatter: Parsed frontmatter dictionary

        Returns:
            Inclusion mode (defaults to 'always')
        """
        inclusion = frontmatter.get("inclusion", "always")
        if inclusion in ("always", "fileMatch", "manual"):
            return inclusion
        logger.warning(f"Invalid inclusion mode '{inclusion}', defaulting to 'always'")
        return "always"

    def _extract_title(self, body: str, file_path: Path) -> str:
        """Extract title from content body.

        Args:
            body: Content without frontmatter
            file_path: Path to file (used as fallback)

        Returns:
            Extracted title
        """
        # Look for first heading
        for line in body.split("\n"):
            line = line.strip()
            if line.startswith("#"):
                return line.lstrip("#").strip()

        # Fallback to filename
        return file_path.stem.replace("-", " ").replace("_", " ").title()

    def serialize_frontmatter(self, steering: SteeringFile) -> str:
        """Serialize steering file back to markdown with frontmatter.

        Args:
            steering: SteeringFile to serialize

        Returns:
            Markdown content with frontmatter
        """
        frontmatter: dict[str, Any] = {}

        if steering.inclusion != "always":
            frontmatter["inclusion"] = steering.inclusion
        if steering.file_match_pattern:
            frontmatter["fileMatchPattern"] = steering.file_match_pattern

        if frontmatter:
            yaml_content = yaml.dump(frontmatter, default_flow_style=False).strip()
            return f"---\n{yaml_content}\n---\n\n{steering.body}"

        return steering.body
