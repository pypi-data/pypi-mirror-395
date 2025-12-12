import io
import tarfile
import zipfile

import pytest

from config_inspector.operations import ArchiveExtractor
from config_inspector.operations import FileDownloader


class DummyResponse:
    def __init__(self, content):
        self.raw = io.BytesIO(content)
        self.status_code = 200

    def raise_for_status(self):  # pragma: no cover
        if self.status_code != 200:  # noqa: PLR2004
            msg = "HTTP error"
            raise Exception(msg)  # noqa: TRY002


@pytest.fixture
def monkeypatch_requests_get(monkeypatch):
    def _patch(content):
        def fake_get(url, stream=True, timeout=10):
            return DummyResponse(content)

        monkeypatch.setattr("requests.get", fake_get)

    return _patch


def test_file_downloader_download(tmp_path, monkeypatch_requests_get):
    content = b"hello world"
    monkeypatch_requests_get(content)
    downloader = FileDownloader()
    url = "http://example.com/test.txt"
    dest_file = downloader.download(url, tmp_path)
    assert dest_file.exists()
    assert dest_file.read_bytes() == content


def test_file_downloader_download_overwrite(tmp_path, monkeypatch_requests_get):
    content = b"new content"
    monkeypatch_requests_get(content)
    downloader = FileDownloader()
    url = "http://example.com/test.txt"
    dest_file = tmp_path / "test.txt"
    dest_file.write_text("old content")
    result = downloader.download(url, tmp_path)
    assert result.exists()
    assert result.read_bytes() == content


def test_archive_extractor_extract_zip(tmp_path):
    # Create a zip file
    zip_path = tmp_path / "test.zip"
    file_inside = "foo.txt"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr(file_inside, "bar")
    extract_dir = tmp_path / "unzipped"
    extractor = ArchiveExtractor()
    extractor.extract_zip(zip_path, extract_dir)
    extracted_file = extract_dir / file_inside
    assert extracted_file.exists()
    assert extracted_file.read_text() == "bar"


def test_archive_extractor_extract_tar_gz(tmp_path):
    tar_path = tmp_path / "test.tar.gz"
    file_inside = "foo.txt"
    file_content = b"bar"
    file_to_add = tmp_path / file_inside
    file_to_add.write_bytes(file_content)
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(file_to_add, arcname=file_inside)
    file_to_add.unlink()
    extract_dir = tmp_path / "untarred"
    extractor = ArchiveExtractor()
    extractor.extract_tar_gz(tar_path, extract_dir)
    extracted_file = extract_dir / file_inside
    assert extracted_file.exists()
    assert extracted_file.read_bytes() == file_content
