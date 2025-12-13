# 核心文档导航 - 真正有价值的文档清单

> **目标读者**: 测试开发人员、框架使用者、新团队成员
> **更新日期**: 2025-12-05
> **框架版本**: v3.17.0

---

## 📌 必读文档（5 分钟快速上手）

### 1. [快速开始](user-guide/QUICK_START.md) ⭐⭐⭐⭐⭐
**阅读时间**: 5 分钟
**价值**: 最快上手框架的方式

**内容**:
- ✅ 安装框架 (`uv sync`)
- ✅ 初始化项目 (`df-test init`)
- ✅ 第一个 HTTP 测试
- ✅ 第一个数据库测试
- ✅ 运行测试和查看报告

**何时读**: 第一次接触框架时必读

---

### 2. [快速参考](user-guide/QUICK_REFERENCE.md) ⭐⭐⭐⭐⭐
**阅读时间**: 3 分钟
**价值**: 日常开发速查表

**内容**:
- ✅ 常用命令速查 (`pytest`, `df-test`)
- ✅ 常用 Fixtures (`http_client`, `database`, `redis_client`)
- ✅ 调试开关 (`enable_http_debug()`, `enable_db_debug()`)
- ✅ Allure 报告常用操作
- ✅ 环境变量配置

**何时读**: 日常开发，忘记命令时翻阅

---

### 3. [最佳实践](user-guide/BEST_PRACTICES.md) ⭐⭐⭐⭐
**阅读时间**: 15 分钟
**价值**: 避免踩坑，规范开发

**内容**:
- ✅ 项目目录结构规范
- ✅ 测试数据管理（Builder、Repository、Cleaner）
- ✅ 配置管理（环境变量、多环境）
- ✅ 敏感信息处理
- ✅ CI/CD 集成建议
- ✅ 性能优化技巧

**何时读**: 开始编写测试前，建立规范项目

---

## 🔧 核心功能指南（按使用频率排序）

### 4. [中间件使用指南](guides/middleware_guide.md) ⭐⭐⭐⭐⭐
**阅读时间**: 20 分钟
**价值**: HTTP 客户端核心机制

**内容**:
- ✅ 中间件系统概念（洋葱模型）
- ✅ 内置中间件（重试、超时、日志、签名）
- ✅ 自定义中间件开发
- ✅ 50+ 实际示例
- ✅ 中间件链调试

**何时读**:
- 需要 HTTP 请求前后处理（认证、签名、日志）
- 需要自定义请求/响应处理逻辑

**实际场景**:
```python
# 场景1: 添加自定义请求头
class CustomHeaderMiddleware(BaseMiddleware):
    async def process_request(self, request: Request) -> Request:
        request.headers["X-Custom-Header"] = "value"
        return request

# 场景2: 统一错误处理
class ErrorHandlingMiddleware(BaseMiddleware):
    async def process_response(self, response: Response) -> Response:
        if response.status_code >= 500:
            raise ServerError(f"服务器错误: {response.text}")
        return response
```

---

### 5. [测试数据清理指南](guides/test_data_cleanup.md) ⭐⭐⭐⭐⭐
**阅读时间**: 10 分钟
**价值**: 保持测试环境干净

**内容**:
- ✅ `CleanupManager` 使用
- ✅ `ListCleanup` 自动清理列表
- ✅ `--keep-test-data` 保留数据调试
- ✅ 数据库事务回滚清理
- ✅ 清理失败处理

**何时读**: 测试会创建数据（用户、订单、文件等）

**实际场景**:
```python
def test_create_order(http_client, cleanup):
    # 创建测试数据
    order_no = DataGenerator.test_id("ORD")
    response = http_client.post("/orders", json={"order_no": order_no})

    # 注册清理（测试结束自动删除）
    cleanup.add("orders", order_no)

    assert response.status_code == 201
    # 测试结束后自动调用 DELETE /orders/{order_no}
```

---

### 6. [EventBus 事件总线指南](guides/event_bus_guide.md) ⭐⭐⭐⭐
**阅读时间**: 15 分钟
**价值**: 解耦测试逻辑，增强可观测性

**内容**:
- ✅ EventBus 发布/订阅模式
- ✅ 内置事件（HTTP、DB、GraphQL、gRPC）
- ✅ 自定义事件和监听器
- ✅ 事件关联（correlation_id）
- ✅ 与 Allure 集成

**何时读**:
- 需要监听 HTTP 请求/响应
- 需要在测试中响应框架事件
- 需要自定义事件驱动逻辑

**实际场景**:
```python
# 场景1: 监听所有 HTTP 请求
def test_with_request_monitor(event_bus, http_client):
    requests = []

    def on_request(event: HttpRequestStartEvent):
        requests.append(event)

    event_bus.subscribe(HttpRequestStartEvent, on_request)

    http_client.get("/users")
    http_client.post("/orders")

    assert len(requests) == 2  # 监听到 2 个请求

# 场景2: 自动记录慢请求
def slow_request_monitor(event: HttpRequestEndEvent):
    if event.duration > 1.0:
        print(f"⚠️ 慢请求: {event.url} - {event.duration}s")
```

---

### 7. [异步 HTTP 客户端指南](guides/async_http_client.md) ⭐⭐⭐⭐
**阅读时间**: 10 分钟
**价值**: 性能提升 40 倍

**内容**:
- ✅ `AsyncHttpClient` 基本使用
- ✅ 并发请求（`asyncio.gather`）
- ✅ 性能对比（同步 vs 异步）
- ✅ 中间件兼容性
- ✅ 最佳实践

**何时读**:
- 需要并发测试（压测、批量操作）
- 性能测试场景

**实际场景**:
```python
# 并发创建 100 个用户（性能提升 40 倍）
async def test_batch_create_users(async_http_client):
    tasks = [
        async_http_client.post("/users", json={"name": f"User-{i}"})
        for i in range(100)
    ]
    responses = await asyncio.gather(*tasks)
    assert all(r.status_code == 201 for r in responses)
```

---

### 8. [代码生成指南](user-guide/code-generation.md) ⭐⭐⭐⭐
**阅读时间**: 10 分钟
**价值**: 提升开发效率 10 倍

**内容**:
- ✅ `df-test gen test` - 生成测试用例
- ✅ `df-test gen builder` - 生成 Builder 类
- ✅ `df-test gen repository` - 生成 Repository
- ✅ `df-test gen api` - 生成 API 客户端
- ✅ 自定义模板

**何时读**: 开始写测试，避免重复编码

**实际场景**:
```bash
# 生成用户相关测试文件
df-test gen test --name user --type api

# 生成订单 Builder
df-test gen builder --name Order

# 生成用户 Repository
df-test gen repository --name User
```

---

## 🏗️ 架构理解（理解框架设计）

### 9. [v3.17 架构总览](architecture/OVERVIEW_V3.17.md) ⭐⭐⭐⭐
**阅读时间**: 20 分钟
**价值**: 理解框架整体设计

**内容**:
- ✅ 五层架构（Layer 0-4）
- ✅ 事件驱动架构
- ✅ OpenTelemetry 追踪整合
- ✅ 测试隔离机制
- ✅ 依赖注入与 Provider

**何时读**:
- 需要深度定制框架
- 需要理解框架内部机制
- 排查复杂问题

---

### 10. [用户手册](user-guide/USER_MANUAL.md) ⭐⭐⭐
**阅读时间**: 30 分钟
**价值**: 全面的功能参考

**内容**:
- ✅ 按场景拆分的操作说明
- ✅ HTTP 客户端完整 API
- ✅ 数据库操作指南
- ✅ UI 测试（Playwright）
- ✅ 配置系统详解

**何时读**: 需要查找特定功能的使用方法

---

## 🔍 问题排查

### 11. [调试指南](troubleshooting/debugging-guide.md) ⭐⭐⭐⭐
**阅读时间**: 10 分钟
**价值**: 快速定位问题

**内容**:
- ✅ HTTP 调试器使用
- ✅ 数据库调试器使用
- ✅ 日志级别调整
- ✅ 常见错误和解决方案

**何时读**: 测试失败，需要排查问题

**实际场景**:
```python
from df_test_framework.testing.debugging import enable_http_debug

# 开启 HTTP 调试，查看所有请求详情
enable_http_debug()

def test_api(http_client):
    response = http_client.get("/users")
    # 终端会显示完整的请求/响应详情
```

---

## 📚 高级功能（按需学习）

### 12. [分布式追踪指南](guides/distributed_tracing.md) ⭐⭐⭐
**阅读时间**: 15 分钟
**价值**: 微服务追踪链路

**何时读**:
- 测试微服务架构
- 需要追踪请求链路
- 集成 Jaeger/Zipkin

---

### 13. [消息队列指南](guides/message_queue.md) ⭐⭐⭐
**阅读时间**: 20 分钟
**价值**: Kafka/RabbitMQ/RocketMQ 测试

**何时读**: 测试消息队列相关功能

---

### 14. [GraphQL 客户端指南](guides/graphql_client.md) ⭐⭐⭐
**阅读时间**: 10 分钟
**价值**: GraphQL API 测试

**何时读**: 测试 GraphQL 接口

---

### 15. [gRPC 客户端指南](guides/grpc_client.md) ⭐⭐⭐
**阅读时间**: 10 分钟
**价值**: gRPC 服务测试

**何时读**: 测试 gRPC 服务

---

## 📖 阅读顺序建议

### 新手（第一次使用框架）
```
1. 快速开始 (5分钟)
   ↓
2. 快速参考 (浏览一遍，知道有什么功能)
   ↓
3. 最佳实践 (15分钟，建立规范)
   ↓
4. 开始编写测试
   ↓
5. 遇到问题时查阅对应的指南
```

### 有经验的测试开发（了解基本概念）
```
1. 快速参考 (3分钟，速查命令)
   ↓
2. 中间件使用指南 (理解 HTTP 核心机制)
   ↓
3. 测试数据清理指南 (规范数据管理)
   ↓
4. 代码生成指南 (提升效率)
   ↓
5. 按需学习高级功能
```

### 框架贡献者/定制开发
```
1. v3.17 架构总览 (理解整体设计)
   ↓
2. 阅读相关 guides/ 了解各模块实现
   ↓
3. 查看 src/ 源码
   ↓
4. 阅读 releases/ 了解演进历史
```

---

## 🎯 按场景查找文档

### 场景 1: 编写 HTTP API 测试
```
必读:
- user-guide/QUICK_START.md (快速上手)
- guides/middleware_guide.md (理解中间件)
- guides/test_data_cleanup.md (数据清理)

可选:
- guides/async_http_client.md (性能测试)
- guides/graphql_client.md (GraphQL)
```

### 场景 2: 编写数据库测试
```
必读:
- user-guide/USER_MANUAL.md (数据库操作章节)
- user-guide/BEST_PRACTICES.md (Repository 模式)

可选:
- user-guide/code-generation.md (生成 Repository)
```

### 场景 3: 编写 UI 测试
```
必读:
- user-guide/ui-testing.md
- user-guide/BEST_PRACTICES.md (Page Object 模式)
```

### 场景 4: 集成 CI/CD
```
必读:
- user-guide/ci-cd.md
- user-guide/BEST_PRACTICES.md (CI/CD 建议章节)
```

### 场景 5: 性能测试
```
必读:
- guides/async_http_client.md (并发请求)
- guides/prometheus_metrics.md (性能监控)
```

### 场景 6: 问题排查
```
必读:
- troubleshooting/debugging-guide.md
- user-guide/QUICK_REFERENCE.md (调试命令)
```

---

## 📊 文档价值评估

| 文档 | 阅读频率 | 实用性 | 必读程度 | 阅读时间 |
|------|---------|--------|---------|---------|
| **快速开始** | 一次 | ⭐⭐⭐⭐⭐ | 必读 | 5分钟 |
| **快速参考** | 高频 | ⭐⭐⭐⭐⭐ | 必读 | 3分钟 |
| **最佳实践** | 中频 | ⭐⭐⭐⭐⭐ | 必读 | 15分钟 |
| **中间件指南** | 中频 | ⭐⭐⭐⭐⭐ | 强烈推荐 | 20分钟 |
| **数据清理指南** | 高频 | ⭐⭐⭐⭐⭐ | 强烈推荐 | 10分钟 |
| **EventBus 指南** | 中频 | ⭐⭐⭐⭐ | 推荐 | 15分钟 |
| **异步 HTTP** | 低频 | ⭐⭐⭐⭐ | 推荐 | 10分钟 |
| **代码生成** | 中频 | ⭐⭐⭐⭐ | 推荐 | 10分钟 |
| **架构总览** | 一次 | ⭐⭐⭐⭐ | 可选 | 20分钟 |
| **用户手册** | 低频 | ⭐⭐⭐ | 参考 | 30分钟 |
| **调试指南** | 中频 | ⭐⭐⭐⭐ | 推荐 | 10分钟 |
| **其他高级功能** | 按需 | ⭐⭐⭐ | 按需 | 10-20分钟 |

---

## ⚡ 极简版（只有 2 分钟）

如果你真的只有 2 分钟，**只看这 2 个文档**：

1. **[快速参考](user-guide/QUICK_REFERENCE.md)** - 知道有什么命令和功能
2. **[快速开始](user-guide/QUICK_START.md)** - 跑通第一个测试

然后：
- 需要什么功能，去对应的 `guides/` 查找
- 遇到问题，去 `troubleshooting/` 查找
- 想了解原理，去 `architecture/` 查找

---

## 🗑️ 不重要的文档（可以忽略）

以下文档是**历史记录、审计报告、内部文档**，普通使用者**不需要阅读**：

```
❌ docs/CHANGELOG_AUDIT_REPORT.md          # 内部审计
❌ docs/DOCUMENTATION_AUDIT_REPORT_*.md     # 内部审计
❌ docs/DOCUMENTATION_CLEANUP_SUMMARY.md    # 内部记录
❌ docs/DOCUMENTATION_MAINTENANCE_COMPLETE.md # 内部记录
❌ docs/archive/                            # 历史归档
❌ docs/releases/ (除了最新版本)             # 历史版本
❌ docs/architecture/archive/               # 历史架构
❌ docs/migration/ (除非你在做迁移)          # 迁移指南
```

这些文档只对以下人员有价值：
- 框架维护者
- 文档管理员
- 需要了解历史演进的贡献者

---

## 📝 总结

### 核心文档清单（Top 8）

对于 **80% 的日常测试开发**，你只需要这 **8 个文档**：

1. ✅ **[快速开始](user-guide/QUICK_START.md)** - 5分钟上手
2. ✅ **[快速参考](user-guide/QUICK_REFERENCE.md)** - 日常速查
3. ✅ **最佳实践** - 规范开发
4. ✅ **中间件指南** - HTTP 核心
5. ✅ **数据清理指南** - 数据管理
6. ✅ **EventBus 指南** - 事件驱动
7. ✅ **代码生成指南** - 提升效率
8. ✅ **调试指南** - 问题排查

### 总阅读时间
- **最小上手**: 8 分钟（快速开始 + 快速参考）
- **基础掌握**: 80 分钟（Top 8 全部阅读）
- **全面精通**: 3-4 小时（Top 15 全部阅读）

---

**建议**: 收藏本文档，作为学习框架的导航地图！ 📌
