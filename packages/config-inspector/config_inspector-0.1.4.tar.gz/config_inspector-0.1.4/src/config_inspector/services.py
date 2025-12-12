from datetime import datetime
from pathlib import Path

from config_inspector.models import FileMeta
from config_inspector.models import FilePayload
from config_inspector.protocols import DateTimeFormatter
from config_inspector.protocols import SizeFormatter


class FileMetadataService:
    """Service for extracting file metadata."""

    def __init__(
        self,
        size_formatter: SizeFormatter,
        datetime_formatter: DateTimeFormatter,
        lang_mapper: dict[str, str] | None = None,
    ):
        self.size_formatter = size_formatter
        self.datetime_formatter = datetime_formatter
        self.lang_mapper = lang_mapper or self._default_lang_mapper()

    def _default_lang_mapper(self) -> dict[str, str]:
        """Default language mapping for code editors."""
        return {
            ".bat": "batchfile",
            ".cfg": "ini",
            ".cmd": "batchfile",
            ".ini": "ini",
            ".js": "javascript",
            ".json": "json",
            ".ps1": "powershell",
            ".py": "python",
            ".sh": "sh",
            ".toml": "toml",
            ".yaml": "yaml",
            ".yml": "yaml",
        }

    def get_lang(self, filepath: Path) -> str:
        """Determine language/syntax for code editor."""
        return self.lang_mapper.get(filepath.suffix.lower(), "text")

    def get_metadata(self, filepath: Path, label: str | None = None) -> FileMeta:
        """Extract file metadata."""
        stat = filepath.stat()
        tz = datetime.now().astimezone().tzinfo
        modified_dt = datetime.fromtimestamp(stat.st_mtime, tz=tz)

        return FileMeta(
            label=label or filepath.stem,
            filepath=filepath,
            name=filepath.name,
            ext=filepath.suffix.lower(),
            size=self.size_formatter.format(stat.st_size),
            lang=self.get_lang(filepath),
            modified=self.datetime_formatter.format(modified_dt),
        )


class FileContentService:
    """Service for reading file contents with size validation."""

    def __init__(
        self,
        metadata_service: FileMetadataService,
        max_size_bytes: int = 268_435_455,  # ~256MB
    ):
        self.metadata_service = metadata_service
        self.max_size_bytes = max_size_bytes

    def is_valid_size(self, filepath: Path) -> bool:
        """Check if file size is within limits."""
        return filepath.stat().st_size < self.max_size_bytes

    def get_payload(self, filepath: Path, key: str, label: str | None = None) -> dict:
        """Get file contents as payload with metadata."""
        if not filepath.is_file():
            return {}

        if not self.is_valid_size(filepath):
            size = filepath.stat().st_size
            msg = (
                f"File {filepath} is too large ({size} bytes, "
                f"max {self.max_size_bytes} bytes)"
            )
            raise ValueError(msg)

        meta = self.metadata_service.get_metadata(filepath, label)
        # Should we ignore errors or replace invalid chars?
        content = filepath.read_text(encoding="utf-8", errors="replace")
        payload = FilePayload(meta, content)

        return payload.to_dict(key)
