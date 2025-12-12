import time

import pytest

from xfintech.common.retry import Retry


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch):
    monkeypatch.setattr(time, "sleep", lambda *_a, **_k: None)


def test_retry_success_no_retry_needed():
    calls = {"n": 0}

    def fn():
        calls["n"] += 1
        return "ok"

    retry = Retry(retry=3, wait=0.01)
    wrapped = retry(fn)
    result = wrapped()
    assert result == "ok"
    assert calls["n"] == 1


def test_retry_eventual_success():
    calls = {"n": 0}

    def fn():
        calls["n"] += 1
        if calls["n"] < 3:
            raise ValueError("temporary")
        return "ok"

    retry = Retry(retry=5, wait=0.01, exceptions=(ValueError,))
    wrapped = retry(fn)
    result = wrapped()
    assert result == "ok"
    assert calls["n"] == 3


def test_retry_exhaust_and_raise():
    calls = {"n": 0}

    def fn():
        calls["n"] += 1
        raise ValueError("always bad")

    retry = Retry(retry=3, wait=0.01, exceptions=(ValueError,))
    wrapped = retry(fn)

    with pytest.raises(ValueError):
        wrapped()

    assert calls["n"] == 3


def test_retry_does_not_catch_unlisted_exception():
    calls = {"n": 0}

    class CustomError(Exception):
        pass

    def fn():
        calls["n"] += 1
        raise CustomError("no retry for this")

    retry = Retry(retry=5, wait=0.01, exceptions=(ValueError,))
    wrapped = retry(fn)
    with pytest.raises(CustomError):
        wrapped()

    assert calls["n"] == 1


def test_retry_passes_args_kwargs():
    def fn(x, y=1):
        return x + y

    retry = Retry(retry=3, wait=0.01)
    wrapped = retry(fn)
    assert wrapped(1, y=2) == 3


def test_retry_with_args_and_kwargs_eventual_success():
    calls = {"n": 0}

    def fn(market: str, limit: int = 5):
        calls["n"] += 1
        if calls["n"] < 3:
            raise ValueError(f"failed for {market}")
        return [f"{market}-{i}" for i in range(limit)]

    retry = Retry(retry=5, wait=0.01, exceptions=(ValueError,))
    wrapped = retry(fn)
    result = wrapped("CN", limit=3)
    assert result == ["CN-0", "CN-1", "CN-2"]
    assert calls["n"] == 3


def test_retry_like_job_usage():
    calls = {"n": 0}

    def job_run(market: str, date: str) -> str:
        calls["n"] += 1

        if calls["n"] < 2:
            raise RuntimeError("temporary downstream error")
        return f"{market}-{date}"

    retry = Retry(retry=3, wait=0.01, exceptions=(RuntimeError,))

    params = {"market": "AU", "date": "2025-11-09"}
    safe_run = retry(job_run)
    result = safe_run(**params)
    assert result == "AU-2025-11-09"
    assert calls["n"] == 2


def test_retry_str_representation():
    retry = Retry(retry=4, wait=0.1)
    assert str(retry) == "4"
    assert "retry=4" in repr(retry)
    assert "wait=0.1" in repr(retry)
    assert "offrate=1.0" in repr(retry)
    assert "exceptions=(<class 'Exception'>,)" in repr(retry)

    retry2 = Retry(retry=2, wait=0.2)
    assert str(retry2) == "2"
    assert "retry=2" in repr(retry2)
    assert "wait=0.2" in repr(retry2)
    assert "offrate=1.0" in repr(retry2)
    assert "exceptions=(<class 'Exception'>,)" in repr(retry2)

    retry3 = Retry()
    assert str(retry3) == "3"
    assert "retry=3" in repr(retry3)
    assert "wait=0.5" in repr(retry3)
    assert "offrate=1.0" in repr(retry3)
    assert "exceptions=(<class 'Exception'>,)" in repr(retry3)


def test_retry_describe():
    retry = Retry(retry=5, wait=0.2, offrate=2.0, exceptions=(ValueError, KeyError))
    desc = retry.describe()
    assert isinstance(desc, dict)
    assert desc["retry"] == 5
    assert desc["wait"] == 0.2
    assert desc["offrate"] == 2.0
    assert desc["exceptions"] == ["ValueError", "KeyError"]


def test_retry_describe_default():
    retry = Retry()
    desc = retry.describe()
    assert isinstance(desc, dict)
    assert desc["retry"] == 3
    assert desc["wait"] == 0.5
    assert desc["offrate"] == 1.0
    assert desc["exceptions"] == ["Exception"]


def test_retry_describe_no_exceptions():
    retry = Retry(retry=2, wait=0.1, offrate=1.5, exceptions=())
    desc = retry.describe()
    assert isinstance(desc, dict)
    assert desc["retry"] == 2
    assert desc["wait"] == 0.1
    assert desc["offrate"] == 1.5
    assert desc["exceptions"] == ["Exception"]


def test_retry_to_dict():
    retry = Retry(retry=4, wait=0.3, offrate=1.2, exceptions=(IndexError,))
    d = retry.to_dict()
    assert isinstance(d, dict)
    assert d["retry"] == 4
    assert d["wait"] == 0.3
    assert d["offrate"] == 1.2
    assert d["exceptions"] == ["IndexError"]


def test_retry_to_dict_default():
    retry = Retry()
    d = retry.to_dict()
    assert isinstance(d, dict)
    assert d["retry"] == 3
    assert d["wait"] == 0.5
    assert d["offrate"] == 1.0
    assert d["exceptions"] == ["Exception"]
