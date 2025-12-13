"""API项目配置模板"""

SETTINGS_TEMPLATE = """\"\"\"项目配置 - v3.5+ 完全声明式配置

基于df-test-framework v3.5的测试项目配置。

v3.5+核心特性:
- ✅ 完全声明式配置（不需要load_dotenv()和os.getenv()）
- ✅ HTTPSettings嵌套配置（零代码中间件配置）
- ✅ Profile环境配置支持（dev/test/staging/prod）
- ✅ 业务配置分离（清晰的配置分层）
- ✅ 类型安全和自动验证（Pydantic v2）

使用方式:
    >>> from df_test_framework import Bootstrap
    >>> from {project_name}.config import {ProjectName}Settings
    >>>
    >>> # ✅ 不需要load_dotenv()，Pydantic自动加载
    >>> runtime = Bootstrap().with_settings({ProjectName}Settings).build().run()
    >>> http_client = runtime.http_client()
    >>> # 中间件自动生效，无需手动添加
\"\"\"

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from df_test_framework import (
    FrameworkSettings,
    DatabaseConfig,
    RedisConfig,
)
from df_test_framework.infrastructure.config import (
    HTTPSettings,
    SignatureMiddlewareSettings,
    BearerTokenMiddlewareSettings,
)


# ========== 自定义HTTP配置（可选）==========

class {ProjectName}HTTPSettings(HTTPSettings):
    \"\"\"项目HTTP配置 - 继承HTTPSettings并自定义默认值

    环境变量：
        APP_HTTP_BASE_URL - API基础URL
        APP_HTTP_TIMEOUT - 请求超时时间
        APP_HTTP_MAX_RETRIES - 最大重试次数
        APP_SIGNATURE_ENABLED - 是否启用签名中间件
        APP_SIGNATURE_SECRET - 签名密钥
        APP_TOKEN_ENABLED - 是否启用Token中间件
        APP_TOKEN_USERNAME - 登录用户名
        APP_TOKEN_PASSWORD - 登录密码
    \"\"\"

    # ========== HTTP基础配置（自定义默认值） ==========
    base_url: str = Field(
        default="http://localhost:8000/api",
        description="API基础URL"
    )

    # ========== 签名中间件配置（自定义默认值） ==========
    # 提示: 如果需要启用签名中间件，请取消下面的注释并修改默认值
    # signature: SignatureMiddlewareSettings = Field(
    #     default_factory=lambda: SignatureMiddlewareSettings(
    #         enabled=True,  # ✅ 默认启用
    #         priority=10,
    #         algorithm="md5",  # 支持: md5, sha256, hmac-sha256
    #         secret="your-secret-key",  # ⚠️ 生产环境必须通过环境变量覆盖
    #         header_name="X-Sign",
    #         include_paths=["/api/**"],
    #         exclude_paths=["/health", "/metrics", "/actuator/**"],
    #         include_query_params=True,
    #         include_json_body=True,
    #         include_timestamp=True,
    #     )
    # )

    # ========== Token中间件配置（自定义默认值） ==========
    # 提示: 如果需要启用Token中间件，请取消下面的注释并修改默认值
    # token: BearerTokenMiddlewareSettings = Field(
    #     default_factory=lambda: BearerTokenMiddlewareSettings(
    #         enabled=True,  # ✅ 默认启用
    #         priority=20,
    #         token_source="login",  # 支持: login, env, file, static
    #         login_url="/auth/login",
    #         username="admin",  # ⚠️ 生产环境必须通过环境变量覆盖
    #         password="password",  # ⚠️ 生产环境必须通过环境变量覆盖
    #         token_field_path="data.token",  # 支持嵌套路径
    #         header_name="Authorization",
    #         token_prefix="Bearer",
    #         include_paths=["/api/**"],
    #         exclude_paths=["/auth/login", "/auth/register"],
    #         cache_enabled=True,
    #     )
    # )


class BusinessConfig(BaseSettings):
    \"\"\"业务配置

    清晰的配置分层:
    - 独立于框架配置
    - 包含业务特定的测试数据和配置
    \"\"\"

    # === 测试数据配置 ===
    test_user_id: str = Field(default="test_user_001", description="测试用户ID")
    test_role: str = Field(default="admin", description="测试角色")

    # === 业务规则配置 ===
    max_retry_count: int = Field(default=3, description="最大重试次数")
    timeout_seconds: int = Field(default=30, description="超时时间（秒）")

    model_config = SettingsConfigDict(
        env_prefix="BUSINESS_",
        env_file=".env",
        extra="ignore",
    )


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

        # 数据库配置
        APP_DB__HOST - 数据库主机
        APP_DB__PORT - 数据库端口
        APP_DB__NAME - 数据库名称
        APP_DB__USER - 数据库用户
        APP_DB__PASSWORD - 数据库密码

        # Redis配置
        APP_REDIS__HOST - Redis主机
        APP_REDIS__PORT - Redis端口
        APP_REDIS__DB - Redis数据库索引
        APP_REDIS__PASSWORD - Redis密码

        # 业务配置
        BUSINESS_TEST_USER_ID - 测试用户ID
        BUSINESS_TEST_ROLE - 测试角色

    Profile配置:
        dev: 开发环境
        test: 测试环境
        staging: 预发布环境
        prod: 生产环境

    使用方式:
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


__all__ = ["{ProjectName}Settings", "BusinessConfig"]
"""

__all__ = ["SETTINGS_TEMPLATE"]
