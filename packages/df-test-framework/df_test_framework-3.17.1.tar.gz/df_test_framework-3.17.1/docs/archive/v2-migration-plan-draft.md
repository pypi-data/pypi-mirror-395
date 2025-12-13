# DF 测试框架 v2 架构改造方案

> 目标：在保持可复用性的前提下，构建一个现代化、可插拔、可维护的自动化测试框架，让业务测试项目的集成体验更顺滑。

## 核心设计理念

- **框架 = 能力平台**：负责提供配置模型、日志策略、资源 provider、Pytest 插件等基础设施，但默认“无副作用”。
- **项目 = 声明式扩展**：业务项目只需要定义自己的配置子类和少量 bootstrap 代码即可接入整个能力面板。
- **可组合 / 可扩展**：所有关键点（配置、日志、资源、插件）都要暴露标准接口，允许替换实现或叠加插件。

## 模块划分

```
df_test_framework/
├── bootstrap/         # 启动流程与组合器
├── config/            # 设置模型、加载器、源
├── logging/           # 日志策略接口及默认策略
├── runtime/           # RuntimeContext 与 Provider 容器
├── providers/         # HTTP/DB/Redis 等资源提供者
├── fixtures/          # Pytest 插件入口
├── extensions/        # Allure、性能监控等可选扩展
└── samples/           # 示例/脚手架
```

## 启动流程（Bootstrap）

1. 选择/注册配置模型 (`with_settings`)。
2. 选择日志策略 (`with_logging`)。
3. 注册扩展/插件 (`with_plugin`)。
4. 调用 `build().run()`：
   - 加载配置（通过 ConfigPipeline）。
   - 初始化日志（使用 LoggerStrategy）。
   - 实例化 RuntimeContext（含依赖容器）。
   - 返回 RuntimeContext（供应用/pytest 使用）。

## 配置系统

- `FrameworkSettings`：基础配置 (http/db/redis/test/logging...)，基于 Pydantic BaseSettings。
- `ConfigSource` 协议：统一封装 env、dotenv、json、CLI、自定义源。
- `ConfigPipeline`：组合多个 source，支持优先级与覆盖。
- `configure_settings()` -> 在 Bootstrap 内部调用，支持多命名空间。
- `create_settings(settings_cls, overrides)` -> 用于测试或局部覆盖。

## 日志系统

- `LoggerStrategy` 协议：`configure(settings, context) -> Logger`。
- 默认实现：
  - `StructuredLoggerStrategy`（JSON + Loguru）。
  - `ConsoleLoggerStrategy`（彩色控制台）。
- 项目可自定义策略，例如接入企业日志或其它 logging 框架。
- `is_logger_configured()` 用于判定是否已经配置；框架内部不主动设置 handler。

## Runtime 与 Provider

- `RuntimeContext`：不可变对象，暴露：
  - `settings` 实例。
  - `logger`（由策略提供）。
  - `resolve(provider_key)` 或快捷方法 `http_client() / database()`。
  - 生命周期控制：`close()`。
- Provider 接口：负责资源创建 & 缓存，支持作用域（global / session / per-call）。
- 内置 Provider：
  - `HttpClientProvider`
  - `DatabaseProvider`
  - `RedisProvider`
  - `AllureProvider`（可选）

## Pytest 集成

- `pytest_plugins = ["df_test_framework.fixtures.core"]`。
- 框架在 `pytest_configure` 时拉起 Bootstrap（读取环境变量/ini 决定 settings 类、日志策略等）。
- Fixtures 通过 RuntimeContext 提供依赖：
  ```python
  @pytest.fixture(scope="session")
  def runtime():
      return get_runtime()

  @pytest.fixture(scope="session")
  def http_client(runtime):
      return runtime.http_client()
  ```
- 项目可在 `conftest.py` 手动创建 Bootstrap，或通过 CLI 设置指向自己的配置类。

## 扩展机制

- 使用 `pluggy` 定义 hook：
  - `df_framework_load_config_sources`
  - `df_framework_register_providers`
  - `df_framework_post_bootstrap`
- 内置扩展：Allure、性能监控、UI。
- 项目通过 entry point 或显式 `with_plugin()` 挂载新扩展。

## 迁移策略

1. **搭建新目录结构**，实现核心模块骨架。
2. **移植现有能力**（HTTP/DB/Redis/装饰器等）到新 provider / runtime。
3. **重写 Pytest fixtures**，保证零副作用。
4. **提供示例项目**（Gift Card）使用新 Bootstrap。
5. **保留兼容层**（旧 API 警告后转调新实现），帮助渐进迁移。
6. **完善文档**：快速开始、定制指南、插件开发。
7. **全量测试**：框架自测 + Gift Card 项目回归。

## 下一步

- [x] 建立 bootstrap/config/logging/runtime 基础代码。
- [x] 迁移核心模块与资源 provider。
- [x] 重构现有项目使用新接口。
- [x] 清理旧实现、发布 v2.0.0 迁移指南。
- [x] 实现插件体系 & CLI 工具。
- [x] 更新文档、示例与验证编译通过。
