"""
中间件工厂类

v3.16.0: 从 MiddlewareConfig 创建 Middleware 实例
"""

from typing import Any

from loguru import logger

from df_test_framework.core.middleware import BaseMiddleware
from df_test_framework.infrastructure.config.middleware_schema import (
    BearerTokenMiddlewareConfig,
    LoggingMiddlewareConfig,
    MiddlewareConfig,
    MiddlewareType,
    RetryMiddlewareConfig,
    SignatureMiddlewareConfig,
    TokenSource,
)

from .auth import BearerTokenMiddleware
from .logging import LoggingMiddleware
from .retry import RetryMiddleware
from .signature import SignatureMiddleware


class MiddlewareFactory:
    """中间件工厂

    从配置创建中间件实例。

    支持的中间件类型：
    - SIGNATURE: SignatureMiddleware
    - BEARER_TOKEN: BearerTokenMiddleware
    - RETRY: RetryMiddleware
    - LOGGING: LoggingMiddleware

    Example:
        ```python
        config = SignatureMiddlewareConfig(
            algorithm="md5",
            secret="my_secret",
        )

        middleware = MiddlewareFactory.create(config)
        ```
    """

    @staticmethod
    def create(config: MiddlewareConfig) -> BaseMiddleware | None:
        """从配置创建中间件实例

        Args:
            config: 中间件配置

        Returns:
            中间件实例，如果配置未启用则返回 None

        Raises:
            ValueError: 不支持的中间件类型
        """
        # 检查是否启用
        if not config.enabled:
            logger.debug(f"[MiddlewareFactory] 中间件已禁用，跳过创建: type={config.type}")
            return None

        # 根据类型创建对应的中间件
        if config.type == MiddlewareType.SIGNATURE:
            return MiddlewareFactory._create_signature(config)

        elif config.type == MiddlewareType.BEARER_TOKEN:
            return MiddlewareFactory._create_bearer_token(config)

        elif config.type == MiddlewareType.RETRY:
            return MiddlewareFactory._create_retry(config)

        elif config.type == MiddlewareType.LOGGING:
            return MiddlewareFactory._create_logging(config)

        else:
            raise ValueError(f"不支持的中间件类型: {config.type}")

    @staticmethod
    def _create_signature(config: SignatureMiddlewareConfig) -> SignatureMiddleware:
        """创建签名中间件"""
        logger.debug(
            f"[MiddlewareFactory] 创建签名中间件: "
            f"algorithm={config.algorithm}, priority={config.priority}"
        )

        return SignatureMiddleware(
            secret=config.secret,
            algorithm=config.algorithm.value,  # Enum → str
            header_name=config.header,
            priority=config.priority,
        )

    @staticmethod
    def _create_bearer_token(config: BearerTokenMiddlewareConfig) -> BearerTokenMiddleware:
        """创建 Bearer Token 中间件

        v3.17.0+: 支持 STATIC、LOGIN、ENV 三种模式。
        """
        logger.debug(
            f"[MiddlewareFactory] 创建 Bearer Token 中间件: "
            f"source={config.source}, priority={config.priority}"
        )

        # 导入辅助类
        from .auth import LoginTokenProvider, create_env_token_provider

        # 根据 token 来源创建不同的中间件
        if config.source == TokenSource.STATIC:
            # 静态 Token
            if not config.token:
                raise ValueError("BearerTokenMiddleware with source=STATIC requires token")

            return BearerTokenMiddleware(
                token=config.token,
                header_name=config.header,
                header_prefix=config.token_prefix,
                priority=config.priority,
            )

        elif config.source == TokenSource.LOGIN:
            # 动态登录获取 Token (v3.17.0+)
            if not config.login_url:
                raise ValueError("BearerTokenMiddleware with source=LOGIN requires login_url")
            if not config.credentials:
                raise ValueError("BearerTokenMiddleware with source=LOGIN requires credentials")

            # 创建 LoginTokenProvider
            login_provider = LoginTokenProvider(
                login_url=config.login_url,
                credentials=config.credentials,
                token_path=config.token_path if hasattr(config, "token_path") else "data.token",
                cache_token=True,
            )

            return BearerTokenMiddleware(
                login_token_provider=login_provider,
                header_name=config.header,
                header_prefix=config.token_prefix,
                priority=config.priority,
            )

        elif config.source == TokenSource.ENV:
            # 从环境变量获取 Token (v3.17.0+)
            env_var = config.env_var if hasattr(config, "env_var") else "API_TOKEN"
            token_provider = create_env_token_provider(env_var)

            return BearerTokenMiddleware(
                token_provider=token_provider,
                header_name=config.header,
                header_prefix=config.token_prefix,
                priority=config.priority,
            )

        else:
            raise ValueError(f"不支持的 TokenSource: {config.source}")

    @staticmethod
    def _create_retry(config: RetryMiddlewareConfig) -> RetryMiddleware:
        """创建重试中间件"""
        logger.debug(
            f"[MiddlewareFactory] 创建重试中间件: "
            f"max_retries={config.max_retries}, strategy={config.strategy}"
        )

        return RetryMiddleware(
            max_retries=config.max_retries,
            initial_delay=config.initial_delay,
            max_delay=config.max_delay,
            retry_on_status=config.retry_on_status,
            priority=config.priority,
        )

    @staticmethod
    def _create_logging(config: LoggingMiddlewareConfig) -> LoggingMiddleware:
        """创建日志中间件"""
        logger.debug(f"[MiddlewareFactory] 创建日志中间件: priority={config.priority}")

        return LoggingMiddleware(
            log_request=config.log_request,
            log_response=config.log_response,
            log_headers=config.log_headers,
            log_body=config.log_body,
            mask_fields=config.mask_fields,
            max_body_length=config.max_body_length,
            priority=config.priority,
        )


class PathFilteredMiddleware(BaseMiddleware[Any, Any]):
    """路径过滤中间件包装器

    包装其他中间件，只在匹配路径时执行。

    Example:
        ```python
        # 原始中间件
        signature = SignatureMiddleware(secret="secret")

        # 包装为路径过滤中间件
        filtered = PathFilteredMiddleware(
            middleware=signature,
            include_paths=["/api/**", "/admin/**"],
            exclude_paths=["/api/health"],
        )
        ```
    """

    def __init__(
        self,
        middleware: BaseMiddleware,
        include_paths: list[str] | None = None,
        exclude_paths: list[str] | None = None,
    ):
        """初始化路径过滤中间件

        Args:
            middleware: 被包装的中间件
            include_paths: 包含的路径模式（支持通配符）
            exclude_paths: 排除的路径模式（支持通配符）
        """
        super().__init__(
            name=f"PathFiltered[{middleware.name}]",
            priority=middleware.priority,
        )
        self._middleware = middleware
        self._include_paths = include_paths or []
        self._exclude_paths = exclude_paths or []

    async def __call__(self, request: Any, call_next):
        """执行路径匹配并调用内部中间件"""
        from df_test_framework.infrastructure.config.schema import PathPattern

        # 获取请求路径
        path = getattr(request, "url", None) or getattr(request, "path", "")

        # 检查排除路径
        for exclude_pattern in self._exclude_paths:
            pattern_obj = PathPattern(pattern=exclude_pattern, regex=False)
            if pattern_obj.matches(path):
                logger.debug(f"[{self.name}] 路径 {path} 匹配排除规则 {exclude_pattern}，跳过执行")
                return await call_next(request)

        # 检查包含路径
        should_execute = False
        if not self._include_paths:
            # 没有配置 include_paths，默认匹配所有路径
            should_execute = True
        else:
            for include_pattern in self._include_paths:
                pattern_obj = PathPattern(pattern=include_pattern, regex=False)
                if pattern_obj.matches(path):
                    should_execute = True
                    break

        if should_execute:
            logger.debug(f"[{self.name}] 路径 {path} 匹配规则，执行中间件")
            return await self._middleware(request, call_next)
        else:
            logger.debug(f"[{self.name}] 路径 {path} 不匹配规则，跳过执行")
            return await call_next(request)


__all__ = [
    "MiddlewareFactory",
    "PathFilteredMiddleware",
]
