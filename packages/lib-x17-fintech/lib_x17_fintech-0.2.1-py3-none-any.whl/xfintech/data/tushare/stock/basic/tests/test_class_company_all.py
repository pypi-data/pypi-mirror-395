from xfintech.data.tushare.base.conf import Conf
from xfintech.data.tushare.stock.basic.company import Company


class FakeSession:
    def __init__(self):
        self.connection = None


def test_resolve_conf_none():
    conf = Company._resolve_conf(None)
    assert isinstance(conf, Conf)
    assert conf.size <= 4000


def test_resolve_conf_dict():
    input_conf = {
        "size": 999,
        "limit": 10,
        "params": {"exchange": "SSE"},
    }
    conf = Company._resolve_conf(input_conf)
    assert isinstance(conf, Conf)
    assert conf.size == 999
    assert conf.limit == 10
    assert conf.get_params() == {"exchange": "SSE"}


def test_resolve_conf_instance():
    original = Conf(size=200, limit=300, params={"x": 1})
    result = Company._resolve_conf(original)
    assert result is original
    assert result.size == 200
    assert result.limit == 300
    assert result.get_params() == {"x": 1}


def test_resolve_conf_force_size_limit():
    input_conf = {
        "size": 99999,
        "params": {},
    }
    conf = Company._resolve_conf(input_conf)
    assert isinstance(conf, Conf)
    assert conf.size == 4000
