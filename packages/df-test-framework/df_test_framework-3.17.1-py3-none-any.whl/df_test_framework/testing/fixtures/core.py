"""
Primary pytest plugin for df-test-framework v2.

Usage:
    pytest_plugins = ["df_test_framework.fixtures.core"]
"""

from __future__ import annotations

import importlib
import os
from collections.abc import Iterable
from typing import cast

import pytest

from df_test_framework.bootstrap import Bootstrap, RuntimeContext
from df_test_framework.infrastructure.config import FrameworkSettings

_runtime_context: RuntimeContext | None = None


def _resolve_settings_class(path: str) -> type[FrameworkSettings]:
    module_name, _, class_name = path.rpartition(".")
    if not module_name:
        raise RuntimeError(f"Invalid settings class path: {path!r}")
    module = importlib.import_module(module_name)
    cls = getattr(module, class_name)
    if not issubclass(cls, FrameworkSettings):
        raise TypeError(f"{path!r} is not a subclass of FrameworkSettings")
    return cast(type[FrameworkSettings], cls)


def _get_settings_path(config: pytest.Config) -> str:
    ini_value = config.getini("df_settings_class") if "df_settings_class" in config.inicfg else None
    cli_value = config.getoption("--df-settings-class", default=None)
    env_value = os.getenv("DF_SETTINGS_CLASS")
    return (
        cli_value
        or ini_value
        or env_value
        or "df_test_framework.infrastructure.config.schema.FrameworkSettings"
    )


def _get_plugin_paths(config: pytest.Config) -> Iterable[str]:
    collected = []
    cli_value = config.getoption("df_plugin") or []
    ini_value = config.getini("df_plugins") if "df_plugins" in config.inicfg else ""
    env_value = os.getenv("DF_PLUGINS", "")

    def parse(value):
        if not value:
            return []
        if isinstance(value, (list, tuple)):
            return [item.strip() for item in value if item and item.strip()]
        return [item.strip() for item in str(value).split(",") if item.strip()]

    for source in (cli_value, ini_value, env_value):
        collected.extend(parse(source))

    # Preserve order, remove duplicates
    seen = set()
    for plugin in collected:
        if plugin not in seen:
            seen.add(plugin)
            yield plugin


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--df-settings-class",
        action="store",
        default=None,
        help="Dotted path to the FrameworkSettings subclass used for bootstrap",
    )
    parser.addini(
        "df_settings_class",
        "Dotted path to the FrameworkSettings subclass used for bootstrap",
        type="string",
        default="",
    )
    parser.addoption(
        "--df-plugin",
        action="append",
        default=[],
        help="Import path of a df-test-framework plugin (repeatable)",
    )
    parser.addini(
        "df_plugins",
        "Comma separated list of df-test-framework plugins to load",
        type="string",
        default="",
    )
    # v3.11.1: 统一的测试数据保留控制（UoW 数据 + API 数据）
    parser.addoption(
        "--keep-test-data",
        action="store_true",
        default=False,
        help="保留所有测试数据（调试用）。包括 UoW 数据（不回滚）和 API 创建的数据（不清理）。",
    )


def pytest_configure(config: pytest.Config) -> None:
    global _runtime_context

    settings_path = _get_settings_path(config)
    settings_cls = _resolve_settings_class(settings_path)

    bootstrap = Bootstrap().with_settings(settings_cls)
    for plugin_path in _get_plugin_paths(config):
        bootstrap.with_plugin(plugin_path)

    app = bootstrap.build()
    _runtime_context = app.run(force_reload=True)

    config._df_runtime_context = _runtime_context  # type: ignore[attr-defined]

    # v3.11.1: 注册测试数据保留标记（统一控制 UoW + API 数据）
    config.addinivalue_line(
        "markers", "keep_data: 保留此测试的所有数据（调试用）。UoW 数据不回滚，API 数据不清理。"
    )


def pytest_unconfigure(config: pytest.Config) -> None:
    runtime: RuntimeContext | None = getattr(config, "_df_runtime_context", None)
    if runtime:
        runtime.close()


@pytest.fixture(scope="session")
def runtime() -> RuntimeContext:
    if _runtime_context is None:
        raise RuntimeError(
            "Runtime context has not been initialised. Ensure pytest_configure executed."
        )
    return _runtime_context


@pytest.fixture(scope="session")
def http_client(runtime: RuntimeContext):
    return runtime.http_client()


@pytest.fixture(scope="session")
def database(runtime: RuntimeContext):
    return runtime.database()


@pytest.fixture(scope="session")
def redis_client(runtime: RuntimeContext):
    return runtime.redis()


@pytest.fixture(scope="session")
def local_file_client(runtime: RuntimeContext):
    """本地文件存储客户端 fixture

    提供本地文件系统存储能力

    Scope: session（跨测试共享）

    Example:
        >>> def test_upload_file(local_file_client):
        ...     # 上传文件
        ...     result = local_file_client.upload("test.txt", b"Hello")
        ...     assert result["size"] == 5
        ...
        ...     # 下载文件
        ...     content = local_file_client.download("test.txt")
        ...     assert content == b"Hello"
        ...
        ...     # 清理
        ...     local_file_client.delete("test.txt")

    Returns:
        LocalFileClient: 本地文件客户端实例
    """
    return runtime.local_file()


@pytest.fixture(scope="session")
def s3_client(runtime: RuntimeContext):
    """S3 对象存储客户端 fixture

    提供 S3 兼容对象存储能力（AWS S3、MinIO）

    Scope: session（跨测试共享）

    Configuration:
        需要在配置中启用 S3 存储:

        ```python
        from df_test_framework import FrameworkSettings
        from df_test_framework.capabilities.storages import S3Config

        class MySettings(FrameworkSettings):
            storage: StorageConfig = StorageConfig(
                s3=S3Config(
                    endpoint_url="http://localhost:9000",
                    access_key="minioadmin",
                    secret_key="minioadmin",
                    bucket_name="test-bucket"
                )
            )
        ```

    Example:
        >>> def test_s3_upload(s3_client):
        ...     # 上传文件
        ...     result = s3_client.upload("test.txt", b"Hello World")
        ...     assert result["size"] == 11
        ...
        ...     # 下载文件
        ...     content = s3_client.download("test.txt")
        ...     assert content == b"Hello World"
        ...
        ...     # 生成预签名URL
        ...     url = s3_client.generate_presigned_url("test.txt", expiration=300)
        ...
        ...     # 清理
        ...     s3_client.delete("test.txt")

    Returns:
        S3Client: S3 客户端实例

    Raises:
        ConfigurationError: 如果 S3 未配置
    """
    return runtime.s3()


@pytest.fixture(scope="session")
def oss_client(runtime: RuntimeContext):
    """阿里云 OSS 对象存储客户端 fixture

    提供阿里云 OSS 对象存储能力（基于 oss2 官方 SDK）

    Scope: session（跨测试共享）

    Configuration:
        需要在配置中启用 OSS 存储:

        ```python
        from df_test_framework import FrameworkSettings
        from df_test_framework.capabilities.storages import OSSConfig

        class MySettings(FrameworkSettings):
            storage: StorageConfig = StorageConfig(
                oss=OSSConfig(
                    access_key_id="LTAI5t...",
                    access_key_secret="xxx...",
                    bucket_name="my-bucket",
                    endpoint="oss-cn-hangzhou.aliyuncs.com"
                )
            )
        ```

    Example:
        >>> def test_oss_upload(oss_client):
        ...     # 上传文件
        ...     result = oss_client.upload("test.txt", b"Hello OSS")
        ...     assert result["etag"]
        ...
        ...     # 下载文件
        ...     content = oss_client.download("test.txt")
        ...     assert content == b"Hello OSS"
        ...
        ...     # 生成预签名URL
        ...     url = oss_client.generate_presigned_url("test.txt", expiration=300)
        ...
        ...     # 清理
        ...     oss_client.delete("test.txt")

    Returns:
        OSSClient: OSS 客户端实例

    Raises:
        ConfigurationError: 如果 OSS 未配置
    """
    return runtime.oss()


@pytest.fixture
def http_mock(http_client):
    """HTTP Mock fixture（v3.5新增）

    提供HTTP Mock功能，用于测试隔离

    Features:
    - 完全Mock HTTP请求，无需真实服务
    - 支持请求匹配和响应定制
    - 自动清理（测试结束后重置）

    Scope: function（每个测试独立）

    Example:
        >>> def test_get_users(http_mock, http_client):
        ...     # Mock GET /api/users
        ...     http_mock.get("/api/users", json={"users": []})
        ...
        ...     # 发送请求（自动返回Mock响应）
        ...     response = http_client.get("/api/users")
        ...     assert response.json() == {"users": []}
        ...
        ...     # 验证请求被调用
        ...     http_mock.assert_called("/api/users", "GET", times=1)

    Advanced:
        >>> def test_post_user(http_mock, http_client):
        ...     # Mock多个请求
        ...     http_mock.post("/api/users", status_code=201, json={"id": 1})
        ...     http_mock.get("/api/users/1", json={"id": 1, "name": "Alice"})
        ...
        ...     # 测试代码...

    Returns:
        HttpMocker实例
    """
    from ..mocking import HttpMocker

    mocker = HttpMocker(http_client)
    yield mocker
    # 测试结束后自动清理
    mocker.reset()


@pytest.fixture
def time_mock():
    """时间Mock fixture（v3.5新增）

    提供时间Mock功能，用于测试时间敏感逻辑

    Features:
    - 冻结时间到指定时刻
    - 时间旅行（前进/后退）
    - 自动清理（测试结束后恢复真实时间）

    Scope: function（每个测试独立）

    Example:
        >>> from datetime import datetime
        >>> def test_expiration(time_mock):
        ...     # 冻结时间到2024-01-01 12:00:00
        ...     time_mock.freeze("2024-01-01 12:00:00")
        ...
        ...     # 验证时间
        ...     now = datetime.now()
        ...     assert now.year == 2024
        ...     assert now.month == 1
        ...     assert now.hour == 12
        ...
        ...     # 时间前进1小时
        ...     time_mock.move_to("2024-01-01 13:00:00")
        ...     now = datetime.now()
        ...     assert now.hour == 13

    Advanced:
        >>> from datetime import timedelta
        >>> def test_time_calculation(time_mock):
        ...     # 冻结时间
        ...     time_mock.freeze("2024-01-01 00:00:00")
        ...
        ...     # 时间增量前进
        ...     time_mock.tick(seconds=3600)  # 前进1小时
        ...     time_mock.tick(delta=timedelta(days=1))  # 前进1天

    Returns:
        TimeMocker实例
    """
    from ..mocking import TimeMocker

    mocker = TimeMocker()
    yield mocker
    # 测试结束后自动恢复真实时间
    mocker.stop()


@pytest.fixture
def uow(database, request, runtime: RuntimeContext):
    """Unit of Work fixture（v3.13.0：配置驱动架构）

    提供 UnitOfWork 实例，管理事务边界和 Repository 生命周期。
    测试结束后自动回滚（默认），可配置保留数据。

    v3.13.0 重要更新:
    - 支持 repository_package 配置化（无需继承 UnitOfWork）
    - 项目只需在 .env 配置 TEST__REPOSITORY_PACKAGE 即可启用自动发现
    - 无需覆盖此 fixture

    Features:
    - 统一的事务边界管理
    - 多个 Repository 共享同一 Session
    - 默认测试结束自动回滚
    - 灵活的数据清理控制
    - Repository 自动发现（通过配置）
    - 符合 DDD 最佳实践

    Scope: function（每个测试独立）

    Example - 基本用法:
        >>> def test_create_card(uow):
        ...     card = uow.cards.find_by_no("CARD001")
        ...     uow.orders.create({...})
        ...     # ✅ 测试结束后自动回滚

    Example - 启用 Repository 自动发现（v3.13.0）:
        在 .env 文件中配置:
        TEST__REPOSITORY_PACKAGE=my_project.repositories

        测试代码无需修改:
        >>> def test_create_card(uow):
        ...     uow.cards.create({...})  # ✅ 自动发现 CardRepository

    Example - 执行原生 SQL:
        >>> from sqlalchemy import text
        >>> def test_query(uow):
        ...     result = uow.execute(
        ...         "SELECT * FROM users WHERE id = :id",
        ...         {"id": 1}
        ...     )
        ...     user = result.mappings().first()

    Example - 保留数据用于调试:
        方式1 - 显式提交:
        >>> def test_demo(uow):
        ...     uow.cards.create({...})
        ...     uow.commit()  # 显式提交，数据保留

        方式2 - 命令行参数:
        $ pytest tests/ --keep-test-data

        方式3 - 测试标记:
        >>> @pytest.mark.keep_data
        >>> def test_demo(uow):
        ...     pass  # 此测试自动提交

    Control Options (v3.13.0 统一配置):
        1. 显式调用 uow.commit()
        2. 标记: @pytest.mark.keep_data
        3. 命令行: pytest --keep-test-data
        4. Settings 配置: .env 文件中 TEST__KEEP_TEST_DATA=1

    Configuration (v3.13.0):
        在 .env 文件中配置:
        TEST__REPOSITORY_PACKAGE=my_project.repositories  # 启用自动发现
        TEST__KEEP_TEST_DATA=0                            # 默认清理数据

    Returns:
        UnitOfWork: UnitOfWork 实例

    Logs:
        - 默认: "✅ UnitOfWork: 数据已回滚（自动清理）"
        - 保留: "⚠️ UnitOfWork: 数据已提交并保留到数据库"
    """
    from loguru import logger

    from df_test_framework.capabilities.databases.uow import UnitOfWork

    from .cleanup import should_keep_test_data

    # v3.12.1: 使用统一的 should_keep_test_data() 检查配置
    # 优先级：测试标记 > 命令行参数 > Settings 配置（.env / 环境变量）
    auto_commit = should_keep_test_data(request)
    if auto_commit:
        logger.info("检测到保留数据配置，测试数据将被提交")

    # v3.13.0: 从配置读取 repository_package
    repository_package = None
    if runtime.settings.test:
        repository_package = runtime.settings.test.repository_package
        if repository_package:
            logger.debug(f"UoW 配置: repository_package={repository_package}")

    # v3.18.0: 获取测试专用的 EventBus
    from df_test_framework.infrastructure.events import get_event_bus

    test_event_bus = get_event_bus()

    # 创建 UnitOfWork（配置驱动 + 事件驱动）
    unit_of_work = UnitOfWork(
        database.session_factory,
        repository_package=repository_package,
        event_bus=test_event_bus,  # v3.18.0: 传入 EventBus 以发布事务事件
    )

    with unit_of_work:
        yield unit_of_work

        # 如果配置了自动提交且未手动提交
        if auto_commit and not unit_of_work._committed:
            unit_of_work.commit()
