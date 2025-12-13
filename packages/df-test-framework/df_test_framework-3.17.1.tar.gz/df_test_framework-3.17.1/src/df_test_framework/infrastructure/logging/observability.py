"""可观测性日志系统

提供统一的实时日志输出，用于本地调试和快速故障定位。

设计原则:
- 统一格式：所有组件使用相同的日志格式
- 实时输出：立即输出到终端，无需等待测试结束
- 可配置：支持独立开关，不影响Allure
- 结构化：使用Loguru的结构化日志能力

与Allure的区别:
- ObservabilityLogger: 实时、终端输出、即时故障定位
- Allure: 异步、HTML报告、可视化审计

Usage:
    >>> from df_test_framework.infrastructure.logging.observability import get_logger
    >>> logger = get_logger("HTTP")
    >>> logger.info("GET /api/users")
"""

from contextvars import ContextVar
from typing import Any

from loguru import logger as _loguru_logger

# 全局开关（优先级：显式设置 > FrameworkSettings > 默认值）
_observability_enabled: ContextVar[bool | None] = ContextVar("observability_enabled", default=None)


def set_observability_enabled(enabled: bool) -> None:
    """设置可观测性日志开关（显式设置，优先级最高）

    Args:
        enabled: 是否启用

    Example:
        >>> set_observability_enabled(False)  # 禁用实时日志
    """
    _observability_enabled.set(enabled)


def is_observability_enabled() -> bool:
    """检查可观测性日志是否启用

    优先级:
    1. 显式调用set_observability_enabled()设置的值
    2. FrameworkSettings.enable_observability配置
    3. 默认值: True

    Returns:
        是否启用

    Example:
        >>> is_observability_enabled()  # 检查当前状态
        True
    """
    # 1. 检查显式设置
    explicit_setting = _observability_enabled.get()
    if explicit_setting is not None:
        return explicit_setting

    # 2. 检查FrameworkSettings配置
    try:
        from ..config import get_settings

        settings = get_settings()
        return settings.enable_observability
    except Exception:
        # 如果获取settings失败（如未配置），使用默认值
        pass

    # 3. 默认启用
    return True


class ObservabilityLogger:
    """可观测性日志记录器

    提供统一格式的日志输出

    日志格式:
        [时间] [组件] [级别] 消息

    Example:
        >>> logger = ObservabilityLogger("HTTP")
        >>> logger.request_start("GET", "/api/users", request_id="req-001")
        [12:34:56] [HTTP] [req-001] → GET /api/users

        >>> logger.request_end("req-001", 200, 145.5)
        [12:34:56] [HTTP] [req-001] ← 200 OK (145.5ms)
    """

    def __init__(self, component: str):
        """初始化日志记录器

        Args:
            component: 组件名称（如HTTP、DB、Redis）
        """
        self.component = component
        self._logger = _loguru_logger.bind(component=component)

    def _should_log(self) -> bool:
        """检查是否应该记录日志

        Returns:
            是否应该记录
        """
        return is_observability_enabled()

    def _format_message(self, request_id: str | None, message: str) -> str:
        """格式化日志消息

        Args:
            request_id: 请求ID（可选）
            message: 消息内容

        Returns:
            格式化后的消息
        """
        if request_id:
            return f"[{request_id}] {message}"
        return message

    # HTTP相关日志方法

    def request_start(self, method: str, url: str, request_id: str | None = None) -> None:
        """记录HTTP请求开始

        Args:
            method: HTTP方法
            url: 请求URL
            request_id: 请求ID
        """
        if not self._should_log():
            return

        msg = self._format_message(request_id, f"→ {method} {url}")
        self._logger.info(msg)

    def request_headers(
        self, headers: dict[str, str], request_id: str | None = None, sanitize: bool = True
    ) -> None:
        """记录HTTP请求头（可选择性输出）

        Args:
            headers: 请求头
            request_id: 请求ID
            sanitize: 是否脱敏
        """
        if not self._should_log():
            return

        # 只输出关键headers（认证、签名等）
        key_headers = {
            k: (self._sanitize_value(v) if sanitize else v)
            for k, v in headers.items()
            if k.lower() in ("authorization", "x-sign", "x-token", "x-signature")
        }

        if key_headers:
            msg = self._format_message(request_id, f"Headers: {key_headers}")
            self._logger.debug(msg)

    def interceptor_execute(
        self, interceptor_name: str, changes: dict[str, Any], request_id: str | None = None
    ) -> None:
        """记录拦截器执行

        Args:
            interceptor_name: 拦截器名称
            changes: 变更内容
            request_id: 请求ID
        """
        if not self._should_log():
            return

        # 简化变更描述
        change_desc = self._describe_changes(changes)
        msg = self._format_message(request_id, f"Interceptor: {interceptor_name} → {change_desc}")
        self._logger.debug(msg)

    def request_end(self, request_id: str | None, status_code: int, duration_ms: float) -> None:
        """记录HTTP请求结束

        Args:
            request_id: 请求ID
            status_code: 响应状态码
            duration_ms: 耗时（毫秒）
        """
        if not self._should_log():
            return

        status_text = self._get_status_text(status_code)
        msg = self._format_message(
            request_id, f"← {status_code} {status_text} ({duration_ms:.1f}ms)"
        )

        # 根据状态码选择日志级别
        if 200 <= status_code < 300:
            self._logger.info(msg)
        elif 400 <= status_code < 500:
            self._logger.warning(msg)
        else:
            self._logger.error(msg)

    def request_error(self, error: Exception, request_id: str | None = None) -> None:
        """记录HTTP请求错误

        Args:
            error: 异常对象
            request_id: 请求ID
        """
        if not self._should_log():
            return

        msg = self._format_message(request_id, f"✗ Error: {error}")
        self._logger.error(msg)

    # Database相关日志方法

    def query_start(self, operation: str, table: str, query_id: str | None = None) -> None:
        """记录数据库查询开始

        Args:
            operation: 操作类型（SELECT/INSERT/UPDATE/DELETE）
            table: 表名
            query_id: 查询ID
        """
        if not self._should_log():
            return

        msg = self._format_message(query_id, f"→ {operation} {table}")
        self._logger.info(msg)

    def query_end(self, query_id: str | None, row_count: int, duration_ms: float) -> None:
        """记录数据库查询结束

        Args:
            query_id: 查询ID
            row_count: 影响行数
            duration_ms: 耗时（毫秒）
        """
        if not self._should_log():
            return

        msg = self._format_message(query_id, f"← {row_count} rows ({duration_ms:.1f}ms)")
        self._logger.info(msg)

    def query_error(self, error: Exception, query_id: str | None = None) -> None:
        """记录数据库查询错误

        Args:
            error: 异常对象
            query_id: 查询ID
        """
        if not self._should_log():
            return

        msg = self._format_message(query_id, f"✗ Error: {error}")
        self._logger.error(msg)

    # Redis相关日志方法

    def cache_operation(self, operation: str, key: str, hit: bool | None = None) -> None:
        """记录Redis缓存操作

        Args:
            operation: 操作类型（GET/SET/DELETE）
            key: 缓存键
            hit: 是否命中（仅GET操作）
        """
        if not self._should_log():
            return

        if operation == "GET" and hit is not None:
            result = "HIT ✓" if hit else "MISS ✗"
            msg = f"{operation} {key} → {result}"
        else:
            msg = f"{operation} {key}"

        self._logger.debug(msg)

    # 通用日志方法

    def info(self, message: str, request_id: str | None = None) -> None:
        """记录INFO级别日志

        Args:
            message: 消息内容
            request_id: 请求ID（可选）
        """
        if not self._should_log():
            return

        msg = self._format_message(request_id, message)
        self._logger.info(msg)

    def debug(self, message: str, request_id: str | None = None) -> None:
        """记录DEBUG级别日志

        Args:
            message: 消息内容
            request_id: 请求ID（可选）
        """
        if not self._should_log():
            return

        msg = self._format_message(request_id, message)
        self._logger.debug(msg)

    def warning(self, message: str, request_id: str | None = None) -> None:
        """记录WARNING级别日志

        Args:
            message: 消息内容
            request_id: 请求ID（可选）
        """
        if not self._should_log():
            return

        msg = self._format_message(request_id, message)
        self._logger.warning(msg)

    def error(self, message: str, request_id: str | None = None) -> None:
        """记录ERROR级别日志

        Args:
            message: 消息内容
            request_id: 请求ID（可选）
        """
        if not self._should_log():
            return

        msg = self._format_message(request_id, message)
        self._logger.error(msg)

    # 辅助方法

    def _sanitize_value(self, value: str) -> str:
        """脱敏敏感值

        Args:
            value: 原始值

        Returns:
            脱敏后的值
        """
        if len(value) <= 10:
            return value[:3] + "..."
        return value[:10] + "..."

    def _describe_changes(self, changes: dict[str, Any]) -> str:
        """描述变更内容

        Args:
            changes: 变更字典

        Returns:
            变更描述
        """
        descriptions = []

        if "headers" in changes:
            headers = changes["headers"]
            if "added" in headers:
                for key in headers["added"].keys():
                    descriptions.append(f"Added {key}")
            if "modified" in headers:
                for key in headers["modified"].keys():
                    descriptions.append(f"Modified {key}")

        if "params" in changes:
            descriptions.append("Modified params")

        if "json" in changes:
            descriptions.append("Modified json")

        return ", ".join(descriptions) if descriptions else "No changes"

    def _get_status_text(self, status_code: int) -> str:
        """获取HTTP状态码文本

        Args:
            status_code: 状态码

        Returns:
            状态文本
        """
        status_texts = {
            200: "OK",
            201: "Created",
            204: "No Content",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error",
            502: "Bad Gateway",
            503: "Service Unavailable",
        }
        return status_texts.get(status_code, "Unknown")


# 全局logger实例缓存
_logger_cache: dict[str, ObservabilityLogger] = {}


def get_logger(component: str) -> ObservabilityLogger:
    """获取组件的可观测性日志记录器

    Args:
        component: 组件名称（如HTTP、DB、Redis）

    Returns:
        日志记录器实例

    Example:
        >>> logger = get_logger("HTTP")
        >>> logger.request_start("GET", "/api/users", "req-001")
    """
    if component not in _logger_cache:
        _logger_cache[component] = ObservabilityLogger(component)
    return _logger_cache[component]


# 便捷方法
def http_logger() -> ObservabilityLogger:
    """获取HTTP日志记录器"""
    return get_logger("HTTP")


def db_logger() -> ObservabilityLogger:
    """获取Database日志记录器"""
    return get_logger("DB")


def redis_logger() -> ObservabilityLogger:
    """获取Redis日志记录器"""
    return get_logger("Redis")


__all__ = [
    "ObservabilityLogger",
    "get_logger",
    "http_logger",
    "db_logger",
    "redis_logger",
    "set_observability_enabled",
    "is_observability_enabled",
]
