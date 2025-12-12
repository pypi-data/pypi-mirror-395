from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd

from xfintech.data.tushare.base.conf import Conf
from xfintech.data.tushare.stock.basic.stock import Stock


class FakeConnection:
    def __init__(self, df: pd.DataFrame):
        self._df = df
        self.calls: List[Dict[str, Any]] = []

    def stock_basic(self, **kwargs) -> pd.DataFrame:
        self.calls.append(kwargs)
        return self._df.copy()


class FakeSession:
    def __init__(self, df: pd.DataFrame):
        self.connection = FakeConnection(df=df)


def make_input_df() -> pd.DataFrame:
    data = {
        "ts_code": ["000001.SZ", "000002.SZ"],
        "symbol": ["000001", "000002"],
        "name": ["平安银行", "万科A"],
        "area": ["深圳", "深圳"],
        "industry": ["银行", "房地产"],
        "fullname": ["平安银行股份有限公司", "万科企业股份有限公司"],
        "enname": ["PING AN BANK CO.,LTD", "CHINA VANKE CO.,LTD"],
        "cnspell": ["payh", "wka"],
        "market": ["主板", "主板"],
        "exchange": ["SZSE", "SZSE"],
        "curr_type": ["CNY", "CNY"],
        "list_status": ["L", "L"],
        "list_date": ["19910403", "19910129"],
        "delist_date": ["", ""],
        "is_hs": ["S", "S"],
        "act_name": [
            "深圳市人民政府国有资产监督管理委员会",
            "深圳市人民政府国有资产监督管理委员会",
        ],
        "act_ent_type": ["地方国资", "地方国资"],
    }
    return pd.DataFrame(data)


def test_resolve_conf_none():
    conf = Stock._resolve_conf(None)
    assert isinstance(conf, Conf)
    assert conf.size == 4000


def test_resolve_conf_dict_and_size_cap():
    input_conf = {
        "size": 99999,
        "limit": 5,
        "params": {"list_status": "L"},
    }
    conf = Stock._resolve_conf(input_conf)
    assert isinstance(conf, Conf)
    assert conf.size == 4000
    assert conf.limit == 5
    assert conf.get_params() == {"list_status": "L"}


def test_transform_basic_mapping():
    df_in = make_input_df()
    session = FakeSession(df_in)
    job = Stock(session=session)
    job.clean()
    df_out = job.transform(df_in)
    cols = job.output.list_column_names()
    assert list(df_out.columns) == cols
    assert df_out.loc[0, "code"] == "000001.SZ"
    assert df_out.loc[0, "symbol"] == "000001"
    assert df_out.loc[0, "name"] == "平安银行"
    assert df_out.loc[0, "currency"] == "CNY"
    assert df_out.loc[0, "ace_name"] == "深圳市人民政府国有资产监督管理委员会"
    assert df_out.loc[0, "ace_type"] == "地方国资"
    assert pd.api.types.is_datetime64_any_dtype(df_out["list_date"])
    assert pd.api.types.is_datetime64_any_dtype(df_out["delist_date"])
    assert df_out["code"].tolist() == sorted(df_out["code"].tolist())
    job.clean()


def test_transform_empty():
    df_empty = pd.DataFrame()
    session = FakeSession(make_input_df())
    job = Stock(session=session)
    job.clean()
    df_out = job.transform(df_empty)
    expected_cols = job.output.list_column_names()
    assert list(df_out.columns) == expected_cols
    assert df_out.empty
    job.clean()


def test_run_with_list_status_param():
    df_in = make_input_df()
    session = FakeSession(df_in)
    conf = Conf(params={"list_status": "L"}, size=2000, limit=2)
    job = Stock(session=session, conf=conf)
    job.clean()
    result = job.run()
    assert isinstance(result, pd.DataFrame)
    assert not result.empty

    conn = session.connection
    assert len(conn.calls) == 1

    call_kwargs = conn.calls[0]
    fields = call_kwargs.get("fields")
    assert isinstance(fields, str)

    for col in job.source.list_column_names():
        assert col in fields
    assert call_kwargs.get("list_status") == "L"
    job.clean()


def test_run_without_list_status_param_calls_all_statuses():
    df_in = make_input_df()
    session = FakeSession(df_in)
    conf = Conf(params={}, size=2000, limit=2)
    job = Stock(session=session, conf=conf)
    job.clean()
    result = job.run()
    assert isinstance(result, pd.DataFrame)
    assert not result.empty

    conn = session.connection
    assert len(conn.calls) == len(job._STATUSES)

    statuses = {c["list_status"] for c in conn.calls}
    assert statuses == set(job._STATUSES)
    job.clean()


def test_list_codes_and_names_use_cache():
    df_in = make_input_df()
    session = FakeSession(df_in)
    job = Stock(session=session, conf={"use_cache": True})
    job.clean()
    codes = job.list_codes()
    names = job.list_names()
    assert len(codes) == len(df_in)
    assert len(names) == len(df_in)

    conn = session.connection
    assert len(conn.calls) >= 1
    assert "_run" in job.cache
    assert "list_codes" in job.cache
    assert "list_names" in job.cache
    job.clean()
