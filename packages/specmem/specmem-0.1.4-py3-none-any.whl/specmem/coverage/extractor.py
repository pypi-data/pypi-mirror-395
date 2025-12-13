"""Criteria Extractor for Spec Coverage Analysis.

Extracts acceptance criteria from spec requirements.md files.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

from specmem.coverage.models import AcceptanceCriterion


logger = logging.getLogger(__name__)


class CriteriaExtractor:
    """Extracts acceptance criteria from spec files.

    Parses requirements.md files to extract numbered acceptance criteria
    in EARS format.
    """

    # Pattern to match requirement headers like "### Requirement 1" or "### Requirement 1: Title"
    REQUIREMENT_PATTERN = re.compile(
        r"^###\s+Requirement\s+(\d+)(?::\s*(.+))?$",
        re.MULTILINE,
    )

    # Pattern to match user story
    USER_STORY_PATTERN = re.compile(
        r"\*\*User Story:\*\*\s*(.+?)(?=\n\n|\n####|\Z)",
        re.DOTALL,
    )

    # Pattern to match acceptance criteria section
    AC_SECTION_PATTERN = re.compile(
        r"####\s+Acceptance Criteria\s*\n(.*?)(?=\n###|\n##|\Z)",
        re.DOTALL,
    )

    # Pattern to match numbered criteria like "1. WHEN..." or "1. THE system SHALL..."
    CRITERION_PATTERN = re.compile(
        r"^(\d+)\.\s+(.+?)(?=\n\d+\.|\Z)",
        re.MULTILINE | re.DOTALL,
    )

    def __init__(self, workspace_path: Path | str) -> None:
        """Initialize the criteria extractor.

        Args:
            workspace_path: Path to the workspace root
        """
        self.workspace_path = Path(workspace_path).resolve()
        self.specs_dir = self.workspace_path / ".kiro" / "specs"

    def extract_from_spec(self, spec_path: Path | str) -> list[AcceptanceCriterion]:
        """Extract all criteria from a spec's requirements.md.

        Args:
            spec_path: Path to the spec directory or requirements.md file

        Returns:
            List of AcceptanceCriterion objects
        """
        spec_path = Path(spec_path)

        # Handle both directory and file paths
        if spec_path.is_dir():
            requirements_file = spec_path / "requirements.md"
            feature_name = spec_path.name
        else:
            requirements_file = spec_path
            feature_name = spec_path.parent.name

        if not requirements_file.exists():
            logger.warning(f"Requirements file not found: {requirements_file}")
            return []

        content = requirements_file.read_text()
        return self.parse_requirements_md(content, feature_name)

    def extract_all(self) -> dict[str, list[AcceptanceCriterion]]:
        """Extract criteria from all specs in workspace.

        Returns:
            Dict mapping feature names to lists of criteria
        """
        result: dict[str, list[AcceptanceCriterion]] = {}

        if not self.specs_dir.exists():
            logger.warning(f"Specs directory not found: {self.specs_dir}")
            return result

        for spec_dir in self.specs_dir.iterdir():
            if spec_dir.is_dir():
                criteria = self.extract_from_spec(spec_dir)
                if criteria:
                    result[spec_dir.name] = criteria

        return result

    def parse_requirements_md(
        self,
        content: str,
        feature_name: str,
    ) -> list[AcceptanceCriterion]:
        """Parse requirements.md content and extract criteria.

        Args:
            content: The markdown content
            feature_name: Name of the feature

        Returns:
            List of AcceptanceCriterion objects
        """
        criteria: list[AcceptanceCriterion] = []

        # Find all requirements
        req_matches = list(self.REQUIREMENT_PATTERN.finditer(content))

        for i, req_match in enumerate(req_matches):
            req_num = req_match.group(1)
            req_match.group(2) or ""

            # Get the content between this requirement and the next
            start = req_match.end()
            end = req_matches[i + 1].start() if i + 1 < len(req_matches) else len(content)
            req_content = content[start:end]

            # Extract user story
            user_story = ""
            story_match = self.USER_STORY_PATTERN.search(req_content)
            if story_match:
                user_story = story_match.group(1).strip()

            # Extract acceptance criteria section
            ac_match = self.AC_SECTION_PATTERN.search(req_content)
            if not ac_match:
                continue

            ac_content = ac_match.group(1)

            # Extract individual criteria
            for crit_match in self.CRITERION_PATTERN.finditer(ac_content):
                crit_num = crit_match.group(1)
                crit_text = crit_match.group(2).strip()

                # Clean up the text (remove extra whitespace)
                crit_text = " ".join(crit_text.split())

                criterion_id = f"{feature_name}.{req_num}.{crit_num}"

                try:
                    criterion = AcceptanceCriterion(
                        id=criterion_id,
                        number=f"{req_num}.{crit_num}",
                        text=crit_text,
                        requirement_id=req_num,
                        user_story=user_story,
                        feature_name=feature_name,
                    )
                    criteria.append(criterion)
                except ValueError as e:
                    logger.warning(f"Invalid criterion {criterion_id}: {e}")

        return criteria

    def get_feature_names(self) -> list[str]:
        """Get list of all feature names in the workspace.

        Returns:
            List of feature names
        """
        if not self.specs_dir.exists():
            return []

        return [
            d.name
            for d in self.specs_dir.iterdir()
            if d.is_dir() and (d / "requirements.md").exists()
        ]
