"""Protocol definitions for dependency injection."""

from abc import ABC
from abc import abstractmethod
from datetime import datetime


class SizeFormatter(ABC):
    """Protocol for formatting byte sizes to human-readable strings."""

    @abstractmethod
    def format(self, size_bytes: int) -> str:
        """
        Format byte size to human-readable string.

        Args:
            size_bytes: Size in bytes

        Returns:
            Formatted string (e.g., "1.5 MB", "500 KB")
        """
        ...


class DateTimeFormatter(ABC):
    """Protocol for formatting datetime objects to strings."""

    @abstractmethod
    def format(self, dt: datetime) -> str:
        """
        Format datetime to string.

        Args:
            dt: Datetime object to format

        Returns:
            Formatted datetime string
        """
        ...
