"""
基于 Pluggy 的插件管理器实现
"""

import importlib
import logging
import pkgutil
from typing import Any

import pluggy

from df_test_framework.core.protocols.plugin import IPluginManager
from df_test_framework.infrastructure.plugins.hooks import HookSpecs


class PluggyPluginManager(IPluginManager):
    """基于 Pluggy 的插件管理器实现

    实现 core/protocols/plugin.py 中定义的 IPluginManager 接口。

    示例:
        pm = PluggyPluginManager()
        pm.register(MyPlugin())
        pm.discover_plugins("df_test_framework.plugins.builtin")

        # 调用 Hook
        providers = pm.hook.df_providers(settings=settings, logger=logger)
    """

    def __init__(
        self,
        project_name: str = "df_test_framework",
        logger: logging.Logger | None = None,
    ):
        """初始化插件管理器

        Args:
            project_name: 项目名称（用于 Pluggy 命名空间）
            logger: 日志对象
        """
        self._pm = pluggy.PluginManager(project_name)
        self._pm.add_hookspecs(HookSpecs)  # 直接使用单一数据源
        self._logger = logger or logging.getLogger(__name__)
        self._registered_plugins: list[Any] = []

    def register(self, plugin: Any, name: str | None = None) -> str | None:
        """注册插件

        Args:
            plugin: 插件实例
            name: 插件名称（可选）

        Returns:
            注册成功返回插件名称，失败返回 None
        """
        try:
            result = self._pm.register(plugin, name=name)
            if result:
                self._registered_plugins.append(plugin)
                self._logger.debug(f"Registered plugin: {result}")
            return result
        except Exception as e:
            self._logger.warning(f"Failed to register plugin: {e}")
            return None

    def unregister(self, plugin: Any) -> None:
        """注销插件

        Args:
            plugin: 要注销的插件实例
        """
        try:
            self._pm.unregister(plugin)
            if plugin in self._registered_plugins:
                self._registered_plugins.remove(plugin)
            self._logger.debug(f"Unregistered plugin: {plugin}")
        except Exception as e:
            self._logger.warning(f"Failed to unregister plugin: {e}")

    @property
    def hook(self) -> Any:
        """获取 Hook 调用代理

        Returns:
            Pluggy Hook 代理对象
        """
        return self._pm.hook

    def discover_plugins(self, package: str) -> None:
        """自动发现并加载插件

        扫描指定包下的所有模块，加载包含 Hook 实现的插件。

        Args:
            package: 插件包路径（如 "df_test_framework.plugins.builtin"）
        """
        try:
            pkg = importlib.import_module(package)
        except ImportError as e:
            self._logger.warning(f"Failed to import plugin package {package}: {e}")
            return

        if not hasattr(pkg, "__path__"):
            self._logger.warning(f"Package {package} has no __path__")
            return

        for _, module_name, is_pkg in pkgutil.walk_packages(pkg.__path__, prefix=f"{package}."):
            try:
                module = importlib.import_module(module_name)

                # 查找模块中的插件类
                for attr_name in dir(module):
                    if attr_name.startswith("_"):
                        continue

                    attr = getattr(module, attr_name)

                    # 检查是否是类且名称以 Plugin 结尾
                    if (
                        isinstance(attr, type)
                        and attr_name.endswith("Plugin")
                        and hasattr(attr, "__module__")
                        and attr.__module__ == module_name
                    ):
                        # 检查是否有 hookimpl 装饰的方法
                        if self._has_hookimpl(attr):
                            instance = attr()
                            self.register(instance, name=attr_name)
                            self._logger.info(f"Discovered plugin: {attr_name}")

            except Exception as e:
                self._logger.warning(f"Failed to load module {module_name}: {e}")

    def _has_hookimpl(self, cls: type) -> bool:
        """检查类是否有 hookimpl 装饰的方法

        Args:
            cls: 要检查的类

        Returns:
            是否有 hookimpl 方法
        """
        for attr_name in dir(cls):
            if attr_name.startswith("_"):
                continue
            try:
                attr = getattr(cls, attr_name)
                if callable(attr) and hasattr(attr, "df_test_framework_impl"):
                    return True
            except Exception:
                pass
        return False

    def get_plugins(self) -> list[Any]:
        """获取所有已注册插件

        Returns:
            插件列表
        """
        return self._registered_plugins.copy()

    def is_registered(self, plugin: Any) -> bool:
        """检查插件是否已注册

        Args:
            plugin: 插件实例

        Returns:
            是否已注册
        """
        return self._pm.is_registered(plugin)

    def get_plugin(self, name: str) -> Any | None:
        """根据名称获取插件

        Args:
            name: 插件名称

        Returns:
            插件实例，未找到返回 None
        """
        return self._pm.get_plugin(name)

    def list_name_plugin(self) -> list[tuple[str, Any]]:
        """列出所有插件名称和实例

        Returns:
            (名称, 插件) 元组列表
        """
        return self._pm.list_name_plugin()
