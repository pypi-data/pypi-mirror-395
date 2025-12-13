# 股票数据存储框架技术概要设计

## 1. 项目概述

### 1.1 项目目标
构建一个配置驱动的股票数据存储框架，专注于后端数据处理流程，通过YAML配置文件定义完整的数据处理workflow。

### 1.2 核心特性
- **配置驱动**：完全通过YAML配置文件定义数据处理流程
- **模块化设计**：采集器、处理器、存储器分离，易于扩展
- **灵活的数据处理**：支持自定义Python脚本进行数据转换
- **多存储支持**：支持SQLite、MySQL、PostgreSQL、CSV等多种存储后端
- **简单易用**：无需编写复杂代码，通过配置即可完成数据流程

### 1.3 技术栈
- **编程语言**：Python 3.8+
- **数据处理**：pandas, numpy
- **数据存储**：SQLAlchemy、pandas（CSV/Parquet）
- **配置管理**：Pydantic + YAML
- **日志管理**：Loguru

## 2. 架构设计

### 2.1 整体架构
```
┌─────────────────────────────────────────────┐
│               Workflow引擎                  │
├─────────────────────────────────────────────┤
│ 1. 解析workflow配置                         │
│ 2. 执行数据采集器                           │
│ 3. 调用数据处理脚本                         │
│ 4. 存储数据到指定后端                       │
└─────────────────────────────────────────────┘
                     │
┌─────────────────────────────────────────────┐
│               配置层                         │
├─────────────────────────────────────────────┤
│  - workflow配置 (YAML)                      │
│  - 采集器配置                               │
│  - 处理器配置                               │
│  - 存储器配置                               │
└─────────────────────────────────────────────┘
                     │
┌─────────────────────────────────────────────┐
│               执行层                         │
├─────────────────────────────────────────────┤
│  - 数据采集器 (akshare, tushare等)          │
│  - 数据处理器 (Python脚本)                  │
│  - 数据存储器 (SQLite, MySQL, CSV等)        │
└─────────────────────────────────────────────┘
```

### 2.2 核心概念
1. **Workflow**：完整的数据处理流程，包含采集、处理、存储三个步骤
2. **Collector**：数据采集器，负责从外部数据源获取数据
3. **Processor**：数据处理器，负责对采集的数据进行转换和处理
4. **Storage**：数据存储器，负责将处理后的数据持久化

## 3. 配置文件设计

### 3.1 主配置文件 (config.yaml)
```yaml
# 应用基础配置
app:
  name: "stock-data-pipeline"
  version: "1.0.0"
  log_level: "INFO"
  log_dir: "./logs"

# 数据采集器配置
collectors:
  akshare1:
    type: "akshare"
    config:
      timeout: 30
      retry_times: 3
  
  tushare1:
    type: "tushare"
    config:
      token: "${TUSHARE_TOKEN}"
      timeout: 30

# 数据存储配置
storages:
  sqlite1:
    type: "sqlite"
    config:
      database: "./data/stock_data.db"
  
  csv1:
    type: "csv"
    config:
      directory: "./data/csv"
  
  mysql1:
    type: "mysql"
    config:
      host: "localhost"
      port: 3306
      database: "stock_data"
      username: "${MYSQL_USER}"
      password: "${MYSQL_PASSWORD}"
```

### 3.2 Workflow配置文件示例
```yaml
# workflow: daily_stock_data.yaml
name: "daily_stock_data"
description: "每日股票数据采集和处理"
schedule: "0 18 * * *"  # 每天18:00执行

# 数据采集配置
collector:
  name: "akshare1"
  config:
    symbols: ["000001", "000002", "000003"]
    start_date: "2024-01-01"
    end_date: "{{ today }}"  # 支持模板变量
    frequency: "daily"

# 数据处理配置
processor:
  # 使用Python脚本处理数据
  script: "./scripts/process_daily_data.py"

# 数据存储配置
storage:
  name: "mysql1"
  config:
    table_name: "daily_stock_data"
```

## 4. 核心组件设计

### 4.1 Workflow引擎
- **功能**：解析workflow配置，按顺序执行采集、处理、存储步骤
- **特性**：
  - 支持模板变量（如{{ today }}）
  - 错误处理和重试机制
  - 执行状态监控和日志记录

### 4.2 数据采集器
- **类型**：
  - akshare采集器：获取A股历史数据
  - tushare采集器：获取tushare平台数据
  - 自定义采集器：支持用户自定义数据源
- **配置**：通过YAML配置数据源参数、股票代码、时间范围等

### 4.3 数据处理器
- **内置处理器**：基于pandas的基础数据处理（去重、类型转换、缺失值处理）
- **自定义处理器**：支持用户编写Python脚本进行复杂数据处理
- **扩展性**：可通过插件机制添加新的处理器类型

### 4.4 数据存储器
- **支持的后端**：
  - SQLite：轻量级本地数据库
  - MySQL/PostgreSQL：关系型数据库
  - CSV/Parquet：文件存储
  - 自定义存储：支持用户实现存储接口
- **表结构管理**：支持自动创建表结构或使用上游字段

## 5. 执行流程

### 5.1 正常流程
1. **配置解析**：读取并解析workflow配置文件
2. **数据采集**：根据配置调用对应采集器获取数据
3. **数据处理**：使用处理器对数据进行清洗和转换
4. **数据存储**：将处理后的数据保存到指定存储后端
5. **结果返回**：返回执行结果和统计信息

### 5.2 错误处理
- **采集失败**：记录错误日志，支持重试机制
- **处理失败**：保留原始数据，提供错误诊断信息
- **存储失败**：数据回滚，保证数据一致性

## 6. 项目结构

```
stock-storage-frame/
├── README.md
├── requirements.txt
├── pyproject.toml
├── config.yaml                    # 主配置文件
├── workflows/                     # workflow配置目录
│   ├── daily_stock_data.yaml
│   ├── weekly_report.yaml
│   └── realtime_data.yaml
├── scripts/                       # 自定义处理脚本
│   ├── process_daily_data.py
│   └── calculate_indicators.py
├── src/
│   └── stock_storage/
│       ├── __init__.py
│       ├── main.py                # 主程序入口
│       ├── engine.py              # Workflow引擎
│       ├── models.py              # 数据模型
│       ├── factories.py           # 组件工厂
│       ├── collectors/            # 采集器实现
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── akshare.py
│       │   └── tushare.py
│       ├── processors/            # 处理器实现
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── pandas.py
│       │   └── custom.py
│       └── storages/              # 存储器实现
│           ├── __init__.py
│           ├── base.py
│           ├── sqlite.py
│           ├── mysql.py
│           └── csv.py
└── data/                          # 数据存储目录
    ├── stock_data.db              # SQLite数据库
    └── csv/                       # CSV文件
```

## 7. 使用示例

### 7.1 创建workflow配置
```yaml
# workflows/my_stock_data.yaml
name: "my_daily_stock"
description: "我的每日股票数据采集"
schedule: "0 17 * * *"

collector:
  name: "akshare1"
  config:
    symbols: ["000001", "600000"]
    start_date: "2024-01-01"
    end_date: "{{ today }}"
    frequency: "daily"

processor:
  script: "./scripts/my_custom_processor.py"

storage:
  name: "sqlite1"
  config:
    table_name: "my_stock_data"
```

### 7.2 自定义处理脚本
```python
# scripts/my_custom_processor.py
import pandas as pd

def process(df: pd.DataFrame) -> pd.DataFrame:
    """自定义数据处理逻辑"""
    # 计算技术指标
    df['ma5'] = df['close'].rolling(5).mean()
    df['ma10'] = df['close'].rolling(10).mean()
    
    # 添加自定义字段
    df['price_change'] = df['close'].pct_change()
    
    return df
```

### 7.3 执行workflow
```bash
# 安装依赖
pip install -r requirements.txt

# 执行单个workflow
python -m stock_storage.main --workflow workflows/my_stock_data.yaml

# 执行所有workflow
python -m stock_storage.main --all
```

## 8. 扩展性设计

### 8.1 插件机制
- **采集器插件**：实现Collector接口即可添加新的数据源
- **处理器插件**：实现Processor接口即可添加新的处理逻辑
- **存储器插件**：实现Storage接口即可添加新的存储后端

### 8.2 配置扩展
- **环境变量支持**：配置文件中支持${ENV_VAR}语法
- **模板变量**：支持{{ today }}、{{ yesterday }}等时间变量
- **条件配置**：支持根据环境选择不同的配置

## 9. 总结

本框架通过YAML配置文件定义完整的数据处理workflow，实现了数据采集、处理、存储的分离。用户无需编写复杂代码，只需通过配置文件即可完成股票数据的自动化处理流程。框架具有良好的扩展性，支持多种数据源和存储后端，适合需要定期采集和存储股票数据的应用场景。

**核心优势**：
1. **配置驱动**：降低使用门槛，非开发人员也可使用
2. **模块化设计**：各组件独立，易于维护和扩展
3. **灵活处理**：支持自定义Python脚本，满足复杂需求
4. **多存储支持**：适应不同的存储需求
5. **易于部署**：依赖简单，部署方便
