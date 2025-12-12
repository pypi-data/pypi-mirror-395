import pandas as pd

from xfintech.common.retry import Retry
from xfintech.data.tushare.stock.basic.st import St


class FakeConnection:
    def __init__(self, frame: pd.DataFrame):
        self.frame = frame.reset_index(drop=True)
        self.calls = []

    def stock_st(self, limit: int, offset: int, **params):
        self.calls.append(
            {
                "limit": limit,
                "offset": offset,
                "params": dict(params),
            }
        )
        page = self.frame.iloc[offset : offset + limit].reset_index(drop=True)
        return page


class FakeSession:
    def __init__(self, connection):
        self.connection = connection


def test_st_resolve_conf_trade_date_str():
    raw_conf = {
        "params": {
            "trade_date": "20250115",
        }
    }
    conf = St._resolve_conf(raw_conf)
    params = conf.get_params()
    assert "trade_date" not in params
    assert params["start_date"] == "20250115"
    assert params["end_date"] == "20250115"
    assert conf.size == 1000


def test_st_resolve_conf_year():
    raw_conf = {
        "params": {
            "year": "2024",
        }
    }
    conf = St._resolve_conf(raw_conf)
    params = conf.get_params()
    assert "year" not in params
    assert params["start_date"] == "20240101"
    assert params["end_date"] == "20241231"


def test_st_transform_basic():
    data = pd.DataFrame(
        {
            "ts_code": ["000001.SZ", "000002.SZ"],
            "name": ["平安银行", "万科A"],
            "trade_date": ["20250102", "20250103"],
            "type": ["ST", "PT"],
            "type_name": ["特别处理", "其他处理"],
        }
    )
    fake_conn = FakeConnection(pd.DataFrame())
    session = FakeSession(fake_conn)
    job = St(session=session)
    job.clean()
    out = job.transform(data)
    cols = job.output.list_column_names()
    assert list(out.columns) == cols
    assert len(out) == len(data)
    assert out.loc[0, "code"] == "000001.SZ"
    assert out.loc[0, "date"].strftime("%Y%m%d") == "20250102"
    assert out.loc[0, "datecode"] == "20250102"
    assert out.loc[0, "type"] == "ST"
    assert out.loc[0, "type_name"] == "特别处理"
    job.clean()


def test_st_run_and_cache():
    raw = pd.DataFrame(
        {
            "ts_code": ["000001.SZ"],
            "name": ["平安银行"],
            "trade_date": ["20250102"],
            "type": ["ST"],
            "type_name": ["特别处理"],
        }
    )
    fake_conn = FakeConnection(raw)
    session = FakeSession(fake_conn)
    conf_dict = {
        "params": {
            "trade_date": "20250102",
        },
        "use_cache": True,
    }
    job = St(
        session=session,
        conf=conf_dict,
        retry=Retry(),
    )
    job.clean()
    df = job.run()
    assert len(fake_conn.calls) >= 1
    assert not df.empty
    assert "_run" in job.cache

    cached = job.cache.get("_run")
    assert isinstance(cached, pd.DataFrame)
    assert cached.equals(df)
    job.clean()


def _build_st_job_for_list_tests():
    raw = pd.DataFrame(
        {
            "ts_code": ["000001.SZ", "000002.SZ"],
            "name": ["平安银行", "万科A"],
            "trade_date": ["20250102", "20250103"],
            "type": ["ST", "PT"],
            "type_name": ["特别处理", "其他处理"],
        }
    )
    fake_conn = FakeConnection(raw)
    session = FakeSession(fake_conn)
    job = St(
        session=session,
        conf={
            "use_cache": True,
        },
        retry=Retry(),
    )
    job.run()
    return job


def test_st_list_codes():
    job = _build_st_job_for_list_tests()
    codes = job.list_codes()
    df = job.cache.get("_run")
    assert codes == df["code"].tolist()
    assert "list_codes" in job.cache
    job.clean()


def test_st_list_names():
    job = _build_st_job_for_list_tests()
    names = job.list_names()
    df = job.cache.get("_run")
    for name in names:
        assert isinstance(name, str)
        assert name in df["name"].values
    assert "list_names" in job.cache
    job.clean()
