"""File operation utilities (download, extract)."""

import logging
import shutil
import tarfile
import zipfile
from pathlib import Path

import requests

logger = logging.getLogger(__name__)


class FileDownloader:
    """Handles HTTP file downloads."""

    def __init__(self, timeout: int = 10):
        """
        Initialize downloader.

        Args:
            timeout: HTTP request timeout in seconds
        """
        self.timeout = timeout

    def download(self, url: str, dest_dir: Path) -> Path:
        """
        Download file from URL to destination directory.

        Args:
            url: URL to download from
            dest_dir: Directory to save file in

        Returns:
            Path to downloaded file

        Raises:
            requests.exceptions.RequestException: On download failure
        """
        filename = Path(url).name
        dest_file = dest_dir / filename

        # Remove existing file
        if dest_file.exists():
            dest_file.unlink()

        logger.info("Downloading %s => %s", url, dest_file)

        response = requests.get(url, stream=True, timeout=self.timeout)
        response.raise_for_status()

        with dest_file.open("wb") as f:
            shutil.copyfileobj(response.raw, f)

        logger.debug("Download complete: %s", dest_file)
        return dest_file


class ArchiveExtractor:
    """Handles archive extraction (ZIP, tar.gz)."""

    def extract_zip(self, filepath: Path, dest_dir: Path) -> None:
        """
        Extract ZIP archive.

        Args:
            filepath: Path to ZIP file
            dest_dir: Directory to extract to

        Raises:
            zipfile.BadZipFile: If file is not a valid ZIP
        """
        logger.info("Extracting zip %s => %s", filepath, dest_dir)
        dest_dir.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(filepath, "r") as zip_ref:
            zip_ref.extractall(dest_dir)  # noqa: S202

        logger.debug("Extraction complete")

    def extract_tar_gz(self, filepath: Path, dest_dir: Path) -> None:
        """
        Extract tar.gz archive.

        Args:
            filepath: Path to tar.gz file
            dest_dir: Directory to extract to

        Raises:
            tarfile.TarError: If file is not a valid tar.gz
        """
        logger.info("Extracting tar.gz %s => %s", filepath, dest_dir)
        dest_dir.mkdir(parents=True, exist_ok=True)

        with tarfile.open(filepath, "r:gz") as tar:
            tar.extractall(dest_dir)  # noqa: S202

        logger.debug("Extraction complete")
