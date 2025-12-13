# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## 项目概述

**DF Test Framework** - 现代化 Python 测试自动化框架

- **版本**: 3.17.0
- **Python**: 3.12+
- **核心技术栈**: pytest + httpx + Pydantic v2 + SQLAlchemy 2.0 + Pluggy
- **架构**: 五层架构 + 横切关注点（能力层驱动设计）
- **核心特性**: 中间件系统（洋葱模型）+ EventBus（事件驱动）+ OpenTelemetry（可观测性）

---

## 核心开发命令

### 环境设置与依赖管理

```bash
# 同步开发依赖（推荐 - 默认包含dev依赖组）
uv sync

# 同步所有可选依赖（包括UI、消息队列等）
uv sync --all-extras
```

### 测试执行

```bash
# 运行所有测试（推荐）
uv run pytest -v

# 排除需要外部服务的测试（Kafka/RabbitMQ/RocketMQ）
uv run pytest -v --ignore=tests/test_messengers/

# 运行特定测试文件
uv run pytest tests/clients/http/test_client.py -v

# 使用标记运行测试
uv run pytest -m smoke -v         # 冒烟测试
uv run pytest -m "not slow" -v    # 排除慢速测试
```

### 代码质量检查

```bash
# Ruff 代码检查 + 自动修复
uv run ruff check --fix src/ tests/

# 格式化代码
uv run ruff format src/ tests/

# 类型检查
uv run mypy src/
```

### 测试覆盖率

```bash
# 生成覆盖率报告（显示未覆盖行）
uv run pytest --cov=src/df_test_framework --cov-report=term-missing

# 覆盖率要求: ≥80%
```

---

## 架构设计

### 五层架构（v3.16.0+）

```
Layer 4 ─── bootstrap/          # 引导层：框架组装和初始化（Bootstrap、Providers、Runtime）
Layer 3 ─── testing/ + cli/     # 门面层：Fixtures、调试工具、CLI 工具（并行）
Layer 2 ─── capabilities/       # 能力层：clients/drivers/databases/messengers/storages
Layer 1 ─── infrastructure/     # 基础设施：config/logging/telemetry/events/plugins
Layer 0 ─── core/               # 核心层：纯抽象（middleware/context/events/protocols）
横切 ───── plugins/             # 插件：MonitoringPlugin、AllurePlugin
```

**依赖规则**:
- Layer 4 (bootstrap/) → 可依赖 Layer 0-3 全部（引导层特权）
- Layer 3 (testing/ + cli/) → 可依赖 Layer 0-2
- Layer 2 (capabilities/) → 可依赖 Layer 0-1
- Layer 1 (infrastructure/) → 只能依赖 Layer 0
- Layer 0 (core/) → 无依赖（最底层，纯抽象）
- plugins/ → 横切关注点，可依赖任意层级

### 能力层（Layer 2 - capabilities/）

| 目录 | 职责 | 状态 |
|------|------|------|
| `clients/http/` | HTTP/REST + 中间件系统（洋葱模型） | ✅ |
| `clients/graphql/` | GraphQL 客户端 + QueryBuilder | ✅ |
| `clients/grpc/` | gRPC 客户端 + 拦截器 | ✅ |
| `drivers/` | Playwright、Selenium | ✅ |
| `databases/` | MySQL、Redis、Repository、UoW | ✅ |
| `messengers/` | Kafka、RabbitMQ、RocketMQ | ✅ |
| `storages/` | LocalFile、S3、OSS | ✅ |
| `engines/` | Spark、Flink | ❌ 预留 |

### 目录结构

```
src/df_test_framework/
├── core/                # Layer 0: 纯抽象（middleware/context/events/protocols）
├── infrastructure/      # Layer 1: 基础设施（config/logging/telemetry/events/plugins）
├── capabilities/        # Layer 2: 能力层
│   ├── clients/         #   HTTP/GraphQL/gRPC 客户端 + 中间件
│   ├── drivers/         #   Playwright/Selenium
│   ├── databases/       #   Database + Redis + Repository + UoW
│   ├── messengers/      #   Kafka + RabbitMQ + RocketMQ
│   └── storages/        #   LocalFile/S3/OSS
├── testing/             # Layer 3: Fixtures、数据工具、调试器
├── cli/                 # Layer 3: CLI 工具 + 脚手架模板
├── bootstrap/           # Layer 4: Bootstrap、Providers、Runtime
├── plugins/             # 横切: MonitoringPlugin、AllurePlugin
├── extensions/          # 向后兼容（已废弃，使用 plugins/）
├── common/              # 向后兼容（已废弃，使用 core/）
├── models/              # Pydantic 数据模型
└── utils/               # 工具函数

tests/                   # 镜像 src/ 结构
```

---

## 测试编写规范

### AAA 模式

```python
def test_example(http_client):
    # Arrange - 准备测试数据
    user_data = {"name": "Alice"}

    # Act - 执行操作
    response = http_client.post("/users", json=user_data)

    # Assert - 验证结果
    assert response.status_code == 201
```

### 测试命名

```python
# ✅ 清晰描述场景
def test_login_with_valid_credentials_returns_token(self):
    pass

# ❌ 不清晰
def test_login(self):
    pass
```

### 数据清理 (v3.11.1+)

```python
from df_test_framework import DataGenerator, CleanupManager

def test_api_data(http_client, cleanup):
    # 生成测试标识符
    order_no = DataGenerator.test_id("TEST_ORD")

    # 调用 API
    response = http_client.post("/orders", json={"order_no": order_no})

    # 注册清理
    cleanup.add("orders", order_no)
    # ✅ 测试结束后自动清理（除非 --keep-test-data）
```

### 中间件系统 (v3.14.0+)

```python
from df_test_framework import HttpClient
from df_test_framework.capabilities.clients.http.middleware import (
    SignatureMiddleware,
    BearerTokenMiddleware,
    RetryMiddleware,
)

# 方式1: 直接创建中间件
client = HttpClient(
    base_url="https://api.example.com",
    middlewares=[
        RetryMiddleware(max_retries=3),
        SignatureMiddleware(secret="xxx", algorithm="md5"),
        BearerTokenMiddleware(token="your_token"),
    ]
)

# 方式2: 配置驱动（推荐）
from df_test_framework.infrastructure.config import (
    HTTPConfig,
    SignatureMiddlewareConfig,
    BearerTokenMiddlewareConfig,
    SignatureAlgorithm,
    TokenSource,
)

http_config = HTTPConfig(
    base_url="https://api.example.com",
    middlewares=[
        SignatureMiddlewareConfig(
            algorithm=SignatureAlgorithm.MD5,
            secret="your_secret",
            include_paths=["/api/**"],
        ),
        BearerTokenMiddlewareConfig(
            source=TokenSource.STATIC,
            token="your_token",
            include_paths=["/admin/**"],
        ),
    ],
)
```

### 事件系统与可观测性 (v3.17.0+)

```python
def test_with_event_tracking(http_client, allure_observer):
    """测试自动事件追踪和 Allure 报告"""
    # allure_observer fixture 自动订阅 EventBus
    # HTTP 请求/响应会自动记录到 Allure 报告

    response = http_client.post("/orders", json={"product": "Phone"})

    assert response.status_code == 201
    # ✅ Allure 报告中会自动包含：
    # - 完整请求体和响应体
    # - OpenTelemetry trace_id/span_id
    # - 事件关联 correlation_id

def test_event_correlation(http_client, event_bus):
    """测试事件关联系统"""
    from df_test_framework.core.events import HttpRequestStartEvent

    # 监听事件
    events = []
    event_bus.subscribe("http.request.*", lambda e: events.append(e))

    # 执行请求
    http_client.get("/users/123")

    # 验证事件关联
    start_event = next(e for e in events if isinstance(e, HttpRequestStartEvent))
    end_event = next(e for e in events if e.event_type == "http.request.completed")

    assert start_event.correlation_id == end_event.correlation_id
    assert start_event.event_id != end_event.event_id
```

---

## 代码质量要求

### 覆盖率

- **目标**: ≥80%
- **验证**: PR 提交前确保覆盖率不低于当前水平

### 类型注解

```python
# ✅ 现代 Python 风格
def create(name: str, items: list[str] | None = None) -> dict[str, Any]:
    pass

# ❌ 旧式
from typing import Dict, List, Optional
def create(name: str, items: Optional[List[str]] = None) -> Dict[str, Any]:
    pass
```

### Ruff 配置

- 行长度: 100
- 目标版本: Python 3.12

---

## 版本管理与更新日志

### 版本号规则（语义化版本）

- `MAJOR.MINOR.PATCH`（如 `3.11.1`）
- `MAJOR`: 不兼容的 API 变更
- `MINOR`: 向后兼容的新功能
- `PATCH`: 向后兼容的 Bug 修复

### CHANGELOG.md 更新规范

**每次发布必须更新**：
1. `CHANGELOG.md` - 简洁摘要
2. `docs/releases/vX.X.X.md` - 详细发布说明（**所有版本都需要**）
3. `docs/guides/xxx.md` - 功能使用指南（如有新功能）

**CHANGELOG.md 格式**：

```markdown
## [3.11.1] - 2025-11-28

### 功能模块名称

**核心特性**: 一句话描述核心价值。

**主要功能**:
- ✨ 功能点 1
- ✨ 功能点 2

**详细内容**: 查看完整发布说明 [v3.11.1](docs/releases/v3.11.1.md)

### 新增
- 新增 `ClassName` - 功能描述

### 文档
- 新增 `docs/releases/v3.11.1.md` - 完整版本发布说明
- 新增 `docs/guides/xxx.md` - 使用指南

### 测试
- 新增 XX 个测试，全部通过

---
```

**原则**：
1. CHANGELOG 保持简洁摘要
2. **每个版本都需要** `docs/releases/vX.X.X.md` 详细发布说明
3. 功能使用指南放在 `docs/guides/`
4. 每个版本条目之间用 `---` 分隔
5. 链接格式：`**详细内容**: 查看完整发布说明 [vX.X.X](docs/releases/vX.X.X.md)`

### 版本发布检查清单

```bash
# 1. 更新版本号
- [ ] pyproject.toml: version = "X.X.X"
- [ ] src/df_test_framework/__init__.py: __version__ = "X.X.X"

# 2. 更新文档（必须）
- [ ] CHANGELOG.md: 添加版本条目（简洁摘要）
- [ ] docs/releases/vX.X.X.md: 详细发布说明（所有版本都需要）
- [ ] docs/guides/: 功能使用指南（如有新功能）

# 3. 验证
- [ ] uv run pytest -v  # 所有测试通过
- [ ] uv run ruff check src/ tests/  # 代码检查通过
```

---

## 开发工作流

### 1. 创建分支

```bash
git checkout -b feature/功能名称    # 新功能
git checkout -b fix/问题描述        # Bug修复
```

### 2. 开发与测试

```bash
# 边写边测试
uv run pytest tests/path/to/test.py -v

# 代码检查
uv run ruff check --fix src/ tests/
uv run ruff format src/ tests/
```

### 3. 提交代码

**Commit Message 格式**: `<type>(<scope>): <subject>`

```bash
# Type: feat/fix/docs/test/refactor/chore
# Subject: 中文描述，简洁明了

# 示例
feat(cleanup): 新增测试数据清理模块
fix(http): 修复超时配置不生效问题
docs: 更新 CHANGELOG
```

### 4. 提交前检查

```bash
uv run pytest -v                    # 测试通过
uv run ruff check src/ tests/       # 代码检查
uv run ruff format src/ tests/      # 格式化
```

---

## 常见任务

### 添加新功能模块

1. 在对应 Layer 创建目录和代码
2. 编写单元测试（覆盖率 ≥80%）
3. 更新 `__init__.py` 导出
4. 更新 CHANGELOG.md
5. 编写使用指南（如需要）

### 添加新的 Fixture

1. 在 `testing/fixtures/` 添加 fixture
2. 在 `__init__.py` 导出
3. 编写测试
4. 更新脚手架模板（如需要）

### 更新脚手架模板

模板位置: `src/df_test_framework/cli/templates/`

- `project/`: 项目初始化模板
- `generators/`: 代码生成模板

---

## 重要提示

### 外部服务测试

`tests/test_messengers/` 需要外部服务（Kafka/RabbitMQ/RocketMQ）:

```bash
uv run pytest -v --ignore=tests/test_messengers/
```

### 预留目录

以下模块仅有目录占位符，**暂未实现**:
- `engines/` - 计算引擎（Spark、Flink）

### Windows 平台

- 使用 `start` 而非 `open` 打开 HTML 报告

---

## 参考文档

| 类型 | 路径 |
|------|------|
| 架构设计 | `docs/architecture/` |
| 使用指南 | `docs/guides/` |
| 版本发布 | `docs/releases/` |
| 更新日志 | `CHANGELOG.md` |
