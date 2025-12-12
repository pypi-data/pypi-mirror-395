from datetime import datetime

import pandas as pd

from xfintech.data.tushare.stock.market.corefactor import CoreFactor


class FakeConnection:
    def __init__(self, frame: pd.DataFrame):
        self.frame = frame

    def daily_basic(self, **kwargs):
        return self.frame


class FakeSession:
    def __init__(self, connection: FakeConnection):
        self.connection = connection


def test_corefactor_resolve_conf_single_stock():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = CoreFactor(session=session)
    assert job.conf.size == 6000
    assert job.conf.coolant == 0.1

    job = CoreFactor(
        session=session,
        conf={
            "params": {"ts_code": "000001.SZ", "start_date": "20240101", "end_date": "20240131"},
            "size": 3000,
        },
    )
    params = job.conf.get_params()
    assert params["ts_code"] == "000001.SZ"
    assert params["start_date"] == "20240101"
    assert params["end_date"] == "20240131"
    assert job.conf.size == 3000
    job.clean()


def test_corefactor_resolve_conf_datetime_conversion():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = CoreFactor(
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


def test_corefactor_resolve_conf_size_limit():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = CoreFactor(
        session=session,
        conf={
            "size": 10000,
            "coolant": 0.01,
        },
    )
    assert job.conf.size == 6000
    assert job.conf.coolant == 0.1
    job.clean()


def test_corefactor_transform_basic():
    data = pd.DataFrame(
        {
            "ts_code": ["000001.SZ", "000002.SZ", "600000.SH"],
            "trade_date": ["20241201", "20241201", "20241201"],
            "close": [10.50, 8.20, 15.30],
            "turnover_rate": [2.45, 1.47, 0.61],
            "turnover_rate_f": [2.50, 1.52, 0.65],
            "volume_ratio": [0.72, 0.88, 0.95],
            "pe": [8.69, 166.40, 23.77],
            "pe_ttm": [9.12, 170.25, 24.15],
            "pb": [3.72, 1.89, 2.38],
            "ps": [1.25, 2.50, 1.75],
            "ps_ttm": [1.30, 2.65, 1.80],
            "dv_ratio": [2.5, 1.2, 3.1],
            "dv_ttm": [2.8, 1.5, 3.5],
            "total_share": [1943278.0, 2847188.0, 2933951.0],
            "float_share": [1943278.0, 2847188.0, 2933951.0],
            "free_share": [1943278.0, 2847188.0, 2933951.0],
            "total_mv": [20404415.0, 23347444.0, 44909481.0],
            "circ_mv": [20404415.0, 23347444.0, 44909481.0],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = CoreFactor(session=session)
    result = job.transform(data)
    assert len(result) == 3
    assert "code" in result.columns
    assert "date" in result.columns
    assert "datecode" in result.columns
    assert "circle_mv" in result.columns
    assert pd.api.types.is_datetime64_any_dtype(result["date"])
    assert result.iloc[0]["datecode"] == "20241201"
    assert result.iloc[0]["close"] == 10.50
    assert result.iloc[0]["turnover_rate"] == 2.45
    assert result.iloc[0]["pe"] == 8.69
    assert result.iloc[0]["circle_mv"] == 20404415.0
    job.clean()


def test_corefactor_transform_empty_data():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = CoreFactor(session=session)
    result = job.transform(None)
    assert result.empty
    assert len(result.columns) == len(job.output.list_column_names())

    empty_df = pd.DataFrame()
    result = job.transform(empty_df)
    assert result.empty
    assert len(result.columns) == len(job.output.list_column_names())
    job.clean()


def test_corefactor_transform_data_quality():
    data = pd.DataFrame(
        {
            "ts_code": ["000001.SZ", "000001.SZ", "000002.SZ"],
            "trade_date": ["20241201", "20241201", "invalid_date"],
            "close": [10.50, 10.50, "invalid"],
            "turnover_rate": [2.45, 2.45, 1.47],
            "turnover_rate_f": [2.50, 2.50, 1.52],
            "volume_ratio": [0.72, 0.72, 0.88],
            "pe": [8.69, 8.69, 166.40],
            "pe_ttm": [9.12, 9.12, 170.25],
            "pb": [3.72, 3.72, 1.89],
            "ps": [1.25, 1.25, 2.50],
            "ps_ttm": [1.30, 1.30, 2.65],
            "dv_ratio": [2.5, 2.5, 1.2],
            "dv_ttm": [2.8, 2.8, 1.5],
            "total_share": [1943278.0, 1943278.0, 2847188.0],
            "float_share": [1943278.0, 1943278.0, 2847188.0],
            "free_share": [1943278.0, 1943278.0, 2847188.0],
            "total_mv": [20404415.0, 20404415.0, 23347444.0],
            "circ_mv": [20404415.0, 20404415.0, 23347444.0],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = CoreFactor(session=session)
    result = job.transform(data)
    assert len(result) == 2

    invalid_row = result[result["code"] == "000002.SZ"].iloc[0]
    assert pd.isna(invalid_row["date"])
    assert pd.isna(invalid_row["close"])
    job.clean()


def test_corefactor_run_and_cache():
    data = pd.DataFrame(
        {
            "ts_code": ["000001.SZ", "000002.SZ"],
            "trade_date": ["20241201", "20241201"],
            "close": [10.50, 8.20],
            "turnover_rate": [2.45, 1.47],
            "turnover_rate_f": [2.50, 1.52],
            "volume_ratio": [0.72, 0.88],
            "pe": [8.69, 166.40],
            "pe_ttm": [9.12, 170.25],
            "pb": [3.72, 1.89],
            "ps": [1.25, 2.50],
            "ps_ttm": [1.30, 2.65],
            "dv_ratio": [2.5, 1.2],
            "dv_ttm": [2.8, 1.5],
            "total_share": [1943278.0, 2847188.0],
            "float_share": [1943278.0, 2847188.0],
            "free_share": [1943278.0, 2847188.0],
            "total_mv": [20404415.0, 23347444.0],
            "circ_mv": [20404415.0, 23347444.0],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = CoreFactor(session=session, conf={"use_cache": True})
    result = job.run()
    assert len(result) == 2
    assert "_run" in job.cache

    cached_data = job.cache.get("_run")
    assert len(cached_data) == 2
    pd.testing.assert_frame_equal(result, cached_data)
    job.clean()


def _build_corefactor_job_for_list_tests():
    data = pd.DataFrame(
        {
            "ts_code": ["000001.SZ", "000002.SZ", "600000.SH"],
            "trade_date": ["20241201", "20241202", "20241201"],
            "close": [10.50, 8.20, 15.30],
            "turnover_rate": [2.45, 1.47, 0.61],
            "turnover_rate_f": [2.50, 1.52, 0.65],
            "volume_ratio": [0.72, 0.88, 0.95],
            "pe": [8.69, 166.40, 23.77],
            "pe_ttm": [9.12, 170.25, 24.15],
            "pb": [3.72, 1.89, 2.38],
            "ps": [1.25, 2.50, 1.75],
            "ps_ttm": [1.30, 2.65, 1.80],
            "dv_ratio": [2.5, 1.2, 3.1],
            "dv_ttm": [2.8, 1.5, 3.5],
            "total_share": [1943278.0, 2847188.0, 2933951.0],
            "float_share": [1943278.0, 2847188.0, 2933951.0],
            "free_share": [1943278.0, 2847188.0, 2933951.0],
            "total_mv": [20404415.0, 23347444.0, 44909481.0],
            "circ_mv": [20404415.0, 23347444.0, 44909481.0],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = CoreFactor(session=session)
    job.run()
    return job


def test_corefactor_source_and_output_config():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = CoreFactor(session=session)
    assert job.source.name == "daily_basic"
    assert "tushare.pro" in job.source.url
    assert "ts_code" in job.source.args
    assert job.output.name == "corefactor"
    assert job.tags["name"] == "corefactor"
    assert job.tags["module"] == "stock"
    assert job.tags["level"] == "market"
    assert job.tags["frequency"] == "interday"
    assert job.tags["scope"] == "daily_basic"


def test_corefactor_multi_stock_sorting():
    data = pd.DataFrame(
        {
            "ts_code": ["600000.SH", "000001.SZ", "000002.SZ"],
            "trade_date": ["20241203", "20241201", "20241202"],
            "close": [15.30, 10.50, 8.20],
            "turnover_rate": [0.61, 2.45, 1.47],
            "turnover_rate_f": [0.65, 2.50, 1.52],
            "volume_ratio": [0.95, 0.72, 0.88],
            "pe": [23.77, 8.69, 166.40],
            "pe_ttm": [24.15, 9.12, 170.25],
            "pb": [2.38, 3.72, 1.89],
            "ps": [1.75, 1.25, 2.50],
            "ps_ttm": [1.80, 1.30, 2.65],
            "dv_ratio": [3.1, 2.5, 1.2],
            "dv_ttm": [3.5, 2.8, 1.5],
            "total_share": [2933951.0, 1943278.0, 2847188.0],
            "float_share": [2933951.0, 1943278.0, 2847188.0],
            "free_share": [2933951.0, 1943278.0, 2847188.0],
            "total_mv": [44909481.0, 20404415.0, 23347444.0],
            "circ_mv": [44909481.0, 20404415.0, 23347444.0],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = CoreFactor(session=session)
    result = job.transform(data)
    expected_order = ["000001.SZ", "000002.SZ", "600000.SH"]
    actual_order = result["code"].tolist()
    assert actual_order == expected_order
    assert result.index.tolist() == [0, 1, 2]
