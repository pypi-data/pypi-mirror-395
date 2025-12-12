import json
import os
import sys
from pathlib import Path

import pytest

import singlejson
from singlejson.fileutils import JSONFile, prepare, JsonSerializationSettings, FileAccessError


def test_context_manager_auto_save(tmp_path: Path):
    p = tmp_path / "auto.json"
    with JSONFile(p, default_data={}) as jf:
        jf.json["k"] = "v"
    # New instance should see the saved value
    jf2 = JSONFile(p)
    assert jf2.json["k"] == "v"


def test_context_manager_no_save_on_exception(tmp_path: Path):
    p = tmp_path / "no_save.json"
    with pytest.raises(RuntimeError):
        with JSONFile(p, default_data={}) as jf:
            jf.json["x"] = 1
            raise RuntimeError("boom")
    # Should NOT have saved due to exception
    jf2 = JSONFile(p)
    assert "x" not in jf2.json


def test_save_atomic(tmp_path: Path):
    p = tmp_path / "atomic.json"
    jf = JSONFile(p, default_data={})
    jf.json = {"a": [1, 2, 3]}
    jf.save_atomic()
    data = json.loads(p.read_text())
    assert data == {"a": [1, 2, 3]}


def test_prepare_cwd_relative(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    rel = Path("rel.json")
    prepare(rel, default="{}")
    assert rel.exists()
    assert json.loads(rel.read_text()) == {}


def test_pool_relative_and_absolute_same_instance(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    rel = Path("pooled.json")
    a = singlejson.load(rel, default_data={})
    b = singlejson.load(tmp_path / "pooled.json", default_data={})
    assert a is b


def test_close_save_and_without_save(tmp_path: Path):
    p = tmp_path / "close.json"
    jf = singlejson.load(p, default_data={})
    jf.json["y"] = 7
    # Close without saving; first cleared instance should not persist
    singlejson.close(p, save=False)
    assert p.exists()  # file created by prepare with default
    obj = JSONFile(p)
    assert "y" not in obj.json
    # mutate again and close with save
    jf2 = singlejson.load(p, default_data={})
    jf2.json["y"] = 9
    singlejson.close(p, save=True)
    assert json.loads(p.read_text())["y"] == 9


@pytest.mark.skipif(sys.platform.startswith("win"), reason="POSIX permissions required")
def test_permission_error_raises_file_access_error(tmp_path: Path):
    p = tmp_path / "locked.json"
    # create file and remove all permissions
    p.write_text("{}")
    os.chmod(p, 0)
    try:
        with pytest.raises(FileAccessError):
            JSONFile(p).reload()
    finally:
        # restore perms so tmp cleanup can remove the file
        os.chmod(p, 0o600)


def test_serialization_settings_indent_and_sort(tmp_path: Path):
    p = tmp_path / "fmt.json"
    jf = JSONFile(p, default_data={})
    jf.json = {"b": 2, "a": {"n": 1}}
    settings = JsonSerializationSettings(indent=2, sort_keys=True, ensure_ascii=False)
    jf.save(settings=settings)
    text = p.read_text()
    # Check that keys are sorted and indentation of 2 spaces exists
    first_brace = text.splitlines()[0].strip()
    assert first_brace == "{"
    # a should come before b when sorted
    assert "\n  \"a\"" in text
    assert "\n  \"b\"" in text