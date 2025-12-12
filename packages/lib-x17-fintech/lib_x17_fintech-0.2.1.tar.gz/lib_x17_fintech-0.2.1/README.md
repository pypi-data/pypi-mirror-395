# lib-x17-fintech

专业的 Tushare 金融数据接口封装库，提供标准化的 A 股市场数据获取能力。

## 概述

lib-x17-fintech 是基于 Tushare Pro API 的数据接口库，通过统一的 Job 模式提供便捷的金融数据访问。所有数据接口都遵循相同的调用模式，支持灵活的参数配置、自动重试和结果缓存。

## 核心特性

- 统一的 Job 接口模式，所有数据源调用方式一致
- 自动数据清洗和标准化输出
- 智能缓存机制，避免重复请求
- 支持批量数据获取和分页处理
- 完整的错误处理和重试策略
- 数据结果包含完整的元数据信息

## 数据接口分类

### 基础数据 (basic)
股票列表、上市公司信息、IPO数据、交易日历等基础静态数据。

### 行情数据 (market)
日线、周线、月线行情，复权因子，基本面指标，技术指标等动态数据。

## 安装

```bash
pip install lib-x17-fintech
```

要求 Python >= 3.11

## 快速开始

所有数据接口的使用方式完全一致，只需三步：

```python
from xfintech.data.tushare.session.session import Session
from xfintech.data.tushare.base.conf import Conf
from xfintech.data.tushare.stock.market.dayline import Dayline

# 步骤1: 创建会话（使用你的 Tushare Token）
session = Session(credential="your_tushare_token")

# 步骤2: 配置参数并创建 Job
job = Dayline(
    session=session,
    conf=Conf(
        params={
            "ts_code": "000001.SZ",
            "start_date": "20241101",
            "end_date": "20241130"
        }
    )
)

# 步骤3: 执行并获取数据
result = job.run()
print(result.head())

# 清理缓存（可选）
job.clean()
```

## 数据接口目录

### 一、基础数据接口

所有基础数据接口位于 `xfintech.data.tushare.stock.basic`

#### 1. Stock - 股票列表

获取沪深 A 股、科创板、创业板全部股票基础信息。

**接口**: `xfintech.data.tushare.stock.basic.stock.Stock`

**参数**: 
- `ts_code` (可选): 股票代码
- `list_status` (可选): 上市状态 L上市 D退市 P暂停上市

**示例**:
```python
from xfintech.data.tushare.stock.basic.stock import Stock

# 获取所有上市股票
job = Stock(session=session)
result = job.run()

# 获取特定股票
job = Stock(
    session=session,
    conf=Conf(params={"ts_code": "000001.SZ"})
)
result = job.run()
```

**输出字段**: 股票代码、股票名称、上市日期、退市日期、市场、行业等

---

#### 2. Company - 上市公司信息

获取上市公司基本信息，包括注册资本、成立日期、主营业务等。

**接口**: `xfintech.data.tushare.stock.basic.company.Company`

**参数**:
- `ts_code` (可选): 股票代码
- `exchange` (可选): 交易所 SSE上交所 SZSE深交所

**示例**:
```python
from xfintech.data.tushare.stock.basic.company import Company

job = Company(
    session=session,
    conf=Conf(params={"ts_code": "000001.SZ"})
)
result = job.run()
```

**输出字段**: 公司名称、注册资本、成立日期、主营业务、办公地址、网站等

---

#### 3. Ipo - IPO 新股上市

获取 IPO 新股上市信息，包括发行价格、募集资金等。

**接口**: `xfintech.data.tushare.stock.basic.ipo.Ipo`

**参数**:
- `ts_code` (可选): 股票代码
- `start_date` (可选): 上市开始日期
- `end_date` (可选): 上市结束日期

**示例**:
```python
from xfintech.data.tushare.stock.basic.ipo import Ipo

job = Ipo(
    session=session,
    conf=Conf(params={
        "start_date": "20241101",
        "end_date": "20241130"
    })
)
result = job.run()
```

**输出字段**: 上市日期、发行价格、发行数量、募集资金、市盈率等

---

#### 4. St - ST 股票

获取特别处理股票列表。

**接口**: `xfintech.data.tushare.stock.basic.st.St`

**参数**: 无必需参数

**示例**:
```python
from xfintech.data.tushare.stock.basic.st import St

job = St(session=session)
result = job.run()
```

**输出字段**: 股票代码、ST 类型、开始日期、结束日期等

---

#### 5. TradeDate - 交易日历

获取交易所交易日历，包括是否开市信息。

**接口**: `xfintech.data.tushare.stock.basic.tradedate.TradeDate`

**参数**:
- `exchange` (可选): 交易所 SSE上交所 SZSE深交所
- `start_date` (可选): 开始日期
- `end_date` (可选): 结束日期
- `is_open` (可选): 是否交易 0否 1是

**示例**:
```python
from xfintech.data.tushare.stock.basic.tradedate import TradeDate

job = TradeDate(
    session=session,
    conf=Conf(params={
        "exchange": "SSE",
        "start_date": "20241101",
        "end_date": "20241231",
        "is_open": "1"
    })
)
result = job.run()
```

**输出字段**: 交易所、日期、是否开市

---

### 二、行情数据接口

所有行情数据接口位于 `xfintech.data.tushare.stock.market`

#### 1. Dayline - 日线行情

获取 A 股日线行情数据（未复权），包括开高低收、成交量、成交额。

**接口**: `xfintech.data.tushare.stock.market.dayline.Dayline`

**参数**:
- `ts_code` (可选): 股票代码，支持多个股票（逗号分隔）
- `trade_date` (可选): 交易日期
- `start_date` (可选): 开始日期
- `end_date` (可选): 结束日期

**积分要求**: 基础积分，每分钟 500 次，单次最多 6000 条

**示例**:
```python
from xfintech.data.tushare.stock.market.dayline import Dayline

# 获取单只股票历史数据
job = Dayline(
    session=session,
    conf=Conf(
        params={
            "ts_code": "000001.SZ",
            "start_date": "20241101",
            "end_date": "20241130"
        },
        size=6000
    )
)
result = job.run()

# 获取多只股票对比数据
job = Dayline(
    session=session,
    conf=Conf(
        params={
            "ts_code": "000001.SZ,000002.SZ,600000.SH",
            "start_date": "20241101",
            "end_date": "20241130"
        }
    )
)
result = job.run()

# 获取某交易日全市场数据
job = Dayline(
    session=session,
    conf=Conf(
        params={"trade_date": "20241130"},
        size=6000
    )
)
result = job.run()
```

**输出字段**: 股票代码、交易日期、开盘价、最高价、最低价、收盘价、昨收价、涨跌额、涨跌幅、成交量、成交额

---

#### 2. Weekline - 周线行情

获取 A 股周线行情数据。

**接口**: `xfintech.data.tushare.stock.market.weekline.Weekline`

**参数**:
- `ts_code` (可选): 股票代码
- `trade_date` (可选): 交易日期
- `start_date` (可选): 开始日期
- `end_date` (可选): 结束日期

**示例**:
```python
from xfintech.data.tushare.stock.market.weekline import Weekline

job = Weekline(
    session=session,
    conf=Conf(params={"ts_code": "000001.SZ"})
)
result = job.run()
```

**输出字段**: 同日线，按周汇总

---

#### 3. Monthline - 月线行情

获取 A 股月线行情数据。

**接口**: `xfintech.data.tushare.stock.market.monthline.Monthline`

**参数**:
- `ts_code` (可选): 股票代码
- `trade_date` (可选): 交易日期
- `start_date` (可选): 开始日期
- `end_date` (可选): 结束日期

**示例**:
```python
from xfintech.data.tushare.stock.market.monthline import Monthline

job = Monthline(
    session=session,
    conf=Conf(params={
        "ts_code": "000001.SZ",
        "start_date": "20240101",
        "end_date": "20241231"
    })
)
result = job.run()
```

**输出字段**: 同日线，按月汇总

---

#### 4. AdjFactor - 复权因子

获取 A 股复权因子数据，用于计算前复权和后复权价格。

**接口**: `xfintech.data.tushare.stock.market.adjfactor.AdjFactor`

**参数**:
- `ts_code` (可选): 股票代码
- `trade_date` (可选): 交易日期
- `start_date` (可选): 开始日期
- `end_date` (可选): 结束日期

**积分要求**: 2000 积分起，单次最多 2000 条

**示例**:
```python
from xfintech.data.tushare.stock.market.adjfactor import AdjFactor

# 获取某交易日全市场复权因子
job = AdjFactor(
    session=session,
    conf=Conf(
        params={"trade_date": "20241130"},
        size=2000
    )
)
result = job.run()

# 获取单只股票全部复权因子
job = AdjFactor(
    session=session,
    conf=Conf(params={"ts_code": "000001.SZ"})
)
result = job.run()
```

**输出字段**: 股票代码、交易日期、复权因子

---

#### 5. CoreFactor - 每日指标

获取 A 股每日基本面指标数据，包括换手率、市盈率、市净率、市值等。

**接口**: `xfintech.data.tushare.stock.market.corefactor.CoreFactor`

**参数**:
- `ts_code` (可选): 股票代码
- `trade_date` (可选): 交易日期
- `start_date` (可选): 开始日期
- `end_date` (可选): 结束日期

**积分要求**: 2000 积分起，单次最多 6000 条

**示例**:
```python
from xfintech.data.tushare.stock.market.corefactor import CoreFactor

# 获取某交易日全市场基本面数据
job = CoreFactor(
    session=session,
    conf=Conf(
        params={"trade_date": "20241130"},
        size=6000
    )
)
result = job.run()

# 获取单只股票历史基本面
job = CoreFactor(
    session=session,
    conf=Conf(params={
        "ts_code": "000001.SZ",
        "start_date": "20241101",
        "end_date": "20241130"
    })
)
result = job.run()
```

**输出字段**: 收盘价、换手率、量比、市盈率、市净率、市销率、股息率、总股本、流通股本、总市值、流通市值

---

#### 6. Daylimit - 涨跌停价格

获取全市场（A/B股和基金）每日涨跌停价格。

**接口**: `xfintech.data.tushare.stock.market.daylimit.Daylimit`

**参数**:
- `ts_code` (可选): 股票代码
- `trade_date` (可选): 交易日期
- `start_date` (可选): 开始日期
- `end_date` (可选): 结束日期

**积分要求**: 2000 积分，单次最多 5800 条

**示例**:
```python
from xfintech.data.tushare.stock.market.daylimit import Daylimit

# 获取某交易日全市场涨跌停价格
job = Daylimit(
    session=session,
    conf=Conf(
        params={"trade_date": "20241130"},
        size=5800
    )
)
result = job.run()

# 获取单只股票涨跌停历史
job = Daylimit(
    session=session,
    conf=Conf(params={
        "ts_code": "000001.SZ",
        "start_date": "20241101",
        "end_date": "20241130"
    })
)
result = job.run()
```

**输出字段**: 股票代码、交易日期、昨日收盘价、涨停价、跌停价

---

#### 7. Daycdm - 技术面因子

获取股票每日技术面因子数据，包含大量技术指标（MA、EMA、MACD、KDJ、BOLL 等）。

**接口**: `xfintech.data.tushare.stock.market.daycdm.Daycdm`

**参数**:
- `ts_code` (可选): 股票代码，支持多个股票（逗号分隔）
- `trade_date` (可选): 交易日期
- `start_date` (可选): 开始日期
- `end_date` (可选): 结束日期

**积分要求**: 5000 积分以上，单次最多 10000 条

**示例**:
```python
from xfintech.data.tushare.stock.market.daycdm import Daycdm

job = Daycdm(
    session=session,
    conf=Conf(
        params={
            "ts_code": "000001.SZ,600000.SH",
            "start_date": "20241101",
            "end_date": "20241130"
        },
        size=5000,
        coolant=2  # 技术指标数据量大，建议增加请求间隔
    )
)
result = job.run()
```

**输出字段**: 基础行情字段 + 80+ 技术指标（包含前复权、后复权、不复权三组指标）

**技术指标包括**:
- 趋势指标: MA、EMA、BOLL、KTN 等
- 动量指标: MACD、KDJ、RSI、CCI 等
- 成交量指标: OBV、MFI、EMV 等
- 其他指标: ATR、BIAS、BRAR、CR、DMI、DPO、MTM、PSY、ROC、TRIX、VR、WR 等

---

## Job 通用方法

所有数据接口（Job）都提供以下通用方法：

### run()
执行数据获取任务，返回 pandas DataFrame。

```python
result = job.run()
```

### clean()
清理缓存数据。

```python
job.clean()
```

### describe()
获取 Job 的详细描述信息，包括数据源、参数、输出格式等。

```python
info = job.describe()
```

### list_codes()
列出结果中包含的所有股票代码（仅行情类接口支持）。

```python
codes = job.list_codes()
```

### list_dates()
列出结果中包含的所有交易日期（仅行情类接口支持）。

```python
dates = job.list_dates()
```

---

## 配置参数说明

### Conf 配置对象

所有可选配置参数：

```python
from xfintech.data.tushare.base.conf import Conf

conf = Conf(
    params={},      # 请求参数字典，根据不同接口传入不同参数
    limit=10000,    # 最大迭代次数，防止无限循环
    size=5000,      # 单次提取数据量，不同接口有不同上限
    coolant=0.1     # 请求间隔时间（秒），根据积分等级调整
)
```

**参数说明**:
- `params`: 接口特定参数，如 ts_code、trade_date、start_date、end_date 等
- `limit`: 循环获取数据的最大次数，默认 10000
- `size`: 单次请求返回的最大记录数，需根据接口限制设置
- `coolant`: 两次请求之间的间隔时间，积分越高可设置越小

### 日期格式

所有日期参数统一使用字符串格式 `YYYYMMDD`：

```python
params = {
    "trade_date": "20241130",      # 单个交易日
    "start_date": "20241101",      # 开始日期
    "end_date": "20241130"         # 结束日期
}
```

也支持 datetime 对象，会自动转换：

```python
from datetime import datetime

params = {
    "trade_date": datetime(2024, 11, 30),
    "start_date": datetime(2024, 11, 1),
    "end_date": datetime(2024, 11, 30)
}
```

---

## 使用技巧

### 1. 批量获取多只股票数据

```python
# 方法一：使用逗号分隔的股票代码
job = Dayline(
    session=session,
    conf=Conf(params={
        "ts_code": "000001.SZ,000002.SZ,600000.SH",
        "start_date": "20241101",
        "end_date": "20241130"
    })
)
result = job.run()

# 方法二：循环获取后合并
codes = ["000001.SZ", "000002.SZ", "600000.SH"]
results = []
for code in codes:
    job = Dayline(
        session=session,
        conf=Conf(params={
            "ts_code": code,
            "start_date": "20241101",
            "end_date": "20241130"
        })
    )
    results.append(job.run())
    job.clean()

import pandas as pd
result = pd.concat(results, ignore_index=True)
```

### 2. 获取全市场数据

使用 `trade_date` 参数获取某个交易日的全市场数据：

```python
job = Dayline(
    session=session,
    conf=Conf(
        params={"trade_date": "20241130"},
        size=6000  # 设置较大的 size 以减少请求次数
    )
)
result = job.run()
```

### 3. 大数据量获取

对于跨度较长的历史数据，建议分段获取：

```python
from datetime import datetime, timedelta

def get_history_data(code, start, end, days_per_batch=30):
    results = []
    current = datetime.strptime(start, "%Y%m%d")
    end_date = datetime.strptime(end, "%Y%m%d")
    
    while current <= end_date:
        batch_end = min(current + timedelta(days=days_per_batch), end_date)
        
        job = Dayline(
            session=session,
            conf=Conf(params={
                "ts_code": code,
                "start_date": current.strftime("%Y%m%d"),
                "end_date": batch_end.strftime("%Y%m%d")
            })
        )
        results.append(job.run())
        job.clean()
        
        current = batch_end + timedelta(days=1)
    
    return pd.concat(results, ignore_index=True)

# 获取一年的数据
result = get_history_data("000001.SZ", "20240101", "20241231")
```

### 4. 控制请求频率

根据 Tushare 积分等级调整 coolant 参数：

```python
# 基础积分（120 以下）：建议 coolant >= 0.5
conf = Conf(params={...}, coolant=0.5)

# 2000 积分：建议 coolant >= 0.1
conf = Conf(params={...}, coolant=0.1)

# 5000 积分及以上：可以设置更小的值
conf = Conf(params={...}, coolant=0.05)
```

### 5. 处理返回结果

所有接口返回标准的 pandas DataFrame：

```python
result = job.run()

# 查看前几行
print(result.head())

# 查看数据信息
print(result.info())

# 统计信息
print(result.describe())

# 保存为 CSV
result.to_csv("output.csv", index=False)

# 保存为 Parquet（推荐，更高效）
result.to_parquet("output.parquet", index=False)
```

---

## 完整示例

项目 `example/` 目录提供了所有接口的完整示例代码：

| 文件 | 说明 |
|------|------|
| `get_stock.py` | 获取股票列表 |
| `get_company.py` | 获取公司信息 |
| `get_ipo.py` | 获取 IPO 信息 |
| `get_st.py` | 获取 ST 股票 |
| `get_tradedates.py` | 获取交易日历 |
| `get_dayline.py` | 获取日线行情 |
| `get_weekline.py` | 获取周线行情 |
| `get_monthline.py` | 获取月线行情 |
| `get_adjfactor.py` | 获取复权因子 |
| `get_corefactor.py` | 获取每日指标 |
| `get_daylimit.py` | 获取涨跌停价格 |
| `get_daycdm.py` | 获取技术面因子 |

每个示例都可以直接运行，只需替换 Tushare Token。

---

## 常见问题

### 1. 如何获取 Tushare Token？

访问 https://tushare.pro 注册账号，在个人中心获取 Token。

### 2. 不同接口的积分要求是什么？

| 接口 | 积分要求 | 单次最大记录数 | 调用频率 |
|------|---------|--------------|---------|
| Stock, Company, Ipo, St, TradeDate | 无要求 | - | 不限 |
| Dayline, Weekline, Monthline | 基础积分 | 6000 | 500次/分钟 |
| AdjFactor | 2000+ | 2000 | 根据积分 |
| CoreFactor | 2000+ | 6000 | 根据积分 |
| Daylimit | 2000+ | 5800 | 根据积分 |
| Daycdm | 5000+ | 10000 | 30次/分钟（5000积分） |

### 3. 遇到限流怎么办？

增大 `coolant` 参数，减少请求频率：

```python
conf = Conf(params={...}, coolant=2.0)  # 每次请求间隔 2 秒
```

### 4. 数据获取失败怎么办？

检查以下几点：
- Token 是否正确
- 积分是否满足接口要求
- 参数格式是否正确
- 网络连接是否正常

### 5. 如何复权行情数据？

使用 AdjFactor 获取复权因子，然后计算：

```python
# 获取行情和复权因子
dayline_job = Dayline(session=session, conf=Conf(params={...}))
adjfactor_job = AdjFactor(session=session, conf=Conf(params={...}))

dayline = dayline_job.run()
adjfactor = adjfactor_job.run()

# 合并数据
merged = dayline.merge(adjfactor, on=["code", "datecode"])

# 计算前复权价格
merged["close_qfq"] = merged["close"] * merged["adj_factor"]
```

---

## 技术支持

- Tushare 文档：https://tushare.pro/document/2
- 积分获取：https://tushare.pro/document/1?doc_id=13
- 问题反馈：提交 GitHub Issue

---

## 版本与许可

**版本**: 0.1.5  
**许可证**: MIT License  
**作者**: Xing Xing (x.xing.work@gmail.com)

## 注意事项

1. 所有接口都需要有效的 Tushare Token
2. 不同接口有不同的积分要求，使用前请确认
3. 高频调用建议使用 5000 积分以上账号
4. 建议启用缓存以提升性能并减少重复请求
5. 生产环境使用时注意合理设置 coolant 参数避免限流
