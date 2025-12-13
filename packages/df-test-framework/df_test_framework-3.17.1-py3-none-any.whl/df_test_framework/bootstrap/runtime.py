"""
运行时上下文 (Layer 4: Bootstrap)

职责:
- RuntimeContext: 保持运行时单例（settings, logger, providers）
- RuntimeBuilder: 构建 RuntimeContext 的辅助类

v3.16.0 架构重构:
- 从 infrastructure/runtime/ 迁移到 bootstrap/
- 作为 Layer 4 可以合法依赖所有层
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from loguru._logger import Logger

from df_test_framework.infrastructure.config.schema import FrameworkSettings
from df_test_framework.infrastructure.plugins import PluggyPluginManager as ExtensionManager

from .providers import ProviderRegistry, default_providers


@dataclass(frozen=True)
class RuntimeContext:
    settings: FrameworkSettings
    logger: Logger
    providers: ProviderRegistry
    extensions: ExtensionManager | None = None

    def get(self, key: str):
        return self.providers.get(key, self)

    def http_client(self):
        return self.get("http_client")

    def database(self):
        return self.get("database")

    def redis(self):
        return self.get("redis")

    def local_file(self):
        """获取本地文件存储客户端"""
        return self.get("local_file")

    def s3(self):
        """获取 S3 对象存储客户端"""
        return self.get("s3")

    def oss(self):
        """获取阿里云 OSS 对象存储客户端"""
        return self.get("oss")

    def close(self) -> None:
        self.providers.shutdown()

    def with_overrides(self, overrides: dict[str, Any]) -> RuntimeContext:
        """创建带有配置覆盖的新RuntimeContext

        v3.5 Phase 3: 运行时动态覆盖配置，用于测试场景

        Args:
            overrides: 要覆盖的配置字典（支持嵌套，如 {"http.timeout": 10}）

        Returns:
            新的RuntimeContext实例，配置已被覆盖

        Example:
            >>> # 在测试中临时修改超时配置
            >>> test_ctx = ctx.with_overrides({"http": {"timeout": 1}})
            >>> client = test_ctx.http_client()  # 使用1秒超时

            >>> # 支持点号路径
            >>> test_ctx = ctx.with_overrides({"http.base_url": "http://mock.local"})

        Note:
            - 返回新实例，不修改原RuntimeContext
            - logger共享（无状态），extensions共享（配置不变）
            - providers必须重新创建，避免SingletonProvider共享导致配置不隔离
            - 适用于测试中临时修改配置，不影响全局
        """
        # 创建settings的副本并应用覆盖
        new_settings = self._apply_overrides_to_settings(self.settings, overrides)

        # 创建新的ProviderRegistry，而非共享
        # 原因: SingletonProvider会缓存实例，导致不同配置下共享同一HttpClient/Database等
        # 解决方案: 使用default_providers()创建新的Provider实例
        new_providers = default_providers()

        # 创建新的RuntimeContext，logger和extensions可共享（无状态）
        return RuntimeContext(
            settings=new_settings,
            logger=self.logger,
            providers=new_providers,
            extensions=self.extensions,
        )

    def _apply_overrides_to_settings(
        self, settings: FrameworkSettings, overrides: dict[str, Any]
    ) -> FrameworkSettings:
        """应用覆盖到settings

        Args:
            settings: 原始settings
            overrides: 覆盖字典

        Returns:
            新的settings实例
        """
        # 将settings转为字典
        settings_dict = settings.model_dump()

        # 应用覆盖（支持嵌套和点号路径）
        for key, value in overrides.items():
            if "." in key:
                # 支持点号路径: "http.timeout" -> {"http": {"timeout": ...}}
                parts = key.split(".")
                current = settings_dict
                for part in parts[:-1]:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
                current[parts[-1]] = value
            else:
                # 直接覆盖
                if (
                    isinstance(value, dict)
                    and key in settings_dict
                    and isinstance(settings_dict[key], dict)
                ):
                    # 嵌套字典：深度合并
                    settings_dict[key] = {**settings_dict[key], **value}
                else:
                    settings_dict[key] = value

        # 重新创建settings实例
        return settings.__class__(**settings_dict)


class RuntimeBuilder:
    """
    Helper responsible for constructing RuntimeContext.
    """

    def __init__(self):
        self._settings: FrameworkSettings | None = None
        self._logger: Logger | None = None
        self._providers_factory: Callable[[], ProviderRegistry] | None = None
        self._extensions: ExtensionManager | None = None

    def with_settings(self, settings: FrameworkSettings) -> RuntimeBuilder:
        self._settings = settings
        return self

    def with_logger(self, logger: Logger) -> RuntimeBuilder:
        self._logger = logger
        return self

    def with_providers(self, factory: Callable[[], ProviderRegistry]) -> RuntimeBuilder:
        self._providers_factory = factory
        return self

    def with_extensions(self, extensions: ExtensionManager) -> RuntimeBuilder:
        self._extensions = extensions
        return self

    def build(self) -> RuntimeContext:
        if not self._settings:
            raise ValueError("Settings must be provided to RuntimeBuilder")
        if not self._logger:
            raise ValueError("Logger must be provided to RuntimeBuilder")

        providers = (
            self._providers_factory()
            if self._providers_factory is not None
            else default_providers()
        )

        return RuntimeContext(
            settings=self._settings,
            logger=self._logger,
            providers=providers,
            extensions=self._extensions,
        )


__all__ = [
    "RuntimeContext",
    "RuntimeBuilder",
]
