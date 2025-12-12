"""Hook parser for Kiro configuration."""

from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING

from specmem.kiro.models import HookInfo, TriggerType


if TYPE_CHECKING:
    from pathlib import Path


logger = logging.getLogger(__name__)


class HookParser:
    """Parses hook configuration files from .kiro/hooks/."""

    def parse(self, hook_path: Path) -> HookInfo | None:
        """Parse a single hook JSON file.

        Args:
            hook_path: Path to the hook JSON file

        Returns:
            Parsed HookInfo object, or None if parsing fails
        """
        try:
            content = hook_path.read_text(encoding="utf-8")
            data = json.loads(content)
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse hook {hook_path}: {e}")
            return None
        except Exception as e:
            logger.warning(f"Failed to read hook {hook_path}: {e}")
            return None

        if not isinstance(data, dict):
            logger.warning(f"Invalid hook format in {hook_path}")
            return None

        # Extract trigger type
        trigger = self._get_trigger_type(data.get("trigger", "manual"))

        hook = HookInfo(
            name=data.get("name", hook_path.stem),
            description=data.get("description", ""),
            trigger=trigger,
            file_pattern=data.get("filePattern"),
            action=data.get("action", ""),
            enabled=data.get("enabled", True),
        )

        logger.debug(f"Parsed hook: {hook.name}")
        return hook

    def parse_directory(self, hooks_dir: Path) -> list[HookInfo]:
        """Parse all hook files in a directory.

        Args:
            hooks_dir: Path to .kiro/hooks/ directory

        Returns:
            List of parsed HookInfo objects
        """
        if not hooks_dir.exists():
            return []

        hooks = []
        for hook_path in hooks_dir.glob("*.json"):
            if hook_path.is_file():
                hook = self.parse(hook_path)
                if hook:
                    hooks.append(hook)

        return hooks

    def get_hooks_for_trigger(
        self,
        hooks: list[HookInfo],
        trigger: TriggerType,
        file_path: str | None = None,
    ) -> list[HookInfo]:
        """Get hooks matching a trigger type and optional file pattern.

        Args:
            hooks: List of all hooks
            trigger: Trigger type to filter by
            file_path: Optional file path to match against patterns

        Returns:
            List of matching hooks
        """
        matching = []

        for hook in hooks:
            if not hook.enabled:
                continue
            if hook.trigger != trigger:
                continue

            # If file_path provided, check pattern match
            if file_path is not None:
                if not hook.matches_file(file_path):
                    continue

            matching.append(hook)

        return matching

    def get_enabled_hooks(self, hooks: list[HookInfo]) -> list[HookInfo]:
        """Get only enabled hooks.

        Args:
            hooks: List of all hooks

        Returns:
            List of enabled hooks only
        """
        return [h for h in hooks if h.enabled]

    def get_disabled_hooks(self, hooks: list[HookInfo]) -> list[HookInfo]:
        """Get only disabled hooks.

        Args:
            hooks: List of all hooks

        Returns:
            List of disabled hooks only
        """
        return [h for h in hooks if not h.enabled]

    def _get_trigger_type(self, trigger: str) -> TriggerType:
        """Validate and return trigger type.

        Args:
            trigger: Trigger string from config

        Returns:
            Valid TriggerType
        """
        if trigger in ("file_save", "manual", "session_start"):
            return trigger
        logger.warning(f"Invalid trigger type '{trigger}', defaulting to 'manual'")
        return "manual"

    def serialize(self, hook: HookInfo) -> str:
        """Serialize hook back to JSON format.

        Args:
            hook: HookInfo to serialize

        Returns:
            JSON string
        """
        data = {
            "name": hook.name,
            "description": hook.description,
            "trigger": hook.trigger,
            "enabled": hook.enabled,
        }
        if hook.file_pattern:
            data["filePattern"] = hook.file_pattern
        if hook.action:
            data["action"] = hook.action

        return json.dumps(data, indent=2)
