from pathlib import Path

import pytest

from config_inspector.registry import FileRegistry


class DummyMeta:
    def __init__(self, path, label):
        self.path = str(path)
        self.label = label


class DummyMetadataService:
    def get_metadata(self, filepath, label=None):
        return DummyMeta(filepath, label)


def test_register_and_get_all_metadata(tmp_path):
    service = DummyMetadataService()
    registry = FileRegistry(service)

    file1 = tmp_path / "file1.txt"
    file1.write_text("abc")
    file2 = tmp_path / "file2.txt"
    file2.write_text("def")

    registry.register(file1, label="A")
    registry.register(file2)

    metas = registry.get_all_metadata()
    assert len(metas) == 2
    assert metas[0].path == str(file1)
    assert metas[0].label == "A"
    assert metas[1].path == str(file2)
    assert metas[1].label is None


def test_register_nonexistent_file(tmp_path):
    service = DummyMetadataService()
    registry = FileRegistry(service)

    non_existent = tmp_path / "nofile.txt"
    registry.register(non_existent)
    assert registry.get_all_metadata() == []


def test_is_registered(tmp_path):
    service = DummyMetadataService()
    registry = FileRegistry(service)

    file1 = tmp_path / "file1.txt"
    file1.write_text("abc")
    file2 = tmp_path / "file2.txt"

    registry.register(file1)
    assert registry.is_registered(file1)
    assert not registry.is_registered(file2)


def test_clear(tmp_path):
    service = DummyMetadataService()
    registry = FileRegistry(service)

    file1 = tmp_path / "file1.txt"
    file1.write_text("abc")
    registry.register(file1)
    assert registry.is_registered(file1)
    registry.clear()
    assert not registry.is_registered(file1)


def test_list_files(tmp_path):
    service = DummyMetadataService()
    registry = FileRegistry(service)

    file1 = tmp_path / "file1.txt"
    file1.write_text("abc")
    file2 = tmp_path / "file2.txt"
    file2.write_text("def")

    registry.register(file1, label="A")
    registry.register(file2)

    files = registry.list_files()
    # print(files)
    assert len(files) == 2
    assert files[0] == (Path(file1), "A")
    assert files[1] == (Path(file2), None)
