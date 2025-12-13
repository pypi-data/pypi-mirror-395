from pathlib import Path


import singlejson
from singlejson.fileutils import JSONFile, JsonSerializationSettings, DEFAULT_SERIALIZATION_SETTINGS


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def test_save_uses_instance_settings_when_not_provided(tmp_path: Path):
    p = tmp_path / "inst.json"
    settings = JsonSerializationSettings(indent=2, sort_keys=True, ensure_ascii=False)
    jf = JSONFile(p, default_data={"b": 2, "a": 1}, settings=settings)
    # mutate a bit and save without explicit settings
    jf.json = {"b": 2, "a": {"z": 9, "m": 1}}
    jf.save()
    text = read_text(p)
    # two-space indentation present
    assert "\n  \"a\"" in text and "\n    \"a\"" not in text
    # keys sorted
    assert text.index("\n  \"a\"") < text.index("\n  \"b\"")


def test_save_explicit_settings_override_instance(tmp_path: Path):
    p = tmp_path / "override.json"
    instance_settings = JsonSerializationSettings(indent=4, sort_keys=False, ensure_ascii=False)
    jf = JSONFile(p, default_data={}, settings=instance_settings)
    jf.json = {"b": 2, "a": 1}
    call_settings = JsonSerializationSettings(indent=2, sort_keys=True, ensure_ascii=True)
    jf.save(settings=call_settings)
    text = read_text(p)
    # explicit indent=2 and sorted keys
    assert "\n  \"a\"" in text and "\n    \"a\"" not in text
    assert text.index("\n  \"a\"") < text.index("\n  \"b\"")


def test_ensure_ascii_true_vs_false(tmp_path: Path):
    p_true = tmp_path / "ascii_true.json"
    p_false = tmp_path / "ascii_false.json"

    # ensure_ascii=True should escape non-ASCII
    jf_true = JSONFile(p_true, default_data={}, settings=JsonSerializationSettings(ensure_ascii=True))
    jf_true.json = {"greet": "hällo"}
    jf_true.save()
    t_true = read_text(p_true)
    assert "\\u00e4" in t_true  # "ä" escaped

    # ensure_ascii=False should keep Unicode characters
    jf_false = JSONFile(p_false, default_data={}, settings=JsonSerializationSettings(ensure_ascii=False))
    jf_false.json = {"greet": "hällo"}
    jf_false.save()
    t_false = read_text(p_false)
    assert "hällo" in t_false and "\\u00e4" not in t_false


def test_context_manager_auto_save_uses_instance_settings(tmp_path: Path):
    p = tmp_path / "cm.json"
    settings = JsonSerializationSettings(indent=2, sort_keys=True)
    with JSONFile(p, default_data={}, settings=settings) as jf:
        jf.json = {"b": 2, "a": 1}
    text = read_text(p)
    # saved on exit with two spaces and sorted keys
    assert "\n  \"a\"" in text and text.index("\n  \"a\"") < text.index("\n  \"b\"")


def test_pool_sync_respects_each_instance_settings(tmp_path: Path):
    p1 = tmp_path / "p1.json"
    p2 = tmp_path / "p2.json"

    f1 = singlejson.load(p1, default_data={})
    f2 = singlejson.load(p2, default_data={})

    # assign different settings per instance
    f1.settings = JsonSerializationSettings(indent=2, sort_keys=True)
    f2.settings = JsonSerializationSettings(indent=4, sort_keys=True)

    f1.json = {"b": 2, "a": 1}
    f2.json = {"b": 2, "a": 1}

    singlejson.sync()

    t1 = read_text(p1)
    t2 = read_text(p2)

    # p1 should have 2-space indentation, p2 should have 4-space indentation
    assert "\n  \"a\"" in t1 and "\n    \"a\"" not in t1
    assert "\n    \"a\"" in t2


def test_default_settings_are_used_when_not_overridden(tmp_path: Path):
    p = tmp_path / "default.json"
    jf = JSONFile(p, default_data={"b": 2, "a": 1})
    # Don't pass settings anywhere; rely on DEFAULT_SERIALIZATION_SETTINGS
    jf.save()
    text = read_text(p)
    # Expect defaults: indent=4 and sort_keys=True per DEFAULT_SERIALIZATION_SETTINGS
    assert "\n    \"a\"" in text and text.index("\n    \"a\"") < text.index("\n    \"b\"")
