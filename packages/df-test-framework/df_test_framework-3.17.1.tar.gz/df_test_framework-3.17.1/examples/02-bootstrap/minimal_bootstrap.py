"""
最小化Bootstrap启动示例

演示最简单的框架初始化方式。
"""

from df_test_framework import Bootstrap


def example_minimal():
    """示例1: 最小化启动"""
    print("\n" + "="*60)
    print("示例1: 最小化启动（使用默认配置）")
    print("="*60)

    # 最简单的启动方式
    app = Bootstrap().build()
    runtime = app.run()

    print("✅ 框架启动成功")
    print(f"框架版本: {runtime.settings.__class__.__name__}")


def example_with_default_settings():
    """示例2: 使用默认配置启动"""
    print("\n" + "="*60)
    print("示例2: 显式指定默认配置")
    print("="*60)

    from df_test_framework import FrameworkSettings

    # 显式指定配置类
    app = Bootstrap().with_settings(FrameworkSettings).build()
    runtime = app.run()

    print("✅ 框架启动成功")
    print(f"HTTP配置: {runtime.settings.http}")
    print(f"日志配置: {runtime.settings.logging}")


def example_chain_methods():
    """示例3: 链式调用"""
    print("\n" + "="*60)
    print("示例3: 链式调用构建器")
    print("="*60)

    from df_test_framework import FrameworkSettings

    # 链式调用多个配置方法
    runtime = (
        Bootstrap()
        .with_settings(FrameworkSettings)
        .build()
        .run()
    )

    print("✅ 一行代码完成启动")
    print(f"Runtime类型: {type(runtime).__name__}")


def example_access_services():
    """示例4: 访问核心服务"""
    print("\n" + "="*60)
    print("示例4: 访问核心服务")
    print("="*60)

    runtime = Bootstrap().build().run()

    # 访问各种服务
    print("可用服务:")

    # HTTP客户端
    http_client = runtime.http_client()
    print(f"  - HTTP客户端: {type(http_client).__name__}")

    # 注意：Database和Redis需要配置才能使用
    # database = runtime.database()
    # redis_client = runtime.redis_client()

    print("✅ 服务访问成功")


if __name__ == "__main__":
    print("\n" + "🚀 最小化Bootstrap启动示例")
    print("="*60)

    # 运行所有示例
    example_minimal()
    example_with_default_settings()
    example_chain_methods()
    example_access_services()

    print("\n" + "="*60)
    print("✅ 所有示例执行完成!")
    print("="*60)
    print("\n💡 提示:")
    print("  - Bootstrap使用Builder模式，支持链式调用")
    print("  - 可以通过with_settings()自定义配置")
    print("  - Runtime提供所有核心服务的访问")
