"""
Configuration schemas used by df-test-framework.

Projects should subclass `FrameworkSettings` to add their own business fields.
"""

from __future__ import annotations

import os
import re
from typing import Any, Literal

from pydantic import BaseModel, Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# v3.16.0: HTTPSettings 已移除

EnvLiteral = Literal["dev", "test", "staging", "prod"]
LogFormatLiteral = Literal["text", "json"]
LogLevelLiteral = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class PathPattern(BaseModel):
    """路径模式配置

    支持:
    - 精确匹配: "/api/login"
    - 通配符: "/api/**" (匹配所有子路径), "/api/*/health" (匹配单级)
    - 正则表达式: "^/api/v[0-9]+/.*"

    Example:
        >>> pattern = PathPattern(pattern="/api/**", regex=False)
        >>> pattern.matches("/api/master/create")
        True
        >>> pattern.matches("/admin/login")
        False
    """

    pattern: str = Field(description="路径模式")
    regex: bool = Field(default=False, description="是否使用正则表达式")

    def matches(self, path: str) -> bool:
        """检查路径是否匹配

        自动标准化路径，支持有无前导斜杠（仅限通配符模式）。

        Args:
            path: 请求路径 (如: "/api/master/create" 或 "api/master/create")

        Returns:
            是否匹配

        Example:
            >>> pattern = PathPattern(pattern="/api/**")
            >>> pattern.matches("/api/users")  # ✅ True
            >>> pattern.matches("api/users")   # ✅ True (自动标准化)
        """
        # 自动标准化：统一添加前导斜杠
        normalized_path = path if path.startswith("/") else f"/{path}"

        # 正则表达式模式：不做normalize，直接匹配
        if self.regex:
            return bool(re.match(self.pattern, normalized_path))

        # 通配符模式：normalize后再匹配
        normalized_pattern = self.pattern if self.pattern.startswith("/") else f"/{self.pattern}"

        # 通配符匹配:
        # 1. ** → .* (匹配任意字符)
        # 2. * → [^/]* (匹配单级路径，不包含/)
        # 注意: 必须先替换**再替换*,避免**被误替换
        pattern = normalized_pattern.replace("**", "DOUBLE_STAR_PLACEHOLDER")
        pattern = pattern.replace("*", "[^/]*")
        pattern = pattern.replace("DOUBLE_STAR_PLACEHOLDER", ".*")
        return bool(re.match(f"^{pattern}$", normalized_path))


class InterceptorConfig(BaseModel):
    """拦截器配置基类

    所有拦截器配置都应继承此类

    ✅ v3.4.0特性:
    - 自动路径标准化: 支持 "/api/**" 和 "api/**" 两种写法
    - 自动配置验证: 检查配置冲突

    Attributes:
        type: 拦截器类型标识
        enabled: 是否启用
        priority: 优先级(数字越小越先执行)
        include_paths: 包含的路径模式列表
        exclude_paths: 排除的路径模式列表
        use_regex: 路径模式是否使用正则表达式
    """

    type: str = Field(description="拦截器类型")
    enabled: bool = Field(default=True, description="是否启用")
    priority: int = Field(default=100, description="优先级(数字越小越先执行)")

    # 路径模式配置
    include_paths: list[str] = Field(
        default_factory=lambda: ["/**"],
        description="包含的路径模式列表 (如: ['/api/**', '/admin/**'])",
    )
    exclude_paths: list[str] = Field(
        default_factory=list, description="排除的路径模式列表 (如: ['/api/health', '/api/login'])"
    )
    use_regex: bool = Field(default=False, description="路径模式是否使用正则表达式")

    @model_validator(mode="after")
    def normalize_paths(self) -> InterceptorConfig:
        """✅ v3.4.0: 自动标准化路径模式

        规范化路径格式，确保都以斜杠开头（更直观）:
        - "api/**" → "/api/**"
        - "/api/**" → "/api/**" (保持不变)
        """
        # 标准化include_paths
        self.include_paths = [p if p.startswith("/") else f"/{p}" for p in self.include_paths]

        # 标准化exclude_paths
        self.exclude_paths = [p if p.startswith("/") else f"/{p}" for p in self.exclude_paths]

        return self

    def should_apply(self, path: str) -> bool:
        """判断拦截器是否应用于指定路径

        Args:
            path: 请求路径 (如: "/api/master/create")

        Returns:
            是否应用拦截器
        """
        if not self.enabled:
            return False

        # 1. 检查排除路径
        for exclude_pattern in self.exclude_paths:
            pattern_obj = PathPattern(pattern=exclude_pattern, regex=self.use_regex)
            if pattern_obj.matches(path):
                return False  # 匹配排除规则,不应用

        # 2. 检查包含路径
        for include_pattern in self.include_paths:
            pattern_obj = PathPattern(pattern=include_pattern, regex=self.use_regex)
            if pattern_obj.matches(path):
                return True  # 匹配包含规则,应用

        return False  # 不匹配任何规则,不应用


class SignatureInterceptorConfig(InterceptorConfig):
    """签名拦截器配置

    支持多种签名算法,与Java后端的SignatureInterceptor对应

    Example:
        >>> config = SignatureInterceptorConfig(
        ...     type="signature",
        ...     enabled=True,
        ...     algorithm="md5",
        ...     secret="my_secret",
        ...     header_name="X-Sign",
        ...     include_paths=["/api/**"],
        ...     exclude_paths=["/api/health"]
        ... )
    """

    type: str = Field(default="signature", description="拦截器类型")

    algorithm: Literal["md5", "sha256", "hmac-sha256", "hmac-sha512"] = Field(
        default="md5", description="签名算法"
    )

    secret: str = Field(description="签名密钥")

    header_name: str = Field(default="X-Sign", description="签名Header名称")

    include_query_params: bool = Field(default=True, description="是否包含URL参数")
    include_json_body: bool = Field(default=True, description="是否包含JSON body")
    include_form_data: bool = Field(default=False, description="是否包含表单数据")


class TokenInterceptorConfig(InterceptorConfig):
    """Token拦截器配置

    Example:
        >>> config = TokenInterceptorConfig(
        ...     type="token",
        ...     enabled=True,
        ...     token="your_token",
        ...     token_type="Bearer",
        ...     header_name="Authorization"
        ... )
    """

    type: str = Field(default="token", description="拦截器类型")

    token: str = Field(description="认证Token")

    token_type: str = Field(default="Bearer", description="Token类型")

    header_name: str = Field(default="Authorization", description="认证Header名称")


class BearerTokenInterceptorConfig(InterceptorConfig):
    """Bearer Token认证拦截器配置

    支持三种Token来源:
    - static: 使用静态Token
    - login: 调用登录接口获取
    - env: 从环境变量读取
    - custom: 自定义获取方式（需要提供回调函数）

    ✅ v3.4.0特性:
    - 自动排除login_url: 当token_source="login"时，自动将login_url添加到exclude_paths，防止无限递归
    - 配置验证: 检查login配置完整性

    Example:
        >>> # 通过登录获取Token
        >>> config = BearerTokenInterceptorConfig(
        ...     type="bearer_token",
        ...     enabled=True,
        ...     token_source="login",
        ...     login_url="/admin/login",
        ...     login_credentials={"username": "admin", "password": "admin123"},
        ...     include_paths=["/admin/**"],
        ...     # ✅ v3.4.0: login_url会自动添加到exclude_paths，无需手动配置
        ... )
        >>> # 使用静态Token
        >>> config = BearerTokenInterceptorConfig(
        ...     type="bearer_token",
        ...     token_source="static",
        ...     static_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        ... )
    """

    type: str = Field(default="bearer_token", description="拦截器类型")

    token_source: Literal["static", "login", "env", "custom"] = Field(
        default="login",
        description="Token来源: static(静态Token) / login(登录获取) / env(环境变量) / custom(自定义)",
    )

    # token_source="static" 时使用
    static_token: str | None = Field(default=None, description="静态Token值")

    # token_source="login" 时使用
    login_url: str | None = Field(default=None, description="登录接口URL (相对路径或绝对路径)")
    login_credentials: dict[str, str] | None = Field(
        default=None, description="登录凭证（如: {'username': 'admin', 'password': 'xxx'}）"
    )
    token_field_path: str = Field(
        default="data.token", description="Token在响应中的字段路径 (如: 'data.token' 或 'token')"
    )

    # token_source="env" 时使用
    env_var_name: str = Field(default="API_TOKEN", description="环境变量名称")

    # 通用配置
    header_name: str = Field(default="Authorization", description="认证Header名称")
    token_prefix: str = Field(default="Bearer", description="Token前缀 (如: 'Bearer', 'Token')")

    @model_validator(mode="after")
    def validate_and_auto_exclude_login_url(self) -> BearerTokenInterceptorConfig:
        """✅ v3.4.0: 自动排除login_url，防止无限递归

        当token_source="login"时:
        1. 验证login_url和login_credentials是否配置
        2. 自动将login_url添加到exclude_paths

        Raises:
            ValueError: 如果login配置不完整
        """
        # 首先调用父类的normalize_paths (Pydantic v2会自动调用)
        # 注意：父类的validator已经在此之前执行了

        if self.token_source == "login":
            # 1. 验证login配置完整性
            if not self.login_url:
                raise ValueError(
                    "BearerTokenInterceptorConfig with token_source='login' requires 'login_url' to be configured"
                )
            if not self.login_credentials:
                raise ValueError(
                    "BearerTokenInterceptorConfig with token_source='login' requires 'login_credentials' to be configured"
                )

            # 2. 自动排除login_url（防止无限递归）
            # 标准化login_url路径
            login_path = self.login_url if self.login_url.startswith("/") else f"/{self.login_url}"

            # 检查是否已在exclude_paths中
            if login_path not in self.exclude_paths:
                # 自动添加
                self.exclude_paths.append(login_path)

        return self


class CustomInterceptorConfig(InterceptorConfig):
    """自定义拦截器配置

    用于加载用户自定义的拦截器类

    Example:
        >>> config = CustomInterceptorConfig(
        ...     type="custom",
        ...     enabled=True,
        ...     class_path="my_project.interceptors.CustomInterceptor",
        ...     params={"key": "value"}
        ... )
    """

    type: str = Field(default="custom", description="拦截器类型")

    class_path: str = Field(
        description="拦截器类的完整路径 (如: my_project.interceptors.MyInterceptor)"
    )

    params: dict[str, Any] = Field(default_factory=dict, description="传递给拦截器构造函数的参数")


class HTTPConfig(BaseModel):
    """HTTP client configuration.

    v3.16.0: 新增 middlewares 字段，取代 interceptors
    - middlewares: 新的中间件配置（推荐）
    - interceptors: 旧的拦截器配置（兼容，自动迁移到 middlewares）
    """

    base_url: str | None = Field(default="http://localhost:8000", description="API base URL")
    timeout: int = Field(default=30, ge=1, le=300, description="Request timeout (seconds)")
    max_retries: int = Field(default=3, ge=0, le=10, description="Retry count for transient errors")
    verify_ssl: bool = Field(default=True, description="Whether to verify SSL certificates")
    max_connections: int = Field(default=50, ge=1, le=500, description="Total connection pool size")
    max_keepalive_connections: int = Field(
        default=20, ge=1, le=200, description="Keep-alive pool size"
    )

    # v3.16.0: 新的中间件配置系统
    middlewares: list[Any] = Field(
        default_factory=list, description="HTTP中间件配置列表（v3.16.0+）"
    )

    # ⚠️ 已废弃: 保留用于向后兼容（v3.16.0 将在运行时自动迁移到 middlewares）
    interceptors: list[InterceptorConfig] = Field(
        default_factory=list, description="HTTP拦截器配置列表（已废弃，请使用 middlewares）"
    )

    @field_validator("timeout")
    @classmethod
    def _validate_timeout(cls, value: int) -> int:
        if value < 5:
            raise ValueError("HTTP timeout should not be lower than 5 seconds")
        return value

    @model_validator(mode="after")
    def migrate_interceptors_to_middlewares(self) -> HTTPConfig:
        """✅ v3.16.0: 自动将 interceptors 迁移到 middlewares

        迁移规则:
        1. 如果 middlewares 为空且 interceptors 有值，执行迁移
        2. 如果两者都有值，打印警告并优先使用 middlewares
        3. 迁移映射:
           - SignatureInterceptorConfig → SignatureMiddlewareConfig
           - BearerTokenInterceptorConfig → BearerTokenMiddlewareConfig
           - 其他类型按需添加
        """
        from loguru import logger

        # 导入 middleware 配置类
        from .middleware_schema import (
            BearerTokenMiddlewareConfig,
            SignatureMiddlewareConfig,
            TokenSource,
        )

        # 情况1: 同时配置了 middlewares 和 interceptors
        if self.middlewares and self.interceptors:
            logger.warning(
                "[HTTPConfig] 同时配置了 middlewares 和 interceptors，"
                "将优先使用 middlewares。建议移除 interceptors 配置。"
            )
            return self

        # 情况2: 只配置了 interceptors，执行自动迁移
        if not self.middlewares and self.interceptors:
            logger.info(
                f"[HTTPConfig] 检测到旧的 interceptors 配置（{len(self.interceptors)} 个），"
                "正在自动迁移到 middlewares..."
            )

            for interceptor in self.interceptors:
                try:
                    # 签名拦截器迁移
                    if interceptor.type == "signature":
                        middleware = SignatureMiddlewareConfig(
                            algorithm=interceptor.algorithm,
                            secret=interceptor.secret,
                            header=interceptor.header_name,
                            enabled=interceptor.enabled,
                            priority=interceptor.priority,
                            include_paths=interceptor.include_paths,
                            exclude_paths=interceptor.exclude_paths,
                        )
                        self.middlewares.append(middleware)
                        logger.debug(
                            "[HTTPConfig] ✅ 已迁移 SignatureInterceptor → SignatureMiddleware"
                        )

                    # Bearer Token 拦截器迁移
                    elif interceptor.type == "bearer_token":
                        # 映射 token_source
                        source_map = {
                            "static": TokenSource.STATIC,
                            "login": TokenSource.LOGIN,
                            "env": TokenSource.ENV,
                        }
                        token_source = source_map.get(interceptor.token_source, TokenSource.LOGIN)

                        # 构建 credentials
                        credentials = {}
                        if hasattr(interceptor, "login_credentials"):
                            credentials = interceptor.login_credentials or {}

                        middleware = BearerTokenMiddlewareConfig(
                            source=token_source,
                            token=getattr(interceptor, "static_token", None),
                            login_url=getattr(interceptor, "login_url", None),
                            credentials=credentials,
                            enabled=interceptor.enabled,
                            priority=interceptor.priority,
                            include_paths=interceptor.include_paths,
                            exclude_paths=interceptor.exclude_paths,
                        )
                        self.middlewares.append(middleware)
                        logger.debug(
                            "[HTTPConfig] ✅ 已迁移 BearerTokenInterceptor → BearerTokenMiddleware"
                        )

                    else:
                        logger.warning(
                            f"[HTTPConfig] ⚠️  未知的拦截器类型: {interceptor.type}，跳过迁移"
                        )

                except Exception as e:
                    logger.error(f"[HTTPConfig] ❌ 迁移拦截器失败: {interceptor.type}, 错误: {e}")

            logger.info(f"[HTTPConfig] 迁移完成！成功迁移 {len(self.middlewares)} 个中间件。")

        return self

    def model_post_init(self, __context) -> None:
        """模型初始化后验证

        ✅ v3.4.0: 增强配置验证
        - 检查BearerToken拦截器的login_url是否在exclude_paths中
        - 检查不同拦截器的路径是否冲突
        """
        from loguru import logger

        # 1. 检查Bearer Token拦截器的login_url
        for interceptor in self.interceptors:
            if hasattr(interceptor, "token_source") and interceptor.token_source == "login":
                if not hasattr(interceptor, "login_url") or not interceptor.login_url:
                    raise ValueError(
                        "BearerTokenInterceptor with token_source='login' requires 'login_url' to be configured"
                    )

                # 提取login路径（去除base_url）
                login_url = interceptor.login_url
                if self.base_url and login_url.startswith(self.base_url):
                    login_path = login_url.replace(self.base_url, "")
                elif login_url.startswith("http"):
                    # 完整URL，无法检查
                    continue
                else:
                    login_path = login_url

                # 标准化路径
                login_path = login_path if login_path.startswith("/") else f"/{login_path}"

                # 检查是否在exclude_paths中
                exclude_paths = getattr(interceptor, "exclude_paths", [])
                normalized_excludes = [p if p.startswith("/") else f"/{p}" for p in exclude_paths]

                if login_path not in normalized_excludes:
                    logger.warning(
                        f"⚠️  BearerTokenInterceptor的login_url '{login_path}' 不在exclude_paths中，"
                        f"可能导致无限递归！建议添加: exclude_paths=[..., '{login_path.lstrip('/')}']"
                    )

        # 2. 检查路径冲突（签名 vs Token）
        signature_paths = set()
        token_paths = set()

        for interceptor in self.interceptors:
            include_paths = getattr(interceptor, "include_paths", [])
            normalized_includes = [p if p.startswith("/") else f"/{p}" for p in include_paths]

            # 判断拦截器类型
            if hasattr(interceptor, "algorithm"):  # SignatureInterceptor
                signature_paths.update(normalized_includes)
            elif hasattr(interceptor, "token_source"):  # BearerTokenInterceptor
                token_paths.update(normalized_includes)

        # 检查是否有完全相同的路径
        conflicts = signature_paths & token_paths
        if conflicts:
            logger.warning(
                f"⚠️  签名拦截器和BearerToken拦截器配置了相同的路径: {conflicts}\n"
                f"   同一路径通常不应同时使用两种认证方式，请检查配置是否合理"
            )


class DatabaseConfig(BaseModel):
    """Database connectivity configuration."""

    connection_string: str | None = Field(
        default=None,
        description="Database connection string, e.g. mysql+pymysql://user:pass@host/db",
    )
    host: str | None = Field(
        default=None, description="Database host (if connection_string is not set)"
    )
    port: int | None = Field(default=None, ge=1, le=65535, description="Database port")
    name: str | None = Field(default=None, description="Database name/schema")
    user: str | None = Field(default=None, description="Database username")
    password: SecretStr | None = Field(default=None, description="Database password")
    charset: str = Field(default="utf8mb4", description="Connection charset")

    pool_size: int = Field(default=10, ge=1, le=100, description="Connection pool size")
    max_overflow: int = Field(
        default=20, ge=0, le=100, description="Extra connections beyond pool_size"
    )
    pool_timeout: int = Field(default=30, ge=1, le=300, description="Pool timeout (seconds)")
    pool_recycle: int = Field(default=3600, ge=60, description="Connection recycle time (seconds)")
    pool_pre_ping: bool = Field(default=True, description="Enable SQLAlchemy pool pre-ping")
    echo: bool = Field(default=False, description="Enable SQL logging for debugging")

    @field_validator("pool_size")
    @classmethod
    def _validate_pool_size(cls, value: int) -> int:
        if value < 5:
            raise ValueError("Database pool size should not be lower than 5")
        return value

    def resolved_connection_string(self) -> str:
        if self.connection_string:
            return self.connection_string
        required = [self.host, self.port, self.name, self.user, self.password]
        if not all(required):
            raise ValueError(
                "Database configuration incomplete. Set connection_string or provide host/port/name/user/password."
            )
        password = self.password.get_secret_value() if self.password else ""
        return (
            f"mysql+pymysql://{self.user}:{password}"
            f"@{self.host}:{self.port}/{self.name}"
            f"?charset={self.charset}"
        )


class RedisConfig(BaseModel):
    """Redis connectivity configuration."""

    host: str = Field(default="localhost", description="Redis host")
    port: int = Field(default=6379, ge=1, le=65535, description="Redis port")
    db: int = Field(default=0, ge=0, le=15, description="Redis database index")
    password: SecretStr | None = Field(default=None, description="Redis password")
    decode_responses: bool = Field(default=True, description="Decode bytes to str automatically")
    socket_timeout: int = Field(default=5, ge=1, le=60, description="Socket timeout (seconds)")
    socket_connect_timeout: int = Field(
        default=5, ge=1, le=60, description="Connection timeout (seconds)"
    )
    max_connections: int = Field(default=50, ge=1, le=1000, description="Connection pool size")
    retry_on_timeout: bool = Field(default=True, description="Retry commands on timeout")


class StorageConfig(BaseModel):
    """Storage configuration.

    支持多种存储类型的统一配置

    Example:
        >>> # 配置本地文件存储
        >>> config = StorageConfig(
        ...     local_file=LocalFileConfig(
        ...         base_path="./test-data",
        ...         auto_create_dirs=True
        ...     )
        ... )
        >>>
        >>> # 配置 S3 对象存储
        >>> config = StorageConfig(
        ...     s3=S3Config(
        ...         endpoint_url="http://localhost:9000",
        ...         access_key="minioadmin",
        ...         secret_key="minioadmin",
        ...         bucket_name="test-bucket"
        ...     )
        ... )
        >>>
        >>> # 配置阿里云 OSS 对象存储
        >>> config = StorageConfig(
        ...     oss=OSSConfig(
        ...         access_key_id="LTAI5t...",
        ...         access_key_secret="xxx...",
        ...         bucket_name="my-bucket",
        ...         endpoint="oss-cn-hangzhou.aliyuncs.com"
        ...     )
        ... )
    """

    # 导入存储配置类（延迟导入避免循环依赖）
    local_file: Any | None = Field(
        default=None, description="Local file system storage configuration"
    )
    s3: Any | None = Field(default=None, description="S3-compatible object storage configuration")
    oss: Any | None = Field(default=None, description="Aliyun OSS object storage configuration")


class TestExecutionConfig(BaseModel):
    """Test execution related settings."""

    parallel_workers: int = Field(default=4, ge=1, le=64, description="Parallel worker count")
    retry_times: int = Field(default=0, ge=0, le=5, description="Retry count for flaky tests")
    default_timeout: int = Field(
        default=300, ge=10, le=3600, description="Default case timeout (seconds)"
    )
    keep_test_data: bool = Field(
        default=False,
        description="保留测试数据（不清理），可通过 KEEP_TEST_DATA=1 环境变量或 .env 配置",
    )
    # v3.13.0: Repository 自动发现配置
    repository_package: str | None = Field(
        default=None,
        description="Repository 包路径，启用 UoW 自动发现。例如: 'my_project.repositories'",
    )

    @field_validator("keep_test_data", mode="before")
    @classmethod
    def _validate_keep_test_data(cls, value: Any) -> bool:
        """支持多种布尔值表示：1/0, true/false, yes/no"""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ("1", "true", "yes", "on")
        return bool(value)

    @field_validator("parallel_workers")
    @classmethod
    def _validate_parallel_workers(cls, value: int) -> int:
        cpu_count = os.cpu_count() or 4
        limit = cpu_count * 2
        if value > limit:
            raise ValueError(
                f"parallel_workers ({value}) should not exceed {limit} on this machine"
            )
        return value


class LoggingConfig(BaseModel):
    """Logging strategy configuration."""

    level: LogLevelLiteral = Field(default="INFO", description="Log level")
    format: LogFormatLiteral = Field(default="text", description="Log output format")
    file: str | None = Field(default=None, description="Optional log file path")
    rotation: str = Field(default="100 MB", description="Log rotation policy (loguru format)")
    retention: str = Field(default="7 days", description="Log retention policy (loguru format)")
    enable_console: bool = Field(default=True, description="Enable console logging")
    sanitize: bool = Field(default=True, description="Mask sensitive fields automatically")


class SignatureConfig(BaseModel):
    """Signature authentication configuration.

    用于配置HTTP签名认证的参数

    Example:
        >>> config = SignatureConfig(
        ...     enabled=True,
        ...     algorithm="md5",
        ...     secret="my_secret",
        ...     header_name="X-Sign"
        ... )
    """

    enabled: bool = Field(default=True, description="是否启用签名验证")

    algorithm: Literal["md5", "sha256", "hmac-sha256", "hmac-sha512"] = Field(
        default="md5", description="签名算法"
    )

    secret: str = Field(description="签名密钥")

    header_name: str = Field(default="X-Sign", description="签名Header名称")

    # 高级配置
    include_query_params: bool = Field(default=True, description="是否包含URL查询参数")

    include_json_body: bool = Field(default=True, description="是否包含JSON请求体")

    include_form_data: bool = Field(default=False, description="是否包含表单数据")


class FrameworkSettings(BaseSettings):
    """
    Base configuration schema for df-test-framework.

    Projects should inherit this class and extend with their own business settings.

    ✅ v3.5+: 现代化配置设计
    - 完全声明式配置（不依赖os.getenv()）
    - 嵌套配置（HTTPSettings → Interceptors）
    - 类型安全和自动验证
    - 不需要load_dotenv()

    环境变量配置：
        # HTTP配置（通过HTTPSettings嵌套）
        APP_HTTP_BASE_URL - API基础URL
        APP_HTTP_TIMEOUT - 请求超时时间
        APP_SIGNATURE_ENABLED - 启用签名拦截器
        APP_TOKEN_ENABLED - 启用Token拦截器

        # 数据库配置
        APP_DB__HOST - 数据库主机
        APP_DB__PORT - 数据库端口

        # Redis配置
        APP_REDIS__HOST - Redis主机
        APP_REDIS__PORT - Redis端口
    """

    env: EnvLiteral = Field(default="test", description="Runtime environment")
    debug: bool = Field(default=False, description="Enable debug mode")

    # ✅ v3.5: 可观测性配置
    enable_observability: bool = Field(
        default=True, description="Enable real-time observability logging (ObservabilityLogger)"
    )
    enable_allure: bool = Field(
        default=True, description="Enable Allure reporting integration (AllureObserver)"
    )
    observability_level: LogLevelLiteral = Field(
        default="INFO",
        description="Observability logging level (DEBUG/INFO/WARNING/ERROR/CRITICAL)",
    )

    # v3.16.0: http_settings 字段已移除
    # 请使用 HTTPConfig 和 middleware 配置
    http: HTTPConfig = Field(default_factory=HTTPConfig, description="HTTP configuration")

    db: DatabaseConfig | None = Field(
        default_factory=DatabaseConfig, description="Database configuration"
    )
    redis: RedisConfig | None = Field(
        default_factory=RedisConfig, description="Redis configuration"
    )
    storage: StorageConfig | None = Field(
        default_factory=StorageConfig, description="Storage configuration"
    )
    test: TestExecutionConfig | None = Field(
        default_factory=TestExecutionConfig, description="Test execution configuration"
    )
    logging: LoggingConfig | None = Field(
        default_factory=LoggingConfig, description="Logging configuration"
    )

    extras: dict = Field(
        default_factory=dict, description="Arbitrary extra configuration namespace"
    )

    # v3.16.0: _init_http_settings 和 get_http_config 已移除
    # http 现在是直接字段，不再是计算属性

    @property
    def is_dev(self) -> bool:
        return self.env == "dev"

    @property
    def is_test(self) -> bool:
        return self.env == "test"

    @property
    def is_staging(self) -> bool:
        return self.env == "staging"

    @property
    def is_prod(self) -> bool:
        return self.env == "prod"

    @field_validator("env")
    @classmethod
    def _validate_env(cls, value: EnvLiteral) -> EnvLiteral:
        if value == "prod" and os.getenv("CI") == "true":
            raise ValueError("Running production configuration in CI is not allowed")
        return value

    @field_validator("debug")
    @classmethod
    def _validate_debug(cls, value: bool, info) -> bool:
        env = info.data.get("env", "test")
        if value and env == "prod":
            raise ValueError("Debug mode must not be enabled in production")
        return value

    # Pydantic v2配置
    model_config = SettingsConfigDict(
        env_prefix="APP_",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_ignore_empty=True,
        extra="allow",
        env_file=".env",
        env_file_encoding="utf-8",
    )
