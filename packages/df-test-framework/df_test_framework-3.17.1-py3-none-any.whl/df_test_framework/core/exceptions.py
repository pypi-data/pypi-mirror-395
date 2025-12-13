"""
框架异常体系

v3.14.0: 从 common/exceptions.py 迁移到 core/exceptions.py
"""

from typing import Any


class FrameworkError(Exception):
    """框架基础异常

    所有框架异常的基类
    """

    def __init__(self, message: str = "", details: dict[str, Any] | None = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ConfigurationError(FrameworkError):
    """配置错误

    配置文件格式错误、必填项缺失、值校验失败等
    """

    pass


class HttpError(FrameworkError):
    """HTTP 错误

    HTTP 请求失败、响应解析错误等
    """

    def __init__(
        self,
        message: str = "",
        status_code: int | None = None,
        response_body: str | None = None,
        details: dict[str, Any] | None = None,
    ):
        super().__init__(message, details)
        self.status_code = status_code
        self.response_body = response_body


class DatabaseError(FrameworkError):
    """数据库错误

    连接失败、查询错误、事务错误等
    """

    def __init__(
        self,
        message: str = "",
        sql: str | None = None,
        params: dict[str, Any] | None = None,
        details: dict[str, Any] | None = None,
    ):
        super().__init__(message, details)
        self.sql = sql
        self.params = params


class MessengerError(FrameworkError):
    """消息队列错误

    发送/消费消息失败等
    """

    def __init__(
        self,
        message: str = "",
        topic: str | None = None,
        details: dict[str, Any] | None = None,
    ):
        super().__init__(message, details)
        self.topic = topic


class StorageError(FrameworkError):
    """存储错误

    文件上传/下载失败等
    """

    def __init__(
        self,
        message: str = "",
        bucket: str | None = None,
        key: str | None = None,
        details: dict[str, Any] | None = None,
    ):
        super().__init__(message, details)
        self.bucket = bucket
        self.key = key


class MiddlewareError(FrameworkError):
    """中间件错误

    中间件执行过程中的错误
    """

    def __init__(
        self,
        message: str = "",
        middleware_name: str | None = None,
        details: dict[str, Any] | None = None,
    ):
        super().__init__(message, details)
        self.middleware_name = middleware_name


class MiddlewareAbort(Exception):
    """中间件主动终止请求

    使用场景：认证失败、限流触发等

    当中间件需要主动终止请求链时抛出此异常，
    可选地携带一个预设响应返回给调用者。
    """

    def __init__(
        self,
        message: str = "",
        response: Any = None,
    ):
        super().__init__(message)
        self.response = response


class PluginError(FrameworkError):
    """插件错误

    插件加载、注册、执行错误等
    """

    def __init__(
        self,
        message: str = "",
        plugin_name: str | None = None,
        details: dict[str, Any] | None = None,
    ):
        super().__init__(message, details)
        self.plugin_name = plugin_name


class TelemetryError(FrameworkError):
    """可观测性错误

    追踪、指标、日志配置或导出错误等
    """

    pass


class ResourceError(FrameworkError):
    """资源错误

    资源（数据库、Redis、HTTP等）访问或操作错误的基类。
    """

    pass


class RedisError(FrameworkError):
    """Redis错误

    Redis连接或操作错误。
    """

    def __init__(
        self,
        message: str = "",
        key: str | None = None,
        details: dict[str, Any] | None = None,
    ):
        super().__init__(message, details)
        self.key = key


class ValidationError(FrameworkError):
    """验证错误

    数据验证、参数检查等错误。
    """

    pass


class ExtensionError(FrameworkError):
    """扩展错误

    扩展加载、执行或Hook调用错误。
    """

    pass


class ProviderError(FrameworkError):
    """Provider错误

    Provider注册、查找或实例化错误。
    """

    pass


class TestError(FrameworkError):
    """测试错误

    测试执行过程中的框架级错误（不是测试断言失败）。
    """

    pass
