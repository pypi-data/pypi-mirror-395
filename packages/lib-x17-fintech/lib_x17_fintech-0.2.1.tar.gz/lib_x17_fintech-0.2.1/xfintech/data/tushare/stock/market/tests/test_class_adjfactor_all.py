from datetime import datetime

import pandas as pd

from xfintech.data.tushare.stock.market.adjfactor import AdjFactor


class FakeConnection:
    def __init__(self, frame: pd.DataFrame):
        self.frame = frame

    def adj_factor(self, **kwargs):
        return self.frame


class FakeSession:
    def __init__(self, connection: FakeConnection):
        self.connection = connection


def test_adjfactor_resolve_conf_single_stock():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = AdjFactor(session=session)
    assert job.conf.coolant == 0.05
    assert job.conf.size == 2000

    job = AdjFactor(
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
    assert job.conf.size == 2000
    job.clean()


def test_adjfactor_resolve_conf_datetime_conversion():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = AdjFactor(
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


def test_adjfactor_resolve_conf_size_limit():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = AdjFactor(
        session=session,
        conf={
            "size": 10000,
            "coolant": 0.01,
        },
    )
    assert job.conf.size == 2000
    assert job.conf.coolant == 0.05
    job.clean()


def test_adjfactor_transform_basic():
    data = pd.DataFrame(
        {
            "ts_code": ["000001.SZ", "000002.SZ", "600000.SH"],
            "trade_date": ["20241201", "20241201", "20241201"],
            "adj_factor": [108.031, 95.234, 152.678],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = AdjFactor(session=session)
    result = job.transform(data)
    assert len(result) == 3
    assert "code" in result.columns
    assert "date" in result.columns
    assert "datecode" in result.columns
    assert "adj_factor" in result.columns
    assert pd.api.types.is_datetime64_any_dtype(result["date"])
    assert result.iloc[0]["datecode"] == "20241201"
    assert result.iloc[0]["adj_factor"] == "108.031"
    assert isinstance(result.iloc[0]["adj_factor"], str)
    job.clean()


def test_adjfactor_transform_empty_data():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = AdjFactor(session=session)
    result = job.transform(None)
    assert result.empty
    assert len(result.columns) == len(job.output.list_column_names())

    empty_df = pd.DataFrame()
    result = job.transform(empty_df)
    assert result.empty
    assert len(result.columns) == len(job.output.list_column_names())
    job.clean()


def test_adjfactor_transform_data_quality():
    data = pd.DataFrame(
        {
            "ts_code": ["000001.SZ", "000001.SZ", "000002.SZ"],
            "trade_date": ["20241201", "20241201", "invalid_date"],
            "adj_factor": [108.031, 108.031, 95.234],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = AdjFactor(session=session)
    result = job.transform(data)
    assert len(result) == 2

    invalid_row = result[result["code"] == "000002.SZ"].iloc[0]
    assert pd.isna(invalid_row["date"])
    assert result.iloc[0]["adj_factor"] == "108.031"
    job.clean()


def test_adjfactor_run_and_cache():
    data = pd.DataFrame(
        {
            "ts_code": ["000001.SZ", "000002.SZ"],
            "trade_date": ["20241201", "20241201"],
            "adj_factor": [108.031, 95.234],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = AdjFactor(session=session, conf={"use_cache": True})
    result = job.run()
    assert len(result) == 2
    assert "_run" in job.cache

    cached_data = job.cache.get("_run")
    assert len(cached_data) == 2
    pd.testing.assert_frame_equal(result, cached_data)
    job.clean()


def _build_adjfactor_job_for_list_tests():
    data = pd.DataFrame(
        {
            "ts_code": ["000001.SZ", "000002.SZ", "600000.SH"],
            "trade_date": ["20241201", "20241202", "20241201"],
            "adj_factor": [108.031, 95.234, 152.678],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = AdjFactor(session=session)
    job.run()
    return job


def test_adjfactor_source_and_output_config():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = AdjFactor(session=session)
    assert job.source.name == "adj_factor"
    assert "tushare.pro" in job.source.url
    assert "ts_code" in job.source.args
    assert job.output.name == "adjfactor"
    assert job.tags["name"] == "adjfactor"
    assert job.tags["module"] == "stock"
    assert job.tags["level"] == "market"
    assert job.tags["frequency"] == "interday"
    assert job.tags["scope"] == "adj_factor"
    job.clean()


def test_adjfactor_multi_stock_sorting():
    data = pd.DataFrame(
        {
            "ts_code": ["600000.SH", "000001.SZ", "000002.SZ"],
            "trade_date": ["20241203", "20241201", "20241202"],
            "adj_factor": [152.678, 108.031, 95.234],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = AdjFactor(session=session)
    result = job.transform(data)
    expected_order = ["000001.SZ", "000002.SZ", "600000.SH"]
    actual_order = result["code"].tolist()
    assert actual_order == expected_order
    assert result.index.tolist() == [0, 1, 2]
    job.clean()
