# DF Test Framework 文档中心

> 版本：v3.17.0 · 最近更新：2025-12-05
> 现代化 Python 测试自动化框架的官方知识库。基于五层架构 + 事件驱动 + 可观测性设计。

---

## ⚡ 快速导航

**新手？** → [核心文档导航 (ESSENTIAL_DOCS.md)](ESSENTIAL_DOCS.md) - 只看最有价值的 8 个文档！

**2 分钟极简上手**:
1. [快速参考](user-guide/QUICK_REFERENCE.md) - 速查命令和 Fixtures
2. [快速开始](user-guide/QUICK_START.md) - 跑通第一个测试

---

## 🚀 入口指南
- [安装指南](getting-started/installation.md) — 统一使用 Python 3.12+ 与 uv，列出了所有可选依赖
- [快速入门](getting-started/quickstart.md) — `df-test init` 脚手架，5 分钟完成首个项目
- [30 分钟教程](getting-started/tutorial.md) — 从零实现第一个 API 测试用例
- [快速开始](user-guide/QUICK_START.md) — 5 分钟完成第一个测试

阅读顺序建议：**安装 → 快速入门 → 教程 → 用户手册**。

---

## 📖 用户指南

### v3.17 新特性 ⚡ (2025-12-05)
- **[v3.17.0 发布说明](releases/v3.17.0.md)** ⭐ — 事件系统重构 + EventBus 与 Allure 深度整合
- **事件系统增强** — 事件关联（correlation_id）、OpenTelemetry 追踪注入、测试隔离
- **[事件系统架构设计](architecture/V3.17_EVENT_SYSTEM_REDESIGN.md)** — 完整设计文档
- **[EventBus 使用指南](guides/event_bus_guide.md)** — 发布/订阅、事件驱动

### v3.16 新特性 (2025-12-05)
- **[v3.16.0 发布说明](releases/v3.16.0.md)** ⭐ — Layer 4 Bootstrap 引导层架构重构
- **五层架构升级** — Layer 0 (core/) → Layer 4 (bootstrap/)
- **[五层架构设计](architecture/V3.16_LAYER4_BOOTSTRAP_ARCHITECTURE.md)** — 完整架构设计
- **破坏性变更** — Bootstrap 导入路径变更（infrastructure → bootstrap）

### v3.14 新特性 (2025-12-03)
- **[v3.14.0 发布说明](releases/v3.14.0.md)** ⭐ — 企业级平台架构升级
- **[中间件使用指南](guides/middleware_guide.md)** ⭐ — 统一中间件系统（600+行，50+示例）
- **[Telemetry 可观测性指南](guides/telemetry_guide.md)** — Tracing + Metrics + Logging
- **Interceptor → Middleware 迁移** — [迁移指南](migration/v3.13-to-v3.14.md)

### v3.12 新特性
- **[v3.12.1 发布说明](releases/v3.12.1.md)** — 统一测试数据保留配置（Settings 支持）
- **[v3.12.0 发布说明](releases/v3.12.0.md)** — Testing 模块架构重构
- **[分布式追踪指南](guides/distributed_tracing.md)** — 包含 GrpcTracingInterceptor
- **AllureObserver 增强** — 并发请求支持、GraphQL/gRPC 协议支持

### v3.11 新特性
- **[v3.11.1 发布说明](releases/v3.11.1.md)** — 测试数据清理模块重构
- **[测试数据清理指南](guides/test_data_cleanup.md)** ⭐ — CleanupManager、ListCleanup 使用指南
- **[GraphQL 客户端指南](guides/graphql_client.md)** — GraphQL 查询、变更、订阅
- **[gRPC 客户端指南](guides/grpc_client.md)** — gRPC 所有 RPC 模式支持

### v3.9 新特性
- **[消息队列使用指南](guides/message_queue.md)** ⭐ — Kafka/RabbitMQ/RocketMQ完整指南
- **[消息队列示例](../examples/07-message-queue/)** — 三大消息队列实际使用示例

### v3.8 新特性
- **[AsyncHttpClient 使用指南](guides/async_http_client.md)** ⭐ — 异步HTTP客户端，性能提升40倍
- **[AsyncHttpClient API 参考](api/async_http_client.md)** — 完整API文档和方法签名
- **[性能对比分析](performance/async_vs_sync.md)** — 同步vs异步性能测试
- **[AsyncHttpClient 架构设计](async_http_client_design.md)** — 设计决策和拦截器兼容性

### v3.10 新特性 ⚡ (开发中)
- **[存储客户端使用指南](guides/storage.md)** ⭐ — LocalFile/S3/OSS 完整指南
- **[分布式追踪使用指南](guides/distributed_tracing.md)** ⭐ — OpenTelemetry 完整指南
- **[测试数据工具指南](guides/test_data.md)** ⭐ — 数据加载器和断言辅助
- **[Prometheus 监控指南](guides/prometheus_metrics.md)** ⭐ — 应用性能监控（APM）

### 通用指南
- [快速参考](user-guide/QUICK_REFERENCE.md) — 常用命令、Fixtures、调试速查表
- [使用手册](user-guide/USER_MANUAL.md) — 按场景拆分的操作说明
- [最佳实践](user-guide/BEST_PRACTICES.md) — 目录规范、数据管理、CI 建议
- [安全最佳实践](user-guide/security-best-practices.md) — 敏感信息管理、SQL注入防护、加密安全
- [FRAMEWORK_CAPABILITIES.md](FRAMEWORK_CAPABILITIES.md) — 各层能力、调试手段、扩展策略
- [测试开发指南](user-guide/testing-development.md) — 框架单元测试与覆盖率管理
- 专题：CI/CD、代码生成、UI 测试等请查看 `user-guide/` 子目录

---

## 🏗️ 架构与设计
- [架构总览](architecture/overview.md) — v3 五层架构、能力层映射
- [V3 架构设计](architecture/V3_ARCHITECTURE.md) — 设计原则、目录约定、能力矩阵
- [V3 实施指南](architecture/V3_IMPLEMENTATION.md) — 重构步骤与验证清单
- [ARCHITECTURE_AUDIT.md](architecture/ARCHITECTURE_AUDIT.md) — 文档与实现一致性验证
- [FUTURE_ENHANCEMENTS.md](architecture/FUTURE_ENHANCEMENTS.md) — 已排期的增强能力
- 历史方案参见 `architecture/archive/`（草案、评审、旧版本）

---

## 📚 API 参考
- [API 索引](api-reference/README.md) — 依照层级梳理 clients / drivers / databases / testing / extensions
- [模型定义](../src/df_test_framework/models/) — Pydantic 请求、响应与通用类型
- [工具函数](../src/df_test_framework/utils/) — 断言工具、性能计时、数据构造
- 旧版(v2) API 文档已转入 `api-reference/core.md`、`patterns.md` 等文件，仅作历史参考

---

## 🧰 CLI 与脚手架
- `df-test init` — 生成标准化项目骨架（API / UI / Full / CI 模板）
- `df-test gen` — 批量生成测试、Builder、Repository、API 客户端
- 参考资料：
  - [快速入门 · 创建项目](getting-started/quickstart.md#🚀-创建第一个测试项目)
  - [最佳实践 · 项目结构](user-guide/BEST_PRACTICES.md#1-项目结构与约定)
  - [代码生成指南](user-guide/code-generation.md)

---

## 🧪 测试支持与调试
- Fixtures（`testing/fixtures/`）：
  - Session 级：`runtime`、`http_client`、`database`、`redis_client`
  - 存储：`local_file_client`、`s3_client`、`oss_client`
  - UI：`browser_manager`、`page`、`goto`、`screenshot`
  - 数据清理：`BaseTestDataCleaner`、`GenericTestDataCleaner`
- 调试工具（`testing/debugging/`）：
  - [HTTPDebugger](../src/df_test_framework/testing/debugging/http.py)
  - [DBDebugger](../src/df_test_framework/testing/debugging/database.py)
- 性能与监控：`extensions/builtin/monitoring`
- 推荐文档： [调试指南](troubleshooting/debugging-guide.md) · [Allure 速查](user-guide/QUICK_REFERENCE.md#📊-allure报告)

---

## 📦 示例与模板
- [examples/README.md](../examples/README.md) — 示例导航
- `examples/01-basic` — HTTP、数据库、Redis、存储（LocalFile/S3/OSS）
- `examples/02-bootstrap` — Bootstrap / Provider 定制
- `examples/03-testing` — Pytest fixtures、数据清理、Allure
- `examples/04-patterns` — Builder / Repository 实践
- `examples/05-extensions` — Pluggy 扩展
- `examples/06-ui-testing` — Playwright UI 测试
- `examples/07-message-queue` — Kafka/RabbitMQ/RocketMQ 消息队列

---

## 🛠️ 故障排查
- [常见错误](troubleshooting/common-errors.md)
- [调试指南](troubleshooting/debugging-guide.md)
- [verify_fixes.py](../verify_fixes.py) — 快速验证脚本示例

---

## 🔄 迁移与历史
- [迁移索引与快速参考](migration/README.md)
- [v2 → v3 迁移指南](migration/v2-to-v3.md)
- [v3.4 → v3.5 迁移指南](migration/v3.4-to-v3.5.md)
- 归档总览：[archive/README.md](archive/README.md)
  - `archive/v1/` — v1 架构、最佳实践
  - `archive/issues/` — 历史问题记录
  - `archive/reports/` — 代码审查、修复总结

---

## 🧾 质量与维护资料

### 开发与贡献
- [CONTRIBUTING.md](../CONTRIBUTING.md) — 贡献指南与开发流程
- [测试开发指南](user-guide/testing-development.md) — 单元测试、集成测试与覆盖率管理

### 报告与审计
- [reports/README.md](reports/README.md) — 行动计划、审计与重构报告索引

### 拦截器与观察性
- [INTERCEPTOR_ARCHITECTURE.md](INTERCEPTOR_ARCHITECTURE.md) — v3.3.0 架构设计与实现
- [INTERCEPTOR_PERFORMANCE_ANALYSIS.md](INTERCEPTOR_PERFORMANCE_ANALYSIS.md) — 基准测试，性能影响 <1%
- [CONFIGURABLE_INTERCEPTORS_IMPLEMENTATION.md](CONFIGURABLE_INTERCEPTORS_IMPLEMENTATION.md) — 配置化拦截器实施细节

### 框架评估
- [FRAMEWORK_ASSESSMENT.md](FRAMEWORK_ASSESSMENT.md) — gift-card-test 实战反馈与改进路线
- [CONFIG_MODERNIZATION_ANALYSIS.md](CONFIG_MODERNIZATION_ANALYSIS.md) — 配置体系现代化评估
- [V3.5_FINAL_SUMMARY.md](V3.5_FINAL_SUMMARY.md) — v3.5 重构验收

### 版本发布
- [发布说明索引](releases/README.md) — 所有版本发布文档
- [v3.8.0 发布说明](releases/v3.8.0.md) — AsyncHttpClient 完整发布说明
- [AsyncHttpClient 设计文档](async_http_client_design.md) — 架构设计决策

### 文档与审计
- [DOCUMENTATION_UPDATE_CHECKLIST.md](DOCUMENTATION_UPDATE_CHECKLIST.md) — 文档自查
- [DOC_UPDATE_SUMMARY.md](DOC_UPDATE_SUMMARY.md) — 文档演进追踪
- [COMPREHENSIVE_FEATURE_AUDIT.md](reports/COMPREHENSIVE_FEATURE_AUDIT.md) — 能力覆盖审计
- [FEATURE_IMPLEMENTATION_AUDIT.md](../FEATURE_IMPLEMENTATION_AUDIT.md) — 功能落地验证
- [MISSING_TESTS_IMPLEMENTATION_GUIDE.md](../MISSING_TESTS_IMPLEMENTATION_GUIDE.md) — 测试缺口计划

---

返回：[项目 README](../README.md) · [示例](../examples/) · [更新日志](../CHANGELOG.md)
