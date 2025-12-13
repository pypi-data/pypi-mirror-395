"""Allure集成 - 自动记录测试操作到Allure报告

通过 autouse fixture 实现零配置自动记录:
- HTTP请求/响应详情
- 中间件执行过程
- 数据库查询
- Redis 缓存操作
- 消息队列操作
- 存储操作
- 事务操作 (commit/rollback)
- 错误和异常

特性:
- 零配置: autouse=True，无需在测试代码中手动启用
- 终端静默: 测试通过时无额外输出
- 详细报告: Allure HTML报告包含完整详情
- 测试隔离: v3.17.0 每个测试使用独立的 EventBus（不会互相干扰）
- 事件驱动: v3.18.0 所有能力层通过 EventBus 统一集成 Allure

生成报告:
    pytest --alluredir=./allure-results
    allure serve ./allure-results

架构设计参考:
    docs/ALLURE_INTEGRATION_DESIGN.md
    docs/V3.5_ALLURE_INTEGRATION_PLAN.md
    docs/architecture/V3.17_EVENT_SYSTEM_REDESIGN.md
"""

from collections.abc import Generator

import pytest

from df_test_framework.core.events import (
    # Cache 事件 (Redis)
    CacheOperationEndEvent,
    CacheOperationErrorEvent,
    CacheOperationStartEvent,
    # Database 事件
    DatabaseQueryEndEvent,
    DatabaseQueryErrorEvent,
    DatabaseQueryStartEvent,
    # HTTP 事件
    HttpRequestEndEvent,
    HttpRequestErrorEvent,
    HttpRequestStartEvent,
    # MQ 事件
    MessageConsumeEvent,
    MessagePublishEvent,
    # 中间件事件
    MiddlewareExecuteEvent,
    # Storage 事件
    StorageOperationEndEvent,
    StorageOperationErrorEvent,
    StorageOperationStartEvent,
    # Transaction 事件
    TransactionCommitEvent,
    TransactionRollbackEvent,
)
from df_test_framework.infrastructure.events import (
    EventBus,
    set_test_event_bus,
)
from df_test_framework.testing.reporting.allure import (
    ALLURE_AVAILABLE,
    AllureObserver,
    set_current_observer,
)

try:
    import allure
except ImportError:
    allure = None


@pytest.fixture(scope="function", autouse=True)
def _auto_allure_observer(request) -> Generator[AllureObserver | None, None, None]:
    """自动启用Allure观察者（零配置）

    autouse=True: 对所有测试自动生效，无需手动添加到测试参数
    scope=function: 每个测试函数独立的observer实例

    特性:
    - 零配置：无需在测试代码中手动启用
    - 自动记录：HTTP请求、拦截器、数据库查询
    - 静默终端：测试通过时无额外输出
    - 详细报告：Allure HTML报告包含完整详情
    - 测试隔离：v3.17.0 每个测试使用独立的 EventBus（不会互相干扰）

    工作原理:
    1. pytest运行每个测试前，自动创建AllureObserver
    2. 通过ContextVar将observer注入到全局上下文
    3. v3.17.0: 创建测试专用的 EventBus（测试隔离）
    4. HttpClient/MiddlewareChain自动调用observer记录操作
    5. 测试结束后，自动清理observer和EventBus

    使用场景:
        # 测试代码无需任何修改，自动记录
        def test_create_user(http_client):
            response = http_client.post("/api/users", json={"name": "Alice"})
            assert response.status_code == 201

        # 生成报告: pytest --alluredir=./allure-results
        # 查看报告: allure serve ./allure-results

    Allure报告内容:
        🌐 POST /api/users
          ├─ 📤 Request Details (JSON附件)
          │   {"method": "POST", "url": "/api/users", "json": {"name": "Alice"}}
          ├─ ⚙️ SignatureMiddleware (sub-step)
          │   └─ Changes: {"headers": {"added": {"X-Sign": "md5_..."}}}
          ├─ ⚙️ TokenMiddleware (sub-step)
          │   └─ Changes: {"headers": {"added": {"Authorization": "Bearer ..."}}}
          └─ ✅ Response (201) - 145ms (JSON附件)
              {"status_code": 201, "body": "{\"id\": 1, \"name\": \"Alice\"}"}

    注意:
    - 如果未安装allure-pytest，此fixture自动跳过
    - 不会影响测试执行，只是不生成Allure报告
    """
    # 如果Allure不可用，直接跳过
    if not ALLURE_AVAILABLE or allure is None:
        yield None
        return

    # 创建当前测试的observer
    test_name = request.node.name
    observer = AllureObserver(test_name=test_name)

    # 设置为当前上下文的observer（通过ContextVar，线程安全）
    set_current_observer(observer)

    # v3.17.0: 创建测试专用的 EventBus（测试隔离）
    # 每个测试使用独立的 EventBus，避免测试之间事件干扰
    test_event_bus = EventBus()
    set_test_event_bus(test_event_bus)

    # v3.18.0: 订阅所有能力层事件（统一 EventBus 驱动）
    # HTTP 事件
    test_event_bus.subscribe(HttpRequestStartEvent, observer.handle_http_request_start_event)
    test_event_bus.subscribe(HttpRequestEndEvent, observer.handle_http_request_end_event)
    test_event_bus.subscribe(HttpRequestErrorEvent, observer.handle_http_request_error_event)
    test_event_bus.subscribe(MiddlewareExecuteEvent, observer.handle_middleware_execute_event)

    # Database 事件
    test_event_bus.subscribe(DatabaseQueryStartEvent, observer.handle_database_query_start_event)
    test_event_bus.subscribe(DatabaseQueryEndEvent, observer.handle_database_query_end_event)
    test_event_bus.subscribe(DatabaseQueryErrorEvent, observer.handle_database_query_error_event)

    # Cache 事件 (Redis)
    test_event_bus.subscribe(CacheOperationStartEvent, observer.handle_cache_operation_start_event)
    test_event_bus.subscribe(CacheOperationEndEvent, observer.handle_cache_operation_end_event)
    test_event_bus.subscribe(CacheOperationErrorEvent, observer.handle_cache_operation_error_event)

    # MQ 事件
    test_event_bus.subscribe(MessagePublishEvent, observer.handle_message_publish_event)
    test_event_bus.subscribe(MessageConsumeEvent, observer.handle_message_consume_event)

    # Storage 事件
    test_event_bus.subscribe(
        StorageOperationStartEvent, observer.handle_storage_operation_start_event
    )
    test_event_bus.subscribe(StorageOperationEndEvent, observer.handle_storage_operation_end_event)
    test_event_bus.subscribe(
        StorageOperationErrorEvent, observer.handle_storage_operation_error_event
    )

    # Transaction 事件 (v3.18.0)
    test_event_bus.subscribe(TransactionCommitEvent, observer.handle_transaction_commit_event)
    test_event_bus.subscribe(TransactionRollbackEvent, observer.handle_transaction_rollback_event)

    try:
        # yield让测试执行
        # 注意: 不需要用 with allure.step()，因为HTTP请求会创建自己的step
        yield observer
    finally:
        # 测试结束，清理observer
        # cleanup() 会关闭所有未正常结束的 step 上下文（异常安全）
        observer.cleanup()
        set_current_observer(None)

        # v3.17.0: 清理测试专用的 EventBus
        test_event_bus.clear()
        set_test_event_bus(None)


__all__ = ["_auto_allure_observer"]
