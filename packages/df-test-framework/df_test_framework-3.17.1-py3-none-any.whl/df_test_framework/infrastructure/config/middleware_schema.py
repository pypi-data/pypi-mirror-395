"""
Middleware 配置模式定义

v3.16.0: 新的中间件配置系统，取代旧的 InterceptorConfig
- 统一的 MiddlewareConfig 基类
- 路径匹配规则（include_paths, exclude_paths）
- 优先级排序（priority）
- 启用/禁用控制（enabled）
"""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class MiddlewareType(str, Enum):
    """中间件类型枚举"""

    SIGNATURE = "signature"
    BEARER_TOKEN = "bearer_token"
    RETRY = "retry"
    LOGGING = "logging"
    TIMEOUT = "timeout"
    RATE_LIMIT = "rate_limit"
    CIRCUIT_BREAKER = "circuit_breaker"


class MiddlewareConfig(BaseModel):
    """
    中间件配置基类

    所有中间件配置必须继承此类。

    Attributes:
        type: 中间件类型（唯一标识）
        enabled: 是否启用（默认 True）
        priority: 执行优先级（数字越小越先执行，默认 50）
        include_paths: 路径白名单（支持通配符 *，如 /api/**）
        exclude_paths: 路径黑名单（支持通配符 *）
    """

    type: MiddlewareType
    enabled: bool = Field(default=True, description="是否启用该中间件")
    priority: int = Field(default=50, ge=0, le=100, description="执行优先级 (0-100)")
    include_paths: list[str] = Field(default_factory=list, description="路径白名单（支持通配符）")
    exclude_paths: list[str] = Field(default_factory=list, description="路径黑名单（支持通配符）")

    @field_validator("include_paths", "exclude_paths", mode="before")
    @classmethod
    def normalize_paths(cls, value: Any) -> list[str]:
        """规范化路径列表"""
        if value is None:
            return []
        if isinstance(value, str):
            return [value]
        return list(value)


# ============================================================
# 具体中间件配置类
# ============================================================


class SignatureAlgorithm(str, Enum):
    """签名算法"""

    MD5 = "md5"
    SHA256 = "sha256"
    HMAC_SHA256 = "hmac_sha256"


class SignatureMiddlewareConfig(MiddlewareConfig):
    """
    签名中间件配置

    用于 API 请求签名认证。

    Example:
        ```python
        config = SignatureMiddlewareConfig(
            algorithm="md5",
            secret="your_secret_key",
            header="X-Sign",
            include_paths=["/api/**", "/master/**"],
        )
        ```
    """

    type: MiddlewareType = Field(default=MiddlewareType.SIGNATURE, frozen=True)
    algorithm: SignatureAlgorithm = Field(description="签名算法")
    secret: str = Field(description="签名密钥")
    header: str = Field(default="X-Sign", description="签名 Header 名称")
    param_name: str | None = Field(default=None, description="签名参数名称（用于查询字符串）")
    exclude_keys: list[str] = Field(default_factory=list, description="签名时排除的参数 key")


class TokenSource(str, Enum):
    """Token 来源"""

    LOGIN = "login"  # 动态登录获取
    STATIC = "static"  # 静态配置
    ENV = "env"  # 环境变量


class BearerTokenMiddlewareConfig(MiddlewareConfig):
    """
    Bearer Token 中间件配置

    用于 JWT/Bearer Token 认证。

    v3.17.0+: 支持 STATIC、LOGIN、ENV 三种模式。

    Example:
        ```python
        # 方式1: 静态 Token
        config = BearerTokenMiddlewareConfig(
            source="static",
            token="your_static_token_here",
        )

        # 方式2: 动态登录（v3.17.0+）
        config = BearerTokenMiddlewareConfig(
            source="login",
            login_url="/auth/login",
            credentials={"username": "admin", "password": "pass"},
            token_path="data.token",  # 从响应 JSON 中提取 Token 的路径
        )

        # 方式3: 环境变量（v3.17.0+）
        config = BearerTokenMiddlewareConfig(
            source="env",
            env_var="MY_API_TOKEN",
        )
        ```
    """

    type: MiddlewareType = Field(default=MiddlewareType.BEARER_TOKEN, frozen=True)
    source: TokenSource = Field(description="Token 来源")
    token: str | None = Field(default=None, description="静态 Token（source=static 时使用）")
    login_url: str | None = Field(default=None, description="登录接口 URL（source=login 时使用）")
    credentials: dict[str, Any] = Field(
        default_factory=dict, description="登录凭据（source=login 时使用）"
    )
    token_path: str = Field(
        default="data.token",
        description="Token 在响应 JSON 中的路径（source=login 时使用，如 'data.token'）",
    )
    env_var: str = Field(default="API_TOKEN", description="环境变量名称（source=env 时使用）")
    header: str = Field(default="Authorization", description="Token Header 名称")
    token_prefix: str = Field(default="Bearer", description="Token 前缀")


class RetryStrategy(str, Enum):
    """重试策略"""

    FIXED = "fixed"  # 固定间隔
    EXPONENTIAL = "exponential"  # 指数退避
    LINEAR = "linear"  # 线性增长


class RetryMiddlewareConfig(MiddlewareConfig):
    """
    重试中间件配置

    用于自动重试失败的请求。

    Example:
        ```python
        config = RetryMiddlewareConfig(
            max_retries=3,
            strategy="exponential",
            initial_delay=1.0,
            retry_on_status=[500, 502, 503, 504],
        )
        ```
    """

    type: MiddlewareType = Field(default=MiddlewareType.RETRY, frozen=True)
    max_retries: int = Field(default=3, ge=0, description="最大重试次数")
    strategy: RetryStrategy = Field(default=RetryStrategy.EXPONENTIAL, description="重试策略")
    initial_delay: float = Field(default=1.0, ge=0, description="初始延迟（秒）")
    max_delay: float = Field(default=60.0, ge=0, description="最大延迟（秒）")
    retry_on_status: list[int] = Field(
        default_factory=lambda: [500, 502, 503, 504],
        description="需要重试的 HTTP 状态码",
    )
    retry_on_exceptions: list[str] = Field(
        default_factory=lambda: ["TimeoutError", "ConnectionError"],
        description="需要重试的异常类型",
    )


class LoggingMiddlewareConfig(MiddlewareConfig):
    """
    日志中间件配置

    用于记录 HTTP 请求/响应日志。

    Example:
        ```python
        config = LoggingMiddlewareConfig(
            log_request=True,
            log_response=True,
            log_headers=False,
            mask_fields=["password", "token"],
        )
        ```
    """

    type: MiddlewareType = Field(default=MiddlewareType.LOGGING, frozen=True)
    log_request: bool = Field(default=True, description="是否记录请求")
    log_response: bool = Field(default=True, description="是否记录响应")
    log_headers: bool = Field(default=False, description="是否记录 Headers")
    log_body: bool = Field(default=True, description="是否记录 Body")
    mask_fields: list[str] = Field(
        default_factory=lambda: ["password", "token", "secret"],
        description="需要脱敏的字段",
    )
    max_body_length: int = Field(default=1000, description="Body 日志最大长度")


# ============================================================
# 导出
# ============================================================

__all__ = [
    # 枚举
    "MiddlewareType",
    "SignatureAlgorithm",
    "TokenSource",
    "RetryStrategy",
    # 配置类
    "MiddlewareConfig",
    "SignatureMiddlewareConfig",
    "BearerTokenMiddlewareConfig",
    "RetryMiddlewareConfig",
    "LoggingMiddlewareConfig",
]
