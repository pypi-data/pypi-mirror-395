from datetime import datetime

import pandas as pd

from xfintech.data.tushare.stock.market.monthline import Monthline


class FakeConnection:
    def __init__(self, frame: pd.DataFrame):
        self.frame = frame

    def monthly(self, **kwargs):
        return self.frame


class FakeSession:
    def __init__(self, connection: FakeConnection):
        self.connection = connection


def test_monthline_resolve_conf_single_stock():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = Monthline(session=session)
    assert job.conf.size == 4500
    assert job.conf.coolant == 0.1

    job = Monthline(
        session=session,
        conf={
            "params": {
                "ts_code": "000001.SZ",
                "start_date": "20240101",
                "end_date": "20240131",
            },
            "size": 3000,
        },
    )
    params = job.conf.get_params()
    assert params["ts_code"] == "000001.SZ"
    assert params["start_date"] == "20240101"
    assert params["end_date"] == "20240131"
    assert job.conf.size == 3000
    job.clean()


def test_monthline_resolve_conf_datetime_conversion():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = Monthline(
        session=session,
        conf={
            "params": {
                "trade_date": datetime(2024, 1, 31),
                "start_date": datetime(2024, 1, 1),
                "end_date": datetime(2024, 1, 31),
            }
        },
    )
    params = job.conf.get_params()
    assert params["trade_date"] == "20240131"
    assert params["start_date"] == "20240101"
    assert params["end_date"] == "20240131"
    job.clean()


def test_monthline_resolve_conf_size_limit():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = Monthline(
        session=session,
        conf={
            "size": 10000,
            "coolant": 0.01,
        },
    )
    assert job.conf.size == 4500
    assert job.conf.coolant == 0.1
    job.clean()


def test_monthline_transform_basic():
    data = pd.DataFrame(
        {
            "ts_code": ["000001.SZ", "000002.SZ", "600000.SH"],
            "trade_date": ["20241031", "20241031", "20241031"],
            "open": [10.50, 8.20, 15.30],
            "high": [10.80, 8.45, 15.60],
            "low": [10.30, 8.00, 15.10],
            "close": [10.75, 8.35, 15.45],
            "pre_close": [10.50, 8.20, 15.20],
            "change": [0.25, 0.15, 0.25],
            "pct_chg": [2.38, 1.83, 1.64],
            "vol": [1250000.0, 980000.0, 2100000.0],
            "amount": [134500.0, 81200.0, 324500.0],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = Monthline(session=session)
    result = job.transform(data)
    assert len(result) == 3
    assert "code" in result.columns
    assert "date" in result.columns
    assert "datecode" in result.columns
    assert pd.api.types.is_datetime64_any_dtype(result["date"])
    assert result.iloc[0]["datecode"] == "20241031"
    assert result.iloc[0]["open"] == 10.50
    assert result.iloc[0]["close"] == 10.75
    assert result.iloc[0]["percent_change"] == 2.38
    assert result.iloc[0]["volume"] == 1250000.0
    assert result.iloc[0]["amount"] == 134500.0
    job.clean()


def test_monthline_transform_empty_data():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = Monthline(session=session)
    result = job.transform(None)
    assert result.empty
    assert len(result.columns) == len(job.output.list_column_names())

    empty_df = pd.DataFrame()
    result = job.transform(empty_df)
    assert result.empty
    assert len(result.columns) == len(job.output.list_column_names())
    job.clean()


def test_monthline_transform_data_quality():
    data = pd.DataFrame(
        {
            "ts_code": ["000001.SZ", "000001.SZ", "000002.SZ"],
            "trade_date": ["20241031", "20241031", "invalid_date"],
            "open": [10.50, 10.50, "invalid"],
            "high": [10.80, 10.80, 8.45],
            "low": [10.30, 10.30, 8.00],
            "close": [10.75, 10.75, 8.35],
            "pre_close": [10.50, 10.50, 8.20],
            "change": [0.25, 0.25, 0.15],
            "pct_chg": [2.38, 2.38, 1.83],
            "vol": [1250000.0, 1250000.0, 980000.0],
            "amount": [134500.0, 134500.0, 81200.0],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = Monthline(session=session)
    result = job.transform(data)
    assert len(result) == 2

    invalid_row = result[result["code"] == "000002.SZ"].iloc[0]
    assert pd.isna(invalid_row["date"])
    assert pd.isna(invalid_row["open"])
    job.clean()


def test_monthline_run_and_cache():
    data = pd.DataFrame(
        {
            "ts_code": ["000001.SZ", "000002.SZ"],
            "trade_date": ["20241031", "20241031"],
            "open": [10.50, 8.20],
            "high": [10.80, 8.45],
            "low": [10.30, 8.00],
            "close": [10.75, 8.35],
            "pre_close": [10.50, 8.20],
            "change": [0.25, 0.15],
            "pct_chg": [2.38, 1.83],
            "vol": [1250000.0, 980000.0],
            "amount": [134500.0, 81200.0],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = Monthline(session=session, conf={"use_cache": True})
    result = job.run()
    assert len(result) == 2
    assert "_run" in job.cache

    cached_data = job.cache.get("_run")
    assert len(cached_data) == 2
    pd.testing.assert_frame_equal(result, cached_data)
    job.clean()


def _build_monthline_job_for_list_tests():
    data = pd.DataFrame(
        {
            "ts_code": ["000001.SZ", "000002.SZ", "600000.SH"],
            "trade_date": ["20241031", "20240930", "20241031"],
            "open": [10.50, 8.20, 15.30],
            "high": [10.80, 8.45, 15.60],
            "low": [10.30, 8.00, 15.10],
            "close": [10.75, 8.35, 15.45],
            "pre_close": [10.50, 8.20, 15.20],
            "change": [0.25, 0.15, 0.25],
            "pct_chg": [2.38, 1.83, 1.64],
            "vol": [1250000.0, 980000.0, 2100000.0],
            "amount": [134500.0, 81200.0, 324500.0],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = Monthline(session=session)
    job.run()
    return job


def test_monthline_source_and_output_config():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = Monthline(session=session)
    assert job.source.name == "monthly"
    assert "tushare.pro" in job.source.url
    assert "ts_code" in job.source.args
    assert job.output.name == "monthline"
    assert job.tags["name"] == "monthline"
    assert job.tags["module"] == "stock"
    assert job.tags["level"] == "market"
    assert job.tags["frequency"] == "interday"


def test_monthline_multi_stock_sorting():
    data = pd.DataFrame(
        {
            "ts_code": ["600000.SH", "000001.SZ", "000002.SZ"],
            "trade_date": ["20240831", "20241031", "20240930"],
            "open": [15.30, 10.50, 8.20],
            "high": [15.60, 10.80, 8.45],
            "low": [15.10, 10.30, 8.00],
            "close": [15.45, 10.75, 8.35],
            "pre_close": [15.20, 10.50, 8.20],
            "change": [0.25, 0.25, 0.15],
            "pct_chg": [1.64, 2.38, 1.83],
            "vol": [2100000.0, 1250000.0, 980000.0],
            "amount": [324500.0, 134500.0, 81200.0],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = Monthline(session=session)
    result = job.transform(data)
    expected_order = ["000001.SZ", "000002.SZ", "600000.SH"]
    actual_order = result["code"].tolist()
    assert actual_order == expected_order
    assert result.index.tolist() == [0, 1, 2]
