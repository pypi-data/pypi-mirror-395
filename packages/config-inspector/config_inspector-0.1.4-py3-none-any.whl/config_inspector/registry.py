from pathlib import Path

from config_inspector.services import FileMeta
from config_inspector.services import FileMetadataService


class FileRegistry:
    """Registry for tracking files with metadata."""

    def __init__(self, metadata_service: FileMetadataService):
        self.metadata_service = metadata_service
        self._files: list[tuple[Path, str | None]] = []

    def register(self, filepath: Path, label: str | None = None) -> None:
        """Register a file to track."""
        if filepath.is_file() and not self.is_registered(filepath):
            self._files.append((filepath, label))

    def get_all_metadata(self) -> list[FileMeta]:
        """Get metadata for all registered files that exist."""
        result = []
        for filepath, label in self._files:
            if filepath.is_file():
                result.append(self.metadata_service.get_metadata(filepath, label))
        return result

    def is_registered(self, filepath: Path) -> bool:
        """Check if file is registered."""
        return any(f == filepath for f, _ in self._files)

    def clear(self) -> None:
        """Clear all registered files."""
        self._files.clear()

    def list_files(self) -> list[tuple[Path, str | None]]:
        """List all registered file paths and labels."""
        return self._files
