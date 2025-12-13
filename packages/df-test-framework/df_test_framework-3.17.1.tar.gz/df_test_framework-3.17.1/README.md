# DF Test Framework

> 简单、强大、可扩展的现代化 Python 测试自动化框架

[![PyPI version](https://img.shields.io/pypi/v/df-test-framework.svg)](https://pypi.org/project/df-test-framework/)
[![Python](https://img.shields.io/badge/python-3.12+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

---

## 🎯 核心特性

### 当前版本亮点 ⚡🔭📊

**v3.17 事件系统重构与可观测性增强**：
- ✅ **事件关联系统** - correlation_id 追踪完整请求生命周期
- ✅ **OpenTelemetry 深度整合** - 自动注入 trace_id/span_id（W3C TraceContext）
- ✅ **测试隔离机制** - 每个测试独立的 EventBus（ContextVar）
- ✅ **AllureObserver 自动集成** - 修复 v3.16.0 报告问题，自动记录 HTTP 请求

**v3.16 五层架构完善**：
- ✅ **Layer 4 Bootstrap 引导层** - 解决架构依赖违规
- ✅ **Middleware 系统成熟** - 完全移除 Interceptor

**v3.14 中间件与事件系统**：
- ✅ **中间件系统（洋葱模型）** - SignatureMiddleware/RetryMiddleware 等
- ✅ **EventBus 事件总线** - 发布-订阅模式，支持可观测性

**v3.11-v3.12 核心能力**：
- ✅ **测试数据清理** - CleanupManager，`--keep-test-data` 控制
- ✅ **OpenTelemetry 分布式追踪** - Jaeger/Zipkin/Tempo 集成
- ✅ **GraphQL/gRPC 客户端** - 多协议支持
- 📡 **消息队列客户端** - Kafka/RabbitMQ/RocketMQ

> 📖 **完整版本历史**: [Release Notes](docs/releases/) | [CHANGELOG](CHANGELOG.md)
> 🔄 **版本迁移**: [Migration Guides](docs/migration/)

### 核心架构

- **按交互模式建模能力层**：`clients/`、`drivers/`、`databases/`、`messengers/`、`storages/`、`engines/`
- **五层架构**：`common → capabilities → infrastructure → testing → extensions`
- **Bootstrap + ProviderRegistry + Pluggy Hooks**，实现高度解耦的运行时装配
- **类型安全 & 可观测性**：Pydantic v2 配置、结构化日志、完整的类型注解

---

## 🗺️ 快速导航

### 🚀 新手入门
| 文档 | 说明 | 时间 |
|------|------|------|
| **[5分钟快速开始](docs/user-guide/QUICK_START.md)** ⭐ | 从零开始运行第一个测试 | 5分钟 |
| **[快速参考](docs/user-guide/QUICK_REFERENCE.md)** 📋 | API 速查表和常用命令 | 2分钟 |
| [核心文档导航](docs/ESSENTIAL_DOCS.md) | 最有价值的15个文档 | - |
| [完整用户手册](docs/user-guide/USER_MANUAL.md) | 深入了解框架能力 | 按需查阅 |

### 📚 核心文档
| 文档类型 | 链接 |
|---------|------|
| **版本发布说明** | [Release Notes](docs/releases/) 📦 |
| **更新日志** | [CHANGELOG.md](CHANGELOG.md) 📝 |
| **版本迁移指南** | [Migration Guides](docs/migration/) 🔄 |
| **完整文档索引** | [Documentation Index](docs/DOCUMENTATION_INDEX.md) 📚 |
| **用户手册** | [User Manual](docs/user-guide/USER_MANUAL.md) 📖 |
| **API 参考** | [API Reference](docs/api-reference/README.md) 🔌 |
| **问题排查** | [Troubleshooting](docs/troubleshooting/) 🔧 |

更多文档请见 [docs/README.md](docs/README.md)。

---

## 📦 安装

### 基础安装

```bash
# 使用 pip（推荐）
pip install df-test-framework     # 即将发布到 PyPI

# 使用 uv（更快）
pip install uv
uv pip install df-test-framework
```

### 📦 可选依赖安装

框架采用**按需安装**设计，核心功能开箱即用，可选功能需要安装对应依赖：

```bash
# UI 测试支持
pip install df-test-framework[ui]

# 消息队列支持（Kafka + RabbitMQ + RocketMQ）
pip install df-test-framework[mq]

# 可观测性支持（OpenTelemetry + Prometheus）
pip install df-test-framework[observability]

# 存储客户端支持（S3 + 阿里云OSS）
pip install df-test-framework[storage]

# 安装所有可选功能
pip install df-test-framework[all]

# 组合安装（示例：UI + 可观测性 + 存储）
pip install df-test-framework[ui,observability,storage]
```

**可选依赖功能对照表**：

| 依赖组 | 包含功能 | 安装命令 |
|--------|---------|---------|
| `ui` | Playwright, Selenium | `pip install df-test-framework[ui]` |
| `kafka` | Kafka 客户端 | `pip install df-test-framework[kafka]` |
| `rabbitmq` | RabbitMQ 客户端 | `pip install df-test-framework[rabbitmq]` |
| `rocketmq` | RocketMQ 客户端 | `pip install df-test-framework[rocketmq]` |
| `mq` | 所有消息队列 | `pip install df-test-framework[mq]` |
| `opentelemetry` | OpenTelemetry 追踪 | `pip install df-test-framework[opentelemetry]` |
| `prometheus` | Prometheus 监控 | `pip install df-test-framework[prometheus]` |
| `observability` | 可观测性全套 | `pip install df-test-framework[observability]` |
| `storage` | S3 + OSS 存储 | `pip install df-test-framework[storage]` |
| `all` | 所有可选功能 | `pip install df-test-framework[all]` |

**💡 提示**：
- ✅ 不安装可选依赖不影响核心功能使用
- ⚠️ 使用未安装的可选功能会抛出 `ImportError`
- 📌 推荐按实际需求安装，减少依赖体积

### 从 Git 仓库安装

```bash
# 基础安装（最新版本）
uv pip install "df-test-framework @ git+https://github.com/yourorg/test-framework.git"

# 安装特定可选依赖
uv pip install "df-test-framework[observability,storage] @ git+https://github.com/yourorg/test-framework.git"

# 安装指定版本
uv pip install "df-test-framework @ git+https://github.com/yourorg/test-framework.git@v3.11.1"
```

### 本地开发

```bash
git clone https://github.com/yourorg/test-framework.git
cd test-framework

# 方式1: 使用 uv sync（推荐）
uv sync --all-extras  # 安装所有依赖（开发 + 可选）
uv run pytest -v      # 运行测试

# 方式2: 传统方式
uv pip install -e ".[all,dev]"  # 安装所有依赖
pytest -v                        # 运行测试
```

---

## ⚡ 快速开始

### 方式一：脚手架秒建项目（推荐）
```bash
df-test init my-test-project              # API 测试项目（默认）
# df-test init my-test-project --type ui  # UI（Playwright）项目
# df-test init my-test-project --type full# API + UI 混合项目

cd my-test-project
cp .env.example .env                      # 修改基础配置
pytest -v                                 # 运行示例测试
```
生成内容包含标准目录结构、脚本、Allure 集成、`db_transaction` 自动回滚等即用能力。详见 [快速入门](docs/getting-started/quickstart.md)。

### 方式二：手动构建

**同步 API 测试：**
```python
from df_test_framework import Bootstrap, FrameworkSettings
from pydantic import Field

class DemoSettings(FrameworkSettings):
    api_base_url: str = Field(default="https://api.example.com")

runtime = (
    Bootstrap()
    .with_settings(DemoSettings)
    .build()
    .run()
)

http = runtime.http_client()
response = http.get("/users/1")
assert response.status_code == 200
```

**异步 API 测试（高性能）：**
```python
import asyncio
from df_test_framework import AsyncHttpClient

async def test_concurrent():
    async with AsyncHttpClient("https://api.example.com") as client:
        # 并发 100 个请求（仅需 0.5 秒，比同步快 40 倍！）
        tasks = [client.get(f"/users/{i}") for i in range(100)]
        responses = await asyncio.gather(*tasks)

        assert len(responses) == 100

asyncio.run(test_concurrent())
```

更多示例：[`examples/`](examples/) | [AsyncHttpClient 指南](docs/guides/async_http_client.md)。

---

## 🧱 架构概览

```
Layer 4 ─ extensions/        # Pluggy 扩展系统 + 内置监控
Layer 3 ─ testing/           # Fixtures、调试工具、数据构建、插件
Layer 2 ─ infrastructure/    # Bootstrap、配置、日志、Provider、Runtime
Layer 1 ─ clients/…          # 能力层：HTTP、UI、数据库、消息、存储、计算
Layer 0 ─ common/            # 异常与基础类型
```

- **能力层** 按交互模式组织：REST 客户端、Playwright 驱动、SQL/Redis 访问、消息/存储/计算预留目录。
- **基础设施层** 负责 Settings 管线、日志策略、ProviderRegistry 与 RuntimeContext。
- **测试支持层** 提供 pytest fixtures、数据构建器、调试器，以及 Allure、环境标记等插件。
- **扩展层** 通过 Hook (`df_config_sources`, `df_providers`, `df_post_bootstrap`) 接入任何自定义能力。

详细设计见 [架构文档](docs/architecture/overview.md)。

---

## 🔌 核心能力

### HTTP 客户端 (`clients/http/rest/httpx`)

- **同步 HttpClient**：重试、敏感信息脱敏、签名/Token/Bearer 拦截器、HTTPDebugger 集成
- **异步 AsyncHttpClient**：
  - 基于 `httpx.AsyncClient`，完整的 async/await 支持
  - 并发性能提升 **10-50 倍**（100个请求从20秒降至0.5秒）
  - HTTP/2 支持、连接池管理、资源占用降低 75%
  - 完全兼容现有拦截器（签名、Token、日志）
  - 详见：[AsyncHttpClient 使用指南](docs/guides/async_http_client.md)

### 消息队列 (`messengers/queue/`)

- **Kafka客户端**：基于 confluent-kafka，性能提升3倍，完整SSL/TLS支持
- **RabbitMQ客户端**：AMQP 0-9-1协议，支持Direct/Topic/Fanout/Headers
- **RocketMQ客户端**：延迟消息、Tags/SQL过滤
- 详见：[消息队列使用指南](docs/guides/message_queue.md)

### 其他能力

- **数据库访问** (`databases/`)：SQLAlchemy QueuePool、事务/保存点、Repository 模式、UnitOfWork 模式、DBDebugger、慢查询监控扩展
- **Redis 客户端**：连接池、常用操作封装
- **UI 驱动** (`drivers/web/playwright`)：浏览器管理器、Page 对象、等待助手、截图
- **数据构建与清理** (`testing/data/builders`, `testing/fixtures/cleanup`)：Builder 模式、通用/自定义数据清理器
- **调试与监控**：HTTP/DB 调试器、性能追踪器、慢查询监控、Allure 集成
- **熔断器**：Circuit Breaker 模式，自动故障保护

更多 API 细节：[`docs/api-reference/`](docs/api-reference/README.md)。

---

## 🚧 计划中的功能

以下功能模块已预留目录结构，**暂未实现**。如有需求，欢迎贡献实现：

### 数据处理引擎 (engines/)
- ❌ **Apache Spark客户端** - 计划中
  - SparkSession管理
  - RDD/DataFrame操作
  - 作业提交和监控
- ❌ **Apache Flink客户端** - 计划中
  - StreamExecutionEnvironment管理
  - DataStream操作
  - 作业提交和监控

### 存储 (storages/)
- ❌ **本地文件系统客户端** - 计划中
  - 文件读写操作
  - 目录管理
  - 文件管理
- ❌ **AWS S3客户端** - 计划中
  - Bucket操作
  - Object操作
  - 分片上传

> **注意**：上述模块目前仅有目录占位符，**暂未实现**。
> 如需使用这些功能，可以：
> 1. 等待官方实现（欢迎关注仓库更新）
> 2. 自行实现并提交PR贡献
> 3. 使用第三方库直接集成（如`boto3`等）

---

## 🧰 CLI 与工具链

- `df-test init` — 生成规范化项目骨架（支持 API / UI / Full / CI 模板）。
- `df-test gen` — 快速生成测试、Builder、Repository、API 客户端样板代码。
- `verify_fixes.py` — 辅助验证修复任务（示例脚本）。

详见 [CLI 指南](docs/user-guide/code-generation.md)。

---

## 🤝 贡献 & 社区

### 开发流程

1. **Fork 仓库并创建特性分支**
   ```bash
   git checkout -b feature/awesome
   ```

2. **同步开发依赖（推荐使用 uv sync）**
   ```bash
   # 方式1: 使用 uv sync（推荐 - 默认包含dev依赖）
   uv sync

   # 注意: 如果需要消息队列功能，需要单独安装（需要librdkafka等）
   # uv pip install confluent-kafka pika rocketmq-python-client

   # 方式2: 传统方式
   uv pip install -e ".[dev]"
   ```

3. **运行测试**
   ```bash
   # 运行所有测试（推荐）
   uv run pytest -v

   # 排除需要外部服务的测试（Kafka/RabbitMQ/RocketMQ）
   uv run pytest -v --ignore=tests/test_messengers/

   # 运行测试并生成覆盖率报告
   uv run pytest --cov=src/df_test_framework --cov-report=term-missing --cov-report=html

   # 查看HTML覆盖率报告
   # Windows: start htmlcov/index.html
   # Linux/Mac: open htmlcov/index.html
   ```

4. **代码质量检查**
   ```bash
   # 使用 uv run 运行代码检查工具
   uv run ruff check src/ tests/
   uv run ruff format src/ tests/

   # 类型检查
   uv run mypy src/
   ```

5. **提交 PR 并描述变更影响**
   - 确保所有测试通过
   - 代码覆盖率不低于 80%（当前目标）
   - 遵循现有代码风格
   - 提供清晰的 PR 描述

### 测试覆盖率要求

- 目标覆盖率：**80%** （配置在 `pyproject.toml` 中）
- 覆盖率报告：`reports/coverage/`
- 排除文件：`__init__.py`、`conftest.py`、测试文件本身

详细的测试开发指南请参考 [CONTRIBUTING.md](CONTRIBUTING.md) 和 [测试开发文档](docs/user-guide/testing-development.md)。

使用本框架的项目欢迎在 ISSUE 中分享最佳实践和需求。

---

## 📄 许可证

MIT License，详见 [LICENSE](LICENSE)。
