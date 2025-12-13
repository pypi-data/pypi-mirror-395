"""
自定义扩展示例

演示如何创建和使用自定义扩展。
"""

from pydantic import Field

from df_test_framework import Bootstrap, FrameworkSettings
from df_test_framework.extensions import hookimpl


class Settings(FrameworkSettings):
    """示例配置"""
    api_base_url: str = Field(default="https://jsonplaceholder.typicode.com")


class RequestLogger:
    """请求日志扩展"""

    def __init__(self, prefix: str = "LOG"):
        self.prefix = prefix
        self.request_count = 0

    @hookimpl
    def before_http_request(self, request):
        """请求前记录日志"""
        self.request_count += 1
        print(f"[{self.prefix}] #{self.request_count} --> {request.method} {request.url}")

    @hookimpl
    def after_http_response(self, response):
        """响应后记录日志"""
        print(f"[{self.prefix}] <-- {response.status_code}")


def example_single_extension():
    """示例1: 单个扩展"""
    print("\n" + "="*60)
    print("示例1: 使用单个扩展")
    print("="*60)

    logger = RequestLogger(prefix="HTTP")

    app = (
        Bootstrap()
        .with_settings(Settings)
        .with_extensions([logger])
        .build()
    )

    runtime = app.run()
    http = runtime.http_client()

    print("\n发送HTTP请求:")
    try:
        response = http.get("/users/1")
        print(f"\n✅ 响应: {response.json()['name']}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")


class PerformanceTracker:
    """性能追踪扩展"""

    def __init__(self):
        import time
        self.time_module = time
        self.start_time = None

    @hookimpl
    def before_http_request(self, request):
        """记录开始时间"""
        self.start_time = self.time_module.time()
        print("⏱️ [性能] 开始计时...")

    @hookimpl
    def after_http_response(self, response):
        """计算耗时"""
        if self.start_time:
            elapsed = (self.time_module.time() - self.start_time) * 1000
            print(f"⏱️ [性能] 耗时: {elapsed:.2f}ms")


class RequestValidator:
    """请求验证扩展"""

    @hookimpl
    def before_http_request(self, request):
        """验证请求"""
        if not request.url.startswith("https://"):
            print("⚠️ [验证] 建议使用HTTPS")

        if not request.headers.get("User-Agent"):
            print("💡 [验证] 建议设置User-Agent")


def example_multiple_extensions():
    """示例2: 多个扩展组合"""
    print("\n" + "="*60)
    print("示例2: 多个扩展组合使用")
    print("="*60)

    extensions = [
        RequestLogger(prefix="REQ"),
        PerformanceTracker(),
        RequestValidator(),
    ]

    app = (
        Bootstrap()
        .with_settings(Settings)
        .with_extensions(extensions)
        .build()
    )

    runtime = app.run()
    http = runtime.http_client()

    print("\n发送HTTP请求:")
    try:
        http.get("/users/1")
        print("\n✅ 请求完成")
    except Exception as e:
        print(f"❌ 请求失败: {e}")


class CacheExtension:
    """缓存扩展示例"""

    def __init__(self):
        self.cache = {}

    @hookimpl
    def before_http_request(self, request):
        """检查缓存"""
        cache_key = f"{request.method}:{request.url}"
        if cache_key in self.cache:
            print("⚡ [缓存] 命中缓存")
        else:
            print("📀 [缓存] 缓存未命中")

    @hookimpl
    def after_http_response(self, response):
        """保存到缓存"""
        # 注意：这只是示例，实际缓存实现需要更完善
        cache_key = f"{response.request.method}:{response.request.url}"
        self.cache[cache_key] = response
        print("💾 [缓存] 已保存")


def example_cache_extension():
    """示例3: 缓存扩展"""
    print("\n" + "="*60)
    print("示例3: 使用缓存扩展")
    print("="*60)

    cache_ext = CacheExtension()

    app = (
        Bootstrap()
        .with_settings(Settings)
        .with_extensions([cache_ext])
        .build()
    )

    runtime = app.run()
    http = runtime.http_client()

    print("\n第一次请求:")
    try:
        http.get("/users/1")
    except:
        pass

    print("\n第二次请求相同URL:")
    try:
        http.get("/users/1")
    except:
        pass


class ErrorHandler:
    """错误处理扩展"""

    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self.retry_count = 0

    @hookimpl
    def after_http_response(self, response):
        """响应后处理错误"""
        if response.status_code >= 500:
            if self.retry_count < self.max_retries:
                self.retry_count += 1
                print(f"⚠️ [错误处理] 服务器错误，准备重试 ({self.retry_count}/{self.max_retries})")
            else:
                print("❌ [错误处理] 已达最大重试次数")
        elif response.status_code >= 400:
            print(f"⚠️ [错误处理] 客户端错误: {response.status_code}")


def example_error_handler():
    """示例4: 错误处理扩展"""
    print("\n" + "="*60)
    print("示例4: 错误处理扩展")
    print("="*60)

    error_handler = ErrorHandler(max_retries=3)

    app = (
        Bootstrap()
        .with_settings(Settings)
        .with_extensions([error_handler])
        .build()
    )

    runtime = app.run()
    http = runtime.http_client()

    print("\n请求不存在的资源:")
    try:
        response = http.get("/users/99999")
        print(f"状态码: {response.status_code}")
    except:
        pass


if __name__ == "__main__":
    print("\n" + "🔌 自定义扩展示例")
    print("="*60)

    # 运行所有示例
    example_single_extension()
    example_multiple_extensions()
    example_cache_extension()
    example_error_handler()

    print("\n" + "="*60)
    print("✅ 所有示例执行完成!")
    print("="*60)
    print("\n💡 提示:")
    print("  - 使用@hookimpl装饰器实现Hook方法")
    print("  - 可以组合多个扩展实现复杂功能")
    print("  - 扩展按注册顺序依次执行")
