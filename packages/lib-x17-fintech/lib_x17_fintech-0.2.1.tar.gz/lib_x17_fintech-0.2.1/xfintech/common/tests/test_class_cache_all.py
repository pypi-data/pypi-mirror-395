import hashlib
from pathlib import Path

from xfintech.common.cache import Cache


def test_cache_init_with_name_and_parent(tmp_path: Path):
    parent = tmp_path / "cache-root"
    cache = Cache(name="my_cache", parent=parent)
    cache.clear()
    assert cache.name == "my_cache"
    assert cache.parent == parent
    assert cache.path == parent / "my_cache"
    assert cache.path.exists()
    assert cache.path.is_dir()
    cache.clear()


def test_cache_init_without_name_generate_uuid_like(tmp_path: Path):
    parent = tmp_path / "cache-root"
    cache = Cache(parent=parent)
    cache.clear()
    assert isinstance(cache.name, str)
    assert len(cache.name) == 8
    assert all(c in "0123456789abcdef" for c in cache.name)
    assert cache.path.exists()


def test_cache_set_and_get_round_trip(tmp_path: Path):
    parent = tmp_path / "cache-root"
    cache = Cache(
        name="roundtrip",
        parent=parent,
    )
    cache.clear()
    key = "key-1"
    value = {"a": 1, "b": 2}
    assert cache.get(key) is None

    cache.set(key, value)
    loaded = cache.get(key)
    assert loaded == value


def test_cache_get_miss_returns_none(tmp_path: Path):
    parent = tmp_path / "cache-root"
    cache = Cache(name="miss", parent=parent)
    cache.clear()
    assert cache.get("non-existent-key") is None


def test_cache_list_returns_md5_stems(tmp_path: Path):
    parent = tmp_path / "cache-root"
    cache = Cache(
        name="list-test",
        parent=parent,
    )
    cache.clear()
    keys = ["key-1", "another-key"]
    for i, k in enumerate(keys):
        cache.set(k, f"value-{i}")

    units = cache.list()
    expected_stems = {hashlib.md5(k.encode("utf-8")).hexdigest() for k in keys}
    assert set(units) == expected_stems


def test_cache_clear_removes_all_units(tmp_path: Path):
    parent = tmp_path / "cache-root"
    cache = Cache(
        name="clear-test",
        parent=parent,
    )
    cache.clear()
    for i in range(3):
        cache.set(f"key-{i}", f"value-{i}")
    assert len(cache.list()) == 3

    cache.clear()
    assert cache.list() == []


def test_cache_get_handles_corrupted_file_gracefully(tmp_path: Path):
    parent = tmp_path / "cache-root"
    cache = Cache(name="corrupt-test", parent=parent)
    cache.clear()
    key = "bad-key"
    unitpath = cache._resolve_unitpath(key)
    unitpath.write_bytes(b"not-a-valid-pickle")
    value = cache.get(key)
    assert value is None
    cache.clear()


def test_cache_describe_and_to_dict_consistency(tmp_path: Path):
    parent = tmp_path / "cache-root"
    cache = Cache(name="desc-test", parent=parent)
    cache.clear()
    cache.set("k1", "v1")
    d1 = cache.to_dict()
    d2 = cache.describe()
    assert d1 == d2
    assert d1["name"] == "desc-test"
    assert d1["parent"] == str(parent)
    assert d1["path"] == str(parent / "desc-test")
    assert set(d1["units"]) == {
        hashlib.md5("k1".encode("utf-8")).hexdigest(),
    }
    cache.clear()
