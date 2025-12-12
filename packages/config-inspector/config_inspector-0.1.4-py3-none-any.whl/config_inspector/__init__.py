"""
FileKit - A generic file management toolkit.

Provides utilities for:
- Config file updates (INI, JSON, TOML)
- File metadata extraction
- Archive operations (zip, tar.gz)
- File downloads
- Content management with size limits
"""

import logging

from .manager import ConfigManager
from .models import FileMeta
from .models import FilePayload
from .operations import ArchiveExtractor
from .operations import FileDownloader
from .registry import FileRegistry
from .services import FileContentService
from .services import FileMetadataService
from .updaters import IniConfigUpdater
from .updaters import JsonConfigUpdater
from .updaters import PlainTextUpdater
from .updaters import TomlConfigUpdater
from .updaters import updater_factory

# Basic logger setup; users of this package can configure logging as needed
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

__version__ = "0.1.4"

__all__ = [
    "ArchiveExtractor",
    "ConfigManager",
    "FileContentService",
    "FileDownloader",
    "FileMeta",
    "FileMetadataService",
    "FilePayload",
    "FileRegistry",
    "IniConfigUpdater",
    "JsonConfigUpdater",
    "PlainTextUpdater",
    "TomlConfigUpdater",
    "updater_factory",
]
