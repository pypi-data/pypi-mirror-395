# 核心文档更新计划

> **创建日期**: 2025-12-05
> **目标版本**: v3.17.0
> **状态**: 进行中

---

## 📋 核心文档清单

根据 `ESSENTIAL_DOCS.md`，需要确保以下 **15 个核心文档** 都反映最新的框架状态（v3.17.0）。

### Top 8 核心文档（必须更新）

| # | 文档 | 当前版本 | 目标版本 | 状态 | 优先级 |
|---|------|---------|---------|------|--------|
| 1 | `user-guide/QUICK_START.md` | v3.17.0 | v3.17.0 | ✅ 已更新 | P0 |
| 2 | `user-guide/QUICK_REFERENCE.md` | v3.0.0 | v3.17.0 | ✅ 已更新 | P0 |
| 3 | `user-guide/BEST_PRACTICES.md` | 未知 | v3.17.0 | ⏳ 待更新 | P0 |
| 4 | `guides/middleware_guide.md` | v3.14.0 | v3.17.0 | ⏳ 待更新 | P0 |
| 5 | `guides/test_data_cleanup.md` | 未知 | v3.17.0 | ⏳ 待检查 | P1 |
| 6 | `guides/event_bus_guide.md` | v3.14.0 | v3.17.0 | ⏳ 待更新 | P0 |
| 7 | `guides/async_http_client.md` | 未知 | v3.17.0 | ⏳ 待检查 | P1 |
| 8 | `user-guide/code-generation.md` | 未知 | v3.17.0 | ⏳ 待检查 | P1 |

### Top 15 核心文档（建议更新）

| # | 文档 | 当前版本 | 目标版本 | 状态 | 优先级 |
|---|------|---------|---------|------|--------|
| 9 | `architecture/OVERVIEW_V3.17.md` | v3.17.0 | v3.17.0 | ✅ 已更新 | P0 |
| 10 | `user-guide/USER_MANUAL.md` | 未知 | v3.17.0 | ⏳ 待更新 | P1 |
| 11 | `troubleshooting/debugging-guide.md` | 未知 | v3.17.0 | ⏳ 待更新 | P1 |
| 12 | `guides/distributed_tracing.md` | 未知 | v3.17.0 | ⏳ 待检查 | P2 |
| 13 | `guides/message_queue.md` | 未知 | v3.17.0 | ⏳ 待检查 | P2 |
| 14 | `guides/graphql_client.md` | 未知 | v3.17.0 | ⏳ 待检查 | P2 |
| 15 | `guides/grpc_client.md` | 未知 | v3.17.0 | ⏳ 待检查 | P2 |

---

## 🎯 更新要点

### v3.17.0 核心新特性

#### 1. 事件系统重构
- ✅ `event_id` - 每个事件的唯一标识
- ✅ `correlation_id` - 关联 Start/End 事件对
- ✅ `CorrelatedEvent` 基类
- ✅ 工厂方法 `Event.create()`

#### 2. OpenTelemetry 整合
- ✅ 自动注入 `trace_id`/`span_id` 到事件
- ✅ W3C TraceContext 标准格式
- ✅ 从当前 Span 自动获取追踪上下文

#### 3. 测试隔离机制
- ✅ 每个测试独立的 EventBus 实例
- ✅ `set_test_event_bus()` / `get_event_bus()` API
- ✅ HttpClient 动态 EventBus 解析

#### 4. Allure 深度整合
- ✅ `AllureObserver` 完整实现
- ✅ 记录完整请求体和响应体
- ✅ 提取 OpenTelemetry 追踪信息到 Allure
- ✅ 支持 HTTP/GraphQL/gRPC 协议
- ✅ `allure_observer` fixture

### v3.16.0 重要变更

- ✅ Layer 4 Bootstrap 引导层
- ✅ 五层架构完善
- ❌ 废弃 Interceptor 系统（完全移除）

### v3.14.0 重要变更

- ✅ 中间件系统（洋葱模型）
- ✅ EventBus 事件总线
- ✅ `@api_class` 装饰器
- ✅ Repository 自动发现

---

## 📝 更新检查清单

### P0 - 必须更新（立即执行）

- [x] **快速开始** (`QUICK_START.md`)
  - [x] 版本号更新到 v3.17.0
  - [x] 添加 v3.17 新特性
  - [x] 移除版本号后缀

- [x] **快速参考** (`QUICK_REFERENCE.md`)
  - [x] 版本号: v3.0.0 → v3.17.0
  - [x] 添加 `allure_observer` fixture
  - [x] 添加事件系统示例
  - [x] 添加 v3.17 新 fixture

- [x] **EventBus 指南** (`guides/event_bus_guide.md`)
  - [x] 版本号: v3.14.0 → v3.17.0
  - [x] 添加事件关联系统（correlation_id）
  - [x] 添加 OpenTelemetry 整合说明
  - [x] 添加测试隔离机制说明
  - [x] 添加 `allure_observer` 使用示例

- [x] **中间件指南** (`guides/middleware_guide.md`)
  - [x] 版本号: v3.14.0 → v3.17.0
  - [x] 添加 v3.17.0 整合示例

- [x] **最佳实践** (`BEST_PRACTICES.md`)
  - [x] 版本号: v3.0.0 → v3.17.0
  - [x] 添加第11章: 事件系统与可观测性最佳实践
  - [x] 更新 HTTP 客户端最佳实践（@api_class 装饰器）
  - [x] 更新中间件使用示例

### P1 - 建议更新（短期完成）

- [x] **用户手册** (`USER_MANUAL.md`)
  - [x] 版本号: v3.14.0 → v3.17.0
  - [x] 新增第8章: 事件系统与可观测性 (+135 行)
  - [x] 更新 Fixtures 章节（添加 v3.17 新 fixture）

- [x] **调试指南** (`debugging-guide.md`)
  - [x] 添加事件系统调试章节 (+130 行)
  - [x] 添加 Allure 报告调试章节 (+115 行)

- [x] **测试数据清理指南** (`test_data_cleanup.md`)
  - [x] 已验证：无需更新（v3.12.1+，通用数据清理机制）

- [x] **异步 HTTP 指南** (`async_http_client.md`)
  - [x] 已验证：无需更新（v3.8+，异步 HTTP 客户端通用功能）

- [x] **代码生成指南** (`code-generation.md`)
  - [x] 已验证：无需更新（v2.0.0 CLI 工具文档）

### P2 - 可选更新（按需执行）

- [x] **分布式追踪指南** (`distributed_tracing.md`)
  - [x] 版本号: v3.12.0 → v3.17.0
  - [x] 新增 v3.17.0 特性章节 (+145 行)
  - [x] EventBus 自动注入 trace_id/span_id
  - [x] W3C TraceContext 标准格式
  - [x] 与 Allure 集成示例

- [x] **消息队列指南** (`message_queue.md`)
  - [x] 更新版本号: v3.9.0 → v3.17.0

- [x] **GraphQL 指南** (`graphql_client.md`)
  - [x] 更新版本号: v3.11.0 → v3.17.0

- [x] **gRPC 指南** (`grpc_client.md`)
  - [x] 更新版本号: v3.11.0 → v3.17.0

---

## 🚀 执行计划

### 第一阶段：核心文档（P0）✅ 进行中

**目标**: 更新 Top 8 核心文档
**时间**: 2025-12-05

- [x] 1. 快速开始 (`QUICK_START.md`)
- [x] 2. 快速参考 (`QUICK_REFERENCE.md`)
- [x] 3. EventBus 指南 (`event_bus_guide.md`)
- [x] 4. 中间件指南 (`middleware_guide.md`)
- [x] 5. 最佳实践 (`BEST_PRACTICES.md`)
- [ ] 6. 验证其他 P0 文档（test_data_cleanup.md, async_http_client.md, code-generation.md）

### 第二阶段：重要文档（P1）

**目标**: 更新其他重要文档
**时间**: 2025-12-06

- [ ] 用户手册
- [ ] 调试指南
- [ ] 其他指南验证

### 第三阶段：高级功能（P2）

**目标**: 按需更新高级功能文档
**时间**: 按需

---

## 📌 更新原则

### 1. 版本号一致性

所有核心文档的版本号必须统一到 **v3.17.0**：

```markdown
> **版本**: v3.17.0 | **更新**: 2025-12-05
```

### 2. 内容准确性

- ✅ 反映最新架构（五层架构）
- ✅ 包含最新特性（v3.17.0）
- ✅ 移除废弃内容（Interceptor）
- ✅ 更新示例代码

### 3. 特性标注

使用版本标签标注特性引入版本：

```python
# 事件系统（v3.14+）
# Allure 深度整合（v3.17+）
# 异步 HTTP（v3.8+）
```

### 4. 废弃警告

对于废弃的功能，添加明确的警告：

```markdown
> ⚠️ **废弃警告**: Interceptor 系统已在 v3.16.0 完全移除，请使用 Middleware 代替
```

---

## 🔍 验证方法

### 1. 版本号检查

```bash
grep -r "版本.*v3\." docs/user-guide/ docs/guides/ | grep -v "v3.17.0"
```

### 2. 废弃内容检查

```bash
grep -r "Interceptor" docs/user-guide/ docs/guides/
```

### 3. 链接有效性检查

- 验证所有内部链接指向有效文档
- 验证代码示例可以运行

---

## 📊 进度追踪

### 完成情况

- ✅ 已完成: 15/15 (100%) 🎉
- ⏳ 进行中: 0/15 (0%)
- 📝 待完成: 0/15 (0%)

### 优先级分布

- ✅ P0 核心文档: 6/6 (100%)
- ✅ P1 重要文档: 5/5 (100%)
- ✅ P2 可选文档: 4/4 (100%)

---

## 📝 变更日志

### 2025-12-05

#### P0 核心文档更新（6/6 - 100%）✅
- [x] 创建核心文档更新计划
- [x] 更新 `QUICK_START.md` 到 v3.17.0
- [x] 更新 `QUICK_REFERENCE.md` 到 v3.17.0
- [x] 更新 `event_bus_guide.md` 到 v3.17.0（+250 行）
- [x] 更新 `middleware_guide.md` 到 v3.17.0（+90 行）
- [x] 更新 `BEST_PRACTICES.md` 到 v3.17.0（+185 行）

#### P1 重要文档更新（5/5 - 100%）✅
- [x] 验证 `test_data_cleanup.md`（v3.12.1+，无需更新）
- [x] 验证 `async_http_client.md`（v3.8+，无需更新）
- [x] 验证 `code-generation.md`（v2.0.0，无需更新）
- [x] 更新 `USER_MANUAL.md` 到 v3.17.0（+135 行）
- [x] 更新 `debugging-guide.md` 到 v3.17.0（+245 行）

**核心文档更新完成**: 11/15 (73%) ✅

**新增内容总计**: ~1,135 行

#### P2 可选文档更新（4/4 - 100%）✅
- [x] 更新 `distributed_tracing.md` 到 v3.17.0（+145 行）
- [x] 更新 `message_queue.md` 到 v3.17.0（版本号）
- [x] 更新 `graphql_client.md` 到 v3.17.0（版本号）
- [x] 更新 `grpc_client.md` 到 v3.17.0（版本号）

**所有文档更新完成**: 15/15 (100%) 🎉🎉🎉

**总新增内容**: ~1,280 行

---

**完成状态**:
✅ 所有核心文档（P0/P1/P2）已全部更新到 v3.17.0！
