import pandas as pd

from xfintech.common.retry import Retry
from xfintech.data.tushare.stock.basic.tradedate import TradeDate


class FakeConnection:
    def __init__(self, frames_by_is_open):
        self.frames_by_is_open = frames_by_is_open
        self.calls = []

    def trade_cal(self, limit: int, offset: int, **params):
        self.calls.append(
            {
                "limit": limit,
                "offset": offset,
                "params": dict(params),
            }
        )
        key = params.get("is_open")
        df = self.frames_by_is_open.get(key)
        if df is None:
            return pd.DataFrame()

        page = df.iloc[offset : offset + limit].reset_index(drop=True)
        return page


class FakeSession:
    def __init__(self, connection):
        self.connection = connection


def test_tradedate_resolve_conf_year_to_start_end():
    raw_conf = {
        "params": {
            "year": "2025",
        }
    }
    conf = TradeDate._resolve_conf(raw_conf)
    params = conf.get_params()
    assert "year" not in params
    assert params["start_date"] == "20250101"
    assert params["end_date"] == "20251231"


def test_tradedate_transform_basic():
    data = pd.DataFrame(
        {
            "cal_date": ["20250101", "20250102", "20250103"],
            "is_open": [1, 0, 1],
            "pretrade_date": ["20241231", "20250102", "20250102"],
        }
    )
    fake_conn = FakeConnection(frames_by_is_open={})
    session = FakeSession(fake_conn)
    job = TradeDate(session=session)
    job.clean()
    out = job.transform(data)
    cols = job.output.tableinfo.list_columns()
    col_names = [c.name for c in cols]
    assert list(out.columns) == col_names
    assert len(out) == len(data)
    assert out.loc[0, "datecode"] == "20250101"
    assert out.loc[0, "date"].strftime("%Y%m%d") == "20250101"
    assert out["is_open"].dtype == bool
    assert bool(out.loc[0, "is_open"]) is True
    assert bool(out.loc[1, "is_open"]) is False
    assert out.loc[0, "previous"].strftime("%Y%m%d") == "20241231"
    assert set(out["exchange"].unique()) == {"ALL"}
    assert out.loc[0, "year"] == 2025
    assert out.loc[0, "month"] == 1
    assert out.loc[0, "day"] == 1
    assert out.loc[0, "quarter"] == 1
    assert out.loc[0, "weekday"] == "Wed"
    job.clean()


def test_tradedate_run_with_is_open_param():
    df_open = pd.DataFrame(
        {
            "cal_date": ["20250101", "20250102"],
            "is_open": [1, 1],
            "pretrade_date": ["20241231", "20250101"],
        }
    )
    fake_conn = FakeConnection(
        frames_by_is_open={
            "1": df_open,
        }
    )
    session = FakeSession(fake_conn)
    conf_dict = {
        "params": {
            "is_open": "1",
        }
    }
    job = TradeDate(
        session=session,
        conf=conf_dict,
        retry=Retry(),
    )
    df = job.run()
    assert not df.empty
    assert df["is_open"].all()
    assert all(c["params"].get("is_open") == "1" for c in fake_conn.calls)
    job.clean()


def test_tradedate_run_without_is_open_param():
    df_open = pd.DataFrame(
        {
            "cal_date": ["20250101", "20250102"],
            "is_open": [1, 1],
            "pretrade_date": ["20241231", "20250101"],
        }
    )
    df_close = pd.DataFrame(
        {
            "cal_date": ["20250101"],
            "is_open": [0],
            "pretrade_date": ["20241231"],
        }
    )
    fake_conn = FakeConnection(
        frames_by_is_open={
            "1": df_open,
            "0": df_close,
        }
    )
    session = FakeSession(fake_conn)
    job = TradeDate(
        session=session,
        conf=None,
        retry=Retry(),
    )
    df = job.run()
    assert not df.empty

    datecodes = set(df["datecode"].tolist())
    assert "20250101" in datecodes
    assert "20250102" in datecodes
    assert df["is_open"].any()
    assert (~df["is_open"]).any()
    job.clean()


def _build_trade_job_for_list_tests():
    df_all = pd.DataFrame(
        {
            "cal_date": ["20250101", "20250102", "20250103"],
            "is_open": [1, 0, 1],
            "pretrade_date": ["20241231", "20250102", "20250102"],
        }
    )
    fake_conn = FakeConnection(
        frames_by_is_open={
            "1": df_all[df_all["is_open"] == 1].reset_index(drop=True),
            "0": df_all[df_all["is_open"] == 0].reset_index(drop=True),
        }
    )
    session = FakeSession(fake_conn)
    job = TradeDate(
        session=session,
        conf={"use_cache": True},
        retry=Retry(),
    )
    df = job.run()
    assert "_run" in job.cache
    return job, df


def test_tradedate_list_dates_and_open_dates():
    job, df = _build_trade_job_for_list_tests()
    dates_all = job.list_dates()
    dates_open = job.list_open_dates()
    assert dates_all == df["date"].tolist()
    assert dates_open == df.loc[df["is_open"], "date"].tolist()
    assert "_run" in job.cache
    assert "list_dates" in job.cache
    assert "list_open_dates" in job.cache
    job.clean()


def test_tradedate_list_datecodes_and_open_datecodes():
    job, df = _build_trade_job_for_list_tests()
    codes_all = job.list_datecodes()
    codes_open = job.list_open_datecodes()
    assert codes_all == df["datecode"].tolist()
    assert codes_open == df.loc[df["is_open"], "datecode"].tolist()
    assert "list_datecodes" in job.cache
    assert "list_open_datecodes" in job.cache
    job.clean()
