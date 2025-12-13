"""
扩展系统示例

演示如何加载和使用扩展插件。
"""

from df_test_framework import Bootstrap, FrameworkSettings
from df_test_framework.extensions import hookimpl


class MyCustomExtension:
    """自定义扩展示例"""

    @hookimpl
    def before_http_request(self, request):
        """HTTP请求前钩子"""
        print(f"  🔵 [扩展] 准备发送请求: {request.method} {request.url}")

    @hookimpl
    def after_http_response(self, response):
        """HTTP响应后钩子"""
        print(f"  🟢 [扩展] 收到响应: {response.status_code}")


def example_custom_extension():
    """示例1: 加载自定义扩展"""
    print("\n" + "="*60)
    print("示例1: 加载自定义扩展")
    print("="*60)

    # 创建扩展实例
    my_extension = MyCustomExtension()

    # 通过Bootstrap加载扩展
    app = (
        Bootstrap()
        .with_settings(FrameworkSettings)
        .with_extensions([my_extension])
        .build()
    )

    runtime = app.run()

    print("✅ 自定义扩展已加载")

    # 使用HTTP客户端（会触发扩展的钩子）
    http = runtime.http_client()

    print("\n发送HTTP请求:")
    try:
        response = http.get("https://jsonplaceholder.typicode.com/users/1")
        print(f"\n✅ 请求成功，用户: {response.json()['name']}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")


class LoggingExtension:
    """日志扩展示例"""

    def __init__(self, prefix: str = "LOG"):
        self.prefix = prefix

    @hookimpl
    def before_http_request(self, request):
        """记录请求"""
        print(f"  [{self.prefix}] --> {request.method} {request.url}")

    @hookimpl
    def after_http_response(self, response):
        """记录响应"""
        print(f"  [{self.prefix}] <-- {response.status_code}")


class MetricsExtension:
    """性能指标扩展"""

    def __init__(self):
        self.request_count = 0

    @hookimpl
    def before_http_request(self, request):
        """计数请求"""
        self.request_count += 1
        print(f"  📊 [指标] 总请求数: {self.request_count}")


def example_multiple_extensions():
    """示例2: 加载多个扩展"""
    print("\n" + "="*60)
    print("示例2: 加载多个扩展")
    print("="*60)

    # 创建多个扩展
    logging_ext = LoggingExtension(prefix="HTTP")
    metrics_ext = MetricsExtension()

    # 加载多个扩展
    app = (
        Bootstrap()
        .with_settings(FrameworkSettings)
        .with_extensions([logging_ext, metrics_ext])
        .build()
    )

    runtime = app.run()

    print("✅ 已加载 2 个扩展")

    # 发送多个请求
    http = runtime.http_client()

    print("\n发送第一个请求:")
    try:
        http.get("https://jsonplaceholder.typicode.com/users/1")
    except:
        pass

    print("\n发送第二个请求:")
    try:
        http.get("https://jsonplaceholder.typicode.com/posts/1")
    except:
        pass


class RetryExtension:
    """重试扩展示例"""

    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries

    @hookimpl
    def after_http_response(self, response):
        """失败时重试"""
        if response.status_code >= 500:
            print("  ⚠️ [重试] 服务器错误，需要重试")


def example_builtin_extensions():
    """示例3: 使用内置扩展"""
    print("\n" + "="*60)
    print("示例3: 使用内置扩展")
    print("="*60)

    from df_test_framework.extensions.builtin.monitoring import APIPerformanceTracker

    # 使用内置的性能追踪扩展
    perf_tracker = APIPerformanceTracker()

    app = (
        Bootstrap()
        .with_settings(FrameworkSettings)
        .with_extensions([perf_tracker])
        .build()
    )

    runtime = app.run()

    print("✅ 已加载内置性能追踪扩展")

    # 发送请求
    http = runtime.http_client()
    try:
        http.get("https://jsonplaceholder.typicode.com/users/1")
        print("\n✅ 请求完成")
    except Exception as e:
        print(f"❌ 请求失败: {e}")


class ValidationExtension:
    """验证扩展示例"""

    @hookimpl
    def before_http_request(self, request):
        """请求前验证"""
        if not request.url.startswith("https://"):
            print("  ⚠️ [验证] 建议使用HTTPS")


def example_extension_chain():
    """示例4: 扩展链式执行"""
    print("\n" + "="*60)
    print("示例4: 扩展链式执行顺序")
    print("="*60)

    # 创建扩展链
    extensions = [
        ValidationExtension(),
        LoggingExtension(prefix="REQ"),
        MetricsExtension(),
    ]

    app = (
        Bootstrap()
        .with_settings(FrameworkSettings)
        .with_extensions(extensions)
        .build()
    )

    runtime = app.run()

    print(f"✅ 已加载 {len(extensions)} 个扩展（按顺序执行）")

    # 发送请求
    http = runtime.http_client()
    try:
        http.get("https://jsonplaceholder.typicode.com/users/1")
    except:
        pass


if __name__ == "__main__":
    print("\n" + "🔌 扩展系统示例")
    print("="*60)

    # 运行所有示例
    example_custom_extension()
    example_multiple_extensions()
    example_builtin_extensions()
    example_extension_chain()

    print("\n" + "="*60)
    print("✅ 所有示例执行完成!")
    print("="*60)
    print("\n💡 提示:")
    print("  - 使用@hookimpl装饰器实现Hook方法")
    print("  - 可以加载多个扩展，按顺序执行")
    print("  - 框架提供内置扩展如性能追踪、慢查询监控")
