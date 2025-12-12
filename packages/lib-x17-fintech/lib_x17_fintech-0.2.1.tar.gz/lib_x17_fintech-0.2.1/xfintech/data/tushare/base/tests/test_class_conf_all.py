from datetime import datetime

from xfintech.data.tushare.base.conf import Conf


def test_jobconf_default_values():
    conf = Conf()

    assert conf.params == {}
    assert conf.limit == 10000
    assert conf.size == 5000
    assert conf.offset == 0
    assert conf.coolant == 0


def test_jobconf_custom_basic_values():
    conf = Conf(
        params={
            "ts_code": "000001.SZ",
            "start_date": "20240101",
        },
        limit=200,
        size=1000,
        offset=10,
        coolant=2,
    )
    assert conf.params == {
        "ts_code": "000001.SZ",
        "start_date": "20240101",
    }
    assert conf.limit == 200
    assert conf.size == 1000
    assert conf.offset == 10
    assert conf.coolant == 2


def test_jobconf_limit_zero_falls_back_to_default():
    conf = Conf(limit=0)
    assert conf.limit == 10000


def test_jobconf_resolve_params_datetime_and_none():
    start = datetime(2024, 1, 1)
    end = datetime(2024, 2, 1)
    conf = Conf(
        params={
            "ts_code": "000001.SZ",
            "start_date": start,
            "end_date": end,
            "optional": None,
        }
    )
    assert conf.params == {
        "ts_code": "000001.SZ",
        "start_date": "20240101",
        "end_date": "20240201",
    }


def test_jobconf_get_params_returns_copy():
    conf = Conf(params={"ts_code": "000001.SZ"})
    p1 = conf.get_params()
    p1["ts_code"] = "SHIT"
    assert conf.params["ts_code"] == "000001.SZ"


def test_jobconf_pagination_next_and_reset():
    conf = Conf(size=1000, offset=0)
    assert conf.offset == 0

    off1 = conf.next()
    assert off1 == 1000
    assert conf.offset == 1000

    off2 = conf.next()
    assert off2 == 2000
    assert conf.offset == 2000

    reset_off = conf.reset()
    assert reset_off == 0
    assert conf.offset == 0


def test_jobconf_str_and_repr_and_describe_consistency():
    conf = Conf(
        params={"ts_code": "000001.SZ"},
        limit=123,
        size=456,
        offset=7,
        coolant=3,
    )
    d = conf.to_dict()
    desc = conf.describe()
    assert d == desc
    assert d["params"] == {"ts_code": "000001.SZ"}
    assert d["limit"] == 123
    assert d["size"] == 456
    assert d["offset"] == 7
    assert d["coolant"] == 3

    s = str(conf)
    assert "ts_code" in s
    assert "limit" in s

    r = repr(conf)
    assert "Conf" in r
    assert "limit=" in r
    assert "size=" in r
