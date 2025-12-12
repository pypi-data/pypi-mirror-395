import logging
from pathlib import Path

from config_inspector.updaters import ConfigUpdater
from config_inspector.updaters import IniConfigUpdater
from config_inspector.updaters import JsonConfigUpdater
from config_inspector.updaters import PlainTextUpdater

# from config_inspector.updaters import TomlConfigUpdater

logger = logging.getLogger(__name__)


class ConfigManager:
    """Facade for managing configuration files."""

    def __init__(self):
        self.updaters: dict[str, ConfigUpdater] = {
            ".ini": IniConfigUpdater(),
            ".cfg": IniConfigUpdater(),
            # ".toml": TomlConfigUpdater(),  # strips comments
            ".toml": PlainTextUpdater(),
            ".json": JsonConfigUpdater(),
            ".bat": PlainTextUpdater(),
            ".ps1": PlainTextUpdater(),
            ".cmd": PlainTextUpdater(),
            ".sh": PlainTextUpdater(),
            ".js": PlainTextUpdater(),
        }

    def update(self, filepath: Path, content: str | dict) -> None:
        """Update config file using appropriate updater."""
        ext = filepath.suffix.lower()
        updater = self.updaters.get(ext)

        if not updater:
            msg = f"No updater found for file type: {ext}"
            logging.error(msg)
            raise ValueError(msg)

        updater.update(filepath, content)

    def register_updater(self, extension: str, updater: ConfigUpdater) -> None:
        """Register custom updater for file extension."""
        self.updaters[extension] = updater
