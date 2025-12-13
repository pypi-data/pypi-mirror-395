"""
Bootstrap 引导程序 (Layer 4: Bootstrap)

职责:
- Bootstrap: 链式配置 settings、logging、providers、plugins
- BootstrapApp: 执行引导流程，返回 RuntimeContext

v3.16.0 架构重构:
- 从 infrastructure/bootstrap/ 迁移到 bootstrap/
- 作为 Layer 4 可以合法依赖所有层
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from typing import Any, TypeVar

from df_test_framework.infrastructure.config import (
    ConfigSource,
    FrameworkSettings,
    SettingsAlreadyConfiguredError,
    SettingsNamespace,
    clear_settings,
    configure_settings,
    get_settings,
)
from df_test_framework.infrastructure.logging import LoggerStrategy, LoguruStructuredStrategy
from df_test_framework.infrastructure.plugins import PluggyPluginManager

from .providers import ProviderRegistry, default_providers
from .runtime import RuntimeBuilder, RuntimeContext

TSettings = TypeVar("TSettings", bound=FrameworkSettings)


ProviderFactory = Callable[[], ProviderRegistry]


@dataclass
class Bootstrap:
    settings_cls: type[FrameworkSettings] = FrameworkSettings
    namespace: SettingsNamespace = "default"
    profile: str | None = None  # 支持profile
    sources: Iterable[ConfigSource] | None = None
    cache_enabled: bool = True
    logger_strategy: LoggerStrategy = field(default_factory=LoguruStructuredStrategy)
    provider_factory: ProviderFactory | None = None
    plugins: list[str | object] = field(default_factory=list)

    def with_settings(
        self,
        settings_cls: type[TSettings],
        *,
        namespace: SettingsNamespace = "default",
        profile: str | None = None,
        sources: Iterable[ConfigSource] | None = None,
        cache_enabled: bool = True,
    ) -> Bootstrap:
        """配置Settings

        Args:
            settings_cls: Settings类
            namespace: 命名空间
            profile: 环境配置（dev/test/staging/prod），优先级高于ENV环境变量
            sources: 配置源
            cache_enabled: 是否缓存

        Example:
            >>> Bootstrap().with_settings(
            ...     CustomSettings,
            ...     profile="dev",  # 明确指定使用dev环境配置
            ... )
        """
        self.settings_cls = settings_cls
        self.namespace = namespace
        self.profile = profile
        self.sources = sources
        self.cache_enabled = cache_enabled
        return self

    def with_logging(self, strategy: LoggerStrategy) -> Bootstrap:
        self.logger_strategy = strategy
        return self

    def with_provider_factory(self, factory: ProviderFactory) -> Bootstrap:
        self.provider_factory = factory
        return self

    def with_plugin(self, plugin: str | object) -> Bootstrap:
        self.plugins.append(plugin)
        return self

    def build(self) -> BootstrapApp:
        return BootstrapApp(
            settings_cls=self.settings_cls,
            namespace=self.namespace,
            profile=self.profile,
            sources=self.sources,
            cache_enabled=self.cache_enabled,
            logger_strategy=self.logger_strategy,
            provider_factory=self.provider_factory,
            plugins=list(self.plugins),
        )


@dataclass
class BootstrapApp:
    settings_cls: type[FrameworkSettings]
    namespace: SettingsNamespace
    profile: str | None
    sources: Iterable[ConfigSource] | None
    cache_enabled: bool
    logger_strategy: LoggerStrategy
    provider_factory: ProviderFactory | None
    plugins: list[str | object]

    def run(self, *, force_reload: bool = False) -> RuntimeContext:
        """
        Execute the bootstrap pipeline and return a RuntimeContext.

        支持profile参数，优先级高于ENV环境变量
        """
        if force_reload:
            clear_settings(self.namespace)

        extensions = PluggyPluginManager()
        for plugin in self.plugins:
            if isinstance(plugin, str):
                # 字符串插件: 导入模块并注册
                import importlib

                module = importlib.import_module(plugin)
                extensions.register(module, name=plugin)
            else:
                # 对象插件: 直接注册
                extensions.register(plugin)
        pm = extensions

        extra_sources: list[Any] = []
        for contributed in pm.hook.df_config_sources(settings_cls=self.settings_cls):
            extra_sources.extend(contributed or [])

        combined_sources: list[Any] = []
        if self.sources:
            combined_sources.extend(self.sources)
        combined_sources.extend(extra_sources)

        try:
            configure_settings(
                self.settings_cls,
                namespace=self.namespace,
                profile=self.profile,
                sources=combined_sources or None,
                cache_enabled=self.cache_enabled,
            )
        except SettingsAlreadyConfiguredError:
            if force_reload:
                clear_settings(self.namespace)
                configure_settings(
                    self.settings_cls,
                    namespace=self.namespace,
                    profile=self.profile,
                    sources=combined_sources or None,
                    cache_enabled=self.cache_enabled,
                )

        settings = get_settings(self.namespace, force_reload=force_reload)
        logging_config = settings.logging
        if logging_config is None:
            from df_test_framework.infrastructure.config.schema import LoggingConfig

            logging_config = LoggingConfig()
        logger = self.logger_strategy.configure(logging_config)

        builder = RuntimeBuilder().with_settings(settings).with_logger(logger)
        providers_factory = self.provider_factory or default_providers
        providers = providers_factory()

        for contributed in pm.hook.df_providers(settings=settings, logger=logger):
            if contributed:
                providers.extend(contributed)

        builder.with_providers(lambda: providers)
        builder.with_extensions(extensions)
        runtime = builder.build()

        pm.hook.df_post_bootstrap(runtime=runtime)
        return runtime


__all__ = [
    "Bootstrap",
    "BootstrapApp",
]
