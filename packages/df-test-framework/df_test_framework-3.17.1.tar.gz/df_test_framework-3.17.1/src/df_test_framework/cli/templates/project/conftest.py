"""API项目pytest配置模板"""

CONFTEST_TEMPLATE = """\"\"\"Pytest全局配置和Fixtures

v3.14.0 企业级平台架构:
- ✅ 升级到 df-test-framework v3.14.0
- ✅ 启用框架的自动Bootstrap
- 🆕 配置化中间件（零代码签名和Token认证）- 洋葱模型
- 🆕 EventBus 事件总线（发布/订阅解耦）
- 🆕 Telemetry 可观测性融合（Tracing + Metrics + Logging）
- ✅ Profile环境配置支持（dev/test/staging/prod）
- ✅ 运行时配置覆盖（with_overrides）
- ✅ Unit of Work 模式（repository_package 自动发现）
- ✅ API 自动发现（@api_class 装饰器）
- ✅ 集成 Allure 报告（自动记录 HTTP/DB 事件）
- ✅ Debug Tools（http_debug, db_debug, debug_mode）
- ✅ 测试数据清理（--keep-test-data, @pytest.mark.keep_data）

框架集成：
- pytest_plugins：启用df-test-framework的核心fixtures和配置管理
\"\"\"

import pytest
from df_test_framework.testing.reporting.allure import AllureHelper

# ========== 启用框架的pytest插件 ==========
# 框架会自动通过 pytest.ini 中的 df_settings_class 初始化 RuntimeContext
pytest_plugins = ["df_test_framework.testing.fixtures.core"]

# ========== 导入项目业务专属 Fixtures ==========
# 注意: 框架通过 pytest_plugins 自动提供核心 fixtures，项目只需导入业务专属 fixtures

# from {project_name}.fixtures import (
#     # 项目业务 API fixtures（如果有）
#     # api_client,
#
#     # Unit of Work（如果实现了）
#     # uow,
#
#     # API测试数据清理（v3.11.1）
#     # cleanup_api_data,
#
#     # 其他项目自定义 fixtures
#     # cleanup_files,
#     # cleanup_redis_keys,
# )


# ========== 提供 settings fixture 供测试使用 ==========

@pytest.fixture(scope="session")
def settings(runtime):
    \"\"\"配置对象（session级别）

    v3.5: 从RuntimeContext获取settings，避免重复创建

    Args:
        runtime: RuntimeContext对象（框架自动提供）

    Returns:
        {ProjectName}Settings配置对象（来自RuntimeContext的单例）
    \"\"\"
    # ✅ 使用框架管理的单例settings
    return runtime.settings


# ========== Pytest配置钩子 ==========

def pytest_configure(config: pytest.Config) -> None:
    \"\"\"Pytest配置钩子 - 在测试运行前执行

    注册项目自定义标记。

    注意:
    - 框架在其 pytest_configure 钩子中自动初始化 RuntimeContext
    - 框架已自动注册 keep_data marker，项目无需重复注册
    - 本钩子只需注册项目业务相关的标记
    \"\"\"
    # 注册项目自定义 pytest 标记
    config.addinivalue_line("markers", "smoke: 冒烟测试，核心功能验证")
    config.addinivalue_line("markers", "regression: 回归测试，全量功能验证")
    config.addinivalue_line("markers", "debug: 调试测试，包含详细的HTTP和DB日志")
    # 注意: keep_data marker 由框架自动注册（v3.11.1），无需在此定义


def pytest_sessionstart(session: pytest.Session) -> None:
    \"\"\"Session开始时执行 - 配置Allure环境信息

    v3.5: 使用声明式配置，settings直接创建即可
    \"\"\"
    try:
        from {project_name}.config import {ProjectName}Settings
        settings = {ProjectName}Settings()

        # 添加Allure环境信息
        AllureHelper.add_environment_info({{
            "环境": settings.env,
            "API地址": settings.http.base_url,
            # "数据库": f"{{settings.db.host}}:{{settings.db.port}}",  # 如果使用数据库
            "Python版本": "3.12+",
            "框架版本": "df-test-framework v3.14.0",
            "项目版本": "{project_name} v1.0.0",
            "测试类型": "API自动化测试",
        }})
    except Exception as e:
        # 配置加载失败不影响测试运行
        print(f"警告: 无法加载Allure环境信息: {{e}}")


def pytest_collection_modifyitems(session, config, items):
    \"\"\"测试收集修改钩子

    自动为测试添加Allure标签
    \"\"\"
    for item in items:
        # 根据文件路径添加feature标签
        if "api" in str(item.fspath):
            item.add_marker(pytest.mark.allure_label("feature", "API测试"))
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.allure_label("feature", "集成测试"))


# ========== v3.5 Debug Tools Fixtures ==========

@pytest.fixture
def http_debug():
    \"\"\"HTTP调试工具 - Function 级别

    v3.5 特性:
    - 自动打印所有HTTP请求详情（URL、方法、headers、body）
    - 自动打印所有HTTP响应详情（状态码、headers、body）
    - 便于快速定位API问题

    使用方式:
        >>> def test_example(http_client, http_debug):
        ...     # http_debug 自动启用，所有 HTTP 请求/响应都会打印
        ...     response = http_client.get("/api/test")

    运行调试测试:
        pytest tests/test_example.py -v -s  # -s 参数显示调试输出
    \"\"\"
    from df_test_framework.testing.debugging import enable_http_debug

    debugger = enable_http_debug()
    yield debugger
    debugger.print_summary()


@pytest.fixture
def db_debug():
    \"\"\"数据库调试工具 - Function 级别

    v3.5 特性:
    - 自动打印所有SQL查询语句
    - 自动打印查询参数
    - 自动打印查询结果行数
    - 便于快速定位数据库问题

    使用方式:
        >>> def test_example(database, db_debug):
        ...     # db_debug 自动启用，所有 SQL 查询都会打印
        ...     result = database.query_one("SELECT * FROM users WHERE id = :id", {{"id": 1}})

    运行调试测试:
        pytest tests/test_example.py -v -s  # -s 参数显示调试输出
    \"\"\"
    from df_test_framework.testing.debugging import enable_db_debug

    debugger = enable_db_debug()
    yield debugger
    debugger.print_summary()


@pytest.fixture
def debug_mode(http_debug, db_debug):
    \"\"\"完整调试模式 - 同时启用HTTP和数据库调试

    v3.5 特性:
    - 同时启用HTTP和数据库调试
    - 一键开启全方位调试
    - 适合复杂场景的端到端调试

    使用方式:
        >>> def test_example(http_client, database, debug_mode):
        ...     # 所有 HTTP 请求和数据库查询都会打印
        ...     response = http_client.get("/api/test")
        ...     result = database.query_one("SELECT * FROM users")

    运行调试测试:
        pytest -m debug -v -s  # 运行所有标记为 debug 的测试
    \"\"\"
    # http_debug 和 db_debug 已经通过参数注入并启用
    # 这个 fixture 只是作为一个便捷的组合
    return {{"http": http_debug, "db": db_debug}}


# ========== v3.11.1 API测试数据清理 Fixture ==========
# 以下是 API 测试数据清理的示例实现（建议在 fixtures/cleanup_fixtures.py 中实现）
# 取消注释并根据项目需求修改
#
# 方式1: 使用 ListCleanup（最简单，适合单表清理）
# ------------------------------------------------------
# import pytest
# from df_test_framework.testing.fixtures.cleanup import ListCleanup
#
# @pytest.fixture
# def cleanup_orders(request, http_client):
#     \"\"\"订单数据清理 - 使用 ListCleanup（最简单方式）
#
#     使用方式:
#         def test_create_order(http_client, cleanup_orders):
#             response = http_client.post("/orders", json={{"order_no": "TEST_001"}})
#             order_id = response.json()["data"]["order_id"]
#
#             # 添加到清理列表
#             cleanup_orders.append(order_id)
#
#             # ... 测试逻辑 ...
#             # ✅ 测试结束后自动清理
#     \"\"\"
#     orders = ListCleanup(request)
#     yield orders
#
#     # 执行清理
#     if orders.should_do_cleanup():
#         for order_id in orders:
#             try:
#                 http_client.delete(f"/orders/{{order_id}}")
#             except Exception as e:
#                 print(f"清理订单 {{order_id}} 失败: {{e}}")
#
#
# 方式2: 使用 CleanupManager 子类（适合复杂清理逻辑）
# ------------------------------------------------------
# import pytest
# from df_test_framework.testing.fixtures.cleanup import CleanupManager
#
# class OrderCleanupManager(CleanupManager):
#     \"\"\"订单数据清理管理器\"\"\"
#
#     def __init__(self, request, http_client):
#         super().__init__(request, db=None)  # API清理不需要db
#         self.http_client = http_client
#
#     def _do_cleanup(self):
#         \"\"\"执行实际清理逻辑\"\"\"
#         for order_id in self.get_items("orders"):
#             try:
#                 self.http_client.delete(f"/orders/{{order_id}}")
#             except Exception as e:
#                 print(f"清理订单 {{order_id}} 失败: {{e}}")
#
# @pytest.fixture
# def cleanup_api_data(request, http_client):
#     \"\"\"API 测试数据清理 - Function 级别\"\"\"
#     manager = OrderCleanupManager(request, http_client)
#     yield manager
#     manager.cleanup()
#
#
# 保留测试数据（调试）:
#     # 方式1: 使用 marker
#     @pytest.mark.keep_data
#     def test_example(cleanup_orders):
#         pass
#
#     # 方式2: 命令行参数
#     pytest --keep-test-data -v
#
#     # 方式3: 环境变量
#     KEEP_TEST_DATA=1 pytest -v


# ========== 导出所有fixtures ==========

__all__ = [
    # 框架自动提供的 fixtures（通过 pytest_plugins 注入，无需导入）
    # - runtime: RuntimeContext 实例
    # - http_client: HTTP 客户端
    # - database: 数据库连接
    # - redis_client: Redis 客户端
    # - http_mock: HTTP Mock 工具
    # - time_mock: 时间 Mock 工具

    # 项目定义的 fixtures
    "settings",  # 配置对象（从 runtime 获取）

    # Debug fixtures（v3.5+）
    "http_debug",
    "db_debug",
    "debug_mode",

    # 项目业务 fixtures（取消注释以启用）
    # "cleanup_api_data",  # API 数据清理（v3.11.1）
    # "uow",  # Unit of Work
]
"""

__all__ = ["CONFTEST_TEMPLATE"]
