import pandas as pd

from xfintech.common.retry import Retry
from xfintech.data.tushare.stock.basic.ipo import Ipo


class FakeConnection:
    def __init__(self, frame: pd.DataFrame):
        self.frame = frame.reset_index(drop=True)
        self.calls = []

    def new_share(self, limit: int, offset: int, **params):
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


def test_ipo_resolve_conf_trade_date_str():
    raw_conf = {
        "params": {
            "trade_date": "20250115",
        }
    }
    conf = Ipo._resolve_conf(raw_conf)
    params = conf.get_params()
    assert "trade_date" not in params
    assert params["start_date"] == "20250115"
    assert params["end_date"] == "20250115"


def test_ipo_resolve_conf_trade_date_datetime():
    from datetime import datetime

    raw_conf = {
        "params": {
            "trade_date": datetime(2025, 1, 20),
        }
    }
    conf = Ipo._resolve_conf(raw_conf)
    params = conf.get_params()
    assert "trade_date" not in params
    assert params["start_date"] == "20250120"
    assert params["end_date"] == "20250120"


def test_ipo_transform_basic():
    data = pd.DataFrame(
        {
            "ts_code": ["000001.SZ", "000002.SZ"],
            "sub_code": ["730001", "730002"],
            "name": ["平安银行", "万科A"],
            "ipo_date": ["20200101", "20200202"],
            "issue_date": ["20200110", "20200212"],
            "amount": ["1000", "2000"],
            "market_amount": ["500", "800"],
            "price": ["10.5", "20.3"],
            "pe": ["15.2", "18.7"],
            "limit_amount": ["10", "15"],
            "funds": ["10.0", "30.5"],
            "ballot": ["0.05", "0.10"],
        }
    )
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = Ipo(session=session)
    out = job.transform(data)
    cols = job.output.list_column_names()
    assert list(out.columns) == cols
    assert len(out) == len(data)
    assert out.loc[0, "code"] == "000001.SZ"
    assert out.loc[0, "name"] == "平安银行"
    assert out.loc[0, "ipo_date"].strftime("%Y%m%d") == "20200101"
    assert out.loc[0, "issue_date"].strftime("%Y%m%d") == "20200110"
    assert out.loc[0, "ipo_datecode"] == "20200101"
    assert out.loc[0, "issue_datecode"] == "20200110"
    for col in [
        "amount",
        "market_amount",
        "price",
        "pe",
        "limit_amount",
        "funds",
        "ballot",
    ]:
        assert pd.api.types.is_numeric_dtype(out[col])
    job.clean()


def test_ipo_run_and_cache():
    raw = pd.DataFrame(
        {
            "ts_code": ["000001.SZ"],
            "sub_code": ["730001"],
            "name": ["平安银行"],
            "ipo_date": ["20200101"],
            "issue_date": ["20200110"],
            "amount": ["1000"],
            "market_amount": ["500"],
            "price": ["10.5"],
            "pe": ["15.2"],
            "limit_amount": ["10"],
            "funds": ["10.0"],
            "ballot": ["0.05"],
        }
    )
    fake_conn = FakeConnection(frame=raw)
    session = FakeSession(fake_conn)
    conf_dict = {
        "params": {
            "start_date": "20200101",
            "end_date": "20200131",
        },
        "use_cache": True,
    }
    job = Ipo(
        session=session,
        conf=conf_dict,
        retry=Retry(),
    )
    df = job.run()
    assert len(fake_conn.calls) >= 1
    assert not df.empty
    assert "_run" in job.cache

    cached = job.cache.get("_run")
    assert isinstance(cached, pd.DataFrame)
    assert cached.equals(df)
    job.clean()


def _build_ipo_job_for_list_tests():
    raw = pd.DataFrame(
        {
            "ts_code": ["000001.SZ", "000002.SZ"],
            "sub_code": ["730001", "730002"],
            "name": ["平安银行", "万科A"],
            "ipo_date": ["20200101", "20200202"],
            "issue_date": ["20200110", "20200212"],
            "amount": ["1000", "2000"],
            "market_amount": ["500", "800"],
            "price": ["10.5", "20.3"],
            "pe": ["15.2", "18.7"],
            "limit_amount": ["10", "15"],
            "funds": ["10.0", "30.5"],
            "ballot": ["0.05", "0.10"],
        }
    )
    fake_conn = FakeConnection(frame=raw)
    session = FakeSession(fake_conn)
    job = Ipo(
        session=session,
        conf={
            "use_cache": True,
        },
        retry=Retry(),
    )
    job.run()
    job.clean()
    return job


def test_ipo_list_codes():
    job = _build_ipo_job_for_list_tests()
    codes = job.list_codes()
    df = job.cache.get("_run")
    assert codes == df["code"].tolist()
    assert "list_codes" in job.cache
    job.clean()


def test_ipo_list_names():
    job = _build_ipo_job_for_list_tests()
    names = job.list_names()
    df = job.cache.get("_run")
    for name in names:
        assert isinstance(name, str)
        assert name in df["name"].values

    assert "list_names" in job.cache
    job.clean()
