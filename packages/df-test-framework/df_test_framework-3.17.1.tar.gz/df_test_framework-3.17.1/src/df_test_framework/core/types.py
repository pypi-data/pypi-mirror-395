"""
核心类型定义

v3.14.0: 从 common/types.py 迁移到 core/types.py
"""

from enum import Enum
from typing import Any, TypeVar


class Environment(str, Enum):
    """环境枚举"""

    DEV = "dev"
    TEST = "test"
    STAGING = "staging"
    PRODUCTION = "production"
    PROD = "prod"

    @classmethod
    def from_string(cls, value: str) -> "Environment":
        """从字符串创建环境枚举"""
        value_lower = value.lower()
        for env in cls:
            if env.value == value_lower:
                return env
        raise ValueError(f"Unknown environment: {value}")


class LogLevel(str, Enum):
    """日志级别"""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class HttpMethod(str, Enum):
    """HTTP 方法"""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class DatabaseDialect(str, Enum):
    """数据库方言"""

    MYSQL = "mysql"
    POSTGRESQL = "postgresql"
    SQLITE = "sqlite"
    ORACLE = "oracle"
    MSSQL = "mssql"


class MessageQueueType(str, Enum):
    """消息队列类型"""

    KAFKA = "kafka"
    RABBITMQ = "rabbitmq"
    ROCKETMQ = "rocketmq"


class StorageType(str, Enum):
    """存储类型"""

    S3 = "s3"
    OSS = "oss"
    MINIO = "minio"
    LOCAL = "local"


# HTTP状态码分组
class HttpStatusGroup(str, Enum):
    """HTTP状态码分组"""

    INFORMATIONAL = "1xx"  # 信息响应
    SUCCESS = "2xx"  # 成功响应
    REDIRECTION = "3xx"  # 重定向
    CLIENT_ERROR = "4xx"  # 客户端错误
    SERVER_ERROR = "5xx"  # 服务器错误


# 常用HTTP状态码
class HttpStatus(int, Enum):
    """常用HTTP状态码"""

    # 2xx 成功
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204

    # 3xx 重定向
    MOVED_PERMANENTLY = 301
    FOUND = 302
    NOT_MODIFIED = 304

    # 4xx 客户端错误
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    TOO_MANY_REQUESTS = 429

    # 5xx 服务器错误
    INTERNAL_SERVER_ERROR = 500
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504


# 数据库操作类型
class DatabaseOperation(str, Enum):
    """数据库操作类型"""

    SELECT = "SELECT"
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


# 测试优先级
class TestPriority(str, Enum):
    """测试用例优先级"""

    CRITICAL = "critical"  # 关键
    HIGH = "high"  # 高
    MEDIUM = "medium"  # 中
    LOW = "low"  # 低


# 测试类型
class TestType(str, Enum):
    """测试类型"""

    SMOKE = "smoke"  # 冒烟测试
    REGRESSION = "regression"  # 回归测试
    INTEGRATION = "integration"  # 集成测试
    E2E = "e2e"  # 端到端测试
    PERFORMANCE = "performance"  # 性能测试
    SECURITY = "security"  # 安全测试


# 类型变量
TRequest = TypeVar("TRequest")
TResponse = TypeVar("TResponse")

# 通用类型别名
JsonDict = dict[str, Any]
Headers = dict[str, str]
QueryParams = dict[str, Any]
