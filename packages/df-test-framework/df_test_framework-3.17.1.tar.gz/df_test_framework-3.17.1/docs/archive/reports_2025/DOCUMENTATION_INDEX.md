# df-test-framework 文档索引

> **最后更新**: 2025-12-02
> **框架版本**: v3.12.0
> **文档总数**: 130+

---

## 🚀 新手路径

**第一次使用df-test-framework？** 按以下顺序阅读：

1. **[5分钟快速开始](user-guide/QUICK_START_V3.5.md)** ⭐ (5分钟)
   - 从零开始创建第一个测试项目
   - 完整的代码示例和配置
   - 立即可运行

2. **[v3.5核心特性](V3.5_FINAL_SUMMARY.md)** (10分钟)
   - 了解v3.5的核心价值
   - Phase 1-3特性总览
   - 框架能力全景

3. **[完整用户手册](user-guide/USER_MANUAL.md)** (按需查阅)
   - 深入了解所有功能
   - API详细说明
   - 高级特性

**从v3.4升级？**
- **[v3.4 → v3.5 迁移指南](migration/v3.4-to-v3.5.md)** ✅ (30分钟-2小时)
  - 完整的迁移步骤
  - gift-card-test实际案例
  - 常见问题解答

---

## 📚 快速导航

| 文档类型 | 文档名称 | 描述 | 适用人群 |
|---------|---------|------|---------|
| 🚀 **快速开始** | [5分钟快速开始](user-guide/QUICK_START_V3.5.md) ⭐ | 从零开始运行第一个测试 | 新手 |
| 🔄 **迁移指南** | [v3.4→v3.5迁移](migration/v3.4-to-v3.5.md) ✅ | v3.4升级完整步骤 | 升级用户 |
| 📖 **用户手册** | [完整用户手册](user-guide/USER_MANUAL.md) | 完整的使用手册 | 所有用户 |
| 🎯 **最佳实践** | [最佳实践](user-guide/VERIFIED_BEST_PRACTICES.md) | 经过验证的最佳实践 | 所有用户 |
| 📋 **v3.5总结** | [v3.5最终总结](V3.5_FINAL_SUMMARY.md) | v3.5所有成果汇总 | 所有人 |
| 📝 **文档完成报告** | [文档整理完成](V3.5_DOCUMENTATION_COMPLETE.md) | 文档体系整理成果 | 开发者 |

---

## 🎯 v3.9 新特性文档 (开发中)

### 📨 消息队列客户端 (v3.9)

| 文档 | 描述 | 路径 |
|------|------|------|
| **使用指南** ⭐ | Kafka/RabbitMQ/RocketMQ完整使用指南 | [guides/message_queue.md](guides/message_queue.md) |
| **示例代码** | 三大消息队列实际使用示例 | [../examples/07-message-queue/](../examples/07-message-queue/) |

**核心特性**:
- ✅ **Kafka客户端** - 基于confluent-kafka 1.9.2 (librdkafka)的高性能Producer/Consumer封装
  - 生产性能提升3倍,消费性能提升50%
  - 完整SSL/TLS/SASL支持
  - AdminClient主题管理
- ✅ **RabbitMQ客户端** - 基于pika的Publisher/Consumer封装
- ✅ **RocketMQ客户端** - 基于rocketmq-python-client的Producer/Consumer封装
- ✅ **Exchange支持** - Direct, Topic, Fanout, Headers (RabbitMQ)
- ✅ **延迟消息** - 18个延迟级别 (RocketMQ)
- ✅ **Pytest Fixtures** - kafka_client, rabbitmq_client, rocketmq_client
- ✅ **Docker Compose** - 一键启动测试环境

---

## 🎯 v3.8 新特性文档

### ⚡ AsyncHttpClient - 异步HTTP客户端 (v3.8)

| 文档 | 描述 | 路径 |
|------|------|------|
| **使用指南** ⭐ | 快速开始、常见场景、性能优化 | [guides/async_http_client.md](guides/async_http_client.md) |
| **API 参考** | 完整的API文档和方法签名 | [api/async_http_client.md](api/async_http_client.md) |
| **性能对比** | 同步vs异步性能测试报告 | [performance/async_vs_sync.md](performance/async_vs_sync.md) |
| **架构设计** | 设计决策和拦截器兼容性 | [async_http_client_design.md](async_http_client_design.md) |
| **发布说明** | v3.8.0 完整发布说明 | [releases/v3.8.0.md](releases/v3.8.0.md) |

**核心亮点**:
- 🚀 并发性能提升 **40倍** (100个请求: 20s → 0.5s)
- 💾 内存占用降低 **90%** (50MB → 5MB)
- ⚙️ CPU占用降低 **75%** (80% → 20%)
- ✅ 完全兼容现有拦截器(签名、Token、日志)
- 🔥 HTTP/2 默认启用、智能连接池管理

---

## 🎯 v3.5 新特性文档

### Phase 1: 配置化拦截器系统

| 文档 | 描述 | 路径 |
|------|------|------|
| **实施报告** | 配置化拦截器完整实施文档 | [CONFIGURABLE_INTERCEPTORS_IMPLEMENTATION.md](CONFIGURABLE_INTERCEPTORS_IMPLEMENTATION.md) |
| **性能分析** | 拦截器性能基准测试报告 | [INTERCEPTOR_PERFORMANCE_ANALYSIS.md](INTERCEPTOR_PERFORMANCE_ANALYSIS.md) |
| **最佳实践** | 拦截器配置最佳实践指南 | [INTERCEPTOR_CONFIG_BEST_PRACTICES.md](INTERCEPTOR_CONFIG_BEST_PRACTICES.md) |
| **架构文档** | 拦截器架构设计 | [INTERCEPTOR_ARCHITECTURE.md](INTERCEPTOR_ARCHITECTURE.md) |

### Phase 2: 可观测性集成

| 文档 | 描述 | 路径 |
|------|------|------|
| **验收报告** | Phase 2验收和测试报告 | [V3.5_PHASE2_ACCEPTANCE_REPORT.md](V3.5_PHASE2_ACCEPTANCE_REPORT.md) |
| **最终状态** | 可观测性功能最终状态 | [V3.5_OBSERVABILITY_FINAL_STATUS.md](V3.5_OBSERVABILITY_FINAL_STATUS.md) |
| **Allure集成** | Allure报告集成计划 | [V3.5_ALLURE_INTEGRATION_PLAN.md](V3.5_ALLURE_INTEGRATION_PLAN.md) |

### Phase 3: 配置API增强

| 文档 | 描述 | 路径 |
|------|------|------|
| **完成报告** | Phase 3完整实施报告 | [PHASE3_COMPLETION_REPORT.md](PHASE3_COMPLETION_REPORT.md) |
| **用户指南** | Profile和with_overrides使用指南（50+示例）| [user-guide/PHASE3_FEATURES.md](user-guide/PHASE3_FEATURES.md) |

---

## 📖 用户指南

### 核心指南

| 文档 | 描述 | 路径 |
|------|------|------|
| **用户手册** | 完整的框架使用手册 | [user-guide/USER_MANUAL.md](user-guide/USER_MANUAL.md) |
| **快速参考** | 常用API速查表 | [user-guide/QUICK_REFERENCE.md](user-guide/QUICK_REFERENCE.md) |
| **最佳实践** | 经过验证的最佳实践 | [user-guide/VERIFIED_BEST_PRACTICES.md](user-guide/VERIFIED_BEST_PRACTICES.md) |
| **配置指南** | 框架配置详解 | [user-guide/configuration.md](user-guide/configuration.md) |
| **嵌套配置指南** ⭐ | BaseModel vs BaseSettings 选择指南 | [user-guide/nested-settings-guide.md](user-guide/nested-settings-guide.md) |

### 功能指南

| 文档 | 描述 | 路径 |
|------|------|------|
| **扩展系统** | 插件和扩展开发指南 | [user-guide/extensions.md](user-guide/extensions.md) |
| **代码生成** | 代码生成工具使用 | [user-guide/CODE_GENERATION.md](user-guide/CODE_GENERATION.md) |
| **调试工具** | Debug工具使用指南 | [user-guide/debugging.md](user-guide/debugging.md) |
| **UI测试** | UI自动化测试指南 | [user-guide/ui-testing.md](user-guide/ui-testing.md) |
| **CI/CD** | 持续集成配置 | [user-guide/ci-cd.md](user-guide/ci-cd.md) |

### 高级主题

| 文档 | 描述 | 路径 |
|------|------|------|
| **跨项目共享** | 跨项目代码复用 | [user-guide/cross-project-sharing.md](user-guide/cross-project-sharing.md) |
| **多仓库管理** | 多仓库项目管理 | [user-guide/multi-repo.md](user-guide/multi-repo.md) |
| **示例集合** | 完整的使用示例 | [user-guide/examples.md](user-guide/examples.md) |

---

## 🔄 迁移指南

| 版本 | 文档 | 路径 |
|------|------|------|
| **概览** | 迁移指南索引与快速参考 | [migration/README.md](migration/README.md) |
| **v1 → v2** | v2架构迁移 | [migration/from-v1-to-v2.md](migration/from-v1-to-v2.md) |
| **v2 → v3** | v3架构迁移 | [migration/v2-to-v3.md](migration/v2-to-v3.md) |
| **v3.2 → v3.3** | v3.3迁移 | [migration/v3.2-to-v3.3.md](migration/v3.2-to-v3.3.md) |
| **v3.3 → v3.4** | v3.4配置现代化迁移 | [migration/v3.3-to-v3.4.md](migration/v3.3-to-v3.4.md) |

---

## 🏗️ 架构文档

### v3.5 架构

| 文档 | 描述 | 路径 |
|------|------|------|
| **架构设计（详细版）** | v3.5完整架构设计方案 | [V3.5_REFACTOR_PLAN_REVISED.md](V3.5_REFACTOR_PLAN_REVISED.md) |
| **架构设计（简要版）** | v3.5架构设计草案 | [V3.5_REFACTOR_PLAN.md](V3.5_REFACTOR_PLAN.md) |
| **最终总结** | v3.5所有成果汇总 | [V3.5_FINAL_SUMMARY.md](V3.5_FINAL_SUMMARY.md) |

### 历史架构

| 文档 | 描述 | 路径 |
|------|------|------|
| **v3.4.0 发布总结** | v3.4.0版本总结 | [V3.4.0_RELEASE_SUMMARY.md](V3.4.0_RELEASE_SUMMARY.md) |
| **v3.3.0 文档更新** | v3.3.0文档更新总结 | [V3.3.0_DOCUMENTATION_UPDATE_SUMMARY.md](V3.3.0_DOCUMENTATION_UPDATE_SUMMARY.md) |

---

## 📊 评估和分析

| 文档 | 描述 | 路径 |
|------|------|------|
| **框架评估** | 框架能力和成熟度评估 | [FRAMEWORK_ASSESSMENT.md](FRAMEWORK_ASSESSMENT.md) |
| **框架能力** | 框架核心能力说明 | [FRAMEWORK_CAPABILITIES.md](FRAMEWORK_CAPABILITIES.md) |
| **配置现代化分析** | v3.4配置系统分析 | [CONFIG_MODERNIZATION_ANALYSIS.md](CONFIG_MODERNIZATION_ANALYSIS.md) |

---

## 🛠️ 开发者文档

| 文档 | 描述 | 路径 |
|------|------|------|
| **Debug系统** | v3.5 Debug工具说明 | [DEBUG_SYSTEM_V3.5.md](DEBUG_SYSTEM_V3.5.md) |
| **文档更新检查清单** | 文档维护检查清单 | [DOCUMENTATION_UPDATE_CHECKLIST.md](DOCUMENTATION_UPDATE_CHECKLIST.md) |
| **重构完成检查** | 重构验收检查清单 | [REFACTORING_COMPLETION_CHECK.md](REFACTORING_COMPLETION_CHECK.md) |

---

## 🔍 按主题查找

### HTTP客户端
- **[AsyncHttpClient 使用指南](guides/async_http_client.md)** ⭐ - 异步HTTP客户端（v3.8新增）
- **[AsyncHttpClient API 参考](api/async_http_client.md)** - 完整API文档
- **[性能对比分析](performance/async_vs_sync.md)** - 同步vs异步性能测试

### 配置管理
- [配置指南](user-guide/configuration.md) - 基础配置使用
- [Phase 3用户指南](user-guide/PHASE3_FEATURES.md) - Profile和运行时覆盖
- [配置现代化分析](CONFIG_MODERNIZATION_ANALYSIS.md) - v3.4配置系统

### HTTP拦截器
- [拦截器最佳实践](INTERCEPTOR_CONFIG_BEST_PRACTICES.md) - 配置最佳实践
- [拦截器实施报告](CONFIGURABLE_INTERCEPTORS_IMPLEMENTATION.md) - 完整实施文档
- [拦截器性能分析](INTERCEPTOR_PERFORMANCE_ANALYSIS.md) - 性能基准测试
- [拦截器架构](INTERCEPTOR_ARCHITECTURE.md) - 架构设计

### 可观测性
- [Phase 2验收报告](V3.5_PHASE2_ACCEPTANCE_REPORT.md) - 可观测性验收
- [可观测性最终状态](V3.5_OBSERVABILITY_FINAL_STATUS.md) - 功能完成状态
- [Allure集成计划](V3.5_ALLURE_INTEGRATION_PLAN.md) - Allure报告集成

### 测试编写
- [最佳实践](user-guide/VERIFIED_BEST_PRACTICES.md) - 测试最佳实践
- [示例集合](user-guide/examples.md) - 完整示例代码
- [UI测试指南](user-guide/ui-testing.md) - UI自动化测试

### 扩展开发
- [扩展系统](user-guide/extensions.md) - 插件开发指南
- [代码生成](user-guide/CODE_GENERATION.md) - 代码生成工具

---

## 📝 文档贡献指南

### 文档分类

1. **用户指南** (`user-guide/`) - 面向框架使用者
2. **架构文档** (`docs/`) - 架构设计和技术方案
3. **迁移指南** (`migration/`) - 版本升级指南
4. **API参考** (`api-reference/`) - API详细文档

### 文档命名规范

- **用户指南**: 小写，用连字符分隔（如 `user-guide/examples.md`）
- **架构文档**: 大写，用下划线分隔（如 `V3.5_FINAL_SUMMARY.md`）
- **版本文档**: 包含版本号（如 `V3.4.0_RELEASE_SUMMARY.md`）

### 更新文档

更新文档时请同时更新：
1. 本索引文件（DOCUMENTATION_INDEX.md）
2. 主README.md中的相关链接
3. 相关文档中的交叉引用

---

## 🔗 外部链接

- **GitHub仓库**: (待补充)
- **问题追踪**: (待补充)
- **讨论论坛**: (待补充)

---

## 📞 获取帮助

如有文档相关问题或建议：

1. 查看 [常见问题](user-guide/FAQ.md)（如果有）
2. 阅读 [用户手册](user-guide/USER_MANUAL.md)
3. 提交 Issue（如果配置了GitHub）

---

**文档版本**: v3.8
**最后更新**: 2025-11-25
**维护者**: df-test-framework团队

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
