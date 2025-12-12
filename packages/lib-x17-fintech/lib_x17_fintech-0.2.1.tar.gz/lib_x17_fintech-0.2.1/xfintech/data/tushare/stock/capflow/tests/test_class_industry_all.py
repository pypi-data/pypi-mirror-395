from datetime import datetime

import pandas as pd

from xfintech.data.tushare.stock.capflow.industry import Industry


class FakeConnection:
    def __init__(self, frame: pd.DataFrame):
        self.frame = frame

    def moneyflow_ind_ths(self, **kwargs):
        return self.frame


class FakeSession:
    def __init__(self, connection: FakeConnection):
        self.connection = connection


def test_industry_resolve_conf_default():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = Industry(session=session)
    assert job.conf.coolant == 1.0
    assert job.conf.size == 5000
    job.clean()


def test_industry_resolve_conf_single_industry():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = Industry(
        session=session,
        conf={
            "params": {
                "ts_code": "886001.TI",
                "start_date": "20240101",
                "end_date": "20240131",
            },
            "size": 3000,
        },
    )
    params = job.conf.get_params()
    assert params["ts_code"] == "886001.TI"
    assert params["start_date"] == "20240101"
    assert params["end_date"] == "20240131"
    assert job.conf.size == 3000
    job.clean()


def test_industry_resolve_conf_datetime_conversion():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = Industry(
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


def test_industry_resolve_conf_size_limit():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = Industry(
        session=session,
        conf={
            "size": 10000,
            "coolant": 0.01,
        },
    )
    assert job.conf.size == 5000
    assert job.conf.coolant == 1.0
    job.clean()


def test_industry_transform_basic():
    data = pd.DataFrame(
        {
            "trade_date": ["20241201", "20241201", "20241201"],
            "ts_code": ["886001.TI", "886002.TI", "886003.TI"],
            "industry": ["电子信息", "生物医药", "新能源"],
            "lead_stock": ["立讯精密", "迈瑞医疗", "宁德时代"],
            "close": [38.52, 325.68, 198.45],
            "pct_change": [1.85, -0.67, 2.34],
            "company_num": [156, 89, 123],
            "pct_change_stock": [2.45, -1.23, 3.56],
            "net_buy_amount": [15.67, -8.43, 23.45],
            "net_sell_amount": [12.34, 11.23, 18.76],
            "net_amount": [3.33, -19.66, 4.69],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = Industry(session=session)
    result = job.transform(data)
    assert len(result) == 3
    assert "code" in result.columns
    assert "date" in result.columns
    assert "datecode" in result.columns
    assert "industry" in result.columns
    assert "lead_stock" in result.columns
    assert "close" in result.columns
    assert "percent_change" in result.columns
    assert "company_num" in result.columns
    assert "pct_change_stock" in result.columns
    assert "net_buy_amount" in result.columns
    assert "net_sell_amount" in result.columns
    assert "net_amount" in result.columns
    assert pd.api.types.is_datetime64_any_dtype(result["date"])
    assert result.iloc[0]["datecode"] == "20241201"
    assert result.iloc[0]["industry"] == "电子信息"
    assert result.iloc[0]["lead_stock"] == "立讯精密"
    assert result.iloc[0]["close"] == 38.52
    assert result.iloc[0]["percent_change"] == 1.85
    assert result.iloc[0]["company_num"] == 156
    job.clean()


def test_industry_transform_empty_data():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = Industry(session=session)
    result = job.transform(None)
    assert result.empty
    assert len(result.columns) == len(job.output.list_column_names())

    empty_df = pd.DataFrame()
    result = job.transform(empty_df)
    assert result.empty
    assert len(result.columns) == len(job.output.list_column_names())
    job.clean()


def test_industry_transform_data_quality():
    data = pd.DataFrame(
        {
            "trade_date": ["20241201", "20241201", "invalid_date"],
            "ts_code": ["886001.TI", "886001.TI", "886002.TI"],
            "industry": ["电子信息", "电子信息", "生物医药"],
            "lead_stock": ["立讯精密", "立讯精密", "迈瑞医疗"],
            "close": [38.52, 38.52, 325.68],
            "pct_change": [1.85, 1.85, -0.67],
            "company_num": [156, 156, 89],
            "pct_change_stock": [2.45, 2.45, -1.23],
            "net_buy_amount": [15.67, 15.67, -8.43],
            "net_sell_amount": [12.34, 12.34, 11.23],
            "net_amount": [3.33, 3.33, -19.66],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = Industry(session=session)
    result = job.transform(data)
    assert len(result) == 2

    invalid_row = result[result["code"] == "886002.TI"].iloc[0]
    assert pd.isna(invalid_row["date"])
    assert result.iloc[0]["close"] == 38.52
    job.clean()


def test_industry_transform_numeric_conversion():
    data = pd.DataFrame(
        {
            "trade_date": ["20241201"],
            "ts_code": ["886001.TI"],
            "industry": ["电子信息"],
            "lead_stock": ["立讯精密"],
            "close": ["38.52"],
            "pct_change": ["1.85"],
            "company_num": ["156"],
            "pct_change_stock": ["2.45"],
            "net_buy_amount": ["15.67"],
            "net_sell_amount": ["12.34"],
            "net_amount": ["3.33"],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = Industry(session=session)
    result = job.transform(data)
    assert result.iloc[0]["close"] == 38.52
    assert result.iloc[0]["percent_change"] == 1.85
    assert result.iloc[0]["company_num"] == 156
    assert result.iloc[0]["net_amount"] == 3.33
    job.clean()


def test_industry_run_and_cache():
    data = pd.DataFrame(
        {
            "trade_date": ["20241201", "20241201"],
            "ts_code": ["886001.TI", "886002.TI"],
            "industry": ["电子信息", "生物医药"],
            "lead_stock": ["立讯精密", "迈瑞医疗"],
            "close": [38.52, 325.68],
            "pct_change": [1.85, -0.67],
            "company_num": [156, 89],
            "pct_change_stock": [2.45, -1.23],
            "net_buy_amount": [15.67, -8.43],
            "net_sell_amount": [12.34, 11.23],
            "net_amount": [3.33, -19.66],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = Industry(session=session, conf={"use_cache": True})
    result = job.run()
    assert len(result) == 2
    assert "_run" in job.cache

    cached_data = job.cache.get("_run")
    assert len(cached_data) == 2
    pd.testing.assert_frame_equal(result, cached_data)
    job.clean()


def test_industry_source_and_output_config():
    fake_conn = FakeConnection(frame=pd.DataFrame())
    session = FakeSession(fake_conn)
    job = Industry(session=session)
    assert job.source.name == "moneyflow_ind_ths"
    assert "tushare.pro" in job.source.url
    assert "ts_code" in job.source.args
    assert job.output.name == "industry"
    assert job.tags["module"] == "stock"
    assert job.tags["level"] == "capflow"
    assert job.tags["frequency"] == "interday"
    assert job.tags["scope"] == "moneyflow_ind_ths"
    job.clean()


def test_industry_multi_industry_sorting():
    data = pd.DataFrame(
        {
            "trade_date": ["20241203", "20241201", "20241202"],
            "ts_code": ["886003.TI", "886001.TI", "886002.TI"],
            "industry": ["新能源", "电子信息", "生物医药"],
            "lead_stock": ["宁德时代", "立讯精密", "迈瑞医疗"],
            "close": [198.45, 38.52, 325.68],
            "pct_change": [2.34, 1.85, -0.67],
            "company_num": [123, 156, 89],
            "pct_change_stock": [3.56, 2.45, -1.23],
            "net_buy_amount": [23.45, 15.67, -8.43],
            "net_sell_amount": [18.76, 12.34, 11.23],
            "net_amount": [4.69, 3.33, -19.66],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = Industry(session=session)
    result = job.transform(data)
    expected_order = ["886001.TI", "886002.TI", "886003.TI"]
    actual_order = result["code"].tolist()
    assert actual_order == expected_order
    assert result.index.tolist() == [0, 1, 2]
    job.clean()


def test_industry_field_mapping():
    data = pd.DataFrame(
        {
            "trade_date": ["20241201"],
            "ts_code": ["886001.TI"],
            "industry": ["电子信息"],
            "lead_stock": ["立讯精密"],
            "close": [38.52],
            "pct_change": [1.85],
            "company_num": [156],
            "pct_change_stock": [2.45],
            "net_buy_amount": [15.67],
            "net_sell_amount": [12.34],
            "net_amount": [3.33],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = Industry(session=session)
    result = job.transform(data)

    # Verify field mappings
    assert "close" in result.columns
    assert "percent_change" in result.columns
    assert "close_price" not in result.columns
    assert "pct_change" not in result.columns
    job.clean()


def test_industry_negative_flow():
    data = pd.DataFrame(
        {
            "trade_date": ["20241201"],
            "ts_code": ["886002.TI"],
            "industry": ["生物医药"],
            "lead_stock": ["迈瑞医疗"],
            "close": [325.68],
            "pct_change": [-0.67],
            "company_num": [89],
            "pct_change_stock": [-1.23],
            "net_buy_amount": [-8.43],
            "net_sell_amount": [11.23],
            "net_amount": [-19.66],
        }
    )
    fake_conn = FakeConnection(frame=data)
    session = FakeSession(fake_conn)
    job = Industry(session=session)
    result = job.transform(data)
    assert result.iloc[0]["percent_change"] == -0.67
    assert result.iloc[0]["pct_change_stock"] == -1.23
    assert result.iloc[0]["net_buy_amount"] == -8.43
    assert result.iloc[0]["net_amount"] == -19.66
    job.clean()
