"""增强的 settings.py 生成模板

包含完整的v3.5+ HTTPSettings和中间件配置示例
"""

SETTINGS_ENHANCED_TEMPLATE = """\"\"\"项目配置 - v3.5+ 完全声明式配置

基于df-test-framework v3.5+的测试项目配置。

v3.5+核心特性:
- ✅ 完全声明式配置（不需要load_dotenv()和os.getenv()）
- ✅ HTTPSettings嵌套配置（零代码中间件配置）
- ✅ Profile环境配置支持（dev/test/prod）
- ✅ 业务配置分离（清晰的配置分层）
- ✅ 类型安全和自动验证（Pydantic v2）

使用示例:
    >>> from df_test_framework import Bootstrap
    >>> from {project_name_snake}.settings import {ProjectName}Settings
    >>>
    >>> # ✅ 不需要load_dotenv()，Pydantic自动加载
    >>> runtime = Bootstrap().with_settings({ProjectName}Settings).build().run()
    >>> http_client = runtime.http_client()
    >>> # 中间件自动生效，无需手动添加
    >>>
    >>> # 方式2: 指定Profile
    >>> runtime = Bootstrap().with_settings({ProjectName}Settings, profile="dev").build().run()
    >>>
    >>> # 方式3: 运行时覆盖配置
    >>> runtime = (
    ...     Bootstrap()
    ...     .with_settings({ProjectName}Settings)
    ...     .build()
    ...     .run()
    ...     .with_overrides({{
    ...         "http.timeout": 5,
    ...         "http.max_retries": 1,
    ...     }})
    ... )
\"\"\"

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from df_test_framework import (
    FrameworkSettings,
    DatabaseConfig,
    RedisConfig,
    LoggingConfig,
)

from df_test_framework.infrastructure.config import (
    HTTPSettings,
    SignatureMiddlewareSettings,
    BearerTokenMiddlewareSettings,
)


# ============================================================
# 自定义 HTTP 配置（继承HTTPSettings）
# ============================================================

class {ProjectName}HTTPSettings(HTTPSettings):
    \"\"\"项目HTTP配置 - 完整中间件配置示例

    v3.5+ 特性:
    - ✅ 完全声明式配置
    - ✅ 嵌套中间件配置
    - ✅ 自动环境变量绑定
    - ✅ 自动生成HTTPConfig对象

    环境变量：
        # HTTP基础配置
        APP_HTTP_BASE_URL - API基础URL
        APP_HTTP_TIMEOUT - 请求超时时间
        APP_HTTP_MAX_RETRIES - 最大重试次数

        # 签名中间件配置
        APP_SIGNATURE_ENABLED - 是否启用签名中间件
        APP_SIGNATURE_ALGORITHM - 签名算法（md5/sha256/hmac-sha256）
        APP_SIGNATURE_SECRET - 签名密钥

        # Token中间件配置
        APP_TOKEN_ENABLED - 是否启用Token中间件
        APP_TOKEN_TOKEN_SOURCE - Token来源（login/env/static）
        APP_TOKEN_USERNAME - 登录用户名
        APP_TOKEN_PASSWORD - 登录密码

    中间件执行顺序（按 priority 从小到大）:
        1. SignatureMiddleware (priority=10) - 添加签名
        2. BearerTokenMiddleware (priority=20) - 添加认证Token

    路径匹配规则:
        - 支持通配符: /api/** 匹配所有 /api/ 开头的路径
        - 支持正则: r'^/api/v\\d+/.*' 匹配版本化API
        - include_paths: 包含路径列表
        - exclude_paths: 排除路径列表
    \"\"\"

    # ========== HTTP基础配置（自定义默认值） ==========
    base_url: str = Field(
        default="http://localhost:8000",
        description="API基础URL"
    )

    # ========== 签名中间件配置（完整示例） ==========
    signature: SignatureMiddlewareSettings = Field(
        default_factory=lambda: SignatureMiddlewareSettings(
            # 基础配置
            enabled=True,  # ✅ 默认启用（可通过APP_SIGNATURE_ENABLED覆盖）
            priority=10,   # 优先级：数字越小越先执行

            # 签名算法配置
            algorithm="md5",  # 支持: md5, sha256, hmac-sha256
            secret="change_me_in_production",  # ⚠️ 生产环境必须通过环境变量覆盖

            # 签名Header配置
            header_name="X-Sign",  # 签名Header名称
            timestamp_header="X-Timestamp",  # 时间戳Header名称

            # 签名计算范围
            include_query_params=True,   # 包含查询参数
            include_json_body=True,      # 包含JSON请求体
            include_timestamp=True,      # 包含时间戳
            include_nonce=False,         # 包含随机数（防重放）

            # 路径匹配规则
            include_paths=["/api/**"],   # 包含路径（通配符）
            exclude_paths=[              # 排除路径
                "/health",
                "/metrics",
                "/api/public/**",
            ],

            # 高级配置（可选）
            # sign_format="{{method}}\\n{{path}}\\n{{timestamp}}\\n{{body}}",
        )
    )

    # ========== Token中间件配置（完整示例） ==========
    token: BearerTokenMiddlewareSettings = Field(
        default_factory=lambda: BearerTokenMiddlewareSettings(
            # 基础配置
            enabled=True,  # ✅ 默认启用（可通过APP_TOKEN_ENABLED覆盖）
            priority=20,   # 优先级：在签名之后执行

            # Token来源配置
            token_source="login",  # 支持: static, login, env, custom

            # === token_source=login 时的配置 ===
            login_url="/api/auth/login",  # 登录接口
            username="admin",  # ⚠️ 生产环境必须通过环境变量覆盖
            password="admin123",  # ⚠️ 生产环境必须通过环境变量覆盖
            token_field_path="data.token",  # Token在响应中的路径（支持嵌套）

            # Token Header配置
            header_name="Authorization",  # Token Header名称
            token_prefix="Bearer",        # Token前缀

            # 路径匹配规则
            include_paths=["/api/**"],
            exclude_paths=[
                "/api/public/**",
                "/api/auth/**",  # 排除登录接口本身
            ],

            # Token缓存配置
            cache_enabled=True,   # 启用Token缓存
            cache_ttl=3600,       # 缓存TTL（秒）
            auto_refresh=True,    # 自动刷新Token

            # 重试配置
            max_retries=3,        # 登录失败最大重试次数
        )
    )


# ============================================================
# 数据库配置（可选）
# ============================================================

# 注意：如果需要数据库和Redis配置，请在主配置类中添加，示例如下：
# db: DatabaseConfig = Field(
#     default_factory=lambda: DatabaseConfig(
#         host="localhost",
#         port=3306,
#         name="test_db",
#         user="root",
#         password="password",  # ⚠️ 生产环境必须通过环境变量覆盖
#         pool_size=10,
#         charset="utf8mb4",
#     )
# )
#
# redis: RedisConfig = Field(
#     default_factory=lambda: RedisConfig(
#         host="localhost",
#         port=6379,
#         db=0,
#         password=None,  # 如果需要密码，请设置
#     )
# )


# ============================================================
# 业务配置类
# ============================================================

class BusinessConfig(BaseSettings):
    \"\"\"业务配置

    清晰的配置分层:
    - 独立于框架配置
    - 包含业务特定的测试数据和配置
    - 使用 BUSINESS_ 前缀的环境变量
    \"\"\"

    # === 测试数据配置 ===
    test_user_id: str = Field(
        default="test_user_001",
        description="测试用户ID"
    )
    test_role: str = Field(
        default="admin",
        description="测试角色"
    )

    # === 业务规则配置 ===
    max_retry_count: int = Field(
        default=3,
        description="最大重试次数"
    )
    timeout_seconds: int = Field(
        default=30,
        description="超时时间（秒）"
    )

    # === API配置 ===
    api_version: str = Field(
        default="v1",
        description="API版本"
    )

    model_config = SettingsConfigDict(
        env_prefix="BUSINESS_",
        env_file=".env",
        extra="ignore",
    )


# ============================================================
# 主配置类
# ============================================================

class {ProjectName}Settings(FrameworkSettings):
    \"\"\"项目测试配置（v3.5+ 完全声明式配置）

    v3.5+特性:
    - ✅ HTTPSettings嵌套配置（零代码中间件配置）
    - ✅ 完全声明式（不需要load_dotenv()和os.getenv()）
    - ✅ Profile 环境配置（.env.dev/.env.test/.env.prod）
    - ✅ 运行时配置覆盖（with_overrides）
    - ✅ 可观测性集成（日志/Allure自动记录）
    - ✅ 业务配置（测试数据配置）

    环境变量配置:
        # HTTP配置（使用自定义HTTPSettings）
        APP_HTTP_BASE_URL - API基础URL
        APP_HTTP_TIMEOUT - 请求超时时间
        APP_HTTP_MAX_RETRIES - 最大重试次数

        # 签名中间件配置
        APP_SIGNATURE_ENABLED - 签名中间件开关
        APP_SIGNATURE_ALGORITHM - 签名算法（md5/sha256/hmac-sha256）
        APP_SIGNATURE_SECRET - 签名密钥

        # Token中间件配置
        APP_TOKEN_ENABLED - Token中间件开关
        APP_TOKEN_USERNAME - Admin登录用户名
        APP_TOKEN_PASSWORD - Admin登录密码

        # 数据库配置（如果启用）
        APP_DB__HOST - 数据库主机
        APP_DB__PORT - 数据库端口
        APP_DB__NAME - 数据库名称
        APP_DB__USER - 数据库用户
        APP_DB__PASSWORD - 数据库密码

        # Redis配置（如果启用）
        APP_REDIS__HOST - Redis主机
        APP_REDIS__PORT - Redis端口
        APP_REDIS__DB - Redis数据库索引
        APP_REDIS__PASSWORD - Redis密码

        # 业务配置
        BUSINESS_TEST_USER_ID - 测试用户ID
        BUSINESS_TEST_ROLE - 测试角色

    Profile配置:
        dev: 开发环境（.env.dev）
        test: 测试环境（.env.test）
        prod: 生产环境（.env.prod）

    使用示例:
        >>> from df_test_framework import Bootstrap
        >>> runtime = Bootstrap().with_settings({ProjectName}Settings).build().run()
        >>> http_client = runtime.http_client()
        >>> print(runtime.settings.business.test_user_id)
    \"\"\"

    # ========== HTTP配置（使用自定义HTTPSettings） ==========
    http_settings: {ProjectName}HTTPSettings = Field(
        default_factory={ProjectName}HTTPSettings,
        description="HTTP配置（包含中间件）"
    )

    # ========== 日志配置 ==========
    logging: LoggingConfig = Field(
        default_factory=lambda: LoggingConfig(
            level="INFO",
            enable_observability=True,
            enable_http_logging=True,
            enable_db_logging=True,
            enable_allure_logging=True,
        ),
        description="日志配置"
    )

    # ========== 数据库配置（可选） ==========
    # 提示: 如果需要数据库，请取消下面的注释并修改默认值
    # db: DatabaseConfig = Field(
    #     default_factory=lambda: DatabaseConfig(
    #         host="localhost",
    #         port=3306,
    #         name="test_db",
    #         user="root",
    #         password="password",  # ⚠️ 生产环境必须通过环境变量覆盖
    #         pool_size=10,
    #         charset="utf8mb4",
    #     ),
    #     description="数据库配置"
    # )

    # ========== Redis配置（可选） ==========
    # 提示: 如果需要Redis，请取消下面的注释并修改默认值
    # redis: RedisConfig = Field(
    #     default_factory=lambda: RedisConfig(
    #         host="localhost",
    #         port=6379,
    #         db=0,
    #         password=None,  # 如果需要密码，请设置
    #     ),
    #     description="Redis配置"
    # )

    # ========== 业务配置 ==========
    business: BusinessConfig = Field(
        default_factory=BusinessConfig,
        description="业务配置"
    )

    # Pydantic v2 配置
    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_nested_delimiter="__",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# ============================================================
# 导出
# ============================================================

__all__ = [
    "{ProjectName}Settings",
    "BusinessConfig",
]
"""

__all__ = ["SETTINGS_ENHANCED_TEMPLATE"]
