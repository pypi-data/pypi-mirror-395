import pytest

from config_inspector.manager import ConfigManager
from config_inspector.updaters import ConfigUpdater


class DummyUpdater(ConfigUpdater):
    def __init__(self):
        self.called = False
        self.last_args = None

    def update(self, filepath, content):
        self.called = True
        self.last_args = (filepath, content)


def test_update_ini_file(tmp_path):
    manager = ConfigManager()
    ini_file = tmp_path / "test.ini"
    content = "[section]\nkey=value\n"
    ini_file.write_text("[old]\nold=1\n")
    manager.update(ini_file, content)
    assert ini_file.read_text() == content


def test_update_json_file(tmp_path):
    manager = ConfigManager()
    json_file = tmp_path / "test.json"
    json_file.write_text('{"a": 1}')
    manager.update(json_file, {"b": 2})
    assert '"b": 2' in json_file.read_text()


def test_update_plain_text_file(tmp_path):
    manager = ConfigManager()
    txt_file = tmp_path / "test.sh"
    content = "echo hello"
    txt_file.write_text("old")
    manager.update(txt_file, content)
    assert txt_file.read_text() == content


def test_update_unknown_extension(tmp_path):
    manager = ConfigManager()
    unknown_file = tmp_path / "test.unknown"
    with pytest.raises(ValueError, match=r"No updater found for file type: \.unknown"):
        manager.update(unknown_file, "data")


def test_register_custom_updater(tmp_path):
    manager = ConfigManager()
    custom_file = tmp_path / "test.custom"
    updater = DummyUpdater()
    manager.register_updater(".custom", updater)
    manager.update(custom_file, "abc")
    assert updater.called
    assert updater.last_args[0] == custom_file
    assert updater.last_args[1] == "abc"
