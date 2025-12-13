"""Kiro Hooks Generator implementation."""

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Literal


logger = logging.getLogger(__name__)


@dataclass
class KiroHook:
    """Configuration for a Kiro Hook.

    Kiro Hooks allow automated agent actions based on file events.
    """

    name: str
    description: str
    trigger: Literal["file_save", "manual", "session_start"]
    file_pattern: str | None = None
    action: str = ""
    enabled: bool = True

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        result = {
            "name": self.name,
            "description": self.description,
            "trigger": self.trigger,
            "enabled": self.enabled,
        }
        if self.file_pattern:
            result["filePattern"] = self.file_pattern
        if self.action:
            result["action"] = self.action
        return result


class KiroHooksGenerator:
    """Generates Kiro Hook configurations for SpecMem integration.

    Creates hooks that:
    - Validate specs on save
    - Update coverage when tests change
    - Remind agents about relevant specs
    """

    def __init__(self, workspace_path: Path):
        """Initialize the hooks generator.

        Args:
            workspace_path: Path to the workspace root
        """
        self.workspace_path = workspace_path
        self.hooks_path = workspace_path / ".kiro" / "hooks"

    def generate_hooks(self) -> list[KiroHook]:
        """Generate all SpecMem hooks.

        Returns:
            List of KiroHook configurations
        """
        hooks = []

        # Hook 1: Validate specs on save
        hooks.append(
            KiroHook(
                name="specmem-validate-on-save",
                description="Automatically validate specifications when saved",
                trigger="file_save",
                file_pattern=".kiro/specs/**/*.md",
                action="specmem validate --file ${file}",
            )
        )

        # Hook 2: Update coverage when tests change
        hooks.append(
            KiroHook(
                name="specmem-coverage-on-test-save",
                description="Update spec coverage analysis when tests are modified",
                trigger="file_save",
                file_pattern="tests/**/*.py",
                action="specmem cov --quiet",
            )
        )

        # Hook 3: Remind agent about relevant specs (manual trigger)
        hooks.append(
            KiroHook(
                name="specmem-context-reminder",
                description="Get relevant specs for the current file",
                trigger="manual",
                action="specmem impact --files ${file} --format markdown",
            )
        )

        # Hook 4: Session start - load context
        hooks.append(
            KiroHook(
                name="specmem-session-context",
                description="Load relevant spec context at session start",
                trigger="session_start",
                action="specmem query 'What are the key requirements and constraints?'",
            )
        )

        return hooks

    def write_hooks(self, hooks: list[KiroHook] | None = None) -> int:
        """Write hooks to the .kiro/hooks/ directory.

        Args:
            hooks: Optional list of hooks to write. If None, generates default hooks.

        Returns:
            Number of hooks written
        """
        if hooks is None:
            hooks = self.generate_hooks()

        # Create hooks directory
        self.hooks_path.mkdir(parents=True, exist_ok=True)

        count = 0
        for hook in hooks:
            hook_file = self.hooks_path / f"{hook.name}.json"

            # Don't overwrite existing hooks
            if hook_file.exists():
                logger.info(f"Hook already exists: {hook.name}")
                continue

            hook_file.write_text(json.dumps(hook.to_dict(), indent=2))
            count += 1
            logger.info(f"Created hook: {hook.name}")

        return count

    def list_hooks(self) -> list[KiroHook]:
        """List existing hooks in the workspace.

        Returns:
            List of existing KiroHook configurations
        """
        hooks = []

        if not self.hooks_path.exists():
            return hooks

        for hook_file in self.hooks_path.glob("*.json"):
            try:
                data = json.loads(hook_file.read_text())
                hook = KiroHook(
                    name=data.get("name", hook_file.stem),
                    description=data.get("description", ""),
                    trigger=data.get("trigger", "manual"),
                    file_pattern=data.get("filePattern"),
                    action=data.get("action", ""),
                    enabled=data.get("enabled", True),
                )
                hooks.append(hook)
            except Exception as e:
                logger.warning(f"Failed to load hook {hook_file}: {e}")

        return hooks
