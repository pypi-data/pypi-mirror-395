"""
插件管理器协议定义

Core 层只定义接口，不依赖 pluggy 等具体实现。
"""

from typing import Any, Protocol


class IPluginManager(Protocol):
    """插件管理器协议

    Core 层不关心具体用 pluggy 还是其他库实现。
    具体实现在 infrastructure/plugins/manager.py
    """

    def register(self, plugin: Any, name: str | None = None) -> str | None:
        """注册插件

        Args:
            plugin: 插件实例
            name: 插件名称（可选）

        Returns:
            注册成功返回插件名称，失败返回 None
        """
        ...

    def unregister(self, plugin: Any) -> None:
        """注销插件

        Args:
            plugin: 要注销的插件实例
        """
        ...

    @property
    def hook(self) -> Any:
        """获取 Hook 调用代理

        通过此属性调用已注册插件的 hook 方法。

        Example:
            results = plugin_manager.hook.df_providers(settings=settings, logger=logger)
        """
        ...

    def discover_plugins(self, package: str) -> None:
        """自动发现并加载插件

        Args:
            package: 插件包路径
        """
        ...

    def get_plugins(self) -> list[Any]:
        """获取所有已注册插件"""
        ...

    def is_registered(self, plugin: Any) -> bool:
        """检查插件是否已注册"""
        ...
