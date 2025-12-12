from datetime import datetime

import pandas as pd

from xfintech.data.tushare.stock.capflow.concept import Concept


class FakeConnection:
    def __init__(self, frame: pd.DataFrame):
        self.frame = frame

    def moneyflow_cnt_ths(self, **kwargs):
        return self.frame


class FakeSession:
    def __init__(self, connection: FakeConnection):
        self.connection = connection


def test_concept_resolve_conf_default():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = Concept(session=session)
    assert job.conf.coolant == 1.0
    assert job.conf.size == 5000
    job.clean()


def test_concept_resolve_conf_single_concept():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = Concept(
        session=session,
        conf={
            "params": {
                "ts_code": "885550.TI",
                "start_date": "20240101",
                "end_date": "20240131",
            },
            "size": 3000,
        },
    )
    params = job.conf.get_params()
    assert params["ts_code"] == "885550.TI"
    assert params["start_date"] == "20240101"
    assert params["end_date"] == "20240131"
    assert job.conf.size == 3000
    job.clean()


def test_concept_resolve_conf_datetime_conversion():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = Concept(
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


def test_concept_resolve_conf_size_limit():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = Concept(
        session=session,
        conf={
            "size": 10000,
            "coolant": 0.01,
        },
    )
    assert job.conf.size == 5000
    assert job.conf.coolant == 1.0
    job.clean()


def test_concept_transform_basic():
    data = pd.DataFrame(
        {
            "trade_date": ["20241201", "20241201", "20241201"],
            "ts_code": ["885550.TI", "885551.TI", "885552.TI"],
            "name": ["人工智能", "5G概念", "芯片概念"],
            "lead_stock": ["科大讯飞", "中兴通讯", "中芯国际"],
            "close_price": [58.32, 32.45, 45.67],
            "pct_change": [2.35, 1.89, -0.56],
            "industry_index": [1234.56, 987.65, 876.54],
            "company_num": [123, 89, 56],
            "pct_change_stock": [3.45, 2.67, -1.23],
            "net_buy_amount": [12.34, 8.76, -5.43],
            "net_sell_amount": [10.23, 7.89, 8.76],
            "net_amount": [2.11, 0.87, -14.19],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = Concept(session=session)
    result = job.transform(data)
    assert len(result) == 3
    assert "code" in result.columns
    assert "date" in result.columns
    assert "datecode" in result.columns
    assert "name" in result.columns
    assert "lead_stock" in result.columns
    assert "close" in result.columns
    assert "percent_change" in result.columns
    assert "industry_index" in result.columns
    assert "company_num" in result.columns
    assert "pct_change_stock" in result.columns
    assert "net_buy_amount" in result.columns
    assert "net_sell_amount" in result.columns
    assert "net_amount" in result.columns
    assert pd.api.types.is_datetime64_any_dtype(result["date"])
    assert result.iloc[0]["datecode"] == "20241201"
    assert result.iloc[0]["name"] == "人工智能"
    assert result.iloc[0]["lead_stock"] == "科大讯飞"
    assert result.iloc[0]["close"] == 58.32
    assert result.iloc[0]["percent_change"] == 2.35
    assert result.iloc[0]["company_num"] == 123
    job.clean()


def test_concept_transform_empty_data():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = Concept(session=session)
    result = job.transform(None)
    assert result.empty
    assert len(result.columns) == len(job.output.list_column_names())

    empty_df = pd.DataFrame()
    result = job.transform(empty_df)
    assert result.empty
    assert len(result.columns) == len(job.output.list_column_names())
    job.clean()


def test_concept_transform_data_quality():
    data = pd.DataFrame(
        {
            "trade_date": ["20241201", "20241201", "invalid_date"],
            "ts_code": ["885550.TI", "885550.TI", "885551.TI"],
            "name": ["人工智能", "人工智能", "5G概念"],
            "lead_stock": ["科大讯飞", "科大讯飞", "中兴通讯"],
            "close_price": [58.32, 58.32, 32.45],
            "pct_change": [2.35, 2.35, 1.89],
            "industry_index": [1234.56, 1234.56, 987.65],
            "company_num": [123, 123, 89],
            "pct_change_stock": [3.45, 3.45, 2.67],
            "net_buy_amount": [12.34, 12.34, 8.76],
            "net_sell_amount": [10.23, 10.23, 7.89],
            "net_amount": [2.11, 2.11, 0.87],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = Concept(session=session)
    result = job.transform(data)
    assert len(result) == 2

    invalid_row = result[result["code"] == "885551.TI"].iloc[0]
    assert pd.isna(invalid_row["date"])
    assert result.iloc[0]["close"] == 58.32
    job.clean()


def test_concept_transform_numeric_conversion():
    data = pd.DataFrame(
        {
            "trade_date": ["20241201"],
            "ts_code": ["885550.TI"],
            "name": ["人工智能"],
            "lead_stock": ["科大讯飞"],
            "close_price": ["58.32"],
            "pct_change": ["2.35"],
            "industry_index": ["1234.56"],
            "company_num": ["123"],
            "pct_change_stock": ["3.45"],
            "net_buy_amount": ["12.34"],
            "net_sell_amount": ["10.23"],
            "net_amount": ["2.11"],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = Concept(session=session)
    result = job.transform(data)
    assert result.iloc[0]["close"] == 58.32
    assert result.iloc[0]["percent_change"] == 2.35
    assert result.iloc[0]["industry_index"] == 1234.56
    assert result.iloc[0]["company_num"] == 123
    assert result.iloc[0]["net_amount"] == 2.11
    job.clean()


def test_concept_run_and_cache():
    data = pd.DataFrame(
        {
            "trade_date": ["20241201", "20241201"],
            "ts_code": ["885550.TI", "885551.TI"],
            "name": ["人工智能", "5G概念"],
            "lead_stock": ["科大讯飞", "中兴通讯"],
            "close_price": [58.32, 32.45],
            "pct_change": [2.35, 1.89],
            "industry_index": [1234.56, 987.65],
            "company_num": [123, 89],
            "pct_change_stock": [3.45, 2.67],
            "net_buy_amount": [12.34, 8.76],
            "net_sell_amount": [10.23, 7.89],
            "net_amount": [2.11, 0.87],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = Concept(session=session, conf={"use_cache": True})
    result = job.run()
    assert len(result) == 2
    assert "_run" in job.cache

    cached_data = job.cache.get("_run")
    assert len(cached_data) == 2
    pd.testing.assert_frame_equal(result, cached_data)
    job.clean()


def test_concept_source_and_output_config():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = Concept(session=session)
    assert job.source.name == "moneyflow_cnt_ths"
    assert "tushare.pro" in job.source.url
    assert "ts_code" in job.source.args
    assert job.output.name == "concept"
    assert job.tags["name"] == "concept"
    assert job.tags["module"] == "stock"
    assert job.tags["level"] == "capflow"
    assert job.tags["frequency"] == "interday"
    assert job.tags["scope"] == "moneyflow_cnt_ths"
    job.clean()


def test_concept_multi_concept_sorting():
    data = pd.DataFrame(
        {
            "trade_date": ["20241203", "20241201", "20241202"],
            "ts_code": ["885552.TI", "885550.TI", "885551.TI"],
            "name": ["芯片概念", "人工智能", "5G概念"],
            "lead_stock": ["中芯国际", "科大讯飞", "中兴通讯"],
            "close_price": [45.67, 58.32, 32.45],
            "pct_change": [-0.56, 2.35, 1.89],
            "industry_index": [876.54, 1234.56, 987.65],
            "company_num": [56, 123, 89],
            "pct_change_stock": [-1.23, 3.45, 2.67],
            "net_buy_amount": [-5.43, 12.34, 8.76],
            "net_sell_amount": [8.76, 10.23, 7.89],
            "net_amount": [-14.19, 2.11, 0.87],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = Concept(session=session)
    result = job.transform(data)
    expected_order = ["885550.TI", "885551.TI", "885552.TI"]
    actual_order = result["code"].tolist()
    assert actual_order == expected_order
    assert result.index.tolist() == [0, 1, 2]
    job.clean()


def test_concept_field_mapping():
    data = pd.DataFrame(
        {
            "trade_date": ["20241201"],
            "ts_code": ["885550.TI"],
            "name": ["人工智能"],
            "lead_stock": ["科大讯飞"],
            "close_price": [58.32],
            "pct_change": [2.35],
            "industry_index": [1234.56],
            "company_num": [123],
            "pct_change_stock": [3.45],
            "net_buy_amount": [12.34],
            "net_sell_amount": [10.23],
            "net_amount": [2.11],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = Concept(session=session)
    result = job.transform(data)

    # Verify field mappings
    assert "close" in result.columns
    assert "percent_change" in result.columns
    assert "close_price" not in result.columns
    assert "pct_change" not in result.columns
    job.clean()
