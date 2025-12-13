"""
事件类型定义

定义框架中使用的各种事件类型。
所有事件都是不可变的 dataclass。

v3.17.0 重构:
- 添加 event_id 唯一标识
- 添加 CorrelatedEvent 支持 Start/End 事件关联
- 添加工厂方法创建事件
- 整合 OpenTelemetry 追踪上下文（trace_id/span_id）
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from df_test_framework.core.context.execution import ExecutionContext


def _get_current_trace_context() -> tuple[str | None, str | None]:
    """获取当前 OpenTelemetry 追踪上下文

    Returns:
        (trace_id, span_id) 元组，如果没有活动追踪则返回 (None, None)
    """
    try:
        from df_test_framework.infrastructure.tracing import OTEL_AVAILABLE

        if not OTEL_AVAILABLE:
            return None, None

        from opentelemetry import trace

        span = trace.get_current_span()
        if span and span.is_recording():
            ctx = span.get_span_context()
            # 格式化为十六进制字符串（标准格式）
            trace_id = format(ctx.trace_id, "032x")
            span_id = format(ctx.span_id, "016x")
            return trace_id, span_id
    except Exception:
        pass

    return None, None


def generate_event_id() -> str:
    """生成事件唯一 ID

    格式: evt-{12位十六进制}
    示例: evt-a1b2c3d4e5f6
    """
    return f"evt-{uuid.uuid4().hex[:12]}"


def generate_correlation_id() -> str:
    """生成关联 ID

    用于关联 Start/End 事件对。
    格式: cor-{12位十六进制}
    示例: cor-x7y8z9a1b2c3
    """
    return f"cor-{uuid.uuid4().hex[:12]}"


@dataclass(frozen=True)
class Event:
    """事件基类

    所有事件都应继承此类。

    属性:
        event_id: 事件唯一标识（自动生成）
        timestamp: 事件发生时间（自动生成）
        context: 执行上下文（可选，用于追踪关联）
        trace_id: OpenTelemetry 追踪 ID（自动从当前 Span 获取）
        span_id: OpenTelemetry Span ID（自动从当前 Span 获取）

    v3.17.0: 新增 event_id 字段
    v3.17.0: 整合 OpenTelemetry，新增 trace_id/span_id 字段
    """

    event_id: str = field(default_factory=generate_event_id)
    timestamp: datetime = field(default_factory=datetime.now)
    context: ExecutionContext | None = None
    # OpenTelemetry 追踪上下文（可选，自动从当前 Span 获取）
    trace_id: str | None = field(default=None)
    span_id: str | None = field(default=None)


@dataclass(frozen=True)
class CorrelatedEvent(Event):
    """可关联事件基类

    用于 Start/End 事件对的关联。
    同一对 Start/End 事件共享相同的 correlation_id。

    属性:
        correlation_id: 关联 ID（同一对 Start/End 共享）

    v3.17.0: 新增
    """

    correlation_id: str = ""


# =============================================================================
# HTTP 事件
# =============================================================================


@dataclass(frozen=True)
class HttpRequestStartEvent(CorrelatedEvent):
    """HTTP 请求开始事件

    在发送 HTTP 请求前触发。
    correlation_id 由发布者生成，End 事件复用同一 ID。

    v3.17.0: 继承 CorrelatedEvent，添加工厂方法
    """

    method: str = ""
    url: str = ""
    headers: dict[str, str] = field(default_factory=dict)
    body: str | None = None

    @classmethod
    def create(
        cls,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        body: str | None = None,
        context: ExecutionContext | None = None,
    ) -> tuple["HttpRequestStartEvent", str]:
        """工厂方法：创建事件并返回 correlation_id

        自动注入当前 OpenTelemetry 追踪上下文（trace_id/span_id）。

        Args:
            method: HTTP 方法
            url: 请求 URL
            headers: 请求头
            body: 请求体
            context: 执行上下文

        Returns:
            (event, correlation_id) 元组
        """
        correlation_id = generate_correlation_id()
        # 自动获取当前追踪上下文
        trace_id, span_id = _get_current_trace_context()
        event = cls(
            method=method,
            url=url,
            headers=headers or {},
            body=body,
            correlation_id=correlation_id,
            context=context,
            trace_id=trace_id,
            span_id=span_id,
        )
        return event, correlation_id


@dataclass(frozen=True)
class HttpRequestEndEvent(CorrelatedEvent):
    """HTTP 请求结束事件

    在收到 HTTP 响应后触发。
    correlation_id 必须与对应的 StartEvent 相同。

    v3.17.0: 继承 CorrelatedEvent，添加工厂方法
    """

    method: str = ""
    url: str = ""
    status_code: int = 0
    duration: float = 0.0
    headers: dict[str, str] = field(default_factory=dict)
    body: str | None = None

    @classmethod
    def create(
        cls,
        correlation_id: str,
        method: str,
        url: str,
        status_code: int,
        duration: float,
        headers: dict[str, str] | None = None,
        body: str | None = None,
        context: ExecutionContext | None = None,
    ) -> "HttpRequestEndEvent":
        """工厂方法：创建事件（复用 correlation_id）

        自动注入当前 OpenTelemetry 追踪上下文（trace_id/span_id）。

        Args:
            correlation_id: 关联 ID（必须与 StartEvent 相同）
            method: HTTP 方法
            url: 请求 URL
            status_code: 响应状态码
            duration: 请求耗时（秒）
            headers: 响应头
            body: 响应体
            context: 执行上下文

        Returns:
            HttpRequestEndEvent 实例
        """
        # 自动获取当前追踪上下文
        trace_id, span_id = _get_current_trace_context()
        return cls(
            method=method,
            url=url,
            status_code=status_code,
            duration=duration,
            headers=headers or {},
            body=body,
            correlation_id=correlation_id,
            context=context,
            trace_id=trace_id,
            span_id=span_id,
        )


@dataclass(frozen=True)
class HttpRequestErrorEvent(CorrelatedEvent):
    """HTTP 请求错误事件

    在 HTTP 请求发生异常时触发。

    v3.17.0: 继承 CorrelatedEvent，添加工厂方法
    """

    method: str = ""
    url: str = ""
    error_type: str = ""
    error_message: str = ""
    duration: float = 0.0

    @classmethod
    def create(
        cls,
        correlation_id: str,
        method: str,
        url: str,
        error: Exception,
        duration: float,
        context: ExecutionContext | None = None,
    ) -> "HttpRequestErrorEvent":
        """工厂方法：创建错误事件

        自动注入当前 OpenTelemetry 追踪上下文（trace_id/span_id）。

        Args:
            correlation_id: 关联 ID
            method: HTTP 方法
            url: 请求 URL
            error: 异常对象
            duration: 请求耗时（秒）
            context: 执行上下文

        Returns:
            HttpRequestErrorEvent 实例
        """
        # 自动获取当前追踪上下文
        trace_id, span_id = _get_current_trace_context()
        return cls(
            method=method,
            url=url,
            error_type=type(error).__name__,
            error_message=str(error),
            duration=duration,
            correlation_id=correlation_id,
            context=context,
            trace_id=trace_id,
            span_id=span_id,
        )


# =============================================================================
# 中间件事件
# =============================================================================


@dataclass(frozen=True)
class MiddlewareExecuteEvent(CorrelatedEvent):
    """中间件执行事件

    记录中间件对请求/响应的修改。

    v3.17.0 新增
    """

    middleware_name: str = ""
    phase: str = ""  # "before" 或 "after"
    changes: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        correlation_id: str,
        middleware_name: str,
        phase: str,
        changes: dict[str, Any],
        context: ExecutionContext | None = None,
    ) -> "MiddlewareExecuteEvent":
        """工厂方法：创建中间件执行事件

        自动注入当前 OpenTelemetry 追踪上下文（trace_id/span_id）。

        Args:
            correlation_id: 关联 ID（与请求事件相同）
            middleware_name: 中间件名称
            phase: 执行阶段 ("before" 或 "after")
            changes: 中间件做的修改

        Returns:
            MiddlewareExecuteEvent 实例
        """
        # 自动获取当前追踪上下文
        trace_id, span_id = _get_current_trace_context()
        return cls(
            middleware_name=middleware_name,
            phase=phase,
            changes=changes,
            correlation_id=correlation_id,
            context=context,
            trace_id=trace_id,
            span_id=span_id,
        )


# =============================================================================
# Database 事件
# =============================================================================


@dataclass(frozen=True)
class DatabaseQueryStartEvent(CorrelatedEvent):
    """数据库查询开始事件

    v3.18.0: 升级为 CorrelatedEvent，支持 Start/End 事件关联
    """

    operation: str = ""  # SELECT, INSERT, UPDATE, DELETE
    table: str = ""
    sql: str = ""
    params: dict[str, Any] = field(default_factory=dict)
    database: str | None = None

    @classmethod
    def create(
        cls,
        operation: str,
        table: str,
        sql: str,
        params: dict[str, Any] | None = None,
        database: str | None = None,
        context: ExecutionContext | None = None,
    ) -> tuple["DatabaseQueryStartEvent", str]:
        """工厂方法：创建事件并返回 correlation_id

        Args:
            operation: 操作类型（SELECT/INSERT/UPDATE/DELETE）
            table: 表名
            sql: SQL 语句
            params: SQL 参数
            database: 数据库名
            context: 执行上下文

        Returns:
            (event, correlation_id) 元组
        """
        correlation_id = generate_correlation_id()
        trace_id, span_id = _get_current_trace_context()
        event = cls(
            operation=operation,
            table=table,
            sql=sql,
            params=params or {},
            database=database,
            correlation_id=correlation_id,
            context=context,
            trace_id=trace_id,
            span_id=span_id,
        )
        return event, correlation_id


@dataclass(frozen=True)
class DatabaseQueryEndEvent(CorrelatedEvent):
    """数据库查询结束事件

    v3.18.0: 升级为 CorrelatedEvent，支持 Start/End 事件关联
    """

    operation: str = ""
    table: str = ""
    sql: str = ""
    params: dict[str, Any] = field(default_factory=dict)
    duration_ms: float = 0.0
    row_count: int = 0
    database: str | None = None

    @classmethod
    def create(
        cls,
        correlation_id: str,
        operation: str,
        table: str,
        sql: str,
        params: dict[str, Any] | None = None,
        duration_ms: float = 0.0,
        row_count: int = 0,
        database: str | None = None,
        context: ExecutionContext | None = None,
    ) -> "DatabaseQueryEndEvent":
        """工厂方法：创建事件（复用 correlation_id）"""
        trace_id, span_id = _get_current_trace_context()
        return cls(
            operation=operation,
            table=table,
            sql=sql,
            params=params or {},
            duration_ms=duration_ms,
            row_count=row_count,
            database=database,
            correlation_id=correlation_id,
            context=context,
            trace_id=trace_id,
            span_id=span_id,
        )


@dataclass(frozen=True)
class DatabaseQueryErrorEvent(CorrelatedEvent):
    """数据库查询错误事件

    v3.18.0: 升级为 CorrelatedEvent，支持 Start/End 事件关联
    """

    operation: str = ""
    table: str = ""
    sql: str = ""
    params: dict[str, Any] = field(default_factory=dict)
    error_type: str = ""
    error_message: str = ""
    duration_ms: float = 0.0
    database: str | None = None

    @classmethod
    def create(
        cls,
        correlation_id: str,
        operation: str,
        table: str,
        sql: str,
        params: dict[str, Any] | None = None,
        error: Exception | None = None,
        duration_ms: float = 0.0,
        database: str | None = None,
        context: ExecutionContext | None = None,
    ) -> "DatabaseQueryErrorEvent":
        """工厂方法：创建事件（复用 correlation_id）"""
        trace_id, span_id = _get_current_trace_context()
        return cls(
            operation=operation,
            table=table,
            sql=sql,
            params=params or {},
            error_type=type(error).__name__ if error else "UnknownError",
            error_message=str(error) if error else "",
            duration_ms=duration_ms,
            database=database,
            correlation_id=correlation_id,
            context=context,
            trace_id=trace_id,
            span_id=span_id,
        )


# =============================================================================
# Cache 事件 (Redis)
# =============================================================================


@dataclass(frozen=True)
class CacheOperationStartEvent(CorrelatedEvent):
    """缓存操作开始事件

    在执行缓存操作前触发。
    correlation_id 由发布者生成，End 事件复用同一 ID。

    v3.18.0: 新增
    """

    operation: str = ""  # SET, GET, DELETE, HSET, HGET, LPUSH, SADD, ZADD 等
    key: str = ""
    field: str | None = None  # Hash 操作的 field

    @classmethod
    def create(
        cls,
        operation: str,
        key: str,
        field: str | None = None,
        context: ExecutionContext | None = None,
    ) -> tuple["CacheOperationStartEvent", str]:
        """工厂方法：创建事件并返回 correlation_id

        Args:
            operation: 缓存操作类型（SET, GET, DELETE 等）
            key: 缓存键
            field: Hash 操作的字段名（可选）
            context: 执行上下文

        Returns:
            (event, correlation_id) 元组
        """
        correlation_id = generate_correlation_id()
        trace_id, span_id = _get_current_trace_context()
        event = cls(
            operation=operation,
            key=key,
            field=field,
            correlation_id=correlation_id,
            context=context,
            trace_id=trace_id,
            span_id=span_id,
        )
        return event, correlation_id


@dataclass(frozen=True)
class CacheOperationEndEvent(CorrelatedEvent):
    """缓存操作结束事件

    在缓存操作完成后触发。
    correlation_id 必须与对应的 StartEvent 相同。

    v3.18.0: 新增
    """

    operation: str = ""
    key: str = ""
    hit: bool | None = None  # GET 操作是否命中（None 表示非 GET 操作）
    duration_ms: float = 0.0
    success: bool = True

    @classmethod
    def create(
        cls,
        correlation_id: str,
        operation: str,
        key: str,
        duration_ms: float,
        hit: bool | None = None,
        context: ExecutionContext | None = None,
    ) -> "CacheOperationEndEvent":
        """工厂方法：创建事件（复用 correlation_id）

        Args:
            correlation_id: 关联 ID（必须与 StartEvent 相同）
            operation: 缓存操作类型
            key: 缓存键
            duration_ms: 操作耗时（毫秒）
            hit: GET 操作是否命中
            context: 执行上下文

        Returns:
            CacheOperationEndEvent 实例
        """
        trace_id, span_id = _get_current_trace_context()
        return cls(
            operation=operation,
            key=key,
            hit=hit,
            duration_ms=duration_ms,
            correlation_id=correlation_id,
            context=context,
            trace_id=trace_id,
            span_id=span_id,
        )


@dataclass(frozen=True)
class CacheOperationErrorEvent(CorrelatedEvent):
    """缓存操作错误事件

    在缓存操作发生异常时触发。

    v3.18.0: 新增
    """

    operation: str = ""
    key: str = ""
    error_type: str = ""
    error_message: str = ""
    duration_ms: float = 0.0

    @classmethod
    def create(
        cls,
        correlation_id: str,
        operation: str,
        key: str,
        error: Exception,
        duration_ms: float,
        context: ExecutionContext | None = None,
    ) -> "CacheOperationErrorEvent":
        """工厂方法：创建错误事件

        Args:
            correlation_id: 关联 ID
            operation: 缓存操作类型
            key: 缓存键
            error: 异常对象
            duration_ms: 操作耗时（毫秒）
            context: 执行上下文

        Returns:
            CacheOperationErrorEvent 实例
        """
        trace_id, span_id = _get_current_trace_context()
        return cls(
            operation=operation,
            key=key,
            error_type=type(error).__name__,
            error_message=str(error),
            duration_ms=duration_ms,
            correlation_id=correlation_id,
            context=context,
            trace_id=trace_id,
            span_id=span_id,
        )


# =============================================================================
# MQ 事件
# =============================================================================


@dataclass(frozen=True)
class MessagePublishEvent(Event):
    """消息发布事件"""

    topic: str = ""
    message_id: str = ""
    body_size: int = 0
    partition: int | None = None


@dataclass(frozen=True)
class MessageConsumeEvent(Event):
    """消息消费事件"""

    topic: str = ""
    message_id: str = ""
    consumer_group: str = ""
    processing_time: float = 0.0
    partition: int | None = None
    offset: int | None = None


# =============================================================================
# Storage 事件 (v3.18.0)
# =============================================================================


@dataclass(frozen=True)
class StorageOperationStartEvent(CorrelatedEvent):
    """存储操作开始事件

    在执行存储操作前触发。
    correlation_id 由发布者生成，End 事件复用同一 ID。

    v3.18.0: 新增
    """

    storage_type: str = ""  # local, s3, oss
    operation: str = ""  # upload, download, delete, copy, move, list
    path: str = ""
    size: int | None = None  # 上传时的文件大小

    @classmethod
    def create(
        cls,
        storage_type: str,
        operation: str,
        path: str,
        size: int | None = None,
        context: ExecutionContext | None = None,
    ) -> tuple["StorageOperationStartEvent", str]:
        """工厂方法：创建事件并返回 correlation_id

        Args:
            storage_type: 存储类型（local, s3, oss）
            operation: 操作类型（upload, download, delete 等）
            path: 文件路径或对象键
            size: 文件大小（字节，上传时可用）
            context: 执行上下文

        Returns:
            (event, correlation_id) 元组
        """
        correlation_id = generate_correlation_id()
        trace_id, span_id = _get_current_trace_context()
        event = cls(
            storage_type=storage_type,
            operation=operation,
            path=path,
            size=size,
            correlation_id=correlation_id,
            context=context,
            trace_id=trace_id,
            span_id=span_id,
        )
        return event, correlation_id


@dataclass(frozen=True)
class StorageOperationEndEvent(CorrelatedEvent):
    """存储操作结束事件

    在存储操作完成后触发。
    correlation_id 必须与对应的 StartEvent 相同。

    v3.18.0: 新增
    """

    storage_type: str = ""
    operation: str = ""
    path: str = ""
    size: int | None = None  # 下载时的文件大小
    duration_ms: float = 0.0
    success: bool = True

    @classmethod
    def create(
        cls,
        correlation_id: str,
        storage_type: str,
        operation: str,
        path: str,
        duration_ms: float,
        size: int | None = None,
        context: ExecutionContext | None = None,
    ) -> "StorageOperationEndEvent":
        """工厂方法：创建事件（复用 correlation_id）

        Args:
            correlation_id: 关联 ID（必须与 StartEvent 相同）
            storage_type: 存储类型
            operation: 操作类型
            path: 文件路径或对象键
            duration_ms: 操作耗时（毫秒）
            size: 文件大小（字节）
            context: 执行上下文

        Returns:
            StorageOperationEndEvent 实例
        """
        trace_id, span_id = _get_current_trace_context()
        return cls(
            storage_type=storage_type,
            operation=operation,
            path=path,
            size=size,
            duration_ms=duration_ms,
            correlation_id=correlation_id,
            context=context,
            trace_id=trace_id,
            span_id=span_id,
        )


@dataclass(frozen=True)
class StorageOperationErrorEvent(CorrelatedEvent):
    """存储操作错误事件

    在存储操作发生异常时触发。

    v3.18.0: 新增
    """

    storage_type: str = ""
    operation: str = ""
    path: str = ""
    error_type: str = ""
    error_message: str = ""
    duration_ms: float = 0.0

    @classmethod
    def create(
        cls,
        correlation_id: str,
        storage_type: str,
        operation: str,
        path: str,
        error: Exception,
        duration_ms: float,
        context: ExecutionContext | None = None,
    ) -> "StorageOperationErrorEvent":
        """工厂方法：创建错误事件

        Args:
            correlation_id: 关联 ID
            storage_type: 存储类型
            operation: 操作类型
            path: 文件路径或对象键
            error: 异常对象
            duration_ms: 操作耗时（毫秒）
            context: 执行上下文

        Returns:
            StorageOperationErrorEvent 实例
        """
        trace_id, span_id = _get_current_trace_context()
        return cls(
            storage_type=storage_type,
            operation=operation,
            path=path,
            error_type=type(error).__name__,
            error_message=str(error),
            duration_ms=duration_ms,
            correlation_id=correlation_id,
            context=context,
            trace_id=trace_id,
            span_id=span_id,
        )


# =============================================================================
# 测试事件
# =============================================================================


@dataclass(frozen=True)
class TestStartEvent(Event):
    """测试开始事件"""

    test_name: str = ""
    test_file: str = ""
    markers: list[str] = field(default_factory=list)
    parameters: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TestEndEvent(Event):
    """测试结束事件"""

    test_name: str = ""
    test_file: str = ""
    status: str = ""  # passed, failed, skipped, error
    duration: float = 0.0
    failure_message: str | None = None
    markers: list[str] = field(default_factory=list)


# =============================================================================
# 事务事件 (v3.18.0)
# =============================================================================


@dataclass(frozen=True)
class TransactionCommitEvent(Event):
    """事务提交事件

    在 UnitOfWork.commit() 时触发。

    v3.18.0: 新增
    """

    repository_count: int = 0  # 涉及的 Repository 数量
    session_id: str | None = None  # Session 标识（可选）

    @classmethod
    def create(
        cls,
        repository_count: int = 0,
        session_id: str | None = None,
        context: ExecutionContext | None = None,
    ) -> "TransactionCommitEvent":
        """工厂方法：创建事件

        Args:
            repository_count: 涉及的 Repository 数量
            session_id: Session 标识
            context: 执行上下文

        Returns:
            TransactionCommitEvent 实例
        """
        trace_id, span_id = _get_current_trace_context()
        return cls(
            repository_count=repository_count,
            session_id=session_id,
            context=context,
            trace_id=trace_id,
            span_id=span_id,
        )


@dataclass(frozen=True)
class TransactionRollbackEvent(Event):
    """事务回滚事件

    在 UnitOfWork.rollback() 时触发。

    v3.18.0: 新增
    """

    repository_count: int = 0  # 涉及的 Repository 数量
    reason: str = "auto"  # auto: 自动回滚, exception: 异常回滚, manual: 手动回滚
    session_id: str | None = None  # Session 标识（可选）

    @classmethod
    def create(
        cls,
        repository_count: int = 0,
        reason: str = "auto",
        session_id: str | None = None,
        context: ExecutionContext | None = None,
    ) -> "TransactionRollbackEvent":
        """工厂方法：创建事件

        Args:
            repository_count: 涉及的 Repository 数量
            reason: 回滚原因（auto/exception/manual）
            session_id: Session 标识
            context: 执行上下文

        Returns:
            TransactionRollbackEvent 实例
        """
        trace_id, span_id = _get_current_trace_context()
        return cls(
            repository_count=repository_count,
            reason=reason,
            session_id=session_id,
            context=context,
            trace_id=trace_id,
            span_id=span_id,
        )
