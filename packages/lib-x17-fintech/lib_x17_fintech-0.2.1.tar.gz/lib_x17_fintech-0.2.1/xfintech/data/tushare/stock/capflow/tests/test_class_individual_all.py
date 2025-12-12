from datetime import datetime

import pandas as pd

from xfintech.data.tushare.stock.capflow.individual import Individual


class FakeConnection:
    def __init__(self, frame: pd.DataFrame):
        self.frame = frame

    def moneyflow(self, **kwargs):
        return self.frame


class FakeSession:
    def __init__(self, connection: FakeConnection):
        self.connection = connection


def test_individual_resolve_conf_default():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = Individual(session=session)
    assert job.conf.coolant == 0.5
    assert job.conf.size == 6000
    job.clean()


def test_individual_resolve_conf_single_stock():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = Individual(
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


def test_individual_resolve_conf_datetime_conversion():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = Individual(
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


def test_individual_resolve_conf_size_limit():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = Individual(
        session=session,
        conf={
            "size": 10000,
            "coolant": 0.01,
        },
    )
    assert job.conf.size == 6000
    assert job.conf.coolant == 0.5
    job.clean()


def test_individual_transform_basic():
    data = pd.DataFrame(
        {
            "ts_code": ["000001.SZ", "000002.SZ", "600000.SH"],
            "trade_date": ["20241201", "20241201", "20241201"],
            "buy_sm_vol": [1200.5, 890.3, 1500.8],
            "buy_sm_amount": [250.3, 180.5, 320.7],
            "sell_sm_vol": [1100.2, 850.1, 1450.3],
            "sell_sm_amount": [230.1, 170.2, 310.5],
            "buy_md_vol": [2300.7, 1680.4, 2800.9],
            "buy_md_amount": [580.4, 420.8, 720.6],
            "sell_md_vol": [2200.5, 1620.3, 2750.7],
            "sell_md_amount": [560.2, 405.6, 700.4],
            "buy_lg_vol": [3400.8, 2500.6, 4100.2],
            "buy_lg_amount": [1250.7, 920.4, 1580.9],
            "sell_lg_vol": [3300.6, 2450.4, 4050.8],
            "sell_lg_amount": [1230.5, 900.2, 1560.7],
            "buy_elg_vol": [5600.9, 4100.7, 6800.3],
            "buy_elg_amount": [3250.8, 2380.6, 3950.4],
            "sell_elg_vol": [5500.7, 4050.5, 6750.1],
            "sell_elg_amount": [3200.6, 2350.4, 3900.2],
            "net_mf_vol": [300.4, 200.6, 450.6],
            "net_mf_amount": [130.7, 90.8, 180.3],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = Individual(session=session)
    result = job.transform(data)
    assert len(result) == 3
    assert "code" in result.columns
    assert "date" in result.columns
    assert "datecode" in result.columns
    assert "buy_sm_vol" in result.columns
    assert "buy_sm_amount" in result.columns
    assert "sell_sm_vol" in result.columns
    assert "buy_md_vol" in result.columns
    assert "buy_lg_vol" in result.columns
    assert "buy_elg_vol" in result.columns
    assert "net_mf_vol" in result.columns
    assert "net_mf_amount" in result.columns
    assert pd.api.types.is_datetime64_any_dtype(result["date"])
    assert result.iloc[0]["datecode"] == "20241201"
    assert result.iloc[0]["buy_sm_vol"] == 1200.5
    assert result.iloc[0]["net_mf_amount"] == 130.7
    job.clean()


def test_individual_transform_empty_data():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = Individual(session=session)
    result = job.transform(None)
    assert result.empty
    assert len(result.columns) == len(job.output.list_column_names())

    empty_df = pd.DataFrame()
    result = job.transform(empty_df)
    assert result.empty
    assert len(result.columns) == len(job.output.list_column_names())
    job.clean()


def test_individual_transform_data_quality():
    data = pd.DataFrame(
        {
            "ts_code": ["000001.SZ", "000001.SZ", "000002.SZ"],
            "trade_date": ["20241201", "20241201", "invalid_date"],
            "buy_sm_vol": [1200.5, 1200.5, 890.3],
            "buy_sm_amount": [250.3, 250.3, 180.5],
            "sell_sm_vol": [1100.2, 1100.2, 850.1],
            "sell_sm_amount": [230.1, 230.1, 170.2],
            "buy_md_vol": [2300.7, 2300.7, 1680.4],
            "buy_md_amount": [580.4, 580.4, 420.8],
            "sell_md_vol": [2200.5, 2200.5, 1620.3],
            "sell_md_amount": [560.2, 560.2, 405.6],
            "buy_lg_vol": [3400.8, 3400.8, 2500.6],
            "buy_lg_amount": [1250.7, 1250.7, 920.4],
            "sell_lg_vol": [3300.6, 3300.6, 2450.4],
            "sell_lg_amount": [1230.5, 1230.5, 900.2],
            "buy_elg_vol": [5600.9, 5600.9, 4100.7],
            "buy_elg_amount": [3250.8, 3250.8, 2380.6],
            "sell_elg_vol": [5500.7, 5500.7, 4050.5],
            "sell_elg_amount": [3200.6, 3200.6, 2350.4],
            "net_mf_vol": [300.4, 300.4, 200.6],
            "net_mf_amount": [130.7, 130.7, 90.8],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = Individual(session=session)
    result = job.transform(data)
    assert len(result) == 2

    invalid_row = result[result["code"] == "000002.SZ"].iloc[0]
    assert pd.isna(invalid_row["date"])
    assert result.iloc[0]["buy_sm_vol"] == 1200.5
    job.clean()


def test_individual_transform_numeric_conversion():
    data = pd.DataFrame(
        {
            "ts_code": ["000001.SZ"],
            "trade_date": ["20241201"],
            "buy_sm_vol": ["1200.5"],
            "buy_sm_amount": ["250.3"],
            "sell_sm_vol": ["1100.2"],
            "sell_sm_amount": ["230.1"],
            "buy_md_vol": ["2300.7"],
            "buy_md_amount": ["580.4"],
            "sell_md_vol": ["2200.5"],
            "sell_md_amount": ["560.2"],
            "buy_lg_vol": ["3400.8"],
            "buy_lg_amount": ["1250.7"],
            "sell_lg_vol": ["3300.6"],
            "sell_lg_amount": ["1230.5"],
            "buy_elg_vol": ["5600.9"],
            "buy_elg_amount": ["3250.8"],
            "sell_elg_vol": ["5500.7"],
            "sell_elg_amount": ["3200.6"],
            "net_mf_vol": ["300.4"],
            "net_mf_amount": ["130.7"],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = Individual(session=session)
    result = job.transform(data)
    assert result.iloc[0]["buy_sm_vol"] == 1200.5
    assert result.iloc[0]["buy_md_amount"] == 580.4
    assert result.iloc[0]["net_mf_amount"] == 130.7
    job.clean()


def test_individual_run_and_cache():
    data = pd.DataFrame(
        {
            "ts_code": ["000001.SZ", "000002.SZ"],
            "trade_date": ["20241201", "20241201"],
            "buy_sm_vol": [1200.5, 890.3],
            "buy_sm_amount": [250.3, 180.5],
            "sell_sm_vol": [1100.2, 850.1],
            "sell_sm_amount": [230.1, 170.2],
            "buy_md_vol": [2300.7, 1680.4],
            "buy_md_amount": [580.4, 420.8],
            "sell_md_vol": [2200.5, 1620.3],
            "sell_md_amount": [560.2, 405.6],
            "buy_lg_vol": [3400.8, 2500.6],
            "buy_lg_amount": [1250.7, 920.4],
            "sell_lg_vol": [3300.6, 2450.4],
            "sell_lg_amount": [1230.5, 900.2],
            "buy_elg_vol": [5600.9, 4100.7],
            "buy_elg_amount": [3250.8, 2380.6],
            "sell_elg_vol": [5500.7, 4050.5],
            "sell_elg_amount": [3200.6, 2350.4],
            "net_mf_vol": [300.4, 200.6],
            "net_mf_amount": [130.7, 90.8],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = Individual(session=session, conf={"use_cache": True})
    result = job.run()
    assert len(result) == 2
    assert "_run" in job.cache

    cached_data = job.cache.get("_run")
    assert len(cached_data) == 2
    pd.testing.assert_frame_equal(result, cached_data)
    job.clean()


def test_individual_source_and_output_config():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = Individual(session=session)
    assert job.source.name == "moneyflow"
    assert "tushare.pro" in job.source.url
    assert "ts_code" in job.source.args
    assert job.output.name == "individual"
    assert job.tags["name"] == "individual"
    assert job.tags["module"] == "stock"
    assert job.tags["level"] == "capflow"
    assert job.tags["frequency"] == "interday"
    assert job.tags["scope"] == "moneyflow"
    job.clean()


def test_individual_multi_stock_sorting():
    data = pd.DataFrame(
        {
            "ts_code": ["600000.SH", "000001.SZ", "000002.SZ"],
            "trade_date": ["20241203", "20241201", "20241202"],
            "buy_sm_vol": [1500.8, 1200.5, 890.3],
            "buy_sm_amount": [320.7, 250.3, 180.5],
            "sell_sm_vol": [1450.3, 1100.2, 850.1],
            "sell_sm_amount": [310.5, 230.1, 170.2],
            "buy_md_vol": [2800.9, 2300.7, 1680.4],
            "buy_md_amount": [720.6, 580.4, 420.8],
            "sell_md_vol": [2750.7, 2200.5, 1620.3],
            "sell_md_amount": [700.4, 560.2, 405.6],
            "buy_lg_vol": [4100.2, 3400.8, 2500.6],
            "buy_lg_amount": [1580.9, 1250.7, 920.4],
            "sell_lg_vol": [4050.8, 3300.6, 2450.4],
            "sell_lg_amount": [1560.7, 1230.5, 900.2],
            "buy_elg_vol": [6800.3, 5600.9, 4100.7],
            "buy_elg_amount": [3950.4, 3250.8, 2380.6],
            "sell_elg_vol": [6750.1, 5500.7, 4050.5],
            "sell_elg_amount": [3900.2, 3200.6, 2350.4],
            "net_mf_vol": [450.6, 300.4, 200.6],
            "net_mf_amount": [180.3, 130.7, 90.8],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = Individual(session=session)
    result = job.transform(data)
    expected_order = ["000001.SZ", "000002.SZ", "600000.SH"]
    actual_order = result["code"].tolist()
    assert actual_order == expected_order
    assert result.index.tolist() == [0, 1, 2]
    job.clean()


def test_individual_all_volume_fields():
    data = pd.DataFrame(
        {
            "ts_code": ["000001.SZ"],
            "trade_date": ["20241201"],
            "buy_sm_vol": [1200.5],
            "buy_sm_amount": [250.3],
            "sell_sm_vol": [1100.2],
            "sell_sm_amount": [230.1],
            "buy_md_vol": [2300.7],
            "buy_md_amount": [580.4],
            "sell_md_vol": [2200.5],
            "sell_md_amount": [560.2],
            "buy_lg_vol": [3400.8],
            "buy_lg_amount": [1250.7],
            "sell_lg_vol": [3300.6],
            "sell_lg_amount": [1230.5],
            "buy_elg_vol": [5600.9],
            "buy_elg_amount": [3250.8],
            "sell_elg_vol": [5500.7],
            "sell_elg_amount": [3200.6],
            "net_mf_vol": [300.4],
            "net_mf_amount": [130.7],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = Individual(session=session)
    result = job.transform(data)

    # Verify all volume and amount fields are present and correctly transformed
    volume_amount_fields = [
        "buy_sm_vol",
        "buy_sm_amount",
        "sell_sm_vol",
        "sell_sm_amount",
        "buy_md_vol",
        "buy_md_amount",
        "sell_md_vol",
        "sell_md_amount",
        "buy_lg_vol",
        "buy_lg_amount",
        "sell_lg_vol",
        "sell_lg_amount",
        "buy_elg_vol",
        "buy_elg_amount",
        "sell_elg_vol",
        "sell_elg_amount",
        "net_mf_vol",
        "net_mf_amount",
    ]
    for field in volume_amount_fields:
        assert field in result.columns
        assert pd.api.types.is_numeric_dtype(result[field])
    job.clean()
