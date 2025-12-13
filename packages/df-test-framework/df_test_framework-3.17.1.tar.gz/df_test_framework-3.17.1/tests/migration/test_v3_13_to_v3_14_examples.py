"""验证 v3.13 到 v3.14 迁移指南中的代码示例

测试迁移指南中的所有代码示例，确保：
1. 新的导入路径正确且可用
2. 旧的导入路径仍然工作（兼容性）
3. API 行为符合预期
4. 示例代码可以正常运行

对应文档: docs/migration/v3.13-to-v3.14.md
"""

import pytest


class TestImportPathMigration:
    """测试导入路径迁移示例"""

    def test_http_client_import_new_path(self):
        """验证 HTTP 客户端新导入路径（1.1 节）"""
        # v3.14.0 新路径
        from df_test_framework.capabilities.clients.http import HttpClient

        assert HttpClient is not None
        assert hasattr(HttpClient, "__init__")

    def test_http_client_import_top_level(self):
        """验证 HTTP 客户端顶层导入（推荐方式）"""
        from df_test_framework import HttpClient

        assert HttpClient is not None

    def test_middleware_import_new_path(self):
        """验证中间件新导入路径（1.2 节）"""
        from df_test_framework.capabilities.clients.http.middleware import (
            BearerTokenMiddleware,
            SignatureMiddleware,
        )

        assert BearerTokenMiddleware is not None
        assert SignatureMiddleware is not None

    def test_database_import_new_path(self):
        """验证数据库新导入路径（1.3 节）"""
        from df_test_framework.capabilities.databases import (
            BaseRepository,
            Database,
            UnitOfWork,
        )

        assert Database is not None
        assert UnitOfWork is not None
        assert BaseRepository is not None

    def test_messenger_import_new_path(self):
        """验证消息队列新导入路径（1.4 节）"""
        pytest.importorskip("confluent_kafka", reason="需要 confluent-kafka")
        # v3.14.0 使用统一的 KafkaClient 替代 Producer/Consumer
        from df_test_framework.capabilities.messengers.queue.kafka import (
            KafkaClient,
            KafkaConfig,
        )

        assert KafkaClient is not None
        assert KafkaConfig is not None

    def test_storage_import_new_path(self):
        """验证存储新导入路径（1.5 节）"""
        from df_test_framework.capabilities.storages.object.s3 import S3Client

        assert S3Client is not None

    def test_infrastructure_import_new_path(self):
        """验证基础设施新导入路径（1.6 节）

        v3.16.0: RuntimeContext 已迁移到 bootstrap/ (Layer 4)
        """
        from df_test_framework.bootstrap import RuntimeContext
        from df_test_framework.infrastructure.config import FrameworkSettings
        from df_test_framework.infrastructure.telemetry import Telemetry

        assert FrameworkSettings is not None
        assert RuntimeContext is not None
        assert Telemetry is not None

    def test_plugin_system_import_new_path(self):
        """验证插件系统新导入路径（1.7 节）"""
        from df_test_framework.core.protocols.plugin import IPluginManager
        from df_test_framework.infrastructure.plugins import PluggyPluginManager
        from df_test_framework.infrastructure.plugins.hooks import HookSpecs, hookimpl

        assert IPluginManager is not None
        assert PluggyPluginManager is not None
        assert HookSpecs is not None
        assert hookimpl is not None

    def test_exceptions_import_new_path(self):
        """验证异常新导入路径（1.8 节）"""
        from df_test_framework.core import FrameworkError, HttpError

        assert FrameworkError is not None
        assert HttpError is not None
        assert issubclass(HttpError, FrameworkError)


class TestBackwardCompatibility:
    """测试向后兼容性 - 旧路径应该仍然工作但有警告"""

    def test_common_import_removed(self):
        """验证 common 模块已被移除（v3.16.0）

        v3.16.0: common/ 已完全删除，不再提供向后兼容层
        """
        with pytest.raises(ModuleNotFoundError, match="No module named 'df_test_framework.common'"):
            from df_test_framework.common import FrameworkError  # noqa: F401

    def test_extensions_import_removed(self):
        """验证 extensions 模块已被移除（v3.17.1）

        v3.16.0: extensions/ 标记为废弃
        v3.17.1: extensions/ 已完全删除，不再提供向后兼容层

        用户应使用 infrastructure.plugins.PluggyPluginManager 替代
        """
        with pytest.raises(
            ModuleNotFoundError, match="No module named 'df_test_framework.extensions'"
        ):
            from df_test_framework.extensions import ExtensionManager  # noqa: F401


class TestMiddlewareMigration:
    """测试中间件迁移示例（2.2 节）"""

    @pytest.mark.asyncio
    async def test_sync_middleware_example(self):
        """验证 SyncMiddleware 继承方式（方式一）"""
        from df_test_framework.core.middleware import SyncMiddleware

        class AddHeaderMiddleware(SyncMiddleware):
            def __init__(self, key: str, value: str):
                super().__init__()
                self.key = key
                self.value = value

            def before(self, request):
                # 简单的请求修改示例
                if not hasattr(request, "headers"):
                    request.headers = {}
                request.headers[self.key] = self.value
                return request

        # 创建中间件实例
        middleware = AddHeaderMiddleware("X-Custom", "test-value")
        assert middleware is not None

        # 验证它是有效的中间件
        from df_test_framework.core.middleware.base import BaseMiddleware

        assert isinstance(middleware, BaseMiddleware)

    @pytest.mark.asyncio
    async def test_function_middleware_example(self):
        """验证函数式中间件（方式二）"""
        from df_test_framework.core.middleware import middleware

        @middleware(priority=100)
        async def add_header(request, call_next):
            # 修改请求
            if not hasattr(request, "headers"):
                request.headers = {}
            request.headers["X-Custom"] = "value"

            # 调用下一个中间件
            response = await call_next(request)
            return response

        # 验证装饰器返回的是中间件类
        assert add_header is not None
        assert hasattr(add_header, "__call__")

    @pytest.mark.asyncio
    async def test_timing_middleware_example(self):
        """验证状态共享的中间件示例（洋葱模型优势）"""
        import time

        from df_test_framework.core.middleware import BaseMiddleware, MiddlewareChain

        class TimingMiddleware(BaseMiddleware):
            """测量请求耗时的中间件"""

            async def __call__(self, request, call_next):
                # before: 记录开始时间（在同一作用域）
                start = time.monotonic()

                # 执行请求
                response = await call_next(request)

                # after: 计算耗时（直接访问 start 变量）
                duration = time.monotonic() - start

                # 可以添加到响应中
                if not hasattr(response, "timing"):
                    response.timing = {}
                response.timing["duration"] = duration

                return response

        # 创建简单的处理器和响应对象
        class MockRequest:
            pass

        class MockResponse:
            pass

        async def handler(req):
            await pytest.importorskip("asyncio").sleep(0.01)  # 模拟处理延迟
            return MockResponse()

        # 创建中间件链并测试
        chain = MiddlewareChain(handler)
        chain.use(TimingMiddleware())

        request = MockRequest()
        response = await chain.execute(request)

        # 验证计时功能
        assert hasattr(response, "timing")
        assert response.timing["duration"] > 0


class TestAsyncFirstMigration:
    """测试异步优先迁移（3.1 节）"""

    def test_async_http_client_import(self):
        """验证 HTTP 客户端可以正确导入和创建"""
        from df_test_framework import HttpClient

        # v3.14.0 HttpClient 默认异步
        client = HttpClient(base_url="https://httpbin.org")

        # 验证客户端创建成功
        assert client is not None
        assert hasattr(client, "get")
        assert hasattr(client, "post")
        assert hasattr(client, "put")
        assert hasattr(client, "delete")


class TestTelemetryMigration:
    """测试可观测性融合迁移（4 节）"""

    def test_telemetry_unified_import(self):
        """验证统一的 Telemetry 导入"""
        from df_test_framework.infrastructure.telemetry import Telemetry

        assert Telemetry is not None

        # 验证 Telemetry 类可以实例化
        # 注意：实际的 API 可能需要配置参数
        # 这里仅验证导入成功
        assert hasattr(Telemetry, "__init__")


class TestEventSystemMigration:
    """测试事件系统迁移"""

    @pytest.mark.asyncio
    async def test_event_bus_basic_usage(self):
        """验证事件总线基本用法"""
        from df_test_framework.core.events import HttpRequestEndEvent
        from df_test_framework.infrastructure.events import EventBus

        bus = EventBus()
        received_events = []

        @bus.on(HttpRequestEndEvent)
        async def handler(event: HttpRequestEndEvent):
            received_events.append(event)

        # 发布事件
        event = HttpRequestEndEvent(method="GET", url="/api/test", status_code=200, duration=0.5)
        await bus.publish(event)

        # 验证事件被接收
        assert len(received_events) == 1
        assert received_events[0].method == "GET"


class TestContextPropagationMigration:
    """测试上下文传播迁移"""

    @pytest.mark.asyncio
    async def test_execution_context_basic_usage(self):
        """验证执行上下文基本用法"""
        from df_test_framework.core.context import (
            ExecutionContext,
            get_current_context,
            with_context_async,
        )

        # 创建上下文
        ctx = (
            ExecutionContext.create_root()
            .with_user("test_user")
            .with_tenant("test_tenant")
            .with_baggage("env", "test")
        )

        assert ctx.user_id == "test_user"
        assert ctx.tenant_id == "test_tenant"
        assert ctx.baggage.get("env") == "test"

        # 测试上下文传播
        async with with_context_async(ctx):
            current = get_current_context()
            assert current.user_id == "test_user"
            assert current.tenant_id == "test_tenant"


class TestPluginSystemMigration:
    """测试插件系统迁移"""

    def test_plugin_manager_creation(self):
        """验证插件管理器创建"""
        from df_test_framework.infrastructure.plugins import PluggyPluginManager

        manager = PluggyPluginManager()
        assert manager is not None

    def test_hookimpl_decorator(self):
        """验证 hookimpl 装饰器"""
        from df_test_framework.infrastructure.plugins.hooks import hookimpl

        class TestPlugin:
            @hookimpl
            def pytest_configure(self, config):
                pass

        plugin = TestPlugin()
        assert hasattr(plugin.pytest_configure, "__self__")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
