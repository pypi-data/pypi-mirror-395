"""
自定义Provider示例

演示如何注册和使用自定义资源提供者。
"""

from typing import Any

from df_test_framework import Bootstrap, FrameworkSettings
from df_test_framework.infrastructure.providers import Provider, ProviderRegistry, SingletonProvider


class EmailService:
    """邮件服务示例"""

    def __init__(self, smtp_host: str, smtp_port: int):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port

    def send_email(self, to: str, subject: str, body: str):
        """发送邮件（模拟）"""
        print(f"📧 发送邮件到 {to}")
        print(f"   主题: {subject}")
        print(f"   SMTP: {self.smtp_host}:{self.smtp_port}")
        return True


class EmailServiceProvider(Provider):
    """邮件服务提供者"""

    def __init__(self, smtp_host: str = "smtp.example.com", smtp_port: int = 25):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self._instance = None

    def provide(self) -> EmailService:
        """提供服务实例（单例模式）"""
        if self._instance is None:
            self._instance = EmailService(self.smtp_host, self.smtp_port)
        return self._instance


def example_custom_provider():
    """示例1: 注册自定义Provider"""
    print("\n" + "="*60)
    print("示例1: 注册和使用自定义Provider")
    print("="*60)

    # 创建Provider注册表
    registry = ProviderRegistry()

    # 注册自定义Provider
    email_provider = EmailServiceProvider(
        smtp_host="smtp.gmail.com",
        smtp_port=587
    )
    registry.register("email", email_provider)

    # 使用Provider
    email_service = registry.get("email")
    email_service.send_email(
        to="user@example.com",
        subject="测试邮件",
        body="这是一封测试邮件"
    )

    # 验证单例模式
    email_service2 = registry.get("email")
    print(f"\n✅ 单例验证: {email_service is email_service2}")


class CacheService:
    """缓存服务示例"""

    def __init__(self):
        self._cache = {}

    def set(self, key: str, value: Any):
        """设置缓存"""
        self._cache[key] = value

    def get(self, key: str) -> Any:
        """获取缓存"""
        return self._cache.get(key)

    def clear(self):
        """清空缓存"""
        self._cache.clear()


def example_singleton_provider():
    """示例2: 使用SingletonProvider"""
    print("\n" + "="*60)
    print("示例2: 使用SingletonProvider")
    print("="*60)

    registry = ProviderRegistry()

    # 使用SingletonProvider（更简单的方式）
    registry.register(
        "cache",
        SingletonProvider(CacheService)
    )

    # 使用缓存服务
    cache1 = registry.get("cache")
    cache1.set("key1", "value1")

    cache2 = registry.get("cache")
    value = cache2.get("key1")

    print(f"缓存值: {value}")
    print(f"✅ 单例验证: {cache1 is cache2}")


class NotificationService:
    """通知服务"""

    def __init__(self, channels: list[str]):
        self.channels = channels

    def notify(self, message: str):
        """发送通知"""
        for channel in self.channels:
            print(f"📢 [{channel}] {message}")


class NotificationProvider(Provider):
    """通知服务Provider"""

    def __init__(self, channels: list[str]):
        self.channels = channels

    def provide(self) -> NotificationService:
        """每次返回新实例（工厂模式）"""
        return NotificationService(self.channels)


def example_factory_provider():
    """示例3: 工厂模式Provider"""
    print("\n" + "="*60)
    print("示例3: 工厂模式Provider（每次新实例）")
    print("="*60)

    registry = ProviderRegistry()

    # 注册工厂Provider
    registry.register(
        "notification",
        NotificationProvider(channels=["email", "sms", "webhook"])
    )

    # 每次获取新实例
    notif1 = registry.get("notification")
    notif1.notify("系统启动")

    notif2 = registry.get("notification")
    notif2.notify("任务完成")

    print(f"\n❌ 非单例验证: {notif1 is notif2}")


class CustomSettings(FrameworkSettings):
    """带自定义Provider的配置"""

    smtp_host: str = "smtp.example.com"
    smtp_port: int = 587


def example_integrate_with_bootstrap():
    """示例4: 集成到Bootstrap"""
    print("\n" + "="*60)
    print("示例4: 集成自定义Provider到Bootstrap")
    print("="*60)

    # 创建自定义Provider
    email_provider = EmailServiceProvider(
        smtp_host="smtp.gmail.com",
        smtp_port=587
    )

    # 通过Bootstrap注册
    app = (
        Bootstrap()
        .with_settings(CustomSettings)
        .with_providers({"email": email_provider})
        .build()
    )

    app.run()

    # 从Runtime获取自定义服务
    # 注意: 需要扩展RuntimeContext来支持自定义服务
    # email_service = runtime.get("email")
    # email_service.send_email(...)

    print("✅ Provider已注册到框架")
    print("💡 实际使用时需要扩展RuntimeContext")


if __name__ == "__main__":
    print("\n" + "🔌 自定义Provider示例")
    print("="*60)

    # 运行所有示例
    example_custom_provider()
    example_singleton_provider()
    example_factory_provider()
    example_integrate_with_bootstrap()

    print("\n" + "="*60)
    print("✅ 所有示例执行完成!")
    print("="*60)
    print("\n💡 提示:")
    print("  - 实现Provider接口创建自定义提供者")
    print("  - 使用SingletonProvider快速创建单例服务")
    print("  - Provider模式实现依赖注入和资源管理")
