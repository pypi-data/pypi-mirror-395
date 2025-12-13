# API 参考文档

> 📖 DF Test Framework **v3.5** API 索引。当前版本不再提供兼容层，所有文档直接映射到 v3.5 目录结构。  
> 设计背景参见 [V3 架构设计](../architecture/V3_ARCHITECTURE.md) 与 [迁移指南](../migration/v3.4-to-v3.5.md)。

---

## 📦 层级导航

| 层级 | 目录 | 文档 | 关键能力 |
|------|------|------|----------|
| 基础设施 | `infrastructure/` | [infrastructure.md](infrastructure.md) | Bootstrap、Runtime、Settings、Provider Registry、日志策略 |
| 能力层 - Clients | `clients/` | [clients.md](clients.md) | HttpClient、BaseAPI、拦截器、业务异常 |
| 能力层 - Drivers | `drivers/` | [drivers.md](drivers.md) | Playwright BrowserManager、Page、等待/定位助手 |
| 能力层 - Databases | `databases/` | [databases.md](databases.md) | Database、RedisClient、Repository/QuerySpec |
| 测试支持 | `testing/` | [testing.md](testing.md) | Fixtures、数据构建、调试器、Allure/环境插件 |
| 扩展系统 | `extensions/` | [extensions.md](extensions.md) | Pluggy hooks、内置监控扩展、APM 集成 |
| 设计模式 | `testing/data/`、`databases/repositories/` | [patterns.md](patterns.md) | Builder、Repository、QuerySpec 使用示例 |

---

## 🧱 基础设施层 (Infrastructure)
- **Bootstrap / Runtime**：`Bootstrap`, `RuntimeBuilder`, `RuntimeContext`，用于按 Profile 构建运行时。
- **配置体系**：`FrameworkSettings`, `HTTPConfig`, `DatabaseConfig`, `RedisConfig`, `LoggingConfig`，统一采用 Pydantic v2。
- **ProviderRegistry**：通过 `Provider`, `SingletonProvider`, `default_providers()` 提供按需惰性加载。
- **日志策略**：`LoguruStructuredStrategy`、`NoOpStrategy`、可自定义的 `LoggerStrategy`。

详见 [infrastructure.md](infrastructure.md)。

---

## 🌐 能力层：Clients
- **HttpClient**：httpx 实现，内置重试、连接池、敏感信息脱敏、配置化拦截器。
- **BaseAPI / BusinessError**：统一的 API 基类与业务异常封装，支持自动模型解析。
- **拦截管线**：与 `common/protocols` 的 `InterceptorChain` 配合，实现 before/after/on_error 生命周期。

参考 [clients.md](clients.md)。

---

## 🖥️ 能力层：Drivers
- **BrowserManager**：Playwright 浏览器工厂，支持多浏览器、可配置 headless。
- **BasePage / WaitHelper / ElementLocator**：页面对象模式、稳定定位与等待工具。
- `drivers.md` 中包含 UI fixtures (`browser_manager`, `page`) 及截图策略。

---

## 💾 能力层：Databases
- **Database**：SQLAlchemy 2.x QueuePool、自动事务/保存点、慢查询监控钩子。
- **RedisClient**：连接池封装、常用操作、调试输出。
- **Repository / QuerySpec**：类型安全的查询构建与数据实体封装。

完整说明见 [databases.md](databases.md) 与 [patterns.md](patterns.md)。

---

## 🧪 测试支持层
- `testing/fixtures`：`runtime`, `http_client`, `database`, `redis_client`, UI 相关 fixtures。
- `testing/data/builders`：`BaseBuilder`, `DictBuilder`, 项目自定义 builder 的指南。
- `testing/debug`：`HTTPDebugger`, `DBDebugger`, 性能计数器、Allure/环境插件。
- `testing/plugins`：可观测性、Allure、Environment Marker、性能追踪。

详情见 [testing.md](testing.md)。

---

## 🔌 扩展系统
- `extensions/core`：`create_extension_manager()`, `ExtensionManager`, `hookimpl`.
- `extensions/builtin`：`APIPerformanceTracker`, `SlowQueryMonitor`, `ObservabilityLogger`.
- 支持 `df_config_sources`, `df_providers`, `df_post_bootstrap` 等 Hook。

参阅 [extensions.md](extensions.md)。

---

## 🧩 设计模式与生成器
- Builder：`BaseBuilder[T]`, `DictBuilder`, 数据构造管线。
- Repository：`BaseRepository[T]`, `QuerySpec`，结合 Database/Redis。
- CLI Generator (`df-test gen`): 代码生成器在 [patterns.md](patterns.md) 与 [user-guide/code-generation.md](../user-guide/code-generation.md) 中有示例。

---

## 🧾 导入示例

### 顶层导入（推荐）
```python
from df_test_framework import (
    Bootstrap,
    FrameworkSettings,
    RuntimeContext,
    HttpClient,
    BaseAPI,
    Database,
    RedisClient,
    BrowserManager,
    BasePage,
    BaseBuilder,
    BaseRepository,
    QuerySpec,
)
```

### 精确导入（按目录）
```python
from df_test_framework.clients.http.rest.httpx import HttpClient, BaseAPI
from df_test_framework.databases.database import Database
from df_test_framework.databases.redis.redis_client import RedisClient
from df_test_framework.databases.repositories import BaseRepository, QuerySpec
from df_test_framework.testing.data.builders import BaseBuilder, DictBuilder
from df_test_framework.drivers.web.playwright import BrowserManager, BasePage
```

---

## 🗂️ Legacy 参考

v2 时代的 API 文档被保留以供迁移查询，不再更新：
- [core.md](core.md) — v2 HttpClient / Database / RedisClient 文档
- [patterns.md](patterns.md) — 包含 v2 Builder / Repository 参考章节
- 其余历史资料已移至 `../archive/`

如无特殊原因，建议直接使用上述 v3.5 文档与实现。
