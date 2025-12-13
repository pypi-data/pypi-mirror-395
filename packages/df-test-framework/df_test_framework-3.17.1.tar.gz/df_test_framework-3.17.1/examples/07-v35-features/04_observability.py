"""示例04: 可观测性集成

v3.5.0核心特性：完整的可观测性支持

演示内容:
1. ObservabilityLogger统一日志格式
2. HTTP请求/响应自动记录
3. 数据库操作自动记录（如果配置了数据库）
4. 配置开关控制可观测性
5. 敏感信息自动脱敏
6. 日志级别动态调整

运行方式:
    # 默认运行（INFO级别）
    python examples/07-v35-features/04_observability.py

    # DEBUG级别（详细日志）
    APP_LOGGING__LEVEL=DEBUG python examples/07-v35-features/04_observability.py

    # 禁用可观测性
    APP_LOGGING__ENABLE_OBSERVABILITY=false python examples/07-v35-features/04_observability.py
"""

import os
from typing import Self

from pydantic import Field, model_validator

from df_test_framework import (
    Bootstrap,
    FrameworkSettings,
    HTTPConfig,
    LoggingConfig,
)
from df_test_framework.infrastructure.config import SignatureInterceptorConfig

# ============================================================
# 示例1: 基础可观测性配置
# ============================================================

def _create_http_config() -> HTTPConfig:
    """创建HTTP配置"""
    return HTTPConfig(
        base_url="https://jsonplaceholder.typicode.com",
        timeout=30,
        interceptors=[
            SignatureInterceptorConfig(
                type="signature",
                enabled=True,
                priority=10,
                algorithm="md5",
                secret="demo_secret_12345",
                header_name="X-Sign",
                include_paths=["/**"],
            ),
        ]
    )


class ObservabilitySettings(FrameworkSettings):
    """启用可观测性的Settings"""

    # 配置日志
    logging: LoggingConfig = Field(
        default_factory=lambda: LoggingConfig(
            level=os.getenv("APP_LOGGING__LEVEL", "INFO"),
            enable_observability=os.getenv("APP_LOGGING__ENABLE_OBSERVABILITY", "true").lower() == "true",
            enable_http_logging=os.getenv("APP_LOGGING__ENABLE_HTTP_LOGGING", "true").lower() == "true",
            enable_db_logging=os.getenv("APP_LOGGING__ENABLE_DB_LOGGING", "true").lower() == "true",
        )
    )

    @model_validator(mode='after')
    def _setup_interceptors(self) -> Self:
        """设置HTTP拦截器"""
        self.http = _create_http_config()
        return self


def demo_basic_observability():
    """演示基础可观测性"""
    print("\n" + "="*60)
    print("示例1: 基础可观测性")
    print("="*60)

    # 创建运行时（启用可观测性）
    runtime = (
        Bootstrap()
        .with_settings(ObservabilitySettings)
        .build()
        .run()
    )

    print("\n可观测性配置:")
    print(f"  日志级别: {runtime.settings.logging.level}")
    print(f"  可观测性: {runtime.settings.logging.enable_observability}")
    print(f"  HTTP日志: {runtime.settings.logging.enable_http_logging}")
    print(f"  DB日志: {runtime.settings.logging.enable_db_logging}")

    # 发送HTTP请求（会自动记录日志）
    print("\n发送HTTP请求...")
    client = runtime.http_client()
    response = client.get("/posts/1")

    print(f"\n响应状态码: {response.status_code}")
    print(f"响应数据: {response.json()}")

    print("\n💡 观察控制台日志:")
    print("  - 应该看到HTTP请求日志（→ GET /posts/1）")
    print("  - 应该看到HTTP响应日志（← 200 OK）")
    print("  - 应该看到签名拦截器日志")

    print("\n✅ 基础可观测性演示完成")


# ============================================================
# 示例2: 不同日志级别演示
# ============================================================

def demo_log_levels():
    """演示不同日志级别"""
    print("\n" + "="*60)
    print("示例2: 不同日志级别")
    print("="*60)

    log_levels = ["DEBUG", "INFO", "WARNING", "ERROR"]

    for level in log_levels:
        print(f"\n{'='*40}")
        print(f"日志级别: {level}")
        print(f"{'='*40}")

        # 创建不同日志级别的Settings
        class LevelSettings(FrameworkSettings):
            logging: LoggingConfig = Field(
                default_factory=lambda: LoggingConfig(
                    level=level,
                    enable_observability=True,
                    enable_http_logging=True,
                )
            )

            @model_validator(mode='after')
            def _setup_interceptors(self) -> Self:
                self.http = _create_http_config()
                return self

        runtime = (
            Bootstrap()
            .with_settings(LevelSettings)
            .build()
            .run()
        )

        # 发送请求
        client = runtime.http_client()
        response = client.get("/posts/1")
        print(f"请求完成: {response.status_code}")

        if level == "DEBUG":
            print("💡 DEBUG级别: 看到最详细的日志（包括请求参数、响应体等）")
        elif level == "INFO":
            print("💡 INFO级别: 看到请求和响应的基本信息")
        elif level == "WARNING":
            print("💡 WARNING级别: 只看到警告和错误")
        elif level == "ERROR":
            print("💡 ERROR级别: 只看到错误")

    print("\n✅ 日志级别演示完成")


# ============================================================
# 示例3: 启用/禁用可观测性
# ============================================================

def demo_toggle_observability():
    """演示启用/禁用可观测性"""
    print("\n" + "="*60)
    print("示例3: 启用/禁用可观测性")
    print("="*60)

    # 场景1: 启用可观测性
    print("\n场景1: 启用可观测性")

    class EnabledSettings(FrameworkSettings):
        logging: LoggingConfig = Field(
            default_factory=lambda: LoggingConfig(
                level="INFO",
                enable_observability=True,  # 启用
                enable_http_logging=True,
            )
        )

        @model_validator(mode='after')
        def _setup_interceptors(self) -> Self:
            self.http = _create_http_config()
            return self

    runtime_enabled = (
        Bootstrap()
        .with_settings(EnabledSettings)
        .build()
        .run()
    )

    client = runtime_enabled.http_client()
    response = client.get("/posts/1")
    print(f"请求完成: {response.status_code}")
    print("💡 应该看到详细的HTTP日志")

    # 场景2: 禁用可观测性
    print("\n场景2: 禁用可观测性")

    class DisabledSettings(FrameworkSettings):
        logging: LoggingConfig = Field(
            default_factory=lambda: LoggingConfig(
                level="INFO",
                enable_observability=False,  # 禁用
                enable_http_logging=False,
            )
        )

        @model_validator(mode='after')
        def _setup_interceptors(self) -> Self:
            self.http = _create_http_config()
            return self

    runtime_disabled = (
        Bootstrap()
        .with_settings(DisabledSettings)
        .build()
        .run()
    )

    client = runtime_disabled.http_client()
    response = client.get("/posts/1")
    print(f"请求完成: {response.status_code}")
    print("💡 日志大幅减少，只保留关键信息")

    print("\n✅ 可观测性开关演示完成")


# ============================================================
# 示例4: HTTP请求日志详解
# ============================================================

def demo_http_logging():
    """演示HTTP请求日志"""
    print("\n" + "="*60)
    print("示例4: HTTP请求日志详解")
    print("="*60)

    class HTTPLoggingSettings(FrameworkSettings):
        logging: LoggingConfig = Field(
            default_factory=lambda: LoggingConfig(
                level="INFO",
                enable_observability=True,
                enable_http_logging=True,
            )
        )

        @model_validator(mode='after')
        def _setup_interceptors(self) -> Self:
            self.http = _create_http_config()
            return self

    runtime = (
        Bootstrap()
        .with_settings(HTTPLoggingSettings)
        .build()
        .run()
    )

    client = runtime.http_client()

    # 示例1: GET请求
    print("\n1. GET请求:")
    print("   观察日志: → GET /posts/1")
    response = client.get("/posts/1")
    print(f"   响应: {response.status_code}")

    # 示例2: POST请求
    print("\n2. POST请求:")
    print("   观察日志: → POST /posts (带请求体)")
    new_post = {
        "title": "Test Post",
        "body": "This is a test post",
        "userId": 1
    }
    response = client.post("/posts", json=new_post)
    print(f"   响应: {response.status_code}")

    # 示例3: PUT请求
    print("\n3. PUT请求:")
    print("   观察日志: → PUT /posts/1")
    update_data = {"title": "Updated Title"}
    response = client.put("/posts/1", json=update_data)
    print(f"   响应: {response.status_code}")

    # 示例4: DELETE请求
    print("\n4. DELETE请求:")
    print("   观察日志: → DELETE /posts/1")
    response = client.delete("/posts/1")
    print(f"   响应: {response.status_code}")

    print("\n💡 HTTP日志包含:")
    print("  - 请求方法和路径")
    print("  - 请求参数（查询参数、请求体）")
    print("  - 响应状态码")
    print("  - 响应时间（毫秒）")
    print("  - 敏感信息自动脱敏（如token、password）")

    print("\n✅ HTTP日志演示完成")


# ============================================================
# 示例5: 敏感信息脱敏
# ============================================================

def demo_sensitive_data_masking():
    """演示敏感信息脱敏"""
    print("\n" + "="*60)
    print("示例5: 敏感信息脱敏")
    print("="*60)

    class MaskingSettings(FrameworkSettings):
        logging: LoggingConfig = Field(
            default_factory=lambda: LoggingConfig(
                level="DEBUG",  # DEBUG级别才会记录请求参数
                enable_observability=True,
                enable_http_logging=True,
            )
        )

        @model_validator(mode='after')
        def _setup_interceptors(self) -> Self:
            self.http = _create_http_config()
            return self

    runtime = (
        Bootstrap()
        .with_settings(MaskingSettings)
        .build()
        .run()
    )

    client = runtime.http_client()

    # 发送带敏感信息的请求
    print("\n发送带敏感信息的请求...")
    print("请求URL: /posts?api_key=secret123&token=abc456&user=john")

    response = client.get("/posts", params={
        "api_key": "secret123",  # 应该被脱敏
        "token": "abc456",  # 应该被脱敏
        "user": "john",  # 不脱敏
    })

    print(f"响应: {response.status_code}")

    print("\n💡 观察日志中的URL:")
    print("  - api_key=**** (已脱敏)")
    print("  - token=**** (已脱敏)")
    print("  - user=john (未脱敏)")

    print("\n自动脱敏的参数名称:")
    print("  - password")
    print("  - token")
    print("  - api_key")
    print("  - secret")
    print("  - authorization")

    print("\n✅ 敏感信息脱敏演示完成")


# ============================================================
# 示例6: 运行时动态调整日志级别
# ============================================================

def demo_dynamic_log_level():
    """演示运行时动态调整日志级别"""
    print("\n" + "="*60)
    print("示例6: 运行时动态调整日志级别")
    print("="*60)

    # 创建INFO级别的运行时
    runtime = (
        Bootstrap()
        .with_settings(ObservabilitySettings)
        .build()
        .run()
    )

    print("\n原始配置: INFO级别")
    client = runtime.http_client()
    response = client.get("/posts/1")
    print(f"请求完成: {response.status_code}")
    print("💡 看到基本的HTTP日志")

    # 使用with_overrides临时调整为DEBUG级别
    print("\n临时调整为DEBUG级别...")
    debug_ctx = runtime.with_overrides({"logging.level": "DEBUG"})
    debug_client = debug_ctx.http_client()
    response = debug_client.get("/posts/2")
    print(f"请求完成: {response.status_code}")
    print("💡 看到详细的DEBUG日志")

    # 原始运行时仍然是INFO级别
    print("\n原始运行时仍然是INFO级别...")
    response = client.get("/posts/3")
    print(f"请求完成: {response.status_code}")
    print("💡 回到基本的INFO日志")

    print("\n✅ 动态调整日志级别演示完成")


# ============================================================
# 示例7: 实战场景 - 生产vs测试环境
# ============================================================

def demo_production_vs_test():
    """实战场景：生产vs测试环境的可观测性配置"""
    print("\n" + "="*60)
    print("示例7: 生产vs测试环境配置")
    print("="*60)

    # 生产环境配置
    print("\n生产环境配置:")
    print("  目标: 最小化日志开销，只记录错误")

    class ProductionSettings(FrameworkSettings):
        logging: LoggingConfig = Field(
            default_factory=lambda: LoggingConfig(
                level="WARNING",  # 只记录警告和错误
                enable_observability=False,  # 关闭可观测性
                enable_http_logging=False,  # 关闭HTTP日志
                enable_db_logging=False,  # 关闭DB日志
            )
        )

        @model_validator(mode='after')
        def _setup_interceptors(self) -> Self:
            self.http = _create_http_config()
            return self

    runtime_prod = (
        Bootstrap()
        .with_settings(ProductionSettings)
        .build()
        .run()
    )

    client_prod = runtime_prod.http_client()
    response = client_prod.get("/posts/1")
    print(f"  请求完成: {response.status_code}")
    print("  💡 日志极少，性能最优")

    # 测试环境配置
    print("\n测试环境配置:")
    print("  目标: 详细日志，便于调试和问题排查")

    class TestSettings(FrameworkSettings):
        logging: LoggingConfig = Field(
            default_factory=lambda: LoggingConfig(
                level="DEBUG",  # 详细日志
                enable_observability=True,  # 启用可观测性
                enable_http_logging=True,  # 记录所有HTTP请求
                enable_db_logging=True,  # 记录所有DB操作
            )
        )

        @model_validator(mode='after')
        def _setup_interceptors(self) -> Self:
            self.http = _create_http_config()
            return self

    runtime_test = (
        Bootstrap()
        .with_settings(TestSettings)
        .build()
        .run()
    )

    client_test = runtime_test.http_client()
    response = client_test.get("/posts/1")
    print(f"  请求完成: {response.status_code}")
    print("  💡 详细日志，便于调试")

    print("\n推荐配置:")
    print("  生产环境: WARNING + 关闭可观测性")
    print("  测试环境: DEBUG + 启用可观测性")
    print("  开发环境: DEBUG + 启用可观测性")

    print("\n✅ 环境配置对比演示完成")


# ============================================================
# 主函数
# ============================================================

def main():
    """运行所有示例"""
    print("\n" + "🚀 v3.5可观测性集成示例".center(60, "="))

    try:
        # 示例1: 基础可观测性
        demo_basic_observability()

        # 示例2: 不同日志级别
        demo_log_levels()

        # 示例3: 启用/禁用可观测性
        demo_toggle_observability()

        # 示例4: HTTP请求日志
        demo_http_logging()

        # 示例5: 敏感信息脱敏
        demo_sensitive_data_masking()

        # 示例6: 运行时动态调整日志级别
        demo_dynamic_log_level()

        # 示例7: 生产vs测试环境
        demo_production_vs_test()

        print("\n" + "✅ 所有示例运行完成！".center(60, "="))

        print("\n💡 关键要点:")
        print("  1. 可观测性通过LoggingConfig配置")
        print("  2. 支持动态调整日志级别（通过with_overrides）")
        print("  3. 敏感信息自动脱敏（token、password等）")
        print("  4. HTTP/DB操作自动记录到日志")
        print("  5. 生产环境建议关闭可观测性（性能优先）")

        print("\n📊 日志级别选择:")
        print("  - DEBUG: 开发调试，看到所有细节")
        print("  - INFO: 正常运行，记录关键操作")
        print("  - WARNING: 生产环境，只记录警告和错误")
        print("  - ERROR: 生产环境，只记录错误")

        print("\n🎯 使用建议:")
        print("  开发环境:")
        print("    - level=DEBUG")
        print("    - enable_observability=True")
        print("  测试环境:")
        print("    - level=INFO")
        print("    - enable_observability=True")
        print("  生产环境:")
        print("    - level=WARNING")
        print("    - enable_observability=False")

        print("\n📚 下一步:")
        print("  - 查看实际项目中的日志配置")
        print("  - 了解如何集成Allure报告")
        print("  - 学习日志聚合和分析")

    except Exception as e:
        print(f"\n❌ 示例运行失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
