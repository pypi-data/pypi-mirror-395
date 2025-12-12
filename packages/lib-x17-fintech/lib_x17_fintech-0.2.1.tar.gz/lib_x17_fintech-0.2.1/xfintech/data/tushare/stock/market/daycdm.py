from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

import pandas as pd

from xfintech.common.output import Output
from xfintech.common.retry import Retry
from xfintech.common.source import Source
from xfintech.data.tushare.base.conf import Conf
from xfintech.data.tushare.base.job import Job
from xfintech.data.tushare.session.session import Session
from xfintech.fabric.column.columninfo import ColumnInfo
from xfintech.fabric.datakind.datakind import DataKind
from xfintech.fabric.table.tableinfo import TableInfo


class Daycdm(Job):
    """
    描述: 获取股票每日技术面因子数据，用于跟踪股票当前走势情况 <br>
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
        cdm_job = Daycdm(
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

    _SIZE = 10000
    _FREQ = 2
    _ARGS = {
        "ts_code": {
            "type": DataKind.STRING,
            "required": "N",
            "desc": "股票代码(支持多个股票同时提取, 逗号分隔)",
        },
        "trade_date": {
            "type": DataKind.STRING,
            "required": "N",
            "desc": "交易日期(YYYYMMDD)",
        },
        "start_date": {
            "type": DataKind.STRING,
            "required": "N",
            "desc": "开始日期(YYYYMMDD)",
        },
        "end_date": {
            "type": DataKind.STRING,
            "required": "N",
            "desc": "结束日期(YYYYMMDD)",
        },
    }
    _IN_QFQ_COLS = [
        ColumnInfo(name="high_qfq", kind=DataKind.FLOAT, desc="最高价(前复权)"),
        ColumnInfo(name="open_qfq", kind=DataKind.FLOAT, desc="开盘价(前复权)"),
        ColumnInfo(name="low_qfq", kind=DataKind.FLOAT, desc="最低价(前复权)"),
        ColumnInfo(name="close_qfq", kind=DataKind.FLOAT, desc="收盘价(前复权)"),
        ColumnInfo(name="asi_qfq", kind=DataKind.FLOAT, desc="振动升降指标-OPEN,CLOSE,HIGH,LOW,M1=26,M2=10"),
        ColumnInfo(name="asit_qfq", kind=DataKind.FLOAT, desc="振动升降指标-OPEN,CLOSE,HIGH,LOW,M1=26,M2=10"),
        ColumnInfo(name="atr_qfq", kind=DataKind.FLOAT, desc="真实波动N日平均值-CLOSE,HIGH,LOW,N=20"),
        ColumnInfo(name="bbi_qfq", kind=DataKind.FLOAT, desc="BBI多空指标-CLOSE,M1=3,M2=6,M3=12,M4=22"),
        ColumnInfo(name="bias1_qfq", kind=DataKind.FLOAT, desc="BIAS乖离率-CLOSE,L1=6,L2=12,L3=24"),
        ColumnInfo(name="bias2_qfq", kind=DataKind.FLOAT, desc="BIAS乖离率-CLOSE,L1=6,L2=12,L3=24"),
        ColumnInfo(name="bias3_qfq", kind=DataKind.FLOAT, desc="BIAS乖离率-CLOSE,L1=6,L2=12,L3=24"),
        ColumnInfo(name="boll_lower_qfq", kind=DataKind.FLOAT, desc="BOLL指标,布林带-CLOSE,N=20,P=2"),
        ColumnInfo(name="boll_mid_qfq", kind=DataKind.FLOAT, desc="BOLL指标,布林带-CLOSE,N=20,P=2"),
        ColumnInfo(name="boll_upper_qfq", kind=DataKind.FLOAT, desc="BOLL指标,布林带-CLOSE,N=20,P=2"),
        ColumnInfo(name="brar_ar_qfq", kind=DataKind.FLOAT, desc="BRAR情绪指标-OPEN,CLOSE,HIGH,LOW,M1=26"),
        ColumnInfo(name="brar_br_qfq", kind=DataKind.FLOAT, desc="BRAR情绪指标-OPEN,CLOSE,HIGH,LOW,M1=26"),
        ColumnInfo(name="cci_qfq", kind=DataKind.FLOAT, desc="顺势指标又叫CCI指标-CLOSE,HIGH,LOW,N=14"),
        ColumnInfo(name="cr_qfq", kind=DataKind.FLOAT, desc="CR价格动量指标-CLOSE,HIGH,LOW,N=20"),
        ColumnInfo(name="dfma_dif_qfq", kind=DataKind.FLOAT, desc="平行线差指标-CLOSE,N1=10,N2=50,M=10"),
        ColumnInfo(name="dfma_difma_qfq", kind=DataKind.FLOAT, desc="平行线差指标-CLOSE,N1=10,N2=50,M=10"),
        ColumnInfo(name="dmi_adx_qfq", kind=DataKind.FLOAT, desc="动向指标-CLOSE,HIGH,LOW,M1=14,M2=6"),
        ColumnInfo(name="dmi_adxr_qfq", kind=DataKind.FLOAT, desc="动向指标-CLOSE,HIGH,LOW,M1=14,M2=6"),
        ColumnInfo(name="dmi_mdi_qfq", kind=DataKind.FLOAT, desc="动向指标-CLOSE,HIGH,LOW,M1=14,M2=6"),
        ColumnInfo(name="dmi_pdi_qfq", kind=DataKind.FLOAT, desc="动向指标-CLOSE,HIGH,LOW,M1=14,M2=6"),
        ColumnInfo(name="dpo_qfq", kind=DataKind.FLOAT, desc="区间震荡线-CLOSE,M1=20,M2=10,M3=6"),
        ColumnInfo(name="madpo_qfq", kind=DataKind.FLOAT, desc="区间震荡线-CLOSE,M1=20,M2=10,M3=6"),
        ColumnInfo(name="ema_qfq_10", kind=DataKind.FLOAT, desc="指数移动平均-N=10"),
        ColumnInfo(name="ema_qfq_20", kind=DataKind.FLOAT, desc="指数移动平均-N=20"),
        ColumnInfo(name="ema_qfq_250", kind=DataKind.FLOAT, desc="指数移动平均-N=250"),
        ColumnInfo(name="ema_qfq_30", kind=DataKind.FLOAT, desc="指数移动平均-N=30"),
        ColumnInfo(name="ema_qfq_5", kind=DataKind.FLOAT, desc="指数移动平均-N=5"),
        ColumnInfo(name="ema_qfq_60", kind=DataKind.FLOAT, desc="指数移动平均-N=60"),
        ColumnInfo(name="ema_qfq_90", kind=DataKind.FLOAT, desc="指数移动平均-N=90"),
        ColumnInfo(name="emv_qfq", kind=DataKind.FLOAT, desc="简易波动指标-HIGH,LOW,VOL,N=14,M=9"),
        ColumnInfo(name="maemv_qfq", kind=DataKind.FLOAT, desc="简易波动指标-HIGH,LOW,VOL,N=14,M=9"),
        ColumnInfo(name="expma_12_qfq", kind=DataKind.FLOAT, desc="EMA指数平均数指标-CLOSE,N1=12,N2=50"),
        ColumnInfo(name="expma_50_qfq", kind=DataKind.FLOAT, desc="EMA指数平均数指标-CLOSE,N1=12,N2=50"),
        ColumnInfo(name="kdj_qfq", kind=DataKind.FLOAT, desc="KDJ指标-CLOSE,HIGH,LOW,N=9,M1=3,M2=3"),
        ColumnInfo(name="kdj_d_qfq", kind=DataKind.FLOAT, desc="KDJ指标-CLOSE,HIGH,LOW,N=9,M1=3,M2=3"),
        ColumnInfo(name="kdj_k_qfq", kind=DataKind.FLOAT, desc="KDJ指标-CLOSE,HIGH,LOW,N=9,M1=3,M2=3"),
        ColumnInfo(name="ktn_down_qfq", kind=DataKind.FLOAT, desc="肯特纳通道,N=20,ATR=10-CLOSE,HIGH,LOW,M=10"),
        ColumnInfo(name="ktn_mid_qfq", kind=DataKind.FLOAT, desc="肯特纳通道,N=20,ATR=10-CLOSE,HIGH,LOW,M=10"),
        ColumnInfo(name="ktn_upper_qfq", kind=DataKind.FLOAT, desc="肯特纳通道,N=20,ATR=10-CLOSE,HIGH,LOW,M=10"),
        ColumnInfo(name="ma_qfq_10", kind=DataKind.FLOAT, desc="简单移动平均-N=10"),
        ColumnInfo(name="ma_qfq_20", kind=DataKind.FLOAT, desc="简单移动平均-N=20"),
        ColumnInfo(name="ma_qfq_250", kind=DataKind.FLOAT, desc="简单移动平均-N=250"),
        ColumnInfo(name="ma_qfq_30", kind=DataKind.FLOAT, desc="简单移动平均-N=30"),
        ColumnInfo(name="ma_qfq_5", kind=DataKind.FLOAT, desc="简单移动平均-N=5"),
        ColumnInfo(name="ma_qfq_60", kind=DataKind.FLOAT, desc="简单移动平均-N=60"),
        ColumnInfo(name="ma_qfq_90", kind=DataKind.FLOAT, desc="简单移动平均-N=90"),
        ColumnInfo(name="macd_qfq", kind=DataKind.FLOAT, desc="MACD指标-CLOSE,SHORT=12,LONG=26,M=9"),
        ColumnInfo(name="macd_dea_qfq", kind=DataKind.FLOAT, desc="MACD指标-CLOSE,SHORT=12,LONG=26,M=9"),
        ColumnInfo(name="macd_dif_qfq", kind=DataKind.FLOAT, desc="MACD指标-CLOSE,SHORT=12,LONG=26,M=9"),
        ColumnInfo(name="mass_qfq", kind=DataKind.FLOAT, desc="梅斯线-HIGH,LOW,N1=9,N2=25,M=6"),
        ColumnInfo(name="ma_mass_qfq", kind=DataKind.FLOAT, desc="梅斯线-HIGH,LOW,N1=9,N2=25,M=6"),
        ColumnInfo(name="mfi_qfq", kind=DataKind.FLOAT, desc="MFI指标是成交量的RSI指标-CLOSE,HIGH,LOW,VOL,N=14"),
        ColumnInfo(name="mtm_qfq", kind=DataKind.FLOAT, desc="动量指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="mtmma_qfq", kind=DataKind.FLOAT, desc="动量指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="obv_qfq", kind=DataKind.FLOAT, desc="能量潮指标-CLOSE,VOL"),
        ColumnInfo(name="psy_qfq", kind=DataKind.FLOAT, desc="投资者对股市涨跌心理波动情绪指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="psyma_qfq", kind=DataKind.FLOAT, desc="投资者对股市涨跌心理波动情绪指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="roc_qfq", kind=DataKind.FLOAT, desc="变动率指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="maroc_qfq", kind=DataKind.FLOAT, desc="变动率指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="rsi_qfq_12", kind=DataKind.FLOAT, desc="RSI指标-CLOSE,N=12"),
        ColumnInfo(name="rsi_qfq_24", kind=DataKind.FLOAT, desc="RSI指标-CLOSE,N=24"),
        ColumnInfo(name="rsi_qfq_6", kind=DataKind.FLOAT, desc="RSI指标-CLOSE,N=6"),
        ColumnInfo(name="taq_down_qfq", kind=DataKind.FLOAT, desc="唐安奇通道(海龟)交易指标-HIGH,LOW,20"),
        ColumnInfo(name="taq_mid_qfq", kind=DataKind.FLOAT, desc="唐安奇通道(海龟)交易指标-HIGH,LOW,20"),
        ColumnInfo(name="taq_up_qfq", kind=DataKind.FLOAT, desc="唐安奇通道(海龟)交易指标-HIGH,LOW,20"),
        ColumnInfo(name="trix_qfq", kind=DataKind.FLOAT, desc="三重指数平滑平均线-CLOSE,M1=12,M2=20"),
        ColumnInfo(name="trma_qfq", kind=DataKind.FLOAT, desc="三重指数平滑平均线-CLOSE,M1=12,M2=20"),
        ColumnInfo(name="vr_qfq", kind=DataKind.FLOAT, desc="VR容量比率-CLOSE,VOL,M1=26"),
        ColumnInfo(name="wr_qfq", kind=DataKind.FLOAT, desc="W&R 威廉指标-CLOSE,HIGH,LOW,N=10,N1=6"),
        ColumnInfo(name="wr1_qfq", kind=DataKind.FLOAT, desc="W&R 威廉指标-CLOSE,HIGH,LOW,N=10,N1=6"),
        ColumnInfo(name="xsii_td1_qfq", kind=DataKind.FLOAT, desc="薛斯通道II-CLOSE,HIGH,LOW,N=102,M=7"),
        ColumnInfo(name="xsii_td2_qfq", kind=DataKind.FLOAT, desc="薛斯通道II-CLOSE,HIGH,LOW,N=102,M=7"),
        ColumnInfo(name="xsii_td3_qfq", kind=DataKind.FLOAT, desc="薛斯通道II-CLOSE,HIGH,LOW,N=102,M=7"),
        ColumnInfo(name="xsii_td4_qfq", kind=DataKind.FLOAT, desc="薛斯通道II-CLOSE,HIGH,LOW,N=102,M=7"),
    ]
    _IN_HFQ_COLS = [
        ColumnInfo(name="high_hfq", kind=DataKind.FLOAT, desc="最高价(后复权)"),
        ColumnInfo(name="open_hfq", kind=DataKind.FLOAT, desc="开盘价(后复权)"),
        ColumnInfo(name="low_hfq", kind=DataKind.FLOAT, desc="最低价(后复权)"),
        ColumnInfo(name="close_hfq", kind=DataKind.FLOAT, desc="收盘价(后复权)"),
        ColumnInfo(name="asi_hfq", kind=DataKind.FLOAT, desc="振动升降指标-OPEN,CLOSE,HIGH,LOW,M1=26,M2=10"),
        ColumnInfo(name="asit_hfq", kind=DataKind.FLOAT, desc="振动升降指标-OPEN,CLOSE,HIGH,LOW,M1=26,M2=10"),
        ColumnInfo(name="atr_hfq", kind=DataKind.FLOAT, desc="真实波动N日平均值-CLOSE,HIGH,LOW,N=20"),
        ColumnInfo(name="bbi_hfq", kind=DataKind.FLOAT, desc="BBI多空指标-CLOSE,M1=3,M2=6,M3=12,M4=21"),
        ColumnInfo(name="bias1_hfq", kind=DataKind.FLOAT, desc="BIAS乖离率-CLOSE,L1=6,L2=12,L3=24"),
        ColumnInfo(name="bias2_hfq", kind=DataKind.FLOAT, desc="BIAS乖离率-CLOSE,L1=6,L2=12,L3=24"),
        ColumnInfo(name="bias3_hfq", kind=DataKind.FLOAT, desc="BIAS乖离率-CLOSE,L1=6,L2=12,L3=24"),
        ColumnInfo(name="boll_lower_hfq", kind=DataKind.FLOAT, desc="BOLL指标,布林带-CLOSE,N=20,P=2"),
        ColumnInfo(name="boll_mid_hfq", kind=DataKind.FLOAT, desc="BOLL指标,布林带-CLOSE,N=20,P=2"),
        ColumnInfo(name="boll_upper_hfq", kind=DataKind.FLOAT, desc="BOLL指标,布林带-CLOSE,N=20,P=2"),
        ColumnInfo(name="brar_ar_hfq", kind=DataKind.FLOAT, desc="BRAR情绪指标-OPEN,CLOSE,HIGH,LOW,M1=26"),
        ColumnInfo(name="brar_br_hfq", kind=DataKind.FLOAT, desc="BRAR情绪指标-OPEN,CLOSE,HIGH,LOW,M1=26"),
        ColumnInfo(name="cci_hfq", kind=DataKind.FLOAT, desc="顺势指标又叫CCI指标-CLOSE,HIGH,LOW,N=14"),
        ColumnInfo(name="cr_hfq", kind=DataKind.FLOAT, desc="CR价格动量指标-CLOSE,HIGH,LOW,N=20"),
        ColumnInfo(name="dfma_dif_hfq", kind=DataKind.FLOAT, desc="平行线差指标-CLOSE,N1=10,N2=50,M=10"),
        ColumnInfo(name="dfma_difma_hfq", kind=DataKind.FLOAT, desc="平行线差指标-CLOSE,N1=10,N2=50,M=10"),
        ColumnInfo(name="dmi_adx_hfq", kind=DataKind.FLOAT, desc="动向指标-CLOSE,HIGH,LOW,M1=14,M2=6"),
        ColumnInfo(name="dmi_adxr_hfq", kind=DataKind.FLOAT, desc="动向指标-CLOSE,HIGH,LOW,M1=14,M2=6"),
        ColumnInfo(name="dmi_mdi_hfq", kind=DataKind.FLOAT, desc="动向指标-CLOSE,HIGH,LOW,M1=14,M2=6"),
        ColumnInfo(name="dmi_pdi_hfq", kind=DataKind.FLOAT, desc="动向指标-CLOSE,HIGH,LOW,M1=14,M2=6"),
        ColumnInfo(name="dpo_hfq", kind=DataKind.FLOAT, desc="区间震荡线-CLOSE,M1=20,M2=10,M3=6"),
        ColumnInfo(name="madpo_hfq", kind=DataKind.FLOAT, desc="区间震荡线-CLOSE,M1=20,M2=10,M3=6"),
        ColumnInfo(name="ema_hfq_10", kind=DataKind.FLOAT, desc="指数移动平均-N=10"),
        ColumnInfo(name="ema_hfq_20", kind=DataKind.FLOAT, desc="指数移动平均-N=20"),
        ColumnInfo(name="ema_hfq_250", kind=DataKind.FLOAT, desc="指数移动平均-N=250"),
        ColumnInfo(name="ema_hfq_30", kind=DataKind.FLOAT, desc="指数移动平均-N=30"),
        ColumnInfo(name="ema_hfq_5", kind=DataKind.FLOAT, desc="指数移动平均-N=5"),
        ColumnInfo(name="ema_hfq_60", kind=DataKind.FLOAT, desc="指数移动平均-N=60"),
        ColumnInfo(name="ema_hfq_90", kind=DataKind.FLOAT, desc="指数移动平均-N=90"),
        ColumnInfo(name="emv_hfq", kind=DataKind.FLOAT, desc="简易波动指标-HIGH,LOW,VOL,N=14,M=9"),
        ColumnInfo(name="maemv_hfq", kind=DataKind.FLOAT, desc="简易波动指标-HIGH,LOW,VOL,N=14,M=9"),
        ColumnInfo(name="expma_12_hfq", kind=DataKind.FLOAT, desc="EMA指数平均数指标-CLOSE,N1=12,N2=50"),
        ColumnInfo(name="expma_50_hfq", kind=DataKind.FLOAT, desc="EMA指数平均数指标-CLOSE,N1=12,N2=50"),
        ColumnInfo(name="kdj_hfq", kind=DataKind.FLOAT, desc="KDJ指标-CLOSE,HIGH,LOW,N=9,M1=3,M2=3"),
        ColumnInfo(name="kdj_d_hfq", kind=DataKind.FLOAT, desc="KDJ指标-CLOSE,HIGH,LOW,N=9,M1=3,M2=3"),
        ColumnInfo(name="kdj_k_hfq", kind=DataKind.FLOAT, desc="KDJ指标-CLOSE,HIGH,LOW,N=9,M1=3,M2=3"),
        ColumnInfo(name="ktn_down_hfq", kind=DataKind.FLOAT, desc="肯特纳通道,N=20,ATR=10-CLOSE,HIGH,LOW,M=10"),
        ColumnInfo(name="ktn_mid_hfq", kind=DataKind.FLOAT, desc="肯特纳通道,N=20,ATR=10-CLOSE,HIGH,LOW,M=10"),
        ColumnInfo(name="ktn_upper_hfq", kind=DataKind.FLOAT, desc="肯特纳通道,N=20,ATR=10-CLOSE,HIGH,LOW,M=10"),
        ColumnInfo(name="ma_hfq_10", kind=DataKind.FLOAT, desc="简单移动平均-N=10"),
        ColumnInfo(name="ma_hfq_20", kind=DataKind.FLOAT, desc="简单移动平均-N=20"),
        ColumnInfo(name="ma_hfq_250", kind=DataKind.FLOAT, desc="简单移动平均-N=250"),
        ColumnInfo(name="ma_hfq_30", kind=DataKind.FLOAT, desc="简单移动平均-N=30"),
        ColumnInfo(name="ma_hfq_5", kind=DataKind.FLOAT, desc="简单移动平均-N=5"),
        ColumnInfo(name="ma_hfq_60", kind=DataKind.FLOAT, desc="简单移动平均-N=60"),
        ColumnInfo(name="ma_hfq_90", kind=DataKind.FLOAT, desc="简单移动平均-N=90"),
        ColumnInfo(name="macd_hfq", kind=DataKind.FLOAT, desc="MACD指标-CLOSE,SHORT=12,LONG=26,M=9"),
        ColumnInfo(name="macd_dea_hfq", kind=DataKind.FLOAT, desc="MACD指标-CLOSE,SHORT=12,LONG=26,M=9"),
        ColumnInfo(name="macd_dif_hfq", kind=DataKind.FLOAT, desc="MACD指标-CLOSE,SHORT=12,LONG=26,M=9"),
        ColumnInfo(name="mass_hfq", kind=DataKind.FLOAT, desc="梅斯线-HIGH,LOW,N1=9,N2=25,M=6"),
        ColumnInfo(name="ma_mass_hfq", kind=DataKind.FLOAT, desc="梅斯线-HIGH,LOW,N1=9,N2=25,M=6"),
        ColumnInfo(name="mfi_hfq", kind=DataKind.FLOAT, desc="MFI指标是成交量的RSI指标-CLOSE,HIGH,LOW,VOL,N=14"),
        ColumnInfo(name="mtm_hfq", kind=DataKind.FLOAT, desc="动量指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="mtmma_hfq", kind=DataKind.FLOAT, desc="动量指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="obv_hfq", kind=DataKind.FLOAT, desc="能量潮指标-CLOSE,VOL"),
        ColumnInfo(name="psy_hfq", kind=DataKind.FLOAT, desc="投资者对股市涨跌心理波动情绪指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="psyma_hfq", kind=DataKind.FLOAT, desc="投资者对股市涨跌心理波动情绪指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="roc_hfq", kind=DataKind.FLOAT, desc="变动率指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="maroc_hfq", kind=DataKind.FLOAT, desc="变动率指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="rsi_hfq_12", kind=DataKind.FLOAT, desc="RSI指标-CLOSE,N=12"),
        ColumnInfo(name="rsi_hfq_24", kind=DataKind.FLOAT, desc="RSI指标-CLOSE,N=24"),
        ColumnInfo(name="rsi_hfq_6", kind=DataKind.FLOAT, desc="RSI指标-CLOSE,N=6"),
        ColumnInfo(name="taq_down_hfq", kind=DataKind.FLOAT, desc="唐安奇通道(海龟)交易指标-HIGH,LOW,20"),
        ColumnInfo(name="taq_mid_hfq", kind=DataKind.FLOAT, desc="唐安奇通道(海龟)交易指标-HIGH,LOW,20"),
        ColumnInfo(name="taq_up_hfq", kind=DataKind.FLOAT, desc="唐安奇通道(海龟)交易指标-HIGH,LOW,20"),
        ColumnInfo(name="trix_hfq", kind=DataKind.FLOAT, desc="三重指数平滑平均线-CLOSE,M1=12,M2=20"),
        ColumnInfo(name="trma_hfq", kind=DataKind.FLOAT, desc="三重指数平滑平均线-CLOSE,M1=12,M2=20"),
        ColumnInfo(name="vr_hfq", kind=DataKind.FLOAT, desc="VR容量比率-CLOSE,VOL,M1=26"),
        ColumnInfo(name="wr_hfq", kind=DataKind.FLOAT, desc="W&R 威廉指标-CLOSE,HIGH,LOW,N=10,N1=6"),
        ColumnInfo(name="wr1_hfq", kind=DataKind.FLOAT, desc="W&R 威廉指标-CLOSE,HIGH,LOW,N=10,N1=6"),
        ColumnInfo(name="xsii_td1_hfq", kind=DataKind.FLOAT, desc="薛斯通道II-CLOSE,HIGH,LOW,N=102,M=7"),
        ColumnInfo(name="xsii_td2_hfq", kind=DataKind.FLOAT, desc="薛斯通道II-CLOSE,HIGH,LOW,N=102,M=7"),
        ColumnInfo(name="xsii_td3_hfq", kind=DataKind.FLOAT, desc="薛斯通道II-CLOSE,HIGH,LOW,N=102,M=7"),
        ColumnInfo(name="xsii_td4_hfq", kind=DataKind.FLOAT, desc="薛斯通道II-CLOSE,HIGH,LOW,N=102,M=7"),
    ]
    _IN_BFQ_COLS = [
        ColumnInfo(name="open", kind=DataKind.FLOAT, desc="开盘价"),
        ColumnInfo(name="high", kind=DataKind.FLOAT, desc="最高价"),
        ColumnInfo(name="low", kind=DataKind.FLOAT, desc="最低价"),
        ColumnInfo(name="close", kind=DataKind.FLOAT, desc="收盘价"),
        ColumnInfo(name="asi_bfq", kind=DataKind.FLOAT, desc="振动升降指标-OPEN,CLOSE,HIGH,LOW,M1=26,M2=10"),
        ColumnInfo(name="asit_bfq", kind=DataKind.FLOAT, desc="振动升降指标-OPEN,CLOSE,HIGH,LOW,M1=26,M2=10"),
        ColumnInfo(name="atr_bfq", kind=DataKind.FLOAT, desc="真实波动N日平均值-CLOSE,HIGH,LOW,N=20"),
        ColumnInfo(name="bbi_bfq", kind=DataKind.FLOAT, desc="BBI多空指标-CLOSE,M1=3,M2=6,M3=12,M4=20"),
        ColumnInfo(name="bias1_bfq", kind=DataKind.FLOAT, desc="BIAS乖离率-CLOSE,L1=6,L2=12,L3=24"),
        ColumnInfo(name="bias2_bfq", kind=DataKind.FLOAT, desc="BIAS乖离率-CLOSE,L1=6,L2=12,L3=24"),
        ColumnInfo(name="bias3_bfq", kind=DataKind.FLOAT, desc="BIAS乖离率-CLOSE,L1=6,L2=12,L3=24"),
        ColumnInfo(name="boll_lower_bfq", kind=DataKind.FLOAT, desc="BOLL指标,布林带-CLOSE,N=20,P=2"),
        ColumnInfo(name="boll_mid_bfq", kind=DataKind.FLOAT, desc="BOLL指标,布林带-CLOSE,N=20,P=2"),
        ColumnInfo(name="boll_upper_bfq", kind=DataKind.FLOAT, desc="BOLL指标,布林带-CLOSE,N=20,P=2"),
        ColumnInfo(name="brar_ar_bfq", kind=DataKind.FLOAT, desc="BRAR情绪指标-OPEN,CLOSE,HIGH,LOW,M1=26"),
        ColumnInfo(name="brar_br_bfq", kind=DataKind.FLOAT, desc="BRAR情绪指标-OPEN,CLOSE,HIGH,LOW,M1=26"),
        ColumnInfo(name="cci_bfq", kind=DataKind.FLOAT, desc="顺势指标又叫CCI指标-CLOSE,HIGH,LOW,N=14"),
        ColumnInfo(name="cr_bfq", kind=DataKind.FLOAT, desc="CR价格动量指标-CLOSE,HIGH,LOW,N=20"),
        ColumnInfo(name="dfma_dif_bfq", kind=DataKind.FLOAT, desc="平行线差指标-CLOSE,N1=10,N2=50,M=10"),
        ColumnInfo(name="dfma_difma_bfq", kind=DataKind.FLOAT, desc="平行线差指标-CLOSE,N1=10,N2=50,M=10"),
        ColumnInfo(name="dmi_adx_bfq", kind=DataKind.FLOAT, desc="动向指标-CLOSE,HIGH,LOW,M1=14,M2=6"),
        ColumnInfo(name="dmi_adxr_bfq", kind=DataKind.FLOAT, desc="动向指标-CLOSE,HIGH,LOW,M1=14,M2=6"),
        ColumnInfo(name="dmi_mdi_bfq", kind=DataKind.FLOAT, desc="动向指标-CLOSE,HIGH,LOW,M1=14,M2=6"),
        ColumnInfo(name="dmi_pdi_bfq", kind=DataKind.FLOAT, desc="动向指标-CLOSE,HIGH,LOW,M1=14,M2=6"),
        ColumnInfo(name="dpo_bfq", kind=DataKind.FLOAT, desc="区间震荡线-CLOSE,M1=20,M2=10,M3=6"),
        ColumnInfo(name="madpo_bfq", kind=DataKind.FLOAT, desc="区间震荡线-CLOSE,M1=20,M2=10,M3=6"),
        ColumnInfo(name="ema_bfq_10", kind=DataKind.FLOAT, desc="指数移动平均-N=10"),
        ColumnInfo(name="ema_bfq_20", kind=DataKind.FLOAT, desc="指数移动平均-N=20"),
        ColumnInfo(name="ema_bfq_250", kind=DataKind.FLOAT, desc="指数移动平均-N=250"),
        ColumnInfo(name="ema_bfq_30", kind=DataKind.FLOAT, desc="指数移动平均-N=30"),
        ColumnInfo(name="ema_bfq_5", kind=DataKind.FLOAT, desc="指数移动平均-N=5"),
        ColumnInfo(name="ema_bfq_60", kind=DataKind.FLOAT, desc="指数移动平均-N=60"),
        ColumnInfo(name="ema_bfq_90", kind=DataKind.FLOAT, desc="指数移动平均-N=90"),
        ColumnInfo(name="emv_bfq", kind=DataKind.FLOAT, desc="简易波动指标-HIGH,LOW,VOL,N=14,M=9"),
        ColumnInfo(name="maemv_bfq", kind=DataKind.FLOAT, desc="简易波动指标-HIGH,LOW,VOL,N=14,M=9"),
        ColumnInfo(name="expma_12_bfq", kind=DataKind.FLOAT, desc="EMA指数平均数指标-CLOSE,N1=12,N2=50"),
        ColumnInfo(name="expma_50_bfq", kind=DataKind.FLOAT, desc="EMA指数平均数指标-CLOSE,N1=12,N2=50"),
        ColumnInfo(name="kdj_bfq", kind=DataKind.FLOAT, desc="KDJ指标-CLOSE,HIGH,LOW,N=9,M1=3,M2=3"),
        ColumnInfo(name="kdj_d_bfq", kind=DataKind.FLOAT, desc="KDJ指标-CLOSE,HIGH,LOW,N=9,M1=3,M2=3"),
        ColumnInfo(name="kdj_k_bfq", kind=DataKind.FLOAT, desc="KDJ指标-CLOSE,HIGH,LOW,N=9,M1=3,M2=3"),
        ColumnInfo(name="ktn_down_bfq", kind=DataKind.FLOAT, desc="肯特纳通道,N=20,ATR=10-CLOSE,HIGH,LOW,M=10"),
        ColumnInfo(name="ktn_mid_bfq", kind=DataKind.FLOAT, desc="肯特纳通道,N=20,ATR=10-CLOSE,HIGH,LOW,M=10"),
        ColumnInfo(name="ktn_upper_bfq", kind=DataKind.FLOAT, desc="肯特纳通道,N=20,ATR=10-CLOSE,HIGH,LOW,M=10"),
        ColumnInfo(name="ma_bfq_10", kind=DataKind.FLOAT, desc="简单移动平均-N=10"),
        ColumnInfo(name="ma_bfq_20", kind=DataKind.FLOAT, desc="简单移动平均-N=20"),
        ColumnInfo(name="ma_bfq_250", kind=DataKind.FLOAT, desc="简单移动平均-N=250"),
        ColumnInfo(name="ma_bfq_30", kind=DataKind.FLOAT, desc="简单移动平均-N=30"),
        ColumnInfo(name="ma_bfq_5", kind=DataKind.FLOAT, desc="简单移动平均-N=5"),
        ColumnInfo(name="ma_bfq_60", kind=DataKind.FLOAT, desc="简单移动平均-N=60"),
        ColumnInfo(name="ma_bfq_90", kind=DataKind.FLOAT, desc="简单移动平均-N=90"),
        ColumnInfo(name="macd_bfq", kind=DataKind.FLOAT, desc="MACD指标-CLOSE,SHORT=12,LONG=26,M=9"),
        ColumnInfo(name="macd_dea_bfq", kind=DataKind.FLOAT, desc="MACD指标-CLOSE,SHORT=12,LONG=26,M=9"),
        ColumnInfo(name="macd_dif_bfq", kind=DataKind.FLOAT, desc="MACD指标-CLOSE,SHORT=12,LONG=26,M=9"),
        ColumnInfo(name="mass_bfq", kind=DataKind.FLOAT, desc="梅斯线-HIGH,LOW,N1=9,N2=25,M=6"),
        ColumnInfo(name="ma_mass_bfq", kind=DataKind.FLOAT, desc="梅斯线-HIGH,LOW,N1=9,N2=25,M=6"),
        ColumnInfo(name="mfi_bfq", kind=DataKind.FLOAT, desc="MFI指标是成交量的RSI指标-CLOSE,HIGH,LOW,VOL,N=14"),
        ColumnInfo(name="mtm_bfq", kind=DataKind.FLOAT, desc="动量指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="mtmma_bfq", kind=DataKind.FLOAT, desc="动量指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="obv_bfq", kind=DataKind.FLOAT, desc="能量潮指标-CLOSE,VOL"),
        ColumnInfo(name="psy_bfq", kind=DataKind.FLOAT, desc="投资者对股市涨跌心理波动情绪指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="psyma_bfq", kind=DataKind.FLOAT, desc="投资者对股市涨跌心理波动情绪指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="roc_bfq", kind=DataKind.FLOAT, desc="变动率指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="maroc_bfq", kind=DataKind.FLOAT, desc="变动率指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="rsi_bfq_12", kind=DataKind.FLOAT, desc="RSI指标-CLOSE,N=12"),
        ColumnInfo(name="rsi_bfq_24", kind=DataKind.FLOAT, desc="RSI指标-CLOSE,N=24"),
        ColumnInfo(name="rsi_bfq_6", kind=DataKind.FLOAT, desc="RSI指标-CLOSE,N=6"),
        ColumnInfo(name="taq_down_bfq", kind=DataKind.FLOAT, desc="唐安奇通道(海龟)交易指标-HIGH,LOW,20"),
        ColumnInfo(name="taq_mid_bfq", kind=DataKind.FLOAT, desc="唐安奇通道(海龟)交易指标-HIGH,LOW,20"),
        ColumnInfo(name="taq_up_bfq", kind=DataKind.FLOAT, desc="唐安奇通道(海龟)交易指标-HIGH,LOW,20"),
        ColumnInfo(name="trix_bfq", kind=DataKind.FLOAT, desc="三重指数平滑平均线-CLOSE,M1=12,M2=20"),
        ColumnInfo(name="trma_bfq", kind=DataKind.FLOAT, desc="三重指数平滑平均线-CLOSE,M1=12,M2=20"),
        ColumnInfo(name="vr_bfq", kind=DataKind.FLOAT, desc="VR容量比率-CLOSE,VOL,M1=26"),
        ColumnInfo(name="wr_bfq", kind=DataKind.FLOAT, desc="W&R 威廉指标-CLOSE,HIGH,LOW,N=10,N1=6"),
        ColumnInfo(name="wr1_bfq", kind=DataKind.FLOAT, desc="W&R 威廉指标-CLOSE,HIGH,LOW,N=10,N1=6"),
        ColumnInfo(name="xsii_td1_bfq", kind=DataKind.FLOAT, desc="薛斯通道II-CLOSE,HIGH,LOW,N=102,M=7"),
        ColumnInfo(name="xsii_td2_bfq", kind=DataKind.FLOAT, desc="薛斯通道II-CLOSE,HIGH,LOW,N=102,M=7"),
        ColumnInfo(name="xsii_td3_bfq", kind=DataKind.FLOAT, desc="薛斯通道II-CLOSE,HIGH,LOW,N=102,M=7"),
        ColumnInfo(name="xsii_td4_bfq", kind=DataKind.FLOAT, desc="薛斯通道II-CLOSE,HIGH,LOW,N=102,M=7"),
    ]
    _IN_MAIN_COLS = [
        ColumnInfo(name="ts_code", kind=DataKind.STRING, desc="股票代码"),
        ColumnInfo(name="trade_date", kind=DataKind.STRING, desc="交易日期"),
        ColumnInfo(name="change", kind=DataKind.FLOAT, desc="涨跌额"),
        ColumnInfo(name="pct_chg", kind=DataKind.FLOAT, desc="涨跌幅(未复权,如果是复权请用 通用行情接口)"),
        ColumnInfo(name="vol", kind=DataKind.FLOAT, desc="成交量(手)"),
        ColumnInfo(name="amount", kind=DataKind.FLOAT, desc="成交额(千元)"),
        ColumnInfo(name="turnover_rate", kind=DataKind.FLOAT, desc="换手率(%)"),
        ColumnInfo(name="turnover_rate_f", kind=DataKind.FLOAT, desc="换手率(自由流通股)"),
        ColumnInfo(name="volume_ratio", kind=DataKind.FLOAT, desc="量比"),
        ColumnInfo(name="pe", kind=DataKind.FLOAT, desc="市盈率(总市值/净利润,亏损的PE为空)"),
        ColumnInfo(name="pe_ttm", kind=DataKind.FLOAT, desc="市盈率(TTM,亏损的PE为空)"),
        ColumnInfo(name="pb", kind=DataKind.FLOAT, desc="市净率(总市值/净资产)"),
        ColumnInfo(name="ps", kind=DataKind.FLOAT, desc="市销率"),
        ColumnInfo(name="ps_ttm", kind=DataKind.FLOAT, desc="市销率(TTM)"),
        ColumnInfo(name="dv_ratio", kind=DataKind.FLOAT, desc="股息率(%)"),
        ColumnInfo(name="dv_ttm", kind=DataKind.FLOAT, desc="股息率(TTM)(%)"),
        ColumnInfo(name="total_share", kind=DataKind.FLOAT, desc="总股本(万股)"),
        ColumnInfo(name="float_share", kind=DataKind.FLOAT, desc="流通股本(万股)"),
        ColumnInfo(name="free_share", kind=DataKind.FLOAT, desc="自由流通股本(万)"),
        ColumnInfo(name="total_mv", kind=DataKind.FLOAT, desc="总市值(万元)"),
        ColumnInfo(name="circ_mv", kind=DataKind.FLOAT, desc="流通市值(万元)"),
        ColumnInfo(name="adj_factor", kind=DataKind.FLOAT, desc="复权因子"),
        ColumnInfo(name="downdays", kind=DataKind.FLOAT, desc="连跌天数"),
        ColumnInfo(name="updays", kind=DataKind.FLOAT, desc="连涨天数"),
        ColumnInfo(name="lowdays", kind=DataKind.FLOAT, desc="当前最低价是近多少周期内最低价的最小值"),
        ColumnInfo(name="topdays", kind=DataKind.FLOAT, desc="当前最高价是近多少周期内最高价的最大值"),
    ]
    _IN = TableInfo(
        desc="A股日线通用数据模型",
        meta={"source": "tushare"},
        columns=_IN_MAIN_COLS + _IN_QFQ_COLS + _IN_HFQ_COLS + _IN_BFQ_COLS,
    )
    _OUT_FA_COLS = [
        ColumnInfo(name="fa_high", kind=DataKind.FLOAT, desc="最高价(前复权)"),
        ColumnInfo(name="fa_open", kind=DataKind.FLOAT, desc="开盘价(前复权)"),
        ColumnInfo(name="fa_low", kind=DataKind.FLOAT, desc="最低价(前复权)"),
        ColumnInfo(name="fa_close", kind=DataKind.FLOAT, desc="收盘价(前复权)"),
        ColumnInfo(name="fa_asi", kind=DataKind.FLOAT, desc="振动升降指标-OPEN,CLOSE,HIGH,LOW,M1=26,M2=10"),
        ColumnInfo(name="fa_asit", kind=DataKind.FLOAT, desc="振动升降指标-OPEN,CLOSE,HIGH,LOW,M1=26,M2=10"),
        ColumnInfo(name="fa_atr", kind=DataKind.FLOAT, desc="真实波动N日平均值-CLOSE,HIGH,LOW,N=20"),
        ColumnInfo(name="fa_bbi", kind=DataKind.FLOAT, desc="BBI多空指标-CLOSE,M1=3,M2=6,M3=12,M4=22"),
        ColumnInfo(name="fa_bias1", kind=DataKind.FLOAT, desc="BIAS乖离率-CLOSE,L1=6,L2=12,L3=24"),
        ColumnInfo(name="fa_bias2", kind=DataKind.FLOAT, desc="BIAS乖离率-CLOSE,L1=6,L2=12,L3=24"),
        ColumnInfo(name="fa_bias3", kind=DataKind.FLOAT, desc="BIAS乖离率-CLOSE,L1=6,L2=12,L3=24"),
        ColumnInfo(name="fa_boll_lower", kind=DataKind.FLOAT, desc="BOLL指标,布林带-CLOSE,N=20,P=2"),
        ColumnInfo(name="fa_boll_mid", kind=DataKind.FLOAT, desc="BOLL指标,布林带-CLOSE,N=20,P=2"),
        ColumnInfo(name="fa_boll_upper", kind=DataKind.FLOAT, desc="BOLL指标,布林带-CLOSE,N=20,P=2"),
        ColumnInfo(name="fa_brar_ar", kind=DataKind.FLOAT, desc="BRAR情绪指标-OPEN,CLOSE,HIGH,LOW,M1=26"),
        ColumnInfo(name="fa_brar_br", kind=DataKind.FLOAT, desc="BRAR情绪指标-OPEN,CLOSE,HIGH,LOW,M1=26"),
        ColumnInfo(name="fa_cci", kind=DataKind.FLOAT, desc="顺势指标又叫CCI指标-CLOSE,HIGH,LOW,N=14"),
        ColumnInfo(name="fa_cr", kind=DataKind.FLOAT, desc="CR价格动量指标-CLOSE,HIGH,LOW,N=20"),
        ColumnInfo(name="fa_dfma_dif", kind=DataKind.FLOAT, desc="平行线差指标-CLOSE,N1=10,N2=50,M=10"),
        ColumnInfo(name="fa_dfma_difma", kind=DataKind.FLOAT, desc="平行线差指标-CLOSE,N1=10,N2=50,M=10"),
        ColumnInfo(name="fa_dmi_adx", kind=DataKind.FLOAT, desc="动向指标-CLOSE,HIGH,LOW,M1=14,M2=6"),
        ColumnInfo(name="fa_dmi_adxr", kind=DataKind.FLOAT, desc="动向指标-CLOSE,HIGH,LOW,M1=14,M2=6"),
        ColumnInfo(name="fa_dmi_mdi", kind=DataKind.FLOAT, desc="动向指标-CLOSE,HIGH,LOW,M1=14,M2=6"),
        ColumnInfo(name="fa_dmi_pdi", kind=DataKind.FLOAT, desc="动向指标-CLOSE,HIGH,LOW,M1=14,M2=6"),
        ColumnInfo(name="fa_dpo", kind=DataKind.FLOAT, desc="区间震荡线-CLOSE,M1=20,M2=10,M3=6"),
        ColumnInfo(name="fa_madpo", kind=DataKind.FLOAT, desc="区间震荡线-CLOSE,M1=20,M2=10,M3=6"),
        ColumnInfo(name="fa_ema_10", kind=DataKind.FLOAT, desc="指数移动平均-N=10"),
        ColumnInfo(name="fa_ema_20", kind=DataKind.FLOAT, desc="指数移动平均-N=20"),
        ColumnInfo(name="fa_ema_250", kind=DataKind.FLOAT, desc="指数移动平均-N=250"),
        ColumnInfo(name="fa_ema_30", kind=DataKind.FLOAT, desc="指数移动平均-N=30"),
        ColumnInfo(name="fa_ema_5", kind=DataKind.FLOAT, desc="指数移动平均-N=5"),
        ColumnInfo(name="fa_ema_60", kind=DataKind.FLOAT, desc="指数移动平均-N=60"),
        ColumnInfo(name="fa_ema_90", kind=DataKind.FLOAT, desc="指数移动平均-N=90"),
        ColumnInfo(name="fa_emv", kind=DataKind.FLOAT, desc="简易波动指标-HIGH,LOW,VOL,N=14,M=9"),
        ColumnInfo(name="fa_maemv", kind=DataKind.FLOAT, desc="简易波动指标-HIGH,LOW,VOL,N=14,M=9"),
        ColumnInfo(name="fa_expma_12", kind=DataKind.FLOAT, desc="EMA指数平均数指标-CLOSE,N1=12,N2=50"),
        ColumnInfo(name="fa_expma_50", kind=DataKind.FLOAT, desc="EMA指数平均数指标-CLOSE,N1=12,N2=50"),
        ColumnInfo(name="fa_kdj", kind=DataKind.FLOAT, desc="KDJ指标-CLOSE,HIGH,LOW,N=9,M1=3,M2=3"),
        ColumnInfo(name="fa_kdj_d", kind=DataKind.FLOAT, desc="KDJ指标-CLOSE,HIGH,LOW,N=9,M1=3,M2=3"),
        ColumnInfo(name="fa_kdj_k", kind=DataKind.FLOAT, desc="KDJ指标-CLOSE,HIGH,LOW,N=9,M1=3,M2=3"),
        ColumnInfo(name="fa_ktn_down", kind=DataKind.FLOAT, desc="肯特纳通道,N=20,ATR=10-CLOSE,HIGH,LOW,M=10"),
        ColumnInfo(name="fa_ktn_mid", kind=DataKind.FLOAT, desc="肯特纳通道,N=20,ATR=10-CLOSE,HIGH,LOW,M=10"),
        ColumnInfo(name="fa_ktn_upper", kind=DataKind.FLOAT, desc="肯特纳通道,N=20,ATR=10-CLOSE,HIGH,LOW,M=10"),
        ColumnInfo(name="fa_ma_10", kind=DataKind.FLOAT, desc="简单移动平均-N=10"),
        ColumnInfo(name="fa_ma_20", kind=DataKind.FLOAT, desc="简单移动平均-N=20"),
        ColumnInfo(name="fa_ma_250", kind=DataKind.FLOAT, desc="简单移动平均-N=250"),
        ColumnInfo(name="fa_ma_30", kind=DataKind.FLOAT, desc="简单移动平均-N=30"),
        ColumnInfo(name="fa_ma_5", kind=DataKind.FLOAT, desc="简单移动平均-N=5"),
        ColumnInfo(name="fa_ma_60", kind=DataKind.FLOAT, desc="简单移动平均-N=60"),
        ColumnInfo(name="fa_ma_90", kind=DataKind.FLOAT, desc="简单移动平均-N=90"),
        ColumnInfo(name="fa_macd", kind=DataKind.FLOAT, desc="MACD指标-CLOSE,SHORT=12,LONG=26,M=9"),
        ColumnInfo(name="fa_macd_dea", kind=DataKind.FLOAT, desc="MACD指标-CLOSE,SHORT=12,LONG=26,M=9"),
        ColumnInfo(name="fa_macd_dif", kind=DataKind.FLOAT, desc="MACD指标-CLOSE,SHORT=12,LONG=26,M=9"),
        ColumnInfo(name="fa_mass", kind=DataKind.FLOAT, desc="梅斯线-HIGH,LOW,N1=9,N2=25,M=6"),
        ColumnInfo(name="fa_ma_mass", kind=DataKind.FLOAT, desc="梅斯线-HIGH,LOW,N1=9,N2=25,M=6"),
        ColumnInfo(name="fa_mfi", kind=DataKind.FLOAT, desc="MFI指标是成交量的RSI指标-CLOSE,HIGH,LOW,VOL,N=14"),
        ColumnInfo(name="fa_mtm", kind=DataKind.FLOAT, desc="动量指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="fa_mtmma", kind=DataKind.FLOAT, desc="动量指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="fa_obv", kind=DataKind.FLOAT, desc="能量潮指标-CLOSE,VOL"),
        ColumnInfo(name="fa_psy", kind=DataKind.FLOAT, desc="投资者对股市涨跌心理波动情绪指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="fa_psyma", kind=DataKind.FLOAT, desc="投资者对股市涨跌心理波动情绪指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="fa_roc", kind=DataKind.FLOAT, desc="变动率指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="fa_maroc", kind=DataKind.FLOAT, desc="变动率指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="fa_rsi_12", kind=DataKind.FLOAT, desc="RSI指标-CLOSE,N=12"),
        ColumnInfo(name="fa_rsi_24", kind=DataKind.FLOAT, desc="RSI指标-CLOSE,N=24"),
        ColumnInfo(name="fa_rsi_6", kind=DataKind.FLOAT, desc="RSI指标-CLOSE,N=6"),
        ColumnInfo(name="fa_taq_down", kind=DataKind.FLOAT, desc="唐安奇通道(海龟)交易指标-HIGH,LOW,20"),
        ColumnInfo(name="fa_taq_mid", kind=DataKind.FLOAT, desc="唐安奇通道(海龟)交易指标-HIGH,LOW,20"),
        ColumnInfo(name="fa_taq_up", kind=DataKind.FLOAT, desc="唐安奇通道(海龟)交易指标-HIGH,LOW,20"),
        ColumnInfo(name="fa_trix", kind=DataKind.FLOAT, desc="三重指数平滑平均线-CLOSE,M1=12,M2=20"),
        ColumnInfo(name="fa_trma", kind=DataKind.FLOAT, desc="三重指数平滑平均线-CLOSE,M1=12,M2=20"),
        ColumnInfo(name="fa_vr", kind=DataKind.FLOAT, desc="VR容量比率-CLOSE,VOL,M1=26"),
        ColumnInfo(name="fa_wr", kind=DataKind.FLOAT, desc="W&R 威廉指标-CLOSE,HIGH,LOW,N=10,N1=6"),
        ColumnInfo(name="fa_wr1", kind=DataKind.FLOAT, desc="W&R 威廉指标-CLOSE,HIGH,LOW,N=10,N1=6"),
        ColumnInfo(name="fa_xsii_td1", kind=DataKind.FLOAT, desc="薛斯通道II-CLOSE,HIGH,LOW,N=102,M=7"),
        ColumnInfo(name="fa_xsii_td2", kind=DataKind.FLOAT, desc="薛斯通道II-CLOSE,HIGH,LOW,N=102,M=7"),
        ColumnInfo(name="fa_xsii_td3", kind=DataKind.FLOAT, desc="薛斯通道II-CLOSE,HIGH,LOW,N=102,M=7"),
        ColumnInfo(name="fa_xsii_td4", kind=DataKind.FLOAT, desc="薛斯通道II-CLOSE,HIGH,LOW,N=102,M=7"),
    ]
    _OUT_BA_COLS = [
        ColumnInfo(name="ba_high", kind=DataKind.FLOAT, desc="最高价(后复权)"),
        ColumnInfo(name="ba_open", kind=DataKind.FLOAT, desc="开盘价(后复权)"),
        ColumnInfo(name="ba_low", kind=DataKind.FLOAT, desc="最低价(后复权)"),
        ColumnInfo(name="ba_close", kind=DataKind.FLOAT, desc="收盘价(后复权)"),
        ColumnInfo(name="ba_asi", kind=DataKind.FLOAT, desc="振动升降指标-OPEN,CLOSE,HIGH,LOW,M1=26,M2=10"),
        ColumnInfo(name="ba_asit", kind=DataKind.FLOAT, desc="振动升降指标-OPEN,CLOSE,HIGH,LOW,M1=26,M2=10"),
        ColumnInfo(name="ba_atr", kind=DataKind.FLOAT, desc="真实波动N日平均值-CLOSE,HIGH,LOW,N=20"),
        ColumnInfo(name="ba_bbi", kind=DataKind.FLOAT, desc="BBI多空指标-CLOSE,M1=3,M2=6,M3=12,M4=21"),
        ColumnInfo(name="ba_bias1", kind=DataKind.FLOAT, desc="BIAS乖离率-CLOSE,L1=6,L2=12,L3=24"),
        ColumnInfo(name="ba_bias2", kind=DataKind.FLOAT, desc="BIAS乖离率-CLOSE,L1=6,L2=12,L3=24"),
        ColumnInfo(name="ba_bias3", kind=DataKind.FLOAT, desc="BIAS乖离率-CLOSE,L1=6,L2=12,L3=24"),
        ColumnInfo(name="ba_boll_lower", kind=DataKind.FLOAT, desc="BOLL指标,布林带-CLOSE,N=20,P=2"),
        ColumnInfo(name="ba_boll_mid", kind=DataKind.FLOAT, desc="BOLL指标,布林带-CLOSE,N=20,P=2"),
        ColumnInfo(name="ba_boll_upper", kind=DataKind.FLOAT, desc="BOLL指标,布林带-CLOSE,N=20,P=2"),
        ColumnInfo(name="ba_brar_ar", kind=DataKind.FLOAT, desc="BRAR情绪指标-OPEN,CLOSE,HIGH,LOW,M1=26"),
        ColumnInfo(name="ba_brar_br", kind=DataKind.FLOAT, desc="BRAR情绪指标-OPEN,CLOSE,HIGH,LOW,M1=26"),
        ColumnInfo(name="ba_cci", kind=DataKind.FLOAT, desc="顺势指标又叫CCI指标-CLOSE,HIGH,LOW,N=14"),
        ColumnInfo(name="ba_cr", kind=DataKind.FLOAT, desc="CR价格动量指标-CLOSE,HIGH,LOW,N=20"),
        ColumnInfo(name="ba_dfma_dif", kind=DataKind.FLOAT, desc="平行线差指标-CLOSE,N1=10,N2=50,M=10"),
        ColumnInfo(name="ba_dfma_difma", kind=DataKind.FLOAT, desc="平行线差指标-CLOSE,N1=10,N2=50,M=10"),
        ColumnInfo(name="ba_dmi_adx", kind=DataKind.FLOAT, desc="动向指标-CLOSE,HIGH,LOW,M1=14,M2=6"),
        ColumnInfo(name="ba_dmi_adxr", kind=DataKind.FLOAT, desc="动向指标-CLOSE,HIGH,LOW,M1=14,M2=6"),
        ColumnInfo(name="ba_dmi_mdi", kind=DataKind.FLOAT, desc="动向指标-CLOSE,HIGH,LOW,M1=14,M2=6"),
        ColumnInfo(name="ba_dmi_pdi", kind=DataKind.FLOAT, desc="动向指标-CLOSE,HIGH,LOW,M1=14,M2=6"),
        ColumnInfo(name="ba_dpo", kind=DataKind.FLOAT, desc="区间震荡线-CLOSE,M1=20,M2=10,M3=6"),
        ColumnInfo(name="ba_madpo", kind=DataKind.FLOAT, desc="区间震荡线-CLOSE,M1=20,M2=10,M3=6"),
        ColumnInfo(name="ba_ema_10", kind=DataKind.FLOAT, desc="指数移动平均-N=10"),
        ColumnInfo(name="ba_ema_20", kind=DataKind.FLOAT, desc="指数移动平均-N=20"),
        ColumnInfo(name="ba_ema_250", kind=DataKind.FLOAT, desc="指数移动平均-N=250"),
        ColumnInfo(name="ba_ema_30", kind=DataKind.FLOAT, desc="指数移动平均-N=30"),
        ColumnInfo(name="ba_ema_5", kind=DataKind.FLOAT, desc="指数移动平均-N=5"),
        ColumnInfo(name="ba_ema_60", kind=DataKind.FLOAT, desc="指数移动平均-N=60"),
        ColumnInfo(name="ba_ema_90", kind=DataKind.FLOAT, desc="指数移动平均-N=90"),
        ColumnInfo(name="ba_emv", kind=DataKind.FLOAT, desc="简易波动指标-HIGH,LOW,VOL,N=14,M=9"),
        ColumnInfo(name="ba_maemv", kind=DataKind.FLOAT, desc="简易波动指标-HIGH,LOW,VOL,N=14,M=9"),
        ColumnInfo(name="ba_expma_12", kind=DataKind.FLOAT, desc="EMA指数平均数指标-CLOSE,N1=12,N2=50"),
        ColumnInfo(name="ba_expma_50", kind=DataKind.FLOAT, desc="EMA指数平均数指标-CLOSE,N1=12,N2=50"),
        ColumnInfo(name="ba_kdj", kind=DataKind.FLOAT, desc="KDJ指标-CLOSE,HIGH,LOW,N=9,M1=3,M2=3"),
        ColumnInfo(name="ba_kdj_d", kind=DataKind.FLOAT, desc="KDJ指标-CLOSE,HIGH,LOW,N=9,M1=3,M2=3"),
        ColumnInfo(name="ba_kdj_k", kind=DataKind.FLOAT, desc="KDJ指标-CLOSE,HIGH,LOW,N=9,M1=3,M2=3"),
        ColumnInfo(name="ba_ktn_down", kind=DataKind.FLOAT, desc="肯特纳通道,N=20,ATR=10-CLOSE,HIGH,LOW,M=10"),
        ColumnInfo(name="ba_ktn_mid", kind=DataKind.FLOAT, desc="肯特纳通道,N=20,ATR=10-CLOSE,HIGH,LOW,M=10"),
        ColumnInfo(name="ba_ktn_upper", kind=DataKind.FLOAT, desc="肯特纳通道N=20日,ATR=10日-CLOSE,HIGH,LOW,M=10"),
        ColumnInfo(name="ba_ma_10", kind=DataKind.FLOAT, desc="简单移动平均-N=10"),
        ColumnInfo(name="ba_ma_20", kind=DataKind.FLOAT, desc="简单移动平均-N=20"),
        ColumnInfo(name="ba_ma_250", kind=DataKind.FLOAT, desc="简单移动平均-N=250"),
        ColumnInfo(name="ba_ma_30", kind=DataKind.FLOAT, desc="简单移动平均-N=30"),
        ColumnInfo(name="ba_ma_5", kind=DataKind.FLOAT, desc="简单移动平均-N=5"),
        ColumnInfo(name="ba_ma_60", kind=DataKind.FLOAT, desc="简单移动平均-N=60"),
        ColumnInfo(name="ba_ma_90", kind=DataKind.FLOAT, desc="简单移动平均-N=90"),
        ColumnInfo(name="ba_macd", kind=DataKind.FLOAT, desc="MACD指标-CLOSE,SHORT=12,LONG=26,M=9"),
        ColumnInfo(name="ba_macd_dea", kind=DataKind.FLOAT, desc="MACD指标-CLOSE,SHORT=12,LONG=26,M=9"),
        ColumnInfo(name="ba_macd_dif", kind=DataKind.FLOAT, desc="MACD指标-CLOSE,SHORT=12,LONG=26,M=9"),
        ColumnInfo(name="ba_mass", kind=DataKind.FLOAT, desc="梅斯线-HIGH,LOW,N1=9,N2=25,M=6"),
        ColumnInfo(name="ba_ma_mass", kind=DataKind.FLOAT, desc="梅斯线-HIGH,LOW,N1=9,N2=25,M=6"),
        ColumnInfo(name="ba_mfi", kind=DataKind.FLOAT, desc="MFI指标是成交量的RSI指标-CLOSE,HIGH,LOW,VOL,N=14"),
        ColumnInfo(name="ba_mtm", kind=DataKind.FLOAT, desc="动量指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="ba_mtmma", kind=DataKind.FLOAT, desc="动量指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="ba_obv", kind=DataKind.FLOAT, desc="能量潮指标-CLOSE,VOL"),
        ColumnInfo(name="ba_psy", kind=DataKind.FLOAT, desc="投资者对股市涨跌心理波动的情绪指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="ba_psyma", kind=DataKind.FLOAT, desc="投资者对股市涨跌心理波动的情绪指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="ba_roc", kind=DataKind.FLOAT, desc="变动率指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="ba_maroc", kind=DataKind.FLOAT, desc="变动率指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="ba_rsi_12", kind=DataKind.FLOAT, desc="RSI指标-CLOSE,N=12"),
        ColumnInfo(name="ba_rsi_24", kind=DataKind.FLOAT, desc="RSI指标-CLOSE,N=24"),
        ColumnInfo(name="ba_rsi_6", kind=DataKind.FLOAT, desc="RSI指标-CLOSE,N=6"),
        ColumnInfo(name="ba_taq_down", kind=DataKind.FLOAT, desc="唐安奇通道(海龟)交易指标-HIGH,LOW,20"),
        ColumnInfo(name="ba_taq_mid", kind=DataKind.FLOAT, desc="唐安奇通道(海龟)交易指标-HIGH,LOW,20"),
        ColumnInfo(name="ba_taq_up", kind=DataKind.FLOAT, desc="唐安奇通道(海龟)交易指标-HIGH,LOW,20"),
        ColumnInfo(name="ba_trix", kind=DataKind.FLOAT, desc="三重指数平滑平均线-CLOSE,M1=12,M2=20"),
        ColumnInfo(name="ba_trma", kind=DataKind.FLOAT, desc="三重指数平滑平均线-CLOSE,M1=12,M2=20"),
        ColumnInfo(name="ba_vr", kind=DataKind.FLOAT, desc="VR容量比率-CLOSE,VOL,M1=26"),
        ColumnInfo(name="ba_wr", kind=DataKind.FLOAT, desc="W&R 威廉指标-CLOSE,HIGH,LOW,N=10,N1=6"),
        ColumnInfo(name="ba_wr1", kind=DataKind.FLOAT, desc="W&R 威廉指标-CLOSE,HIGH,LOW,N=10,N1=6"),
        ColumnInfo(name="ba_xsii_td1", kind=DataKind.FLOAT, desc="薛斯通道II-CLOSE,HIGH,LOW,N=102,M=7"),
        ColumnInfo(name="ba_xsii_td2", kind=DataKind.FLOAT, desc="薛斯通道II-CLOSE,HIGH,LOW,N=102,M=7"),
        ColumnInfo(name="ba_xsii_td3", kind=DataKind.FLOAT, desc="薛斯通道II-CLOSE,HIGH,LOW,N=102,M=7"),
        ColumnInfo(name="ba_xsii_td4", kind=DataKind.FLOAT, desc="薛斯通道II-CLOSE,HIGH,LOW,N=102,M=7"),
    ]
    _OUT_NA_COLS = [
        ColumnInfo(name="open", kind=DataKind.FLOAT, desc="开盘价"),
        ColumnInfo(name="high", kind=DataKind.FLOAT, desc="最高价"),
        ColumnInfo(name="low", kind=DataKind.FLOAT, desc="最低价"),
        ColumnInfo(name="close", kind=DataKind.FLOAT, desc="收盘价"),
        ColumnInfo(name="asi", kind=DataKind.FLOAT, desc="振动升降指标-OPEN,CLOSE,HIGH,LOW,M1=26,M2=10"),
        ColumnInfo(name="asit", kind=DataKind.FLOAT, desc="振动升降指标-OPEN,CLOSE,HIGH,LOW,M1=26,M2=10"),
        ColumnInfo(name="atr", kind=DataKind.FLOAT, desc="真实波动N日平均值-CLOSE,HIGH,LOW,N=20"),
        ColumnInfo(name="bbi", kind=DataKind.FLOAT, desc="BBI多空指标-CLOSE,M1=3,M2=6,M3=12,M4=20"),
        ColumnInfo(name="bias1", kind=DataKind.FLOAT, desc="BIAS乖离率-CLOSE,L1=6,L2=12,L3=24"),
        ColumnInfo(name="bias2", kind=DataKind.FLOAT, desc="BIAS乖离率-CLOSE,L1=6,L2=12,L3=24"),
        ColumnInfo(name="bias3", kind=DataKind.FLOAT, desc="BIAS乖离率-CLOSE,L1=6,L2=12,L3=24"),
        ColumnInfo(name="boll_lower", kind=DataKind.FLOAT, desc="BOLL指标,布林带-CLOSE,N=20,P=2"),
        ColumnInfo(name="boll_mid", kind=DataKind.FLOAT, desc="BOLL指标,布林带-CLOSE,N=20,P=2"),
        ColumnInfo(name="boll_upper", kind=DataKind.FLOAT, desc="BOLL指标,布林带-CLOSE,N=20,P=2"),
        ColumnInfo(name="brar_ar", kind=DataKind.FLOAT, desc="BRAR情绪指标-OPEN,CLOSE,HIGH,LOW,M1=26"),
        ColumnInfo(name="brar_br", kind=DataKind.FLOAT, desc="BRAR情绪指标-OPEN,CLOSE,HIGH,LOW,M1=26"),
        ColumnInfo(name="cci", kind=DataKind.FLOAT, desc="顺势指标又叫CCI指标-CLOSE,HIGH,LOW,N=14"),
        ColumnInfo(name="cr", kind=DataKind.FLOAT, desc="CR价格动量指标-CLOSE,HIGH,LOW,N=20"),
        ColumnInfo(name="dfma_dif", kind=DataKind.FLOAT, desc="平行线差指标-CLOSE,N1=10,N2=50,M=10"),
        ColumnInfo(name="dfma_difma", kind=DataKind.FLOAT, desc="平行线差指标-CLOSE,N1=10,N2=50,M=10"),
        ColumnInfo(name="dmi_adx", kind=DataKind.FLOAT, desc="动向指标-CLOSE,HIGH,LOW,M1=14,M2=6"),
        ColumnInfo(name="dmi_adxr", kind=DataKind.FLOAT, desc="动向指标-CLOSE,HIGH,LOW,M1=14,M2=6"),
        ColumnInfo(name="dmi_mdi", kind=DataKind.FLOAT, desc="动向指标-CLOSE,HIGH,LOW,M1=14,M2=6"),
        ColumnInfo(name="dmi_pdi", kind=DataKind.FLOAT, desc="动向指标-CLOSE,HIGH,LOW,M1=14,M2=6"),
        ColumnInfo(name="dpo", kind=DataKind.FLOAT, desc="区间震荡线-CLOSE,M1=20,M2=10,M3=6"),
        ColumnInfo(name="madpo", kind=DataKind.FLOAT, desc="区间震荡线-CLOSE,M1=20,M2=10,M3=6"),
        ColumnInfo(name="ema_10", kind=DataKind.FLOAT, desc="指数移动平均-N=10"),
        ColumnInfo(name="ema_20", kind=DataKind.FLOAT, desc="指数移动平均-N=20"),
        ColumnInfo(name="ema_250", kind=DataKind.FLOAT, desc="指数移动平均-N=250"),
        ColumnInfo(name="ema_30", kind=DataKind.FLOAT, desc="指数移动平均-N=30"),
        ColumnInfo(name="ema_5", kind=DataKind.FLOAT, desc="指数移动平均-N=5"),
        ColumnInfo(name="ema_60", kind=DataKind.FLOAT, desc="指数移动平均-N=60"),
        ColumnInfo(name="ema_90", kind=DataKind.FLOAT, desc="指数移动平均-N=90"),
        ColumnInfo(name="emv", kind=DataKind.FLOAT, desc="简易波动指标-HIGH,LOW,VOL,N=14,M=9"),
        ColumnInfo(name="maemv", kind=DataKind.FLOAT, desc="简易波动指标-HIGH,LOW,VOL,N=14,M=9"),
        ColumnInfo(name="expma_12", kind=DataKind.FLOAT, desc="EMA指数平均数指标-CLOSE,N1=12,N2=50"),
        ColumnInfo(name="expma_50", kind=DataKind.FLOAT, desc="EMA指数平均数指标-CLOSE,N1=12,N2=50"),
        ColumnInfo(name="kdj", kind=DataKind.FLOAT, desc="KDJ指标-CLOSE,HIGH,LOW,N=9,M1=3,M2=3"),
        ColumnInfo(name="kdj_d", kind=DataKind.FLOAT, desc="KDJ指标-CLOSE,HIGH,LOW,N=9,M1=3,M2=3"),
        ColumnInfo(name="kdj_k", kind=DataKind.FLOAT, desc="KDJ指标-CLOSE,HIGH,LOW,N=9,M1=3,M2=3"),
        ColumnInfo(name="ktn_down", kind=DataKind.FLOAT, desc="肯特纳通道N=20日"),
        ColumnInfo(name="ktn_mid", kind=DataKind.FLOAT, desc="肯特纳通道N=20日"),
        ColumnInfo(name="ktn_upper", kind=DataKind.FLOAT, desc="肯特纳通道N=20日"),
        ColumnInfo(name="ma_10", kind=DataKind.FLOAT, desc="简单移动平均-N=10"),
        ColumnInfo(name="ma_20", kind=DataKind.FLOAT, desc="简单移动平均-N=20"),
        ColumnInfo(name="ma_250", kind=DataKind.FLOAT, desc="简单移动平均-N=250"),
        ColumnInfo(name="ma_30", kind=DataKind.FLOAT, desc="简单移动平均-N=30"),
        ColumnInfo(name="ma_5", kind=DataKind.FLOAT, desc="简单移动平均-N=5"),
        ColumnInfo(name="ma_60", kind=DataKind.FLOAT, desc="简单移动平均-N=60"),
        ColumnInfo(name="ma_90", kind=DataKind.FLOAT, desc="简单移动平均-N=90"),
        ColumnInfo(name="macd", kind=DataKind.FLOAT, desc="MACD指标-CLOSE,SHORT=12,LONG=26,M=9"),
        ColumnInfo(name="macd_dea", kind=DataKind.FLOAT, desc="MACD指标-CLOSE,SHORT=12,LONG=26,M=9"),
        ColumnInfo(name="macd_dif", kind=DataKind.FLOAT, desc="MACD指标-CLOSE,SHORT=12,LONG=26,M=9"),
        ColumnInfo(name="mass", kind=DataKind.FLOAT, desc="梅斯线-HIGH,LOW,N1=9,N2=25,M=6"),
        ColumnInfo(name="ma_mass", kind=DataKind.FLOAT, desc="梅斯线-HIGH,LOW,N1=9,N2=25,M=6"),
        ColumnInfo(name="mfi", kind=DataKind.FLOAT, desc="MFI指标是成交量的RSI指标-CLOSE,HIGH,LOW,VOL,N=14"),
        ColumnInfo(name="mtm", kind=DataKind.FLOAT, desc="动量指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="mtmma", kind=DataKind.FLOAT, desc="动量指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="obv", kind=DataKind.FLOAT, desc="能量潮指标-CLOSE,VOL"),
        ColumnInfo(name="psy", kind=DataKind.FLOAT, desc="投资者对股市涨跌心理波动情绪指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="psyma", kind=DataKind.FLOAT, desc="投资者对股市涨跌心理波动情绪指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="roc", kind=DataKind.FLOAT, desc="变动率指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="maroc", kind=DataKind.FLOAT, desc="变动率指标-CLOSE,N=12,M=6"),
        ColumnInfo(name="rsi_12", kind=DataKind.FLOAT, desc="RSI指标-CLOSE,N=12"),
        ColumnInfo(name="rsi_24", kind=DataKind.FLOAT, desc="RSI指标-CLOSE,N=24"),
        ColumnInfo(name="rsi_6", kind=DataKind.FLOAT, desc="RSI指标-CLOSE,N=6"),
        ColumnInfo(name="taq_down", kind=DataKind.FLOAT, desc="唐安奇通道(海龟)交易指标-HIGH,LOW,20"),
        ColumnInfo(name="taq_mid", kind=DataKind.FLOAT, desc="唐安奇通道(海龟)交易指标-HIGH,LOW,20"),
        ColumnInfo(name="taq_up", kind=DataKind.FLOAT, desc="唐安奇通道(海龟)交易指标-HIGH,LOW,20"),
        ColumnInfo(name="trix", kind=DataKind.FLOAT, desc="三重指数平滑平均线-CLOSE,M1=12,M2=20"),
        ColumnInfo(name="trma", kind=DataKind.FLOAT, desc="三重指数平滑平均线-CLOSE,M1=12,M2=20"),
        ColumnInfo(name="vr", kind=DataKind.FLOAT, desc="VR容量比率-CLOSE,VOL,M1=26"),
        ColumnInfo(name="wr", kind=DataKind.FLOAT, desc="W&R 威廉指标-CLOSE,HIGH,LOW,N=10,N1=6"),
        ColumnInfo(name="wr1", kind=DataKind.FLOAT, desc="W&R 威廉指标-CLOSE,HIGH,LOW,N=10,N1=6"),
        ColumnInfo(name="xsii_td1", kind=DataKind.FLOAT, desc="薛斯通道II-CLOSE,HIGH,LOW,N=102,M=7"),
        ColumnInfo(name="xsii_td2", kind=DataKind.FLOAT, desc="薛斯通道II-CLOSE,HIGH,LOW,N=102,M=7"),
        ColumnInfo(name="xsii_td3", kind=DataKind.FLOAT, desc="薛斯通道II-CLOSE,HIGH,LOW,N=102,M=7"),
        ColumnInfo(name="xsii_td4", kind=DataKind.FLOAT, desc="薛斯通道II-CLOSE,HIGH,LOW,N=102,M=7"),
    ]
    _OUT_MAIN_COLS = [
        ColumnInfo(name="code", kind=DataKind.STRING, desc="股票代码"),
        ColumnInfo(name="date", kind=DataKind.STRING, desc="交易日期"),
        ColumnInfo(name="datecode", kind=DataKind.STRING, desc="交易日期代码(YYYYMMDD)"),
        ColumnInfo(name="change", kind=DataKind.FLOAT, desc="涨跌额"),
        ColumnInfo(name="percent_change", kind=DataKind.FLOAT, desc="涨跌幅(未复权,如果是复权请用 通用行情接口)"),
        ColumnInfo(name="volume", kind=DataKind.FLOAT, desc="成交量(手)"),
        ColumnInfo(name="amount", kind=DataKind.FLOAT, desc="成交额(千元)"),
        ColumnInfo(name="turnover_rate", kind=DataKind.FLOAT, desc="换手率(%)"),
        ColumnInfo(name="turnover_rate_f", kind=DataKind.FLOAT, desc="换手率(自由流通股)"),
        ColumnInfo(name="volume_ratio", kind=DataKind.FLOAT, desc="量比"),
        ColumnInfo(name="pe", kind=DataKind.FLOAT, desc="市盈率(总市值/净利润,亏损的PE为空)"),
        ColumnInfo(name="pe_ttm", kind=DataKind.FLOAT, desc="市盈率(TTM,亏损的PE为空)"),
        ColumnInfo(name="pb", kind=DataKind.FLOAT, desc="市净率(总市值/净资产)"),
        ColumnInfo(name="ps", kind=DataKind.FLOAT, desc="市销率"),
        ColumnInfo(name="ps_ttm", kind=DataKind.FLOAT, desc="市销率(TTM)"),
        ColumnInfo(name="dv_ratio", kind=DataKind.FLOAT, desc="股息率(%)"),
        ColumnInfo(name="dv_ttm", kind=DataKind.FLOAT, desc="股息率(TTM)(%)"),
        ColumnInfo(name="total_share", kind=DataKind.FLOAT, desc="总股本(万股)"),
        ColumnInfo(name="float_share", kind=DataKind.FLOAT, desc="流通股本(万股)"),
        ColumnInfo(name="free_share", kind=DataKind.FLOAT, desc="自由流通股本(万)"),
        ColumnInfo(name="total_mv", kind=DataKind.FLOAT, desc="总市值(万元)"),
        ColumnInfo(name="circle_mv", kind=DataKind.FLOAT, desc="流通市值(万元)"),
        ColumnInfo(name="adj_factor", kind=DataKind.FLOAT, desc="复权因子"),
        ColumnInfo(name="downdays", kind=DataKind.FLOAT, desc="连跌天数"),
        ColumnInfo(name="updays", kind=DataKind.FLOAT, desc="连涨天数"),
        ColumnInfo(name="lowdays", kind=DataKind.FLOAT, desc="表示当前最低价是近多少周期内最低价的最小值"),
        ColumnInfo(name="topdays", kind=DataKind.FLOAT, desc="表示当前最高价是近多少周期内最高价的最大值"),
    ]
    _OUT = TableInfo(
        desc="A股日线通用数据模型",
        meta={"source": "tushare"},
        columns=_OUT_MAIN_COLS + _OUT_NA_COLS + _OUT_BA_COLS + _OUT_FA_COLS,
    )

    def __init__(
        self,
        session: Session,
        conf: Optional[Conf | Dict[str, Any]] = None,
        retry: Optional[Retry] = None,
    ) -> None:
        super().__init__(
            session=session,
            conf=self._resolve_conf(conf),
            source=Source(
                name="stk_factor_pro",
                url="https://tushare.pro/document/2?doc_id=328",
                args=self._ARGS,
                tableinfo=self._IN,
            ),
            output=Output(
                name="daycdm",
                tableinfo=self._OUT,
            ),
            retry=retry,
            tags={
                "name": "daycdm",
                "module": "stock",
                "level": "market",
                "frequency": "interday",
                "scope": "stk_factor_pro",
            },
        )

    @classmethod
    def _resolve_conf(
        cls,
        conf: Optional[Conf | Dict[str, Any]] = None,
    ) -> Conf:
        if conf is None:
            obj = Conf(size=cls._SIZE, coolant=cls._FREQ)
        else:
            obj = Conf.from_dict(conf)

        params = obj.get_params() or {}

        if "trade_date" in params:
            trade_date = params.get("trade_date")
            if isinstance(trade_date, datetime):
                params["trade_date"] = trade_date.strftime("%Y%m%d")

        if "start_date" in params and "end_date" in params:
            start_date = params["start_date"]
            end_date = params["end_date"]
            if isinstance(start_date, datetime):
                params["start_date"] = start_date.strftime("%Y%m%d")
            if isinstance(end_date, datetime):
                params["end_date"] = end_date.strftime("%Y%m%d")

        obj.set_params(params)

        if obj.size > cls._SIZE:
            obj.set_size(cls._SIZE)

        if obj.coolant < cls._FREQ:
            obj.coolant = cls._FREQ

        return obj

    def _run(self) -> object:
        params = dict(self.conf.get_params() or {})
        df = self._fetchall(
            api=self.connection.stk_factor_pro,
            **params,
        )
        df = self.transform(df)
        if self.conf.use_cache:
            self.cache.set("_run", df)
        return df

    def _transform_main(self, data: pd.DataFrame) -> pd.DataFrame:
        transformed = {}
        transformed["code"] = data["ts_code"].astype(str)
        transformed["date"] = pd.to_datetime(
            data["trade_date"],
            format="%Y%m%d",
            errors="coerce",
        )
        transformed["datecode"] = transformed["date"].dt.strftime("%Y%m%d")
        transformed["change"] = pd.to_numeric(data["change"], errors="coerce")
        transformed["percent_change"] = pd.to_numeric(data["pct_chg"], errors="coerce")
        transformed["volume"] = pd.to_numeric(data["vol"], errors="coerce")
        transformed["amount"] = pd.to_numeric(data["amount"], errors="coerce")
        transformed["turnover_rate"] = pd.to_numeric(data["turnover_rate"], errors="coerce")
        transformed["turnover_rate_f"] = pd.to_numeric(data["turnover_rate_f"], errors="coerce")
        transformed["volume_ratio"] = pd.to_numeric(data["volume_ratio"], errors="coerce")
        transformed["pe"] = pd.to_numeric(data["pe"], errors="coerce")
        transformed["pe_ttm"] = pd.to_numeric(data["pe_ttm"], errors="coerce")
        transformed["pb"] = pd.to_numeric(data["pb"], errors="coerce")
        transformed["ps"] = pd.to_numeric(data["ps"], errors="coerce")
        transformed["ps_ttm"] = pd.to_numeric(data["ps_ttm"], errors="coerce")
        transformed["dv_ratio"] = pd.to_numeric(data["dv_ratio"], errors="coerce")
        transformed["dv_ttm"] = pd.to_numeric(data["dv_ttm"], errors="coerce")
        transformed["total_share"] = pd.to_numeric(data["total_share"], errors="coerce")
        transformed["float_share"] = pd.to_numeric(data["float_share"], errors="coerce")
        transformed["free_share"] = pd.to_numeric(data["free_share"], errors="coerce")
        transformed["total_mv"] = pd.to_numeric(data["total_mv"], errors="coerce")
        transformed["circle_mv"] = pd.to_numeric(data["circ_mv"], errors="coerce")
        transformed["adj_factor"] = pd.to_numeric(data["adj_factor"], errors="coerce")
        transformed["downdays"] = pd.to_numeric(data["downdays"], errors="coerce")
        transformed["updays"] = pd.to_numeric(data["updays"], errors="coerce")
        transformed["lowdays"] = pd.to_numeric(data["lowdays"], errors="coerce")
        transformed["topdays"] = pd.to_numeric(data["topdays"], errors="coerce")
        return pd.DataFrame(transformed)

    def _transform_na(self, data: pd.DataFrame) -> pd.DataFrame:
        transformed = {}
        for col in self._IN_BFQ_COLS:
            src = col.name
            dst = src.replace("_bfq", "")
            if src in data.columns:
                transformed[dst] = pd.to_numeric(data[src], errors="coerce")
            else:
                transformed[dst] = pd.NA
        return pd.DataFrame(transformed)

    def _transform_ba(self, data: pd.DataFrame) -> pd.DataFrame:
        transformed = {}
        for col in self._IN_HFQ_COLS:
            src = col.name
            base = src.replace("_hfq", "")
            dst = f"ba_{base}"
            if src in data.columns:
                transformed[dst] = pd.to_numeric(data[src], errors="coerce")
            else:
                transformed[dst] = pd.NA
        return pd.DataFrame(transformed)

    def _transform_fa(self, data: pd.DataFrame) -> pd.DataFrame:
        transformed = {}
        for col in self._IN_QFQ_COLS:
            src = col.name
            base = src.replace("_qfq", "")
            dst = f"fa_{base}"
            if src in data.columns:
                transformed[dst] = pd.to_numeric(data[src], errors="coerce")
            else:
                transformed[dst] = pd.NA
        return pd.DataFrame(transformed)

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        cols = self.output.list_column_names()
        if data is None or data.empty:
            return pd.DataFrame(columns=cols)

        main_df = self._transform_main(data).reset_index(drop=True)
        na_df = self._transform_na(data).reset_index(drop=True)
        ba_df = self._transform_ba(data).reset_index(drop=True)
        fa_df = self._transform_fa(data).reset_index(drop=True)
        transformed = pd.concat([main_df, na_df, ba_df, fa_df], axis=1)
        return transformed[cols].reset_index(drop=True)

    def get_main_only(
        self,
        data: pd.DataFrame | None = None,
    ) -> pd.DataFrame:
        if data is not None:
            df = data
        elif "_run" in self.cache:
            df = self.cache.get("_run")
        else:
            df = self.run()
        maincols = [col.name for col in self._OUT_MAIN_COLS]
        if df.empty:
            return pd.DataFrame(columns=maincols)
        else:
            return df[maincols]

    def get_fa_only(
        self,
        data: pd.DataFrame | None = None,
    ) -> pd.DataFrame:
        if data is not None:
            df = data
        elif "_run" in self.cache:
            df = self.cache.get("_run")
        else:
            df = self.run()
        maincols = [col.name for col in self._OUT_MAIN_COLS]
        facols = [col.name for col in self._OUT_FA_COLS]
        if df.empty:
            return pd.DataFrame(columns=maincols + facols)
        else:
            return df[maincols + facols]

    def get_ba_only(
        self,
        data: pd.DataFrame | None = None,
    ) -> pd.DataFrame:
        if data is not None:
            df = data
        elif "_run" in self.cache:
            df = self.cache.get("_run")
        else:
            df = self.run()
        maincols = [col.name for col in self._OUT_MAIN_COLS]
        bacols = [col.name for col in self._OUT_BA_COLS]
        if df.empty:
            return pd.DataFrame(columns=maincols + bacols)
        else:
            return df[maincols + bacols]

    def get_na_only(
        self,
        data: pd.DataFrame | None = None,
    ) -> pd.DataFrame:
        if data is not None:
            df = data
        elif "_run" in self.cache:
            df = self.cache.get("_run")
        else:
            df = self.run()
        maincols = [col.name for col in self._OUT_MAIN_COLS]
        nacols = [col.name for col in self._OUT_NA_COLS]

        if df.empty:
            return pd.DataFrame(columns=maincols + nacols)
        else:
            return df[maincols + nacols]

    def describe_fa(self) -> TableInfo:
        result = super().describe()
        result["output"] = TableInfo(
            desc="A股日线通用数据模型", meta={"source": "tushare"}, columns=self._OUT_MAIN_COLS + self._OUT_FA_COLS
        ).describe()
        return result

    def describe_ba(self) -> TableInfo:
        result = super().describe()
        result["output"] = TableInfo(
            desc="A股日线通用数据模型", meta={"source": "tushare"}, columns=self._OUT_MAIN_COLS + self._OUT_BA_COLS
        ).describe()
        return result

    def describe_na(self) -> TableInfo:
        result = super().describe()
        result["output"] = TableInfo(
            desc="A股日线通用数据模型", meta={"source": "tushare"}, columns=self._OUT_MAIN_COLS + self._OUT_NA_COLS
        ).describe()
        return result
