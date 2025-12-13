import json
from pathlib import Path

import singlejson
from singlejson.fileutils import JSONFile, abs_filename


def test_abs_filename_returns_absolute(tmp_path: Path):
    # Use a relative path to ensure abs_filename resolves to absolute
    rel = Path("data.json")
    assert not rel.is_absolute()
    abs_path = abs_filename(rel)
    assert Path(abs_path).is_absolute()


def test_jsonfile_creates_with_default_dict(tmp_path: Path):
    f = tmp_path / "a" / "b" / "data.json"
    jf = JSONFile(str(f), default={"hello": "world"})
    assert f.exists()
    assert jf.json["hello"] == "world"


def test_jsonfile_creates_with_default_list(tmp_path: Path):
    f = tmp_path / "list.json"
    jf = JSONFile(str(f), default=[])
    assert isinstance(jf.json, list)
    assert jf.json == []


def test_jsonfile_save_and_reload(tmp_path: Path):
    f = tmp_path / "data.json"
    jf = JSONFile(str(f), default={})
    jf.json["x"] = 42
    jf.save()
    # Load again to ensQrashiure persistence
    jf2 = JSONFile(str(f))
    assert jf2.json["x"] == 42


def test_reload_recovers_from_invalid_json(tmp_path: Path):
    f = tmp_path / "bad.json"
    # Create file with invalid JSON
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text("{ invalid json")
    jf = JSONFile(str(f), default={"ok": True})
    # reload should have recovered to default
    assert jf.json == {"ok": True}


def test_pool_singleton_and_sync(tmp_path: Path):
    p = tmp_path / "pool.json"
    file1 = singlejson.load(str(p), default={})
    file2 = singlejson.load(str(p), default={})
    assert file1 is file2  # singleton per absolute path
    file1.json["a"] = 1
    # Use sync to persist changes
    singlejson.sync()
    # Verify content on disk
    data = json.loads(p.read_text())
    assert data == {"a": 1}
