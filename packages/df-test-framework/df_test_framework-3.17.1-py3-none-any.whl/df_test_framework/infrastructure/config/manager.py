"""
Settings registry responsible for loading and caching configuration instances.
"""

from __future__ import annotations

import os
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import TypeVar

from .pipeline import ConfigPipeline
from .schema import FrameworkSettings
from .sources import (
    ArgSource,
    ConfigSource,
    DotenvSource,
    EnvVarSource,
    merge_dicts,
)

TSettings = TypeVar("TSettings", bound=FrameworkSettings)

SettingsNamespace = str


class SettingsAlreadyConfiguredError(RuntimeError):
    pass


class SettingsNotConfiguredError(RuntimeError):
    pass


@dataclass
class _RegisteredSettings:
    cls: type[FrameworkSettings]
    pipeline: ConfigPipeline
    cache_enabled: bool = True


_REGISTRY: dict[SettingsNamespace, _RegisteredSettings] = {}
_CACHE: dict[SettingsNamespace, FrameworkSettings] = {}


def _default_dotenv_files(env_name: str) -> list[Path]:
    return [
        Path(".env"),
        Path(f".env.{env_name}"),
        Path(".env.local"),
    ]


def _detect_env_name() -> str:
    return (os.getenv("ENV") or os.getenv("APP_ENV") or "test").lower()


def _build_default_pipeline(settings_cls: type[FrameworkSettings]) -> ConfigPipeline:
    """构建默认配置管道（自动检测环境）"""
    env_name = _detect_env_name()
    return _build_default_pipeline_with_profile(settings_cls, env_name)


def _build_default_pipeline_with_profile(
    settings_cls: type[FrameworkSettings], env_name: str
) -> ConfigPipeline:
    """构建默认配置管道（指定环境profile）

    v3.5 Phase 3: 支持通过profile参数明确指定环境

    Args:
        settings_cls: Settings类
        env_name: 环境名称 (dev/test/staging/prod)

    Returns:
        配置管道

    加载顺序（优先级从低到高）:
    1. .env (基础配置)
    2. .env.{profile} (环境特定配置) ✅ v3.5 Phase 3
    3. .env.local (本地覆盖)
    4. 环境变量
    5. 命令行参数
    """
    pipeline = ConfigPipeline()
    pipeline.add(
        DotenvSource(files=_default_dotenv_files(env_name)),
    ).add(EnvVarSource()).add(ArgSource())
    return pipeline


def configure_settings[TSettings: FrameworkSettings](
    settings_cls: type[TSettings],
    *,
    namespace: SettingsNamespace = "default",
    profile: str | None = None,  # ✅ v3.5 Phase 3: 支持profile参数
    sources: Iterable[ConfigSource] | None = None,
    cache_enabled: bool = True,
) -> None:
    """
    Register a settings class for later retrieval.

    Args:
        settings_cls: subclass of FrameworkSettings
        namespace: optional identifier (allowing multiple configs)
        profile: environment profile (dev/test/staging/prod), overrides ENV variable
        sources: optional iterable of ConfigSource overriding the defaults
        cache_enabled: whether to cache the instantiated settings object

    v3.5 Phase 3: profile参数优先级高于ENV环境变量，用于明确指定运行环境

    Example:
        >>> configure_settings(MySettings, profile="dev")  # 强制使用dev配置
    """
    if namespace in _REGISTRY:
        raise SettingsAlreadyConfiguredError(f"Settings already configured for {namespace!r}")

    if sources is None:
        # ✅ v3.5 Phase 3: 使用profile参数或自动检测
        env_name = profile if profile else _detect_env_name()
        pipeline = _build_default_pipeline_with_profile(settings_cls, env_name)
    else:
        pipeline = ConfigPipeline(list(sources))

    _REGISTRY[namespace] = _RegisteredSettings(
        cls=settings_cls,
        pipeline=pipeline,
        cache_enabled=cache_enabled,
    )


def _load(namespace: SettingsNamespace, *, overrides: dict | None = None) -> FrameworkSettings:
    if namespace not in _REGISTRY:
        raise SettingsNotConfiguredError(
            f"No settings configured for namespace {namespace!r}. Call configure_settings() first."
        )

    registered = _REGISTRY[namespace]
    data = registered.pipeline.load()
    if overrides:
        data = merge_dicts(data, overrides)
    return registered.cls(**data)


def get_settings(
    namespace: SettingsNamespace = "default",
    *,
    force_reload: bool = False,
) -> FrameworkSettings:
    """
    Retrieve configuration instance for the namespace (default: "default").

    Instances are cached unless cache_enabled=False during registration.
    """
    if not force_reload and namespace in _CACHE:
        return _CACHE[namespace]

    settings = _load(namespace)
    registered = _REGISTRY[namespace]

    if registered.cache_enabled:
        _CACHE[namespace] = settings

    return settings


def create_settings[TSettings: FrameworkSettings](
    settings_cls: type[TSettings],
    *,
    sources: Iterable[ConfigSource] | None = None,
    overrides: dict | None = None,
) -> TSettings:
    """
    Create a settings instance without touching the registry.
    """
    pipeline = ConfigPipeline(list(sources) if sources else [])
    if not pipeline.sources:
        pipeline = _build_default_pipeline(settings_cls)
    data = pipeline.load()
    if overrides:
        data = merge_dicts(data, overrides)
    return settings_cls(**data)


def clear_settings(namespace: SettingsNamespace = "default") -> None:
    """
    Clear cached settings and registry for a namespace. Mainly used in tests.
    """
    _CACHE.pop(namespace, None)
    _REGISTRY.pop(namespace, None)
