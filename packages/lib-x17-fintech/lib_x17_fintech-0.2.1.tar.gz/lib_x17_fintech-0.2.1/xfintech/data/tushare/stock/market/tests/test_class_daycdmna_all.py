from datetime import datetime

import pandas as pd

from xfintech.data.tushare.stock.market.daycdmna import DaycdmNa


class FakeConnection:
    def __init__(self, frame: pd.DataFrame):
        self.frame = frame

    def stk_factor_pro(self, **kwargs):
        return self.frame


class FakeSession:
    def __init__(self, connection: FakeConnection):
        self.connection = connection


def test_daycdmna_resolve_conf_defaults():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = DaycdmNa(session=session)
    assert job.conf.coolant == 2
    assert job.conf.size == 10000
    job.clean()


def test_daycdmna_resolve_conf_with_params():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = DaycdmNa(
        session=session,
        conf={
            "params": {
                "ts_code": "000001.SZ",
                "start_date": "20240101",
                "end_date": "20240131",
            },
            "size": 5000,
        },
    )
    params = job.conf.get_params()
    assert params["ts_code"] == "000001.SZ"
    assert params["start_date"] == "20240101"
    assert params["end_date"] == "20240131"
    assert job.conf.size == 5000
    job.clean()


def test_daycdmna_resolve_conf_datetime_conversion():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = DaycdmNa(
        session=session,
        conf={
            "params": {
                "trade_date": datetime(2024, 1, 15),
                "start_date": datetime(2024, 1, 1),
                "end_date": datetime(2024, 1, 31),
            }
        },
    )
    params = job.conf.get_params()
    assert params["trade_date"] == "20240115"
    assert params["start_date"] == "20240101"
    assert params["end_date"] == "20240131"
    job.clean()


def test_daycdmna_transform_with_na_indicators():
    data = pd.DataFrame(
        {
            "ts_code": ["000001.SZ", "000002.SZ"],
            "trade_date": ["20241201", "20241201"],
            "change": [0.15, -0.23],
            "pct_chg": [1.10, -0.82],
            "vol": [1234567.0, 987654.0],
            "amount": [123456.0, 98765.0],
            "turnover_rate": [2.45, 1.78],
            "turnover_rate_f": [2.50, 1.80],
            "volume_ratio": [1.23, 0.87],
            "pe": [15.6, 12.3],
            "pe_ttm": [16.2, 13.1],
            "pb": [1.8, 1.5],
            "ps": [2.3, 1.9],
            "ps_ttm": [2.4, 2.0],
            "dv_ratio": [2.1, 1.8],
            "dv_ttm": [2.2, 1.9],
            "total_share": [100000.0, 80000.0],
            "float_share": [80000.0, 60000.0],
            "free_share": [70000.0, 50000.0],
            "total_mv": [1500000.0, 1200000.0],
            "circ_mv": [1200000.0, 900000.0],
            "adj_factor": [1.234, 1.567],
            "downdays": [0, 2],
            "updays": [3, 0],
            "lowdays": [5, 10],
            "topdays": [20, 15],
            "open": [13.50, 28.00],
            "high": [13.80, 28.30],
            "low": [13.40, 27.90],
            "close": [13.69, 28.13],
            "macd_bfq": [0.123, 0.234],
            "kdj_k_bfq": [65.4, 70.2],
            "rsi_bfq_6": [55.6, 60.8],
            "ma_bfq_5": [13.60, 28.10],
            "ema_bfq_10": [13.65, 28.15],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = DaycdmNa(session=session)
    result = job.transform(data)
    assert len(result) == 2
    assert "code" in result.columns
    assert "date" in result.columns
    assert "open" in result.columns
    assert "high" in result.columns
    assert "low" in result.columns
    assert "close" in result.columns
    assert "macd" in result.columns
    assert "kdj_k" in result.columns
    assert "rsi_6" in result.columns
    assert "ma_5" in result.columns
    assert "ema_10" in result.columns
    assert result.iloc[0]["open"] == 13.50
    assert result.iloc[0]["high"] == 13.80
    assert result.iloc[0]["macd"] == 0.123
    assert result.iloc[0]["kdj_k"] == 65.4
    assert "ba_high" not in result.columns
    assert "fa_high" not in result.columns
    job.clean()


def test_daycdmna_transform_missing_na_indicators():
    data = pd.DataFrame(
        {
            "ts_code": ["000001.SZ"],
            "trade_date": ["20241201"],
            "change": [0.15],
            "pct_chg": [1.10],
            "vol": [1234567.0],
            "amount": [123456.0],
            "turnover_rate": [2.45],
            "turnover_rate_f": [2.50],
            "volume_ratio": [1.23],
            "pe": [15.6],
            "pe_ttm": [16.2],
            "pb": [1.8],
            "ps": [2.3],
            "ps_ttm": [2.4],
            "dv_ratio": [2.1],
            "dv_ttm": [2.2],
            "total_share": [100000.0],
            "float_share": [80000.0],
            "free_share": [70000.0],
            "total_mv": [1500000.0],
            "circ_mv": [1200000.0],
            "adj_factor": [1.234],
            "downdays": [0],
            "updays": [3],
            "lowdays": [5],
            "topdays": [20],
            "open": [13.50],
            "high": [13.80],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = DaycdmNa(session=session)
    result = job.transform(data)
    assert len(result) == 1
    assert "open" in result.columns
    assert "macd" in result.columns
    assert result.iloc[0]["open"] == 13.50
    assert pd.isna(result.iloc[0]["macd"])
    job.clean()


def test_daycdmna_transform_empty_data():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = DaycdmNa(session=session)
    result = job.transform(None)
    assert result.empty
    assert len(result.columns) == len(job.output.list_column_names())

    empty_df = pd.DataFrame()
    result = job.transform(empty_df)
    assert result.empty
    assert len(result.columns) == len(job.output.list_column_names())
    job.clean()


def test_daycdmna_run_and_cache():
    data = pd.DataFrame(
        {
            "ts_code": ["000001.SZ", "000002.SZ"],
            "trade_date": ["20241201", "20241201"],
            "change": [0.15, -0.23],
            "pct_chg": [1.10, -0.82],
            "vol": [1234567.0, 987654.0],
            "amount": [123456.0, 98765.0],
            "turnover_rate": [2.45, 1.78],
            "turnover_rate_f": [2.50, 1.80],
            "volume_ratio": [1.23, 0.87],
            "pe": [15.6, 12.3],
            "pe_ttm": [16.2, 13.1],
            "pb": [1.8, 1.5],
            "ps": [2.3, 1.9],
            "ps_ttm": [2.4, 2.0],
            "dv_ratio": [2.1, 1.8],
            "dv_ttm": [2.2, 1.9],
            "total_share": [100000.0, 80000.0],
            "float_share": [80000.0, 60000.0],
            "free_share": [70000.0, 50000.0],
            "total_mv": [1500000.0, 1200000.0],
            "circ_mv": [1200000.0, 900000.0],
            "adj_factor": [1.234, 1.567],
            "downdays": [0, 2],
            "updays": [3, 0],
            "lowdays": [5, 10],
            "topdays": [20, 15],
            "open": [13.50, 28.00],
            "high": [13.80, 28.30],
            "low": [13.40, 27.90],
            "close": [13.69, 28.13],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = DaycdmNa(session=session, conf={"use_cache": True})
    result = job.run()
    assert len(result) == 2
    assert "_run" in job.cache

    cached_data = job.cache.get("_run")
    assert len(cached_data) == 2
    pd.testing.assert_frame_equal(result, cached_data)
    job.clean()


def test_daycdmna_source_and_output_config():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = DaycdmNa(session=session)
    assert job.source.name == "stk_factor_pro"
    assert "tushare.pro" in job.source.url
    assert job.output.name == "daycdmna"
    assert job.tags["name"] == "daycdmna"
    assert job.tags["module"] == "stock"
    assert job.tags["level"] == "market"
    assert job.tags["frequency"] == "interday"
    assert job.tags["scope"] == "stk_factor_pro"
    job.clean()


def test_daycdmna_output_columns():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = DaycdmNa(session=session)
    columns = job.output.list_column_names()
    assert "code" in columns
    assert "date" in columns
    assert "open" in columns
    assert "high" in columns
    assert "macd" in columns
    assert "ba_high" not in columns
    assert "fa_high" not in columns
    job.clean()
