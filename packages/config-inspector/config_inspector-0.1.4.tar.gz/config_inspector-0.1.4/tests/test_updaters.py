import configparser
import json

import pytest
import toml

from config_inspector.updaters import IniConfigUpdater
from config_inspector.updaters import JsonConfigUpdater
from config_inspector.updaters import PlainTextUpdater
from config_inspector.updaters import TomlConfigUpdater
from config_inspector.updaters import updater_factory


def test_ini_config_updater_valid(tmp_path):
    updater = IniConfigUpdater()
    ini_file = tmp_path / "test.ini"
    content = "[section]\nkey=value\n"
    updater.update(ini_file, content)
    assert ini_file.read_text() == content


def test_ini_config_updater_invalid(tmp_path):
    updater = IniConfigUpdater()
    ini_file = tmp_path / "bad.ini"
    bad_content = "no_section_header"
    with pytest.raises(configparser.MissingSectionHeaderError):
        updater.update(ini_file, bad_content)


def test_toml_config_updater_valid(tmp_path):
    updater = TomlConfigUpdater()
    toml_file = tmp_path / "test.toml"
    toml_file.write_text("a = 1\n", encoding="utf8")
    updater.update(toml_file, {"b": 2})
    data = toml.loads(toml_file.read_text())
    assert data["a"] == 1
    assert data["b"] == 2


def test_toml_config_updater_invalid(tmp_path):
    updater = TomlConfigUpdater()
    toml_file = tmp_path / "bad.toml"
    toml_file.write_text('not = "valid"\n[', encoding="utf8")
    with pytest.raises(toml.TomlDecodeError):
        updater.update(toml_file, {"x": 1})


def test_json_config_updater_valid(tmp_path):
    updater = JsonConfigUpdater()
    json_file = tmp_path / "test.json"
    json_file.write_text('{"a": 1}', encoding="utf8")
    updater.update(json_file, {"b": 2})
    data = json.loads(json_file.read_text())
    assert data["a"] == 1
    assert data["b"] == 2


def test_json_config_updater_invalid(tmp_path):
    updater = JsonConfigUpdater()
    json_file = tmp_path / "bad.json"
    json_file.write_text("{bad json}", encoding="utf8")
    with pytest.raises(json.JSONDecodeError):
        updater.update(json_file, {"x": 1})


def test_plain_text_updater(tmp_path):
    updater = PlainTextUpdater()
    txt_file = tmp_path / "test.txt"
    content = "hello world"
    updater.update(txt_file, content)
    assert txt_file.read_text() == content


def test_updater_factory():
    assert isinstance(updater_factory(".ini"), IniConfigUpdater)
    assert isinstance(updater_factory(".toml"), TomlConfigUpdater)
    assert isinstance(updater_factory(".json"), JsonConfigUpdater)
    assert isinstance(updater_factory(".txt"), PlainTextUpdater)
    assert isinstance(updater_factory(".unknown"), PlainTextUpdater)
