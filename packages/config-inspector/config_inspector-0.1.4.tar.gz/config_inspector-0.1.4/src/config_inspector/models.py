"""Data models for file operations."""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class FileMeta:
    """
    Metadata about a file.

    Attributes:
        label: Human-readable label for the file
        filepath: Full path to the file
        name: Filename with extension
        ext: File extension (with dot)
        size: Human-readable size string
        lang: Language/syntax for code editor
        modified: Human-readable modification timestamp
    """

    label: str
    filepath: Path
    name: str
    ext: str
    size: str
    lang: str
    modified: str

    def to_dict(self) -> dict:
        """
        Convert to dictionary representation.

        Returns:
            Dictionary with all metadata fields
        """
        return {
            "label": self.label,
            "filepath": str(self.filepath),
            "name": self.name,
            "ext": self.ext,
            "size": self.size,
            "lang": self.lang,
            "modified": self.modified,
        }


@dataclass
class FilePayload:
    """
    File contents with metadata.

    Attributes:
        meta: File metadata
        content: File contents as string
    """

    meta: FileMeta
    content: str

    def to_dict(self, key: str | None = None) -> dict:
        """
        Convert to dictionary with content included.

        Args:
            key: Top-level key to wrap the payload

        Returns:
            Dictionary with metadata and content
        """
        result = self.meta.to_dict()
        result["content"] = self.content
        if key is None:
            return result
        return {key: result}
