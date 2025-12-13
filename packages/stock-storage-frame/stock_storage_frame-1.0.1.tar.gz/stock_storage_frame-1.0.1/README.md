# Stock Storage Frame

一个配置驱动的股票数据存储框架，专注于后端数据处理流程。

## 特性

- **配置驱动**：完全通过YAML配置文件定义数据处理流程
- **模块化设计**：采集器、处理器、存储器分离，易于扩展
- **灵活的数据处理**：支持自定义Python脚本进行数据转换
- **多存储支持**：支持SQLite、MySQL、PostgreSQL、CSV等多种存储后端
- **简单易用**：无需编写复杂代码，通过配置即可完成数据流程

## 安装
```bash
python3 -m venv venv
source venv/bin/activate
## 国内源
pip install -i https://mirrors.aliyun.com/pypi/simple -r requirements.txt
## 官方源
pip install -i https://pypi.org/simple/ -r requirements.txt
```
```bash
# 使用pip安装
pip install stock-storage-frame

# 或者从源码安装
git clone https://gitee.com/panhuachao/stock-storage-frame.git
cd stock-storage-frame
pip install -e .
```

## 快速开始

### 1. 创建配置文件

创建 `config.yaml`：

```yaml
app:
  name: "stock-data-pipeline"
  version: "1.0.0"
  log_level: "INFO"
  log_dir: "./logs"

collectors:
  akshare1:
    type: "akshare"
    config:
      timeout: 30
      retry_times: 3

storages:
  sqlite1:
    type: "sqlite"
    config:
      database: "./data/stock_data.db"
```

### 2. 创建Workflow配置

创建 `workflows/daily_stock_data.yaml`：

```yaml
name: "daily_stock_data"
description: "每日股票数据采集和处理"
schedule: "0 18 * * *"

collector:
  name: "akshare1"
  config:
    symbols: ["000001", "000002"]
    start_date: "2024-01-01"
    end_date: "{{ today }}"
    frequency: "daily"

processor:
  script: "./scripts/process_daily_data.py"

storage:
  name: "sqlite1"
  config:
    table_name: "daily_stock_data"
```

### 3. 创建自定义处理脚本

创建 `scripts/process_daily_data.py`：

```python
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

### 4. 执行Workflow

```bash
# 执行单个workflow
python -m src.stock_storage.main --workflow workflows/daily_stock_data.yaml

# 对特定workflow开启定时任务
python -m src.stock_storage.main --workflow workflows/daily_stock_data.yaml --schedule

# 执行特定目录下所有workflow
python -m src.stock_storage.main --workflows-dir workflows

# 对目录下所有workflow执行定时任务
python -m src.stock_storage.main --workflows-dir workflows --schedule

# 执行所有workflow（默认目录）
python -m src.stock_storage.main --all

# 测试所有组件
python -m src.stock_storage.main --test

# 验证workflow配置
python -m src.stock_storage.main --validate workflows/daily_stock_data.yaml

# 查看调度器状态
python -m src.stock_storage.main --scheduler-status
```

### 5. 定时器调度

框架提供了内置的定时器调度功能，可以根据workflow配置中的schedule字段自动执行任务。

```bash
# 启动调度器（后台运行）- 调度所有有schedule的workflow
python -m src.stock_storage.main --schedule

# 对特定workflow开启定时任务
python -m src.stock_storage.main --workflow workflows/daily_stock_data.yaml --schedule

# 对目录下所有workflow执行定时任务
python -m src.stock_storage.main --workflows-dir workflows --schedule

# 查看调度器状态
python -m src.stock_storage.main --scheduler-status

# 使用自定义配置和workflow目录
python -m src.stock_storage.main --schedule --config custom_config.yaml --workflows-dir custom_workflows
```

调度器功能：
- 自动加载所有包含schedule字段的workflow配置
- 根据cron表达式计算下一次执行时间
- 支持优雅关闭（Ctrl+C）
- 实时日志记录执行结果
- 支持多workflow并发调度
- 支持调度特定workflow或整个目录

## 项目结构

```
stock-storage-frame/
├── README.md
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

## 配置说明

### 主配置文件 (config.yaml)

主配置文件定义了全局的采集器、处理器和存储器配置。支持环境变量替换 `${ENV_VAR}`。

### Workflow配置文件

每个workflow配置文件定义了一个完整的数据处理流程，包括：
- **name**: workflow名称
- **description**: 描述信息
- **schedule**: 执行计划（cron表达式）
- **collector**: 数据采集配置
- **processor**: 数据处理配置
- **storage**: 数据存储配置

### 模板变量

workflow配置支持以下模板变量：
- `{ today:YYYYMMDD }}或{{ today:YYYY-MM-DD }}`: 今天日期
- `{{ yesterday:YYYYMMDD }}或{{ yesterday:YYYY-MM-DD }}`: 昨天日期
- `{{ now }}`: 当前时间

## 扩展开发

### 添加新的采集器

1. 在 `src/stock_storage/collectors/` 目录下创建新的采集器类
2. 继承 `BaseCollector` 类并实现必要的方法
3. 在 `factories.py` 中注册新的采集器

### 添加新的存储器

1. 在 `src/stock_storage/storages/` 目录下创建新的存储器类
2. 继承 `BaseStorage` 类并实现必要的方法
3. 在 `factories.py` 中注册新的存储器

### 添加新的处理器

1. 在 `src/stock_storage/processors/` 目录下创建新的处理器类
2. 继承 `BaseProcessor` 类并实现必要的方法
3. 在 `factories.py` 中注册新的处理器

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 发布流程

项目提供了自动化发布脚本 `RELEASE_BASH.sh`，用于简化发布到 PyPI 和 TestPyPI 的流程。

### 使用发布脚本

```bash
# 给予执行权限
chmod +x RELEASE_BASH.sh

# 查看帮助
./RELEASE_BASH.sh --help

# 只运行检查
./RELEASE_BASH.sh --check

# 只构建包
./RELEASE_BASH.sh --build

# 构建并上传到 TestPyPI
./RELEASE_BASH.sh --test

# 构建并上传到 PyPI
./RELEASE_BASH.sh --pypi

# 完整发布流程（交互式）
./RELEASE_BASH.sh
```

### 发布前准备

1. **更新版本号**: 修改 `pyproject.toml` 中的 `version` 字段
2. **更新变更日志**: 更新 `CHANGELOG.md` 文件
3. **运行测试**: 确保所有测试通过
4. **提交代码**: 提交所有更改到 Git 仓库

### 发布步骤

1. **清理旧构建**: 删除 `dist/`, `build/` 等目录
2. **构建包**: 生成 `.tar.gz` 和 `.whl` 文件
3. **检查包**: 使用 `twine check` 验证包格式
4. **上传到 TestPyPI**: 在测试环境验证包
5. **从 TestPyPI 安装测试**: 验证包可以正常安装
6. **上传到 PyPI**: 发布到正式 PyPI
7. **创建 Git 标签**: 创建版本标签并推送到远程仓库

### 环境要求

- Python 3.7+
- `pip` 和 `twine` 工具
- `build` 包（用于构建）
- Git 命令行工具
- PyPI 或 TestPyPI 账号和 token

### 配置 PyPI token

在 `~/.pypirc` 文件中配置 PyPI token：

```ini
[pypi]
username = __token__
password = pypi-your-token-here

[testpypi]
username = __token__
password = pypi-your-test-token-here
```

## 联系方式

- 项目地址: https://gitee.com/panhuachao/stock-storage-frame
- 作者: Pan Huachao
