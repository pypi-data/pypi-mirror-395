"""Session search configuration management.

Handles loading, saving, and validating session search configuration
in .specmem.toml files.
"""

import json
from pathlib import Path

from specmem.core.exceptions import ConfigurationError
from specmem.sessions.models import SessionConfig


try:
    import tomli
    import tomli_w

    TOML_AVAILABLE = True
except ImportError:
    TOML_AVAILABLE = False


class SessionConfigManager:
    """Manages session search configuration.

    Handles loading and saving session configuration to .specmem.toml,
    with support for interactive configuration and auto-discovery.
    """

    def __init__(self, config_path: Path | None = None):
        """Initialize the config manager.

        Args:
            config_path: Path to config file. Defaults to .specmem.toml in cwd.
        """
        self.config_path = config_path or Path.cwd() / ".specmem.toml"

    def load_config(self) -> SessionConfig | None:
        """Load existing session configuration from .specmem.toml.

        Returns:
            SessionConfig if configured, None if not configured or file doesn't exist.

        Raises:
            ConfigurationError: If config file exists but is invalid.
        """
        if not self.config_path.exists():
            return None

        try:
            content = self.config_path.read_text()

            if self.config_path.suffix == ".toml":
                if not TOML_AVAILABLE:
                    raise ConfigurationError(
                        "TOML support not available. Install tomli and tomli-w.",
                        code="TOML_NOT_AVAILABLE",
                    )
                data = tomli.loads(content)
            elif self.config_path.suffix == ".json":
                data = json.loads(content)
            else:
                return None

            sessions_data = data.get("sessions")
            if not sessions_data:
                return None

            return SessionConfig.from_dict(sessions_data)

        except Exception as e:
            if isinstance(e, ConfigurationError):
                raise
            raise ConfigurationError(
                f"Failed to load session config: {e}",
                code="CONFIG_LOAD_ERROR",
                details={"path": str(self.config_path), "error": str(e)},
            ) from e

    def save_config(self, config: SessionConfig) -> None:
        """Save session configuration to .specmem.toml.

        Args:
            config: Session configuration to save.

        Raises:
            ConfigurationError: If save fails.
        """
        try:
            # Load existing config or create new
            if self.config_path.exists():
                content = self.config_path.read_text()
                if self.config_path.suffix == ".toml":
                    if not TOML_AVAILABLE:
                        raise ConfigurationError(
                            "TOML support not available. Install tomli and tomli-w.",
                            code="TOML_NOT_AVAILABLE",
                        )
                    data = tomli.loads(content)
                else:
                    data = json.loads(content)
            else:
                data = {}

            # Update sessions section
            data["sessions"] = config.to_dict()

            # Write back
            if self.config_path.suffix == ".toml":
                if not TOML_AVAILABLE:
                    raise ConfigurationError(
                        "TOML support not available. Install tomli and tomli-w.",
                        code="TOML_NOT_AVAILABLE",
                    )
                output = tomli_w.dumps(data)
            else:
                output = json.dumps(data, indent=2)

            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            self.config_path.write_text(output)

        except Exception as e:
            if isinstance(e, ConfigurationError):
                raise
            raise ConfigurationError(
                f"Failed to save session config: {e}",
                code="CONFIG_SAVE_ERROR",
                details={"path": str(self.config_path), "error": str(e)},
            ) from e

    def is_configured(self) -> bool:
        """Check if session search is configured and enabled.

        Returns:
            True if session search is configured and enabled.
        """
        config = self.load_config()
        return config is not None and config.enabled and config.sessions_path is not None

    def configure_with_path(self, path: Path, workspace_only: bool = False) -> SessionConfig:
        """Configure session search with an explicit path.

        Args:
            path: Path to the Kiro sessions directory.
            workspace_only: If True, only search sessions for current workspace.

        Returns:
            The saved SessionConfig.

        Raises:
            ConfigurationError: If path is invalid.
        """
        # Validate path exists
        if not path.exists():
            raise ConfigurationError(
                f"Sessions directory does not exist: {path}",
                code="INVALID_PATH",
                details={"path": str(path)},
            )

        if not path.is_dir():
            raise ConfigurationError(
                f"Sessions path is not a directory: {path}",
                code="INVALID_PATH",
                details={"path": str(path)},
            )

        config = SessionConfig(
            sessions_path=path,
            workspace_only=workspace_only,
            enabled=True,
        )

        self.save_config(config)
        return config

    def disable(self) -> None:
        """Disable session search."""
        config = self.load_config() or SessionConfig()
        config.enabled = False
        self.save_config(config)

    def get_config_or_raise(self) -> SessionConfig:
        """Get session config or raise if not configured.

        Returns:
            SessionConfig if configured.

        Raises:
            SessionNotConfiguredError: If session search is not configured.
        """
        from specmem.sessions.exceptions import SessionNotConfiguredError

        config = self.load_config()
        if config is None or not config.enabled or config.sessions_path is None:
            raise SessionNotConfiguredError()

        return config
