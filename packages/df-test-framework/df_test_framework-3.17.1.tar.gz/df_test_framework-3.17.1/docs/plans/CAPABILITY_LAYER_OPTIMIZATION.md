# 能力层集成优化计划

> **版本**: v3.18.0 规划
> **创建日期**: 2025-01-08
> **更新日期**: 2025-12-08
> **状态**: ✅ 核心重构已完成
> **目标**: 统一能力层的 EventBus、Allure、可观测性集成，统一同步/异步模式

---

## 一、架构变更总结（v3.18.0）

### 1.1 核心架构变更

**之前（混合模式）**：
```
能力层客户端 ─┬─→ 直接调用 AllureObserver（��耦合）
             └─→ EventBus 事件发布（松耦合）
```

**之后（纯 EventBus 模式）**：
```
能力层客户端 ──→ EventBus 事件发布 ──→ AllureObserver 订阅处理
```

### 1.2 集成状态矩阵（已更新）

| 能力层客户端 | EventBus 事件 | Allure 报告 | 事件发布模式 | 集成完整度 | 状态 |
|---|---|---|---|---|---|
| **HTTP Client** | ✅ 完全集成 | ✅ EventBus 订阅 | publish_sync | 100% | ✅ 已完成 |
| **Database** | ✅ CorrelatedEvent | ✅ EventBus 订阅 | publish_sync | 100% | ✅ 已完成 |
| **Redis** | ✅ CorrelatedEvent | ✅ EventBus 订阅 | publish_sync | 100% | ✅ 已完成 |
| **Kafka** | ✅ 完全集成 | ✅ EventBus 订阅 | publish_sync | 95% | ✅ 已完成 |
| **RabbitMQ** | ✅ 完全集成 | ✅ EventBus 订阅 | publish_sync | 95% | ✅ 已完成 |
| **RocketMQ** | ✅ 完全集成 | ✅ EventBus 订阅 | publish_sync | 95% | ✅ 已完成 |
| **LocalFile** | ⏳ 事件类型已定义 | ⏳ 处理器已添加 | - | 60% | 待客户端集成 |
| **S3Client** | ⏳ 事件类型已定义 | ⏳ 处理器已添加 | - | 60% | 待客户端集成 |
| **OSSClient** | ⏳ 事件类型已定义 | ⏳ 处理器已添加 | - | 60% | 待客户端集成 |
| **GraphQL** | ❌ 无 | ❌ 无 | - | 20% | 待规划 |
| **gRPC** | ❌ 无 | ❌ 无 | - | 20% | 待规划 |

---

## 二、已完成内容

### 2.1 P1 - Redis 完善 ✅

- 新增 Cache 事件类型（CorrelatedEvent）
- RedisClient 所有操作支持 EventBus
- 使用 `publish_sync()` 同步发布
- 63 个测试全部通过

### 2.2 P2-A - 消息队列事件发布修复 ✅

**修改内容**：
- Kafka/RabbitMQ/RocketMQ 客户端改用 `publish_sync()` 同步发布
- 添加 `_get_event_bus()` 辅助方法，统一获取逻辑
- 移除未使用的 `asyncio` 导入

**新增 AllureObserver 方法**：
- `on_message_publish()` - 记录消息发布
- `on_message_consume()` - 记录消息消费
- 对应的异步事件处理器

### 2.3 P2-B - Storage 事件类型 ✅

**新增事件类型** (`core/events/types.py`)：
- `StorageOperationStartEvent`
- `StorageOperationEndEvent`
- `StorageOperationErrorEvent`

**新增 AllureObserver 方法**：
- `on_storage_operation()` - 记录存储操作
- 对应的异步事件处理器

### 2.4 统一 Allure 集成重构 ✅

**核心变更**：
- 移除所有能力层客户端对 AllureObserver 的直接调用
- 所有 Allure 报告通过 EventBus 事件订阅自动生成
- 统一同步发布模式: `publish_sync()` 确保事件完整性

**Database 事件升级**：
- `DatabaseQueryStartEvent/EndEvent/ErrorEvent` 升级为 CorrelatedEvent
- 添加 `operation/table` 字段和 `create()` 工厂方法
- 字段名变更: `duration` → `duration_ms`
- 修改 `execute/query_one/query_all/insert` 方法使用新事件

**AllureObserver 清理**：
- 删除废弃方法: `on_query_start/on_query_end/on_query_error/on_cache_operation`
- 新增 Database EventBus 事件处理器
- 保留所有 EventBus 事件处理器

**Allure Fixture 增强** (`testing/fixtures/allure.py`)：
```python
# 订阅所有能力层事件
# HTTP
HttpRequestStartEvent, HttpRequestEndEvent, HttpRequestErrorEvent
MiddlewareExecuteEvent

# Database
DatabaseQueryStartEvent, DatabaseQueryEndEvent, DatabaseQueryErrorEvent

# Redis (Cache)
CacheOperationStartEvent, CacheOperationEndEvent, CacheOperationErrorEvent

# MQ
MessagePublishEvent, MessageConsumeEvent

# Storage
StorageOperationStartEvent, StorageOperationEndEvent, StorageOperationErrorEvent
```

---

## 三、待完成内容

### 3.1 Storage 客户端集成（P2-B 剩余）

事件类型和 AllureObserver 处理器已就绪，需要改造客户端：

- `capabilities/storages/file/local/client.py`
- `capabilities/storages/object/s3/client.py`
- `capabilities/storages/object/oss/client.py`

### 3.2 GraphQL/gRPC 集成（P3）

低优先级，暂不规划。

---

## 四、设计规范

### 4.1 同步/异步模式原则

**统一采用同步 API + 同步事件发布模式**：

1. **公开 API 同步化**：所有能力层客户端的公开方法使用 `def`（非 `async def`）
2. **事件发布统一使用 `publish_sync()`**：确保事件在操作完成前发布完毕
3. **内部可异步**：HttpClient 等可内部使用异步实现，但对外暴露同步接口

**原因**：
- 测试代码通常是同步的（pytest 默认同步）
- 避免事件循环嵌套问题
- 保证事件顺序和完整性
- 简化调用方使用

### 4.2 Allure 集成原则

**纯 EventBus 驱动模式**：

1. 能力层客户端**只发布事件**，不直接调用 AllureObserver
2. AllureObserver 通过 EventBus 订阅事件并生成报告
3. allure fixture 负责创建 EventBus 和注册订阅

**优势**：
- **松耦合**：客户端不依赖 AllureObserver
- **可扩展**：任何订阅者都能监听事件（日志、监控、调试等）
- **可测试**：可以 mock EventBus 进行单元测试
- **统一性**：所有能力层使用相同的集成模式

### 4.3 能力层客户端模板

```python
class XxxClient:
    def __init__(self, ..., event_bus: Any | None = None):
        self._event_bus = event_bus

    def _get_event_bus(self):
        """获取 EventBus 实例（支持测试隔离）"""
        if self._event_bus is not None:
            return self._event_bus
        try:
            from df_test_framework.infrastructure.events import get_event_bus
            return get_event_bus()
        except Exception:
            return None

    def _publish_event(self, event: Any) -> None:
        """发布事件到 EventBus（同步模式）"""
        event_bus = self._get_event_bus()
        if event_bus:
            try:
                event_bus.publish_sync(event)
            except Exception:
                pass  # 静默失败，不影响主流程

    def some_operation(self, ...):
        """示例操作"""
        # 1. 发布开始事件
        start_event, correlation_id = XxxStartEvent.create(...)
        self._publish_event(start_event)

        # 2. 执行操作
        start_time = time.perf_counter()
        try:
            result = self._do_something()
            duration_ms = (time.perf_counter() - start_time) * 1000

            # 3. 发布结束事件（Allure 通过 EventBus 订阅自动记录）
            end_event = XxxEndEvent.create(correlation_id, duration_ms=duration_ms, ...)
            self._publish_event(end_event)

            return result

        except Exception as e:
            duration_ms = (time.perf_counter() - start_time) * 1000
            # 4. 发布错误事件
            error_event = XxxErrorEvent.create(correlation_id, error=e, duration_ms=duration_ms, ...)
            self._publish_event(error_event)
            raise
```

---

## 五、测试验证

### 5.1 测试结果

- ✅ 1267 passed, 40 skipped
- ✅ 语法检查通过
- ✅ Ruff 检查通过

### 5.2 提交记录

```
1a5b288 feat(capabilities): 统一能力层 EventBus 和 Allure 集成
501c06a refactor(allure): 统一能力层 Allure 集成为纯 EventBus 驱动模式
```

---

## 六、预期收益

1. **统一的可观测性** - 所有能力层客户端具备一致的事件、日志、报告能力
2. **更好的调试体验** - Allure 报告中可以看到所有操作详情
3. **事件驱动架构** - 支持通过 EventBus 扩展监控、告警等能力
4. **向后兼容** - 所有改动保持 API 兼容，event_bus 参数可选
5. **统一的同步/异步模式** - 避免事件丢失，保证事件顺序
6. **松耦合设计** - 能力层客户端不依赖 AllureObserver，便于测试和扩展
