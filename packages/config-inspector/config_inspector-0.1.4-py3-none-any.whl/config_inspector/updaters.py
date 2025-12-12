"""Configuration file updaters using the Strategy pattern."""

import configparser
import json
import logging
from abc import ABC
from abc import abstractmethod
from pathlib import Path

import toml

logger = logging.getLogger(__name__)


class ConfigUpdater(ABC):
    """Abstract base class for configuration file updaters."""

    @abstractmethod
    def update(self, filepath: Path, content) -> None:
        """
        Update config file with validation.

        Args:
            filepath: Path to the config file
            content: New content (type varies by implementation)

        Raises:
            Various exceptions depending on format parsing errors
        """


class IniConfigUpdater(ConfigUpdater):
    """Updates INI configuration files with validation."""

    def update(self, filepath: Path, content: str) -> None:
        """
        Update INI config file.

        Args:
            filepath: Path to INI file
            content: INI content as string

        Raises:
            configparser.MissingSectionHeaderError: If INI is invalid
        """
        logger.info("Updating INI config: %s", filepath)

        # Validate by parsing
        config = configparser.ConfigParser()
        try:
            config.read_string(content)
        except configparser.MissingSectionHeaderError as err:
            logger.warning("INI decode error: %s", err)
            raise

        filepath.write_text(content, encoding="utf8", errors="replace")


class TomlConfigUpdater(ConfigUpdater):
    """Updates TOML configuration files with merging."""

    def update(self, filepath: Path, content: dict) -> None:
        """
        Update TOML config file, merging with existing content.

        Args:
            filepath: Path to TOML file
            content: Dictionary of values to merge

        Raises:
            toml.TomlDecodeError: If existing TOML is invalid
        """
        logger.info("Updating TOML config: %s", filepath)

        # Load existing config
        try:
            existing = toml.loads(filepath.read_text(encoding="utf8"))
        except toml.TomlDecodeError as err:
            logger.warning("TOML decode error: %s", err)
            raise

        # Merge and save
        existing.update(content)
        filepath.write_text(toml.dumps(existing), encoding="utf8", errors="replace")


class JsonConfigUpdater(ConfigUpdater):
    """Updates JSON configuration files with merging."""

    def update(self, filepath: Path, content: dict) -> None:
        """
        Update JSON config file, merging with existing content.

        Args:
            filepath: Path to JSON file
            content: Dictionary of values to merge

        Raises:
            json.JSONDecodeError: If existing JSON is invalid
        """
        logger.info("Updating JSON config: %s", filepath)

        # Load existing config
        try:
            existing = json.loads(filepath.read_text(encoding="utf8"))
        except json.JSONDecodeError as err:
            logger.warning("JSON decode error: %s", err)
            raise

        # Merge and save
        existing.update(content)
        filepath.write_text(
            json.dumps(existing, indent=4), encoding="utf8", errors="replace"
        )


class PlainTextUpdater(ConfigUpdater):
    """Updates plain text files without validation."""

    def update(self, filepath: Path, content: str) -> None:
        """
        Update plain text file (e.g., .bat, .sh, .txt).

        Args:
            filepath: Path to file
            content: New content as string
        """
        logger.info("Updating file: %s", filepath)
        filepath.write_text(content, encoding="utf8", errors="replace")


def updater_factory(file_extension: str) -> ConfigUpdater:
    """
    Factory function to get appropriate ConfigUpdater based on file extension.

    Args:
        file_extension: File extension (e.g., '.ini', '.toml', '.json', '.txt')

    Returns:
        Instance of ConfigUpdater

    Raises:
        ValueError: If no suitable updater is found
    """
    ext = file_extension.lower()
    if ext == ".ini":
        return IniConfigUpdater()
    if ext == ".toml":
        return TomlConfigUpdater()
    if ext == ".json":
        return JsonConfigUpdater()
    if ext in {".txt", ".sh", ".bat"}:
        return PlainTextUpdater()

    # logger.warning("No updater available for extension: %s", file_extension)
    return PlainTextUpdater()
