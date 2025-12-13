"""
框架 Hook 规范 - 单一数据源

所有 Hook 定义只在此文件中定义，避免重复维护。
使用 pluggy 的 @hookspec 装饰器。

设计原则：
- 此文件是 HookSpecs 的唯一定义点
- 避免在 core 层重复定义
- 具体实现在 plugins/ 目录
"""

from typing import Any

import pluggy

# Pluggy 标记器
hookspec = pluggy.HookspecMarker("df_test_framework")
hookimpl = pluggy.HookimplMarker("df_test_framework")


class HookSpecs:
    """框架 Hook 规范（单一数据源）

    所有 Hook 都在此类中定义，PluggyPluginManager 直接使用此类。

    Hook 命名规范：
    - 前缀 df_: 框架命名空间
    - 动词 + 名词: 描述 Hook 行为

    实现示例：
        class MyPlugin:
            @hookimpl
            def df_providers(self, settings, logger):
                return {"my_service": MyService()}
    """

    # =========================================================================
    # 配置相关 Hooks
    # =========================================================================

    @hookspec
    def df_config_sources(self, settings_cls: type) -> list[Any]:
        """返回额外的配置源

        在配置加载阶段调用，允许插件提供额外的配置源。

        Args:
            settings_cls: 配置类

        Returns:
            配置源列表
        """

    @hookspec
    def df_config_loaded(self, settings: Any) -> None:
        """配置加载完成后钩子

        在所有配置加载完成后调用。

        Args:
            settings: 加载完成的配置对象
        """

    # =========================================================================
    # Provider 相关 Hooks
    # =========================================================================

    @hookspec
    def df_providers(self, settings: Any, logger: Any) -> dict[str, Any]:
        """返回自定义 Provider 映射

        在依赖注入阶段调用，允许插件注册自定义服务。

        Args:
            settings: 配置对象
            logger: 日志对象

        Returns:
            Provider 名称到实例的映射
        """

    # =========================================================================
    # Bootstrap 相关 Hooks
    # =========================================================================

    @hookspec
    def df_pre_bootstrap(self, bootstrap: Any) -> None:
        """Bootstrap 开始前钩子

        Args:
            bootstrap: Bootstrap 实例
        """

    @hookspec
    def df_post_bootstrap(self, runtime: Any) -> None:
        """Bootstrap 完成后钩子

        在框架完全初始化后调用。

        Args:
            runtime: 运行时上下文
        """

    # =========================================================================
    # 中间件相关 Hooks
    # =========================================================================

    @hookspec
    def df_http_middlewares(self, settings: Any) -> list[Any]:
        """返回 HTTP 中间件列表

        Args:
            settings: 配置对象

        Returns:
            HTTP 中间件列表
        """

    @hookspec
    def df_db_middlewares(self, settings: Any) -> list[Any]:
        """返回数据库中间件列表

        Args:
            settings: 配置对象

        Returns:
            数据库中间件列表
        """

    @hookspec
    def df_mq_middlewares(self, settings: Any) -> list[Any]:
        """返回消息队列中间件列表

        Args:
            settings: 配置对象

        Returns:
            MQ 中间件列表
        """

    # =========================================================================
    # 事件相关 Hooks
    # =========================================================================

    @hookspec
    def df_event_handlers(self, event_bus: Any) -> list[Any]:
        """注册事件处理器

        在事件总线初始化后调用，允许插件注册事件处理器。

        Args:
            event_bus: 事件总线实例

        Returns:
            注册的事件处理器列表
        """

    # =========================================================================
    # 可观测性相关 Hooks
    # =========================================================================

    @hookspec
    def df_telemetry_exporters(self, settings: Any) -> list[Any]:
        """返回遥测导出器列表

        Args:
            settings: 配置对象

        Returns:
            导出器列表
        """

    # =========================================================================
    # 测试相关 Hooks
    # =========================================================================

    @hookspec
    def df_test_setup(self, request: Any, runtime: Any) -> None:
        """测试开始前钩子

        在每个测试开始前调用。

        Args:
            request: pytest request 对象
            runtime: 运行时上下文
        """

    @hookspec
    def df_test_teardown(self, request: Any, runtime: Any, outcome: Any) -> None:
        """测试结束后钩子

        在每个测试结束后调用。

        Args:
            request: pytest request 对象
            runtime: 运行时上下文
            outcome: 测试结果
        """

    @hookspec
    def df_session_start(self, session: Any) -> None:
        """测试会话开始钩子

        Args:
            session: pytest session 对象
        """

    @hookspec
    def df_session_finish(self, session: Any, exitstatus: int) -> None:
        """测试会话结束钩子

        Args:
            session: pytest session 对象
            exitstatus: 退出状态码
        """
