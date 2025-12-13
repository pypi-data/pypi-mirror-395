"""
自定义配置示例

演示如何自定义框架配置以适配项目需求。
"""

from decimal import Decimal

from pydantic import Field

from df_test_framework import Bootstrap, FrameworkSettings


class MyProjectSettings(FrameworkSettings):
    """项目自定义配置"""

    # 自定义字段
    project_name: str = Field(
        default="我的测试项目",
        description="项目名称"
    )

    api_version: str = Field(
        default="v1",
        description="API版本"
    )

    max_retry_times: int = Field(
        default=3,
        description="最大重试次数"
    )

    default_timeout: int = Field(
        default=30,
        description="默认超时时间（秒）"
    )


def example_custom_settings():
    """示例1: 使用自定义配置"""
    print("\n" + "="*60)
    print("示例1: 使用自定义配置")
    print("="*60)

    app = Bootstrap().with_settings(MyProjectSettings).build()
    runtime = app.run()

    # 访问自定义配置
    settings = runtime.settings

    print(f"项目名称: {settings.project_name}")
    print(f"API版本: {settings.api_version}")
    print(f"最大重试次数: {settings.max_retry_times}")
    print(f"默认超时: {settings.default_timeout}秒")


class MultiEnvSettings(FrameworkSettings):
    """多环境配置"""

    # 环境标识
    env: str = Field(
        default="dev",
        description="环境: dev/test/prod"
    )

    # 根据环境不同的配置
    api_base_url: str = Field(
        default="http://localhost:8000",
        description="API基础URL"
    )

    debug_mode: bool = Field(
        default=True,
        description="调试模式"
    )


def example_environment_config():
    """示例2: 环境配置"""
    print("\n" + "="*60)
    print("示例2: 多环境配置")
    print("="*60)

    # 开发环境
    print("\n开发环境配置:")
    MultiEnvSettings(
        env="dev",
        api_base_url="http://localhost:8000",
        debug_mode=True
    )
    app = Bootstrap().with_settings(MultiEnvSettings).build()
    runtime = app.run()

    print(f"  环境: {runtime.settings.env}")
    print(f"  API URL: {runtime.settings.api_base_url}")
    print(f"  调试模式: {runtime.settings.debug_mode}")

    # 生产环境
    print("\n生产环境配置:")
    prod_settings = MultiEnvSettings(
        env="prod",
        api_base_url="https://api.production.com",
        debug_mode=False
    )

    print(f"  环境: {prod_settings.env}")
    print(f"  API URL: {prod_settings.api_base_url}")
    print(f"  调试模式: {prod_settings.debug_mode}")


class NestedSettings(FrameworkSettings):
    """嵌套配置"""

    class BusinessConfig:
        """业务配置"""
        default_amount: Decimal = Decimal("100.00")
        template_id: str = "TMPL_001"
        enable_notification: bool = True

    business: BusinessConfig = Field(
        default_factory=BusinessConfig,
        description="业务配置"
    )


def example_nested_config():
    """示例3: 嵌套配置"""
    print("\n" + "="*60)
    print("示例3: 嵌套配置结构")
    print("="*60)

    app = Bootstrap().with_settings(NestedSettings).build()
    runtime = app.run()

    # 访问嵌套配置
    business = runtime.settings.business

    print(f"默认金额: {business.default_amount}")
    print(f"模板ID: {business.template_id}")
    print(f"启用通知: {business.enable_notification}")


class ValidatedSettings(FrameworkSettings):
    """带验证的配置"""

    port: int = Field(
        default=8080,
        ge=1024,
        le=65535,
        description="端口号（1024-65535）"
    )

    email: str = Field(
        default="admin@example.com",
        pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$",
        description="邮箱地址"
    )


def example_validated_config():
    """示例4: 配置验证"""
    print("\n" + "="*60)
    print("示例4: 配置验证")
    print("="*60)

    # 有效配置
    try:
        valid_settings = ValidatedSettings(
            port=8080,
            email="admin@example.com"
        )
        print(f"✅ 有效配置: 端口={valid_settings.port}, 邮箱={valid_settings.email}")
    except Exception as e:
        print(f"❌ 配置验证失败: {e}")

    # 无效配置
    try:
        ValidatedSettings(
            port=100,  # 小于1024
            email="invalid-email"  # 无效格式
        )
    except Exception:
        print("❌ 预期的验证失败: 端口或邮箱格式错误")


if __name__ == "__main__":
    print("\n" + "⚙️ 自定义配置示例")
    print("="*60)

    # 运行所有示例
    example_custom_settings()
    example_environment_config()
    example_nested_config()
    example_validated_config()

    print("\n" + "="*60)
    print("✅ 所有示例执行完成!")
    print("="*60)
    print("\n💡 提示:")
    print("  - 继承FrameworkSettings创建自定义配置")
    print("  - 使用Pydantic的Field定义配置字段")
    print("  - 支持环境变量、嵌套配置、数据验证")
