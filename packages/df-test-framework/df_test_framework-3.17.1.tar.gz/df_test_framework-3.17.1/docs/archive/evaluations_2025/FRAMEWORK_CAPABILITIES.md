# DF Test Framework 能力与项目集成指南

> 面向测试团队和框架使用者，系统梳理 v3 能力层、配套基础设施以及项目落地方式。阅读后你应当了解框架提供了哪些工具、每种能力如何启用，以及如何在业务测试项目中形成标准化工程实践。

---

## 1. 体系概览

| 维度 | 能力 | 关键目录 |
|------|------|----------|
| 架构分层 | `common → capabilities → infrastructure → testing → extensions` | `src/df_test_framework/*` |
| 能力层（Capability Layer） | HTTP 客户端、UI 驱动、数据库、消息、存储、计算 | `clients/`, `drivers/`, `databases/`, `messengers/`, `storages/`, `engines/` |
| 基础设施层 | 配置（Pydantic v2）、Bootstrap、Provider 注册表、日志策略 | `infrastructure/` |
| 测试支持层 | Fixtures、数据构建器、调试器、pytest 插件 | `testing/` |
| 扩展层 | Pluggy Hook、内置监控扩展 | `extensions/` |
| 项目支撑 | CLI 脚手架、代码生成器、示例、文档 | `src/df_test_framework/cli/`, `examples/`, `docs/` |

> **核心理念**：先定义“交互模式”（Capability），再通过 Bootstrap + Provider 组合能力，与测试支持层解耦，从而让 API/UI/数据/消息测试能共享同一套基础设施。

---

## 2. 能力层（Capability Layer）

### 2.1 HTTP 请求-响应模式（`clients/http/`）

- `http/rest/httpx/client.py`：基于 httpx 的同步客户端，具备：
  - 自动重试（5xx + 超时 → 指数退避）
  - URL 敏感信息脱敏日志
  - 认证拦截器（Bearer/Token/Basic/API Key）
  - 签名策略（MD5/SHA/HMAC）
  - `HTTPDebugger` 集成（请求/响应/错误记录）
- `http/rest/httpx/base_api.py`：业务 API 基类，支持：
  - 请求/响应拦截器链
  - `_check_business_error()` 指定业务错误规则
  - 自动 JSON 解析 + Pydantic 模型校验
- `http/rest/protocols.py` + `factory.py`：协议 & 工厂模式，后续可扩展 `requests`、`grpc` 等实现。

**项目使用**：默认通过 `runtime.http_client()` 获取；亦可在业务层封装继承 `BaseAPI` 的类统一处理业务码。

### 2.2 会话式交互（`drivers/web/playwright/`）

- `BrowserManager`：管理 Playwright 浏览器、上下文、页面、超时、无头模式等。
- `BasePage`, `ElementLocator`, `WaitHelper`：PO 模式基类、封装常见等待/定位操作。
- Pytest fixtures（`testing/fixtures/ui.py`）提供 `browser_manager`, `page`, `goto`, `screenshot`。

### 2.3 数据访问（`databases/`）

- `database.py`：SQLAlchemy 驱动，支持 QueuePool、事务、保存点、表名白名单、防泄漏日志。
- `redis/redis_client.py`：redis-py 封装，提供连接池、常用操作。
- `repositories/`：
  - `BaseRepository`：标准 CRUD、条件查询、计数、存在性校验。
  - `QuerySpec`：灵活组合查询条件。
- Debug 集成：所有 `execute/query` 自动写入 `DBDebugger`。

### 2.4 消息、存储、计算（`messengers/`, `storages/`, `engines/`）

目录已预留，约定按交互模式扩展 Kafka、S3、Spark 等客户端，通过 Provider 注入使用。

---

## 3. 基础设施层（`infrastructure/`）

### 3.1 配置系统

- `config/schema.py`: `FrameworkSettings` 基于 Pydantic BaseSettings，默认包含：
  - `env`, `debug`
  - `http`, `db`, `redis`, `test`, `logging`, `extras`
- `config/sources.py`: 支持 `.env`、环境变量、命令行、字典源，深度合并。
- 自定义项目可继承 `FrameworkSettings` 添加业务字段，如 `admin_token`、`report_bucket` 等。

### 3.2 Bootstrap 管线（`infrastructure/bootstrap`）

```python
runtime = (
    Bootstrap()
    .with_settings(MySettings, namespace="test")
    .with_plugin("my_project.plugins")         # 注册 Pluggy 插件
    .with_provider_factory(custom_providers)   # 扩展 Provider
    .build()
    .run()
)
```

执行流程：
1. 清理/加载 Settings（支持命名空间、缓存）
2. 初始化日志策略（Loguru）
3. 构建 ProviderRegistry（含默认 `http_client`、`database`、`redis`）
4. 注册扩展，触发 `df_config_sources` / `df_providers` / `df_post_bootstrap`
5. 返回 `RuntimeContext`（settings, logger, providers, extensions）

### 3.3 Provider 体系（`infrastructure/providers`）

- `SingletonProvider`: 线程安全的双检锁单例，支持 `close/shutdown` 自动清理。
- `ProviderRegistry`: 注册/扩展 Provider，集中调用 `shutdown()`。
- `default_providers`: 根据 `FrameworkSettings` 实例化 HTTP/DB/Redis。
- 自定义 Provider：通过插件或自定义 factory 扩展，如消息客户端、缓存等。

### 3.4 日志与观测（`infrastructure/logging`）

- Loguru 集成：支持文件/控制台输出、旋转、保留、敏感字段脱敏。
- `LoggerStrategy` 接口可自定义日志策略（默认 `LoguruStructuredStrategy`）。

---

## 4. 测试支持层（`testing/`）

### 4.1 Pytest Fixtures（`testing/fixtures`）

| Fixture | 描述 |
|---------|------|
| `runtime` | session 级 `RuntimeContext` |
| `http_client` / `database` / `redis_client` | 能力层实例 |
| `db_transaction` | 项目脚手架提供的事务 fixture，测试结束自动 `ROLLBACK` |
| `http_debugger` / `db_debugger` | 函数级调试器，打印请求/SQL 摘要 |
| UI 相关 (`browser_manager`, `page`, `goto`, `screenshot`) | Playwright 自动化支持 |
| `auto_debug_on_failure` | 失败时自动打印调试摘要 |

> 项目中的 `tests/conftest.py` 只需 `pytest_plugins = ["df_test_framework.testing.fixtures.core"]` 即可加载核心 fixtures。

### 4.2 数据构建与清理

- `testing/data/builders`: `BaseBuilder`, `DictBuilder`，链式设置字段、支持深拷贝重置。
- `testing/fixtures/cleanup`: `BaseTestDataCleaner`, `GenericTestDataCleaner`，统一注册测试过程中产生的数据，退出时自动清理。

### 4.3 调试与监控

- `testing/debug/http_debugger.py` / `db_debugger.py`: 记录请求、响应、错误、慢查询，支持 `print_summary()`。
- `extensions/builtin/monitoring`: `APIPerformanceTracker`、`SlowQueryMonitor`，通过 Provider 注入，监控调用耗时和慢 SQL。
- `testing/plugins/allure.py`: Allure 附加工具（日志、JSON、截图、环境信息）。

### 4.4 pytest 插件（`testing/plugins`）

- 环境标记：`skip_if_prod`, `dev_only`, `get_env` 等辅助在多环境执行。
- Allure 步骤/附件辅助函数：`step`, `attach_json`, `attach_log` 等。

---

## 5. 项目工程化流程

### 5.1 使用 CLI 脚手架

```bash
df-test init my-project --type api
```

生成内容：标准目录、默认 `FrameworkSettings`、示例 fixtures、`db_transaction`、Allure 配置、README、CI 模板（可选）。

### 5.2 自定义配置

```python
from df_test_framework import FrameworkSettings
from pydantic import Field

class MySettings(FrameworkSettings):
    service_base_url: str = Field(default="https://api.example.com")
    admin_token: str = Field(default="")
```

在 `tests/conftest.py` 或 `fixtures/core.py` 中替换 settings class：
```python
from df_test_framework import Bootstrap
from .config.settings import MySettings

def pytest_configure(config):
    Bootstrap().with_settings(MySettings).build().run(force_reload=True)
```

### 5.3 集成能力层

- HTTP：`http_client` fixture；如需业务封装，继承 `BaseAPI`，实现 `_check_business_error`。
- 数据库：使用 `database` / `db_transaction`，结合自定义 `Repository`，回滚数据污染。
- Redis：`redis_client`，支持 ping、set/get、hash、list 等常用操作。
- UI：Playwright fixtures (`page`, `goto`)，配合 `BasePage` 实现页面对象。

### 5.4 测试用例组织建议

- `tests/api/`：接口级用例，搭配 `http_client`、`BaseAPI`。
- `tests/data/`：测试数据（YAML/JSON），供 Builder/Repository 使用。
- `tests/ui/`：UI 脚本，使用 `page`、`goto`、`screenshot` 等 fixtures。
- `tests/conftest.py`：加载框架 fixtures、注册 CLI 插件、定义业务级 fixture（如 `user_api`）。

---

## 6. 调试、监控与报告

| 能力 | 触发方式 | 输出 |
|------|----------|------|
| HTTPDebugger | `enable_http_debug()` 或 `http_debugger` fixture | 请求/响应摘要、状态码、耗时 |
| DBDebugger | `enable_db_debug()` 或 `db_debugger` fixture | SQL、参数、耗时、慢查询标记 |
| APIPerformanceTracker | 通过 Provider 获取 `api_performance_tracker` | API 耗时统计、P50/P95/P99 等 |
| SlowQueryMonitor | `setup_slow_query_logging(engine, monitor)` | 慢查询列表、统计 |
| Allure | pytest 参数 `--alluredir` + 工具方法 | 可视化报告、步骤、附件 |

调试技巧详见：[Troubleshooting 文档](troubleshooting/debugging-guide.md)。

---

## 7. 扩展机制（`extensions/`）

- 基于 Pluggy 定义 Hooks：
  - `df_config_sources(settings_cls)`：追加配置源（如远程配置中心）。
  - `df_providers(settings, logger)`：注册自定义 Provider（如 MQ 客户端）。
  - `df_post_bootstrap(runtime)`：在 Runtime 准备好后执行自定义逻辑（如指标上报）。
- `extensions/core/manager.py` 提供注册字符串路径或对象实例的方法。
- 内置扩展：监控相关 Provider，可作为参考实现。

项目中可创建 `my_project/plugins.py`，实现上述 Hook，并在 Bootstrap 链式调用中 `.with_plugin("my_project.plugins")`。

---

## 8. CLI 工具链

| 命令 | 用途 |
|------|------|
| `df-test init <path> [--type api|ui|full] [--ci ...]` | 生成新项目脚手架 |
| `df-test gen test <name>` | 生成 API 测试文件（支持 Allure feature/story） |
| `df-test gen builder <entity>` | 生成 Builder 类模板 |
| `df-test gen repo <entity>` | 生成 Repository 类模板 |
| `df-test gen api <entity>` | 生成业务 API 封装模板 |

模板代码位于 `src/df_test_framework/cli/templates/`，可按团队规范修改后重新发布。

---

## 9. 典型落地流程（建议）

1. **脚手架初始化**：`df-test init` 创建项目，确认 `.env`、`pytest.ini`、`conftest.py` 正常。
2. **配置接入系统**：继承 `FrameworkSettings` 添加业务配置，注册 Bootstrap。
3. **能力封装**：
   - 构建请求/响应模型（Pydantic）：对应后端 DTO/VO（如 `MasterCardCreateRequest`、`AdminConsumptionRecordsResponse`）。
   - 编写 `GiftCardBaseAPI(BaseAPI)` 子类：`self.post/get` + `model=...`，全局 `_check_business_error`。
   - 数据访问层使用 Repository：例如 `CardRepository(BaseRepository)`、`ConsumptionRepository`。
   - 可选：CLI 生成 Builder/Repository 模板 (`df-test gen builder/repo`)，协助构造测试数据。
4. **测试编写**：
   - API 用例：`http_client` + 业务 API + `db_transaction`。直接使用响应模型属性（`response.data.records`）。
   - 数据验证：调用 Repository 对数据库状态断言。
   - UI 用例：`page` + `BasePage` 或 `BrowserManager`，必要时开启调试器。
5. **调试与报告**：启用 `http_debugger` / `db_debugger`，或使用 `debug_mode` fixture；配置 Allure 环境信息、附件。
6. **扩展能力**（可选）：通过 Hook 注册自定义 Provider（如 Kafka、S3）、追加配置源等。

---

## 10. 相关文档索引

- [架构总览](architecture/overview.md)
- [V3 架构设计](architecture/V3_ARCHITECTURE.md)
- [API 参考索引](api-reference/README.md)
- [用户手册](user-guide/USER_MANUAL.md)
- [最佳实践](user-guide/BEST_PRACTICES.md)
- [调试指南](troubleshooting/debugging-guide.md)
- [快速开始](getting-started/quickstart.md)
- [迁移指南 v2 → v3](migration/v2-to-v3.md)
- [历史报告归档](archive/README.md)

---

> 如需进一步定制（企业认证、分布式 Provider、云原生部署），建议基于 Pluggy Hook 实现扩展或提交贡献，共建框架生态。
