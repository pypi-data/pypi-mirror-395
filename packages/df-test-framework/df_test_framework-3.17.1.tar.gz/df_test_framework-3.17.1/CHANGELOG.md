# Changelog

本文档记录df-test-framework的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/),
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [3.17.1] - 2025-12-08

### 能力层 Allure 集成优化与 UoW 事务事件

**核心特性**: 统一能力层 Allure 集成为纯 EventBus 驱动模式，实现 UoW 事务事件自动记录，修复同步/异步事件处理器兼容性问题。

**主要功能**:
- ✨ 能力层完全移除对 AllureObserver 的直接依赖
- ✨ 所有 Allure 报告通过 EventBus 自动生成
- ✨ EventBus 支持同步和异步两种事件处理器
- ✨ Database 事件升级为 CorrelatedEvent
- ✨ UoW 事务事件集成 - commit/rollback 自动记录到 Allure
- ✨ 回滚原因追踪（auto/exception/manual）
- ✨ AllurePlugin 标记为 DEPRECATED，规划未来纯插件模式

**详细内容**: 查看完整发布说明 [v3.17.1](docs/releases/v3.17.1.md)

### 新增

#### 事务事件
- 新增 `TransactionCommitEvent` - 事务提交事件类型
- 新增 `TransactionRollbackEvent` - 事务回滚事件类型
- 新增 `UnitOfWork.commit()` 事件发布功能
- 新增 `UnitOfWork.rollback(reason)` 事件发布功能
- 新增 `AllureObserver.handle_transaction_commit_event()` 处理器
- 新增 `AllureObserver.handle_transaction_rollback_event()` 处理器

#### Database 事件升级
- 新增 `DatabaseQueryStartEvent.operation/table` 字段
- 新增 `DatabaseQueryStartEvent/EndEvent/ErrorEvent.create()` 工厂方法
- 新增 EventBus 同步/异步处理器自动检测机制

### 修复
- 修复 EventBus 无条件 await 导致同步处理器报错的问题
- 修复 BearerTokenMiddleware LOGIN 模式未自动注入 http_client 的问题
- 修复能力层直接调用 AllureObserver 导致的紧耦合问题
- 修复 Database/Redis 事件处理器异步/同步不匹配问题
- 修复 `uow` fixture 未传递 `event_bus` 参数导致事务事件无法发布的问题
- 修复 `_publish_event()` 使用异步方法的问题，改为 `_publish_event_sync()`

### 重构
- 重构 Database 客户端事件发布逻辑（统一使用 publish_sync）
- 重构 Redis 客户端移除直接 AllureObserver 调用
- 重构 AllureObserver 删除废弃方法（on_query_start/on_query_end/on_query_error/on_cache_operation）

### 变更
- `UnitOfWork.rollback()` 现在接受 `reason` 参数（默认 "manual"）
- `UnitOfWork.__exit__()` 根据退出情况传递不同的 reason（auto/exception）
- AllurePlugin 标记为 DEPRECATED（推荐使用 EventBus + allure fixture）
- Database 事件升级为 CorrelatedEvent（向后兼容）

### 文档
- 新增 `docs/releases/v3.17.1.md` - 完整版本发布说明（含 UoW 事务事件）
- 新增 `docs/architecture/future_allure_plugin_plans.md` - 未来 Allure 插件纯插件模式规划
- 新增 `docs/architecture/ALLURE_INTEGRATION_OPTIMIZATION_SUMMARY.md` - 实施总结
- 新增 `docs/architecture/ALLURE_INTEGRATION_ANALYSIS.md` - 架构分析
- 新增 `docs/architecture/CAPABILITIES_OPTIMIZATION_PLAN.md` - 优化计划

### 测试
- 新增事务事件测试，2/2 通过
- 框架测试：1307/1307 通过

---

## [3.17.0] - 2025-12-05

### 事件系统重构与可观测性增强

**核心特性**: 完全重构事件系统，支持事件关联、OpenTelemetry 追踪整合、测试隔离，修复 Allure 报告记录问题。

**主要功能**:
- ✨ 事件唯一标识（event_id）与关联系统（correlation_id）
- ✨ OpenTelemetry 自动整合（trace_id/span_id，W3C TraceContext）
- ✨ 测试级 EventBus 隔离（ContextVar 实现）
- ✨ AllureObserver 自动集成（修复 v3.16.0 报告问题）
- ✨ 工厂方法模式（Event.create()）

**详细内容**: 查看完整发布说明 [v3.17.0](docs/releases/v3.17.0.md)

### 新增
- 新增 `Event.event_id` - 事件唯一标识
- 新增 `CorrelatedEvent.correlation_id` - 事件关联 ID
- 新增 `Event.trace_id/span_id` - OpenTelemetry 追踪上下文
- 新增 `Event.create()` 系列工厂方法
- 新增 `set_test_event_bus()` / `get_event_bus()` - 测试隔离 API
- 新增 `allure_observer` fixture - Allure 自动集成

### 修复
- 修复 v3.16.0 Allure 报告无法记录 HTTP 请求/响应的问题
- 修复 Session/Function 级 EventBus 路由失败
- 修复事件关联使用脆弱的字符串匹配

### 文档
- 新增 `docs/architecture/V3.17_EVENT_SYSTEM_REDESIGN.md` - 架构设计文档
- 更新 15 个核心文档到 v3.17.0（新增 1,280+ 行内容）

### 测试
- 新增事件系统完整测试套件，全部通过

---

## [3.16.0] - 2025-12-05

### 五层架构重构 - Layer 4 Bootstrap 引导层

**核心特性**: 解决架构依赖违规问题，引入 Layer 4 Bootstrap 引导层。

**问题背景**:
- v3.14.0 设计规定 `infrastructure/` (Layer 1) 只能依赖 `core/` (Layer 0)
- 但 `bootstrap/`、`providers/`、`runtime/` 需要创建 `capabilities/` (Layer 2) 的实例
- 这导致了 Layer 1 → Layer 2 的依赖违规

**解决方案**:
- 将 `bootstrap/`、`providers/`、`runtime/` 提升为独立的 Layer 4（引导层）
- Layer 4 作为"组装层"，可以合法依赖所有其他层

**架构变更**:

| 层级 | 目录 | 说明 |
|------|------|------|
| **Layer 0** | `core/` | 纯抽象（无第三方依赖） |
| **Layer 1** | `infrastructure/` | 基础设施（config、logging、telemetry、events、plugins） |
| **Layer 2** | `capabilities/` | 能力层（clients、databases、messengers、storages、drivers） |
| **Layer 3** | `testing/` + `cli/` | 门面层（并行） |
| **Layer 4** | `bootstrap/` | **引导层（新增）** - 框架组装和初始化 |
| **横切** | `plugins/` | 插件实现 |

**依赖规则**:
```
Layer 4 (bootstrap/)           ──► 可依赖 Layer 0-3 全部（引导层特权）
Layer 3 (testing/ + cli/)      ──► 可依赖 Layer 0-2（门面层，并行）
Layer 2 (capabilities/)        ──► 可依赖 Layer 0-1
Layer 1 (infrastructure/)      ──► 只能依赖 Layer 0
Layer 0 (core/)                ──► 无依赖（最底层）
plugins/ (横切关注点)           ──► 可依赖任意层级
```

**详细内容**: 查看完整发布说明 [v3.16.0](docs/releases/v3.16.0.md) 和架构设计 [V3.16_LAYER4_BOOTSTRAP_ARCHITECTURE.md](docs/architecture/V3.16_LAYER4_BOOTSTRAP_ARCHITECTURE.md)

### 新增

#### Bootstrap 层 (Layer 4)
- 新增 `bootstrap/` - 独立的引导层目录
- 新增 `bootstrap/bootstrap.py` - 框架初始化入口（Bootstrap 类）
- 新增 `bootstrap/providers.py` - 服务工厂注册（ProviderRegistry、Provider、SingletonProvider）
- 新增 `bootstrap/runtime.py` - 运行时上下文管理（RuntimeContext、RuntimeBuilder）
- 新增 `default_providers()` - 默认服务工厂集合

### 变更

#### 导入路径变更（破坏性变更）
```python
# v3.14.0 导入（旧，已移除）
# from df_test_framework.infrastructure.bootstrap import Bootstrap  # ❌ 不再可用
# from df_test_framework.infrastructure.providers import ProviderRegistry  # ❌ 不再可用
# from df_test_framework.infrastructure.runtime import RuntimeContext  # ❌ 不再可用

# v3.16.0 导入（新）
from df_test_framework.bootstrap import (
    Bootstrap,
    BootstrapApp,
    ProviderRegistry,
    Provider,
    SingletonProvider,
    RuntimeContext,
    RuntimeBuilder,
    default_providers,
)

# 顶层便捷导入（推荐）
from df_test_framework import (
    Bootstrap,
    BootstrapApp,
    ProviderRegistry,
    RuntimeContext,
    RuntimeBuilder,
)
```

### 移除

- ❌ `df_test_framework.infrastructure.bootstrap/` - 已迁移到 `df_test_framework.bootstrap`
- ❌ `df_test_framework.infrastructure.providers/` - 已迁移到 `df_test_framework.bootstrap`
- ❌ `df_test_framework.infrastructure.runtime/` - 已迁移到 `df_test_framework.bootstrap`

**迁移指南**: 将所有 `from df_test_framework.infrastructure.xxx` 导入改为 `from df_test_framework.bootstrap` 或 `from df_test_framework`

### 文档

- 新增 `docs/architecture/V3.16_LAYER4_BOOTSTRAP_ARCHITECTURE.md` - 五层架构完整设计文档
- 新增 `docs/releases/v3.16.0.md` - 完整版本发布说明

### 测试

- ✅ 导入路径测试（新路径可用、旧路径已移除）
- ✅ Bootstrap 功能测试（框架初始化、服务注册、运行时上下文）
- ✅ ProviderRegistry 测试（服务注册/获取、单例模式、默认 Providers）
- ✅ RuntimeContext 测试（服务访问、RuntimeBuilder、上下文管理）
- ✅ 核心测试 100% 通过

---

## [3.14.0] - 2025-12-03

### 🔧 Hotfix (2025-12-04)

**修复 AsyncHttpClient 拦截器加载失败问题**:
- 🐛 修复 `_load_interceptors_from_config()` 使用错误属性名 `config.paths` 的 bug
- ✅ 改为正确检查 `include_paths` 和 `exclude_paths` 属性（与同步 HttpClient 保持一致）
- 📝 新增详细技术文档：`docs/troubleshooting/async_http_client_interceptor_issue.md`

**影响**: 修复前所有使用配置驱动的 AsyncHttpClient 拦截器都无法工作，导致 401 签名验证失败。

**详细信息**: 查看 [AsyncHttpClient 拦截器问题排查报告](docs/troubleshooting/async_http_client_interceptor_issue.md)

---

### 企业级平台架构升级

**核心特性**: 四层架构 + 横切关注点设计，统一中间件系统，可观测性融合。

**架构变更**:

| 层级 | 目录 | 说明 |
|------|------|------|
| **Layer 0** | `core/` | 纯抽象（middleware、context、events、protocols）- 无第三方依赖 |
| **Layer 1** | `infrastructure/` | 基础设施（config、providers、runtime、bootstrap、telemetry、plugins） |
| **Layer 2** | `capabilities/` | 能力层（clients、databases、messengers、storages、drivers） |
| **Layer 3** | `testing/` + `cli/` | 接口层（并行） |
| **横切** | `plugins/` | 插件实现（不在层级中） |

**主要功能**:
- 🧅 **统一中间件系统**: `Interceptor` → `Middleware`（洋葱模型）
- 📡 **可观测性融合**: `Telemetry` = Tracing + Metrics + Logging
- 🔗 **上下文传播**: `ExecutionContext` 贯穿全链路
- 📢 **事件驱动**: `EventBus` 发布/订阅模式
- 📁 **目录重组**: 四层架构，职责清晰

**详细内容**: 查看完整发布说明 [v3.14.0](docs/releases/v3.14.0.md)

### 新增

#### Core 层 (Layer 0)
- 新增 `core/protocols/` - 协议定义（IHttpClient、ITelemetry、IEventBus、IPluginManager 等）
- 新增 `core/middleware/` - 统一中间件系统（Middleware、MiddlewareChain、BaseMiddleware）
- 新增 `core/context/` - 上下文传播（ExecutionContext、get_or_create_context）
- 新增 `core/events/` - 事件类型（HttpRequestEndEvent、DatabaseQueryEndEvent 等）
- 新增 `core/exceptions.py` - 异常体系迁移
- 新增 `core/types.py` - 类型定义迁移

#### Infrastructure 层 (Layer 1)
- 新增 `infrastructure/plugins/` - 插件系统（HookSpecs、PluggyPluginManager）
- 新增 `infrastructure/telemetry/` - 可观测性实现（Telemetry、NoopTelemetry）
- 新增 `infrastructure/events/` - 事件总线实现（EventBus）
- 新增 `infrastructure/context/carriers/` - 上下文载体（HttpContextCarrier、GrpcContextCarrier、MqContextCarrier）

#### Capabilities 层 (Layer 2)
- 新增 `capabilities/` - 能力层统一目录
- 新增 `capabilities/clients/http/middleware/` - HTTP 中间件
  - `SignatureMiddleware` - 签名中间件
  - `BearerTokenMiddleware` - Bearer Token 认证
  - `RetryMiddleware` - 重试中间件
  - `LoggingMiddleware` - 日志中间件
  - `HttpTelemetryMiddleware` - 可观测性中间件

#### Plugins (横切关注点)
- 新增 `plugins/builtin/monitoring/` - 监控插件（MonitoringPlugin）
- 新增 `plugins/builtin/reporting/` - 报告插件（AllurePlugin）

### 迁移指南

详见 [v3.13 到 v3.14 迁移指南](docs/migration/v3.13-to-v3.14.md)

**快速迁移检查清单**:
- [ ] `Interceptor` → `Middleware` 重命名
- [ ] 调整中间件优先级值（反转：priority 数字越小越先执行）
- [ ] 异步测试添加 `@pytest.mark.asyncio`
- [ ] `extensions/` → `plugins/`（插件实现）

### 文档

- 新增 `docs/architecture/V3.14_ENTERPRISE_PLATFORM_DESIGN.md` - 架构设计文档
- 新增 `docs/migration/v3.13-to-v3.14.md` - 迁移指南
- 新增 `docs/releases/v3.14.0.md` - 完整版本发布说明

### 测试

- ✅ 新增 `tests/core/test_middleware.py` - 中间件系统完整单元测试（14个测试，100%通过）
  - 测试 MiddlewareChain 基本功能
  - 测试洋葱模型执行顺序
  - 测试状态共享、异常处理、中止逻辑
  - 测试 SyncMiddleware 和 @middleware 装饰器
  - 测试重试中间件等复杂场景
- ✅ 新增 `tests/core/test_events.py` - 事件总线完整单元测试（20个测试，100%通过）
  - 测试 EventBus 订阅/发布机制
  - 测试 @bus.on() 装饰器
  - 测试全局订阅和取消订阅
  - 测试异常处理和异步并发
  - 测试框架内置事件（HttpRequestEndEvent、DatabaseQueryEndEvent）
  - 测试实际应用场景（日志记录、指标收集）
- ✅ 新增 `tests/core/test_context.py` - 上下文传播完整单元测试（22个测试，100%通过）
  - 测试 ExecutionContext 创建和子上下文
  - 测试上下文不可变性和链式调用
  - 测试 baggage、user_id、tenant_id 等属性
  - 测试上下文管理器（with_context 和 with_context_async）
  - 测试上下文传播和隔离
  - 测试嵌套上下文和流式构建

- ✅ 新增 `tests/migration/test_v3_13_to_v3_14_examples.py` - 迁移指南示例验证（20个测试，19通过，1跳过）
  - 验证所有导入路径迁移示例
  - 验证向后兼容性和废弃警告
  - 验证中间件迁移示例
  - 验证事件系统、上下文传播、插件系统迁移
- ✅ 新增 `tests/README.md` - 测试目录结构说明文档
  - 说明四层架构镜像结构
  - 测试分类和命名规范
  - 运行测试指南

**测试覆盖率**: v3.14.0 核心功能测试覆盖率显著提升
- 中间件系统: 14个测试用例（100%通过）
- 事件总线: 20个测试用例（100%通过）
- 上下文传播: 22个测试用例（100%通过）
- 迁移验证: 20个测试用例（19通过，1跳过）
- **总测试数: 1426个** (+172个新增，包括重组后的测试）
- **通过率: 100%**（排除需要外部服务的测试）

### 测试目录重组

- ✨ 创建镜像 src/ 的四层架构测试目录
  - `tests/core/` - Layer 0 核心抽象层测试
  - `tests/infrastructure/` - Layer 1 基础设施层测试
  - `tests/capabilities/` - Layer 2 能力层测试
    - `capabilities/clients/` - HTTP/GraphQL/gRPC客户端测试
    - `capabilities/databases/` - 数据库测试
    - `capabilities/messengers/` - 消息队列测试
  - `tests/plugins/` - 横切关注点插件测试
  - `tests/migration/` - 迁移验证测试
- ✅ 旧目录保留以确保向后兼容（将在 v3.16.0 清理）

### 代码集成（2025-12-04）

**核心特性**: 将新架构系统完全集成到现有代码中。

**主要功能**:
- ✨ HttpClient/AsyncHttpClient 集成 MiddlewareChain，新增 `middlewares` 参数和 `.use()` 方法
- ✨ Database/UnitOfWork 集成 EventBus，自动发布查询事件
- ✨ Kafka/RabbitMQ/RocketMQ 集成 EventBus，自动发布消息事件
- ✅ 完全向后兼容，旧 API 仍可使用但会触发废弃警告

**详细内容**: 查看完整发布说明 [v3.14.0](docs/releases/v3.14.0.md)

### 新增
- 新增 `HttpClient.use()` - 链式添加中间件
- 新增 `HttpClient.request_with_middleware()` - 使用新中间件系统发送请求
- 新增 `Database(event_bus=...)` - 支持事件总线集成
- 新增 `UnitOfWork(event_bus=...)` - 支持事务事件
- 新增 `KafkaClient(event_bus=...)` - 支持消息事件
- 新增 `RabbitMQClient(event_bus=...)` - 支持消息事件
- 新增 `RocketMQClient(event_bus=...)` - 支持消息事件

### 变更
- 变更主入口异常类导入路径（从 `common` 改为 `core`）
- 标记 `interceptors` 模块为废弃（v3.16.0 移除）

### 文档
- 新增 `docs/migration/v3.14-migration-status.md` - 迁移状态追踪文档
- 更新 `docs/releases/v3.14.0.md` - 添加代码集成说明

### 测试
- ✅ 新增集成测试，验证 MiddlewareChain 和 EventBus 集成
- ✅ 测试通过: 1464 passed, 40 skipped

### 兼容性与废弃

- ⚠️ **废弃警告**: `common/` 和 `extensions/` 模块（v3.16.0 移除）
- ⚠️ **废弃警告**: `interceptors` 模块（v3.16.0 移除）

### 文档和模板全面更新（2025-12-04）

**P0+P1+P2 文档更新完成**

#### 新增核心指南
- 新增 `docs/user-guide/QUICK_START_V3.14.md` - v3.14.0 快速开始（5分钟上手）
- 新增 `docs/guides/middleware_guide.md` - 中间件使用指南（600+行，50+示例）
- 新增 `docs/guides/event_bus_guide.md` - EventBus 使用指南
- 新增 `docs/guides/telemetry_guide.md` - Telemetry 可观测性指南
- 新增 `docs/migration/v3.14-docs-templates-audit.md` - 文档模板审计报告

#### 全面术语统一
- 更新 11 个用户指南文档（USER_MANUAL、BEST_PRACTICES 等）
- 更新 9 个脚手架模板文件
- 全局替换: "拦截器" → "中间件"、"Interceptor" → "Middleware"
- 统一版本号: v3.12.0/v3.11.0 → v3.14.0
- 更新导入路径到新架构

#### 变更统计
- 新增文档: 5 个（1650+ 行）
- 更新文档: 11 个
- 更新模板: 9 个
- 总变更: 25+ 文件，2000+ 行

---

## [3.13.0] - 2025-12-03

### UnitOfWork 配置驱动架构重构

**核心特性**: UnitOfWork 支持配置驱动，无需继承或覆盖 fixture。

**重大变更**:
- 🗑️ 移除 `BaseUnitOfWork`（直接使用 `UnitOfWork`）
- ✨ 新增 `TestExecutionConfig.repository_package` 配置
- ✨ `uow` fixture 支持配置驱动，自动读取 `TEST__REPOSITORY_PACKAGE`
- ✨ Repository 自动发现通过配置启用

**使用方式变更**:

| 版本 | 方式 | 代码量 |
|------|------|--------|
| v3.12.x | 继承 `BaseUnitOfWork` + 覆盖 `uow` fixture | ~166 行 |
| v3.13.0 | 配置 `TEST__REPOSITORY_PACKAGE` | 1 行 |

**配置示例**:
```env
# .env
TEST__REPOSITORY_PACKAGE=my_project.repositories
```

**测试代码**:
```python
def test_example(uow):
    uow.users.create({"name": "test"})  # ✅ 自动发现 Repository
    # 测试结束自动回滚
```

**详细内容**: 查看完整发布说明 [v3.13.0](docs/releases/v3.13.0.md)

---

## [3.12.1] - 2025-12-02

### 统一测试数据保留配置

**核心特性**: `should_keep_test_data()` 支持 Settings 配置，UoW 和 cleanup 共享统一配置。

**主要变更**:
- ✨ `TestExecutionConfig` 新增 `keep_test_data` 字段
- ✨ `should_keep_test_data()` 改用 `get_settings()` 读取配置
- ✨ `uow` fixture 改用 `should_keep_test_data()` 统一检查
- 🗑️ 移除直接的 `os.getenv("KEEP_TEST_DATA")` 调用

**配置方式**:

| 优先级 | 方式 | 用法 |
|-------|-----|------|
| 1 | 测试标记 | `@pytest.mark.keep_data` |
| 2 | 命令行参数 | `pytest --keep-test-data` |
| 3 | Settings 配置 | `.env` 中 `TEST__KEEP_TEST_DATA=1` |

**注意**: `.env` 文件格式为 `TEST__KEEP_TEST_DATA=1`（双下划线表示嵌套），系统环境变量需要 `APP_` 前缀。

**详细内容**: 查看完整发布说明 [v3.12.1](docs/releases/v3.12.1.md)

---

## [3.12.0] - 2025-12-02

### Testing 模块架构重构

**核心特性**: 基于 V3 架构设计优化 testing 模块组织结构。

**主要变更**:
- ✨ 创建 `testing/reporting/allure/` 子系统（非扁平设计）
- ✨ 统一 `testing/debugging/` 调试工具模块
- ✨ 迁移 `TracingInterceptor` 到 `infrastructure/tracing/interceptors/`
- ✨ AllureObserver 增强：并发请求支持、异常安全、GraphQL/gRPC 协议支持
- ✨ 新增 `GrpcTracingInterceptor` 分布式追踪拦截器
- 🗑️ 删除分散的 `testing/observers/` 目录

**详细内容**: 查看完整发布说明 [v3.12.0](docs/releases/v3.12.0.md)

### 变更

#### 模块重组
- `testing/reporting/allure/` - Allure 报告子系统（observer、helper、fixtures）
- `testing/debugging/` - 调试工具统一（http、database、pytest_plugin）
- `infrastructure/tracing/interceptors/` - 追踪拦截器归位

#### 导入路径变更
```python
# Allure（新路径）
from df_test_framework.testing.reporting.allure import AllureObserver, AllureHelper

# Debug（新路径）
from df_test_framework.testing.debugging import HTTPDebugger, DBDebugger

# Tracing（新路径）
from df_test_framework.infrastructure.tracing.interceptors import (
    TracingInterceptor,       # HTTP 追踪
    GrpcTracingInterceptor,   # gRPC 追踪（新增）
)
```

### 移除
- 移除 `testing/observers/` 目录
- 移除 `testing/plugins/allure.py`（迁移至 reporting/allure/helper.py）
- 移除 `testing/plugins/debug.py`（迁移至 debugging/pytest_plugin.py）
- 移除 `clients/http/interceptors/tracing.py`（迁移至 infrastructure/）

### 文档
- 新增 `docs/releases/v3.12.0.md` - 完整版本发布说明
- 新增 `docs/architecture/TESTING_MODULE_OPTIMIZATION.md` - 架构优化方案

### 新增
- 新增 `GrpcTracingInterceptor` - gRPC 分布式追踪拦截器
- 新增 `AllureObserver.on_graphql_request_start/end` - GraphQL 协议支持
- 新增 `AllureObserver.on_grpc_call_start/end` - gRPC 协议支持
- 新增 `AllureObserver` 可配置截断参数：`max_body_length`、`max_value_length`、`max_sql_length`

### 修复
- 修复 AllureObserver 并发请求上下文被覆盖问题（P0）
- 修复 AllureObserver 异常时上下文未正确关闭问题（P0）

### 测试
- 全部 1134 个测试通过（新增 24 个）

---

## [3.11.1] - 2025-11-28

### 测试数据清理模块重构

**核心特性**: 统一的测试数据清理机制，支持 `--keep-test-data` 配置控制。

**主要功能**:
- ✨ `should_keep_test_data()` - 统一配置检查函数（标记 > CLI参数 > 环境变量）
- ✨ `CleanupManager` - 清理管理器基类，自动检查配置
- ✨ `SimpleCleanupManager` - 回调函数模式清理器
- ✨ `ListCleanup` - 列表式清理器，继承自 list
- ✨ `DataGenerator.test_id()` - 类方法，无需实例化生成测试数据标识符

**详细内容**: 查看完整发布说明 [v3.11.1](docs/releases/v3.11.1.md)

### 新增

#### 清理模块 (`testing/fixtures/cleanup.py`)
- 新增 `should_keep_test_data(request)` - 检查是否保留测试数据
- 新增 `CleanupManager` - 抽象基类，子类实现 `_do_cleanup()`
- 新增 `SimpleCleanupManager` - 通过 `register_cleanup(type, callback)` 注册清理函数
- 新增 `ListCleanup` - 继承 list，提供 `should_keep()`/`should_do_cleanup()` 方法

#### 数据生成器增强
- 新增 `DataGenerator.test_id(prefix)` 类方法 - 无需实例化，直接生成测试标识符
- 格式: `{prefix}{timestamp14}{random6}`，如 `TEST_ORD20251128123456789012`

### 移除
- 移除旧的 `test_data_cleaner` fixture（已由新 API 替代）

### 文档
- 新增 `docs/releases/v3.11.1.md` - 完整版本发布说明
- 新增 `docs/guides/test_data_cleanup.md` - 使用指南
- 更新 `CLAUDE.md` - 数据清理示例代码

### 测试
- 新增清理模块测试：41 个（全部通过）
- 新增 `DataGenerator.test_id()` 测试：3 个（全部通过）
- 总计：78 个相关测试通过

---

## [3.11.0] - 2025-11-26

### Phase 2 完整交付 (P2.5-P2.8)

**核心特性**: 协议扩展 + Mock 工具增强 + 测试覆盖率提升

**主要功能**:
- ✨ GraphQL 客户端 (P2.5) - 支持 Query/Mutation/Subscription、QueryBuilder、批量操作、文件上传
- ✨ gRPC 客户端 (P2.6) - 支持所有 RPC 模式、拦截器、健康检查
- ✨ DatabaseMocker (P2.7) - 数据库操作 Mock，SQL 标准化、调用历史
- ✨ RedisMocker (P2.7) - Redis 操作 Mock，支持 fakeredis 或简单内存实现
- ✅ 新增 104+ 个单元测试 (P2.8)
- ✅ 测试总数达到 1078 个，通过率 98.9%

**详细内容**: 查看完整发布说明 [v3.11.0](docs/releases/v3.11.0.md)

### 新增

#### GraphQL 客户端
- 新增 `GraphQLClient` - 基于 httpx 的 GraphQL 客户端
- 新增 `QueryBuilder` - 流畅的 GraphQL 查询构建器
- 新增 `GraphQLRequest/Response/Error` 数据模型
- 支持批量查询、文件上传

#### gRPC 客户端
- 新增 `GrpcClient` - 通用 gRPC 客户端
- 新增 `LoggingInterceptor/MetadataInterceptor/RetryInterceptor/TimingInterceptor` 拦截器
- 新增 `GrpcResponse[T]/GrpcError/GrpcStatusCode` 数据模型
- 新增 `ChannelOptions` 通道配置
- 支持所有 RPC 调用模式（Unary/Server Streaming/Client Streaming/Bidirectional）

#### Mock 工具增强
- 新增 `DatabaseMocker` - 数据库操作 Mock 工具
- 新增 `RedisMocker` - Redis 操作 Mock 工具
- RedisMocker 支持 fakeredis 或降级到简单内存实现
- DatabaseMocker 支持 SQL 标准化、调用历史、断言辅助

### 测试
- 新增 GraphQL 客户端测试：37 个（全部通过）
- 新增 gRPC 客户端测试：39 个通过，1 个跳过
- 新增 Mock 工具测试：28 个通过，1 个跳过
- 总测试数：1078 个
- 测试通过率：98.9% (1036/1047)
- 测试覆盖率：57.02%

### 文档
- 新增 `docs/releases/v3.11.0.md` - 完整版本发布说明
- 更新 `CHANGELOG.md` - Phase 2 完整摘要

---

## [3.10.0] - 2025-11-26

### 存储客户端 - LocalFile + S3 + 阿里云OSS

**核心特性**: 统一的文件存储抽象，支持本地文件、AWS S3、阿里云OSS三种存储方式。

**主要功能**:
- LocalFileClient - 本地文件系统存储，支持元数据、路径安全验证
- S3Client - 基于 boto3 的 AWS S3 对象存储，支持 MinIO
- OSSClient - 基于 oss2 的阿里云 OSS 对象存储，支持 STS、CRC64、内网访问
- 统一的 CRUD API（upload/download/delete/list/copy）
- 分片上传支持（大文件自动分片）
- 预签名 URL 生成
- 完整的 pytest fixtures（local_file_client、s3_client、oss_client）

**详细内容**: 查看完整使用指南 [storage.md](docs/guides/storage.md)

### 测试覆盖
- 75个单元测试，全部通过
- LocalFileClient 测试覆盖率 95%+
- S3Client 测试覆盖率 95%+
- OSSClient 测试覆盖率 95%+

### OpenTelemetry 分布式追踪

**核心特性**: 基于 OpenTelemetry 标准的分布式追踪能力，支持 Console/OTLP/Jaeger/Zipkin 导出器。

**主要功能**:
- TracingManager 追踪管理器，支持多导出器配置
- @trace_span/@trace_async_span/@TraceClass 装饰器，零侵入式追踪
- TracingContext 和 Baggage 上下文传播机制
- HTTP 请求追踪拦截器，自动记录请求链路
- 数据库查询追踪集成，记录 SQL 执行详情
- 70个单元测试，覆盖率 95%+

**详细内容**: 查看完整发布说明 [v3.10.0](docs/releases/v3.10.0.md)

### 测试数据工具增强

**核心特性**: 数据加载器和响应断言辅助，提升测试数据处理效率。

**主要功能**:
- JSONLoader/CSVLoader/YAMLLoader 三种数据加载器
- 支持 JSONPath 查询、类型转换、环境变量替换
- ResponseAssertions 响应断言辅助（链式调用 + 静态方法）
- 支持状态码、JSON、响应头、响应时间断言
- pytest 参数化支持

**预置工厂说明**:
- UserFactory/OrderFactory 等 8 个预置工厂已标记为 **示例代码**
- 这些工厂是业务领域特定的，不同项目字段差异大
- **建议**: 项目根据自身需求继承 Factory 基类自定义工厂
- Factory 基类提供 Sequence、LazyAttribute、FakerAttribute 等通用能力

**详细内容**: 查看完整发布说明 [v3.10.0](docs/releases/v3.10.0.md)

### Prometheus 指标监控

**核心特性**: 基于 Prometheus 的应用性能监控（APM），零配置模式。

**主要功能**:
- MetricsManager 指标管理器，支持 Prometheus exporter 和 Pushgateway
- Counter/Gauge/Histogram/Summary 四种指标类型，线程安全
- @count_calls/@time_calls/@track_in_progress 等 6 个装饰器
- HttpMetrics 自动收集 HTTP 请求指标
- DatabaseMetrics 自动收集数据库查询指标
- 零配置模式（无需安装 prometheus_client 即可使用）
- 44个单元测试，全部通过

**详细内容**: 查看完整发布说明 [v3.10.0](docs/releases/v3.10.0.md)

### 文档
- 新增 `docs/guides/storage.md` - 存储客户端完整使用指南
- 新增 `docs/guides/distributed_tracing.md` - 分布式追踪完整使用指南
- 新增 `docs/guides/test_data.md` - 测试数据工具完整使用指南
- 新增 `docs/guides/prometheus_metrics.md` - Prometheus 监控完整使用指南
- 新增 `docs/releases/v3.10.0.md` - 完整版本发布说明
- 新增 `examples/01-basic/storage_usage.py` - 存储客户端使用示例

### 测试覆盖
- 257个新增测试用例，全部通过
- 存储模块: 75个测试，覆盖率 95%+
- 追踪模块: 70个测试，覆盖率 95%+
- 测试数据: 68个测试，覆盖率 90%+
- 指标模块: 44个测试，覆盖率 92%+

---

## [3.9.0] - 2025-11-25

### 消息队列客户端 - Kafka + RabbitMQ + RocketMQ

**核心特性**: 提供三大主流消息队列的统一封装,支持企业级测试场景。

**主要功能**:
- Kafka客户端 (confluent-kafka 1.9.2)，生产性能提升3倍
- RabbitMQ客户端 (pika, AMQP 0-9-1)，支持延迟队列和死信队列
- RocketMQ客户端，支持顺序消息和事务消息
- SSL/TLS 支持，完整的证书认证和 SASL 认证
- 统一的 API 设计，便于切换不同消息队列

**详细内容**: 查看完整发布说明 [v3.9.0](docs/releases/v3.9.0.md)

### 测试覆盖
- 68个单元测试和集成测试
- Kafka测试覆盖率 96.32%
- RabbitMQ测试覆盖率 94.85%
- RocketMQ测试覆盖率 91.47%

---

## [3.8.0] - 2025-11-25

### AsyncHttpClient - 异步HTTP客户端

**核心特性**: 基于 httpx.AsyncClient 实现的异步HTTP客户端，性能提升 10-50 倍。

**主要功能**:
- 并发性能提升 40 倍 (100个请求从 20秒 降至 0.5秒)
- 内存占用降低 90%，CPU占用降低 75%
- 默认启用 HTTP/2 支持，连接复用
- 完全兼容现有拦截器，无需修改
- 适用场景: 批量操作、压力测试、微服务调用、数据迁移

**详细内容**: 查看完整发布说明 [v3.8.0](docs/releases/v3.8.0.md)

### 修复
- 更新 CLI 生成模板的版本引用 (v3.7 → v3.8)
- 重构 Repository 测试从 MockDatabase 到 MockSession

### 依赖变更
- 新增 pytest-asyncio>=1.3.0 (异步测试支持)

---

## [3.7.0] - 2025-11-24

### Unit of Work 模式 - 现代化数据访问架构

**核心特性**: 统一管理事务边界和 Repository 生命周期，解决 v3.6.2 事务隔离失效问题。

**主要功能**:
- 新增 BaseUnitOfWork 类，支持 Repository 懒加载和缓存
- 新增 uow fixture，替代 db_transaction，确保所有操作在同一事务中
- 所有 Repository 共享同一个 Session，事务隔离正确
- 新增熔断器 (Circuit Breaker) 模块，防止级联失败
- 新增安全最佳实践指南 (8000+字)
- 集成 CI/CD 依赖漏洞扫描 (Safety/Bandit/pip-audit)

**详细内容**: 查看完整发布说明 [v3.7.0](docs/releases/v3.7.0.md)

### 测试覆盖
- 19个 UnitOfWork 单元测试，覆盖率 94.52%
- 26个熔断器单元测试，覆盖率 98.40%

---

## [3.6.2] - 2025-11-24

### 测试数据清理控制机制

**核心特性**: 增强 db_transaction fixture 的数据清理控制，提供灵活的清理策略。

**主要功能**:
- 默认强制回滚，确保测试数据不残留
- 支持三种控制方式：命令行参数、测试标记、环境变量
- 移除 TransactionalDatabase 包装器，直接返回 SQLAlchemy Session
- 新增框架架构说明文档

**详细内容**: 查看完整发布说明 [v3.6.2](docs/releases/v3.6.2.md)

### 测试
- 17个集成测试，覆盖所有数据清理场景

---

## [3.6.1] - 2025-11-23

### 日志系统修复 + Loguru/Pytest 深度集成

**核心特性**: 修复日志传播导致的重复输出问题，增强 Loguru 和 pytest 集成。

**主要功能**:
- 修复日志传播链导致的重复输出问题
- 新增 LoguruHandler 集成 Loguru 到 Python logging
- 新增 LoguruPytestHandler 集成到 pytest 日志系统
- 新增 pytest_configure_logging hook 自动配置

**详细内容**: 查看完整发布说明 [v3.6.1](docs/releases/v3.6.1.md)

### 测试
- 26个日志系统单元测试

---

## [3.6.0] - 2025-11-22

### Decimal 零配置序列化 + HttpClient Pydantic 支持

**核心特性**: Decimal 类型的 JSON 序列化零配置支持，HttpClient 增强 Pydantic 集成。

**主要功能**:
- 全局 Decimal JSON 编码器，自动转换为字符串
- HttpClient 原生支持 Pydantic 模型序列化/反序列化
- 新增 DecimalJSONEncoder 和 DecimalJSONProvider (Flask扩展)
- 修复 LogConfig 死循环问题

**详细内容**: 查看完整发布说明 [v3.6.0](docs/releases/v3.6.0.md)

### 测试
- 22个单元测试，全部通过

---

## [3.5.0] - 2025-11-21

### 核心特性
- Repository基类：基础的CRUD能力
- 查询构建器：支持链式调用和复杂查询
- 数据库工厂：自动管理Session生命周期
- 事务支持：上下文管理器模式
- SQLAlchemy 2.0 原生支持

### 依赖变更
- SQLAlchemy >= 2.0.0

---

## [3.4.0] - 2025-11-20

### 核心特性
- HttpClient：统一的HTTP客户端接口
- 拦截器链：支持请求/响应拦截
- 重试机制：指数退避 + 抖动
- Mock支持：MockHttpClient 测试辅助

### 依赖变更
- httpx >= 0.27.0
- tenacity >= 8.5.0

---

## [3.3.0] - 2025-11-19

### 核心特性
- Factory模式：测试数据生成
- Faker集成：真实感测试数据
- 序列和懒加载：灵活的数据生成

### 依赖变更
- Faker >= 30.8.2

---

## [3.2.0] - 2025-11-18

### 核心特性
- 日志系统：LogConfig配置化管理
- Loguru集成：更优雅的日志输出
- 多输出支持：控制台、文件、JSON、Syslog

### 依赖变更
- loguru >= 0.7.3

---

## [3.1.0] - 2025-11-17

### 核心特性
- BaseModel：统一的数据模型基类
- 配置系统：环境变量管理
- 验证器：Pydantic集成

### 依赖变更
- pydantic >= 2.10.3
- pydantic-settings >= 2.7.0

---

## [3.0.0] - 2025-11-16

### 重大变更
- 项目重构：模块化架构
- Python 3.12+：现代化类型注解
- pytest 8.0+：最新测试框架

### 核心特性
- clients/：HTTP、数据库客户端
- infrastructure/：基础设施层
- testing/：测试工具集

---

## [2.x.x] - Legacy 版本

早期版本的变更记录已归档。详见: [CHANGELOG_V2.md](CHANGELOG_V2.md)
