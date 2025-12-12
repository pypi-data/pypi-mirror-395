import pytest

from config_inspector.services import FileContentService
from config_inspector.services import FileMetadataService


class DummySizeFormatter:
    def format(self, size):
        return f"{size} bytes"


class DummyDateTimeFormatter:
    def format(self, dt):
        return dt.strftime("%Y-%m-%d %H:%M:%S")


def test_file_metadata_service(tmp_path):
    file = tmp_path / "test.py"
    file.write_text("print('hello')")

    service = FileMetadataService(
        size_formatter=DummySizeFormatter(), datetime_formatter=DummyDateTimeFormatter()
    )

    meta = service.get_metadata(file, label="mylabel")
    assert meta.label == "mylabel"
    assert meta.filepath == file
    assert meta.name == "test.py"
    assert meta.ext == ".py"
    assert meta.size.endswith("bytes")
    assert meta.lang == "python"
    assert isinstance(meta.modified, str)


def test_file_content_service_valid(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("hello world")

    meta_service = FileMetadataService(
        size_formatter=DummySizeFormatter(), datetime_formatter=DummyDateTimeFormatter()
    )
    content_service = FileContentService(meta_service, max_size_bytes=100)

    payload = content_service.get_payload(file, key="myfile", label="lbl")
    assert "myfile" in payload
    assert payload["myfile"]["label"] == "lbl"
    assert payload["myfile"]["name"] == "test.txt"
    assert payload["myfile"]["ext"] == ".txt"
    assert payload["myfile"]["size"].endswith("bytes")
    assert payload["myfile"]["lang"] == "text"
    assert isinstance(payload["myfile"]["modified"], str)
    assert payload["myfile"]["content"] == "hello world"


def test_file_content_service_too_large(tmp_path):
    file = tmp_path / "big.txt"
    file.write_text("x" * 200)

    meta_service = FileMetadataService(
        size_formatter=DummySizeFormatter(), datetime_formatter=DummyDateTimeFormatter()
    )
    content_service = FileContentService(meta_service, max_size_bytes=100)

    with pytest.raises(ValueError):
        content_service.get_payload(file, key="file")


def test_file_content_service_nonexistent(tmp_path):
    file = tmp_path / "nofile.txt"

    meta_service = FileMetadataService(
        size_formatter=DummySizeFormatter(), datetime_formatter=DummyDateTimeFormatter()
    )
    content_service = FileContentService(meta_service, max_size_bytes=100)

    payload = content_service.get_payload(file, key="file")
    assert payload == {}


def test_file_content_service_no_key(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("hello world")

    meta_service = FileMetadataService(
        size_formatter=DummySizeFormatter(), datetime_formatter=DummyDateTimeFormatter()
    )
    content_service = FileContentService(meta_service, max_size_bytes=100)

    payload = content_service.get_payload(file, key=None, label="lbl")
    assert payload["label"] == "lbl"
    assert payload["name"] == "test.txt"
    assert payload["ext"] == ".txt"
    assert payload["size"].endswith("bytes")
    assert payload["lang"] == "text"
    assert isinstance(payload["modified"], str)
    assert payload["content"] == "hello world"
