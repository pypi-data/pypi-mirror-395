from __future__ import annotations

from typing import Any, Dict, Optional

import pandas as pd

from xfintech.common.output import Output
from xfintech.common.retry import Retry
from xfintech.data.tushare.base.conf import Conf
from xfintech.data.tushare.session.session import Session
from xfintech.data.tushare.stock.market.daycdm import Daycdm
from xfintech.fabric.table.tableinfo import TableInfo


class DaycdmBa(Daycdm):
    """
    描述: 获取股票每日[前复权]技术面因子数据，用于跟踪股票当前走势情况 <br>
    说明: 单次调取最多返回10000条数据, 可以通过日期参数循环, 覆盖全历史 <br>
    使用: 基础积分每分钟内可调取500次, 5000积分每分钟可以请求30次, 8000积分以上每分钟500次 <br>

    参数:
    - session: Session, 必需, Tushare API会话对象
    - conf: Conf | Dict[str, Any], 可选, 作业配置, 支持以下参数:
        - params: Dict, 可选, 请求参数
            - ts_code: str, 可选, 股票代码(支持多个股票, 逗号分隔)
                格式: XXXXXX.SZ(深圳) / XXXXXX.SH(上海) / XXXXXX.BJ(北交所)
            - trade_date: str, 可选, 特定交易日期(YYYYMMDD)
                用于获取某个交易日的全市场数据
            - start_date: str, 可选, 开始日期(YYYYMMDD)
            - end_date: str, 可选, 结束日期(YYYYMMDD)
        - limit: int, 可选, 最大迭代次数, 默认10000
        - size: int, 可选, 每次提取数据量, 建议不超过6000
        - coolant: float, 可选, 请求间隔时间(秒), 默认0.1
    - retry: Retry, 可选, 重试配置

    例子:
    ```python
        # 获取多只股票数据进行对比分析
        cdm_job = DaycdmBa(
            session=session,
            conf=Conf(
                params={
                    "ts_code": "000001.SZ",
                    "start_date": "20241101",
                    "end_date": "20241201"
                }
            )
        )
        result = cdm_job.run()
        cdm_job.clean()  # 清理缓存
    ```
    """

    _SIZE = Daycdm._SIZE
    _FREQ = Daycdm._FREQ
    _ARGS = Daycdm._ARGS
    _IN_QFQ_COLS = Daycdm._IN_QFQ_COLS
    _IN_HFQ_COLS = Daycdm._IN_HFQ_COLS
    _IN_BFQ_COLS = Daycdm._IN_BFQ_COLS
    _IN_MAIN_COLS = Daycdm._IN_MAIN_COLS
    _IN = Daycdm._IN
    _OUT_BA_COLS = Daycdm._OUT_BA_COLS
    _OUT_MAIN_COLS = Daycdm._OUT_MAIN_COLS
    _OUT = TableInfo(
        desc="A股日线通用数据模型",
        meta={"source": "tushare"},
        columns=_OUT_MAIN_COLS + _OUT_BA_COLS,
    )

    def __init__(
        self,
        session: Session,
        conf: Optional[Conf | Dict[str, Any]] = None,
        retry: Optional[Retry] = None,
    ) -> None:
        super().__init__(
            session=session,
            conf=conf,
            retry=retry,
        )
        self.output = Output(
            name="daycdmba",
            tableinfo=self._OUT,
        )
        self.tags = {
            "name": "daycdmba",
            "module": "stock",
            "level": "market",
            "frequency": "interday",
            "scope": "stk_factor_pro",
        }

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        cols = self.output.list_column_names()
        if data is None or data.empty:
            return pd.DataFrame(columns=cols)

        main_df = self._transform_main(data).reset_index(drop=True)
        ba_df = self._transform_ba(data).reset_index(drop=True)
        transformed = pd.concat([main_df, ba_df], axis=1)
        return transformed[cols].reset_index(drop=True)
