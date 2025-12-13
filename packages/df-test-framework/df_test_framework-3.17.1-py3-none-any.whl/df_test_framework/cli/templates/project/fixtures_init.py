"""Fixtures模块导出模板"""

FIXTURES_INIT_TEMPLATE = """\"\"\"Pytest Fixtures (v3.11.1)

导出项目自定义 fixtures。

框架自动提供（通过 pytest_plugins）:
- runtime: 运行时上下文
- http_client: HTTP客户端
- database: 数据库连接
- redis_client: Redis客户端
- http_mock: HTTP Mock 工具
- time_mock: 时间 Mock 工具

项目自定义:
- 业务 API fixtures（如需要）
- uow: Unit of Work（事务管理 + Repository）
- cleanup_api_data: API测试数据清理

v3.11.1 新增:
- 测试数据清理工具（should_keep_test_data, CleanupManager, ListCleanup）
- DataGenerator.test_id() - 无需实例化生成测试标识符
\"\"\"

# ========== 项目业务专属 Fixtures ==========
# 项目只需定义业务专属 fixtures，核心 fixtures 由框架自动提供

# from .api_fixtures import (
#     api_client,  # 示例：业务 API 客户端
# )

# from .uow_fixture import uow  # Unit of Work

# from .cleanup_fixtures import cleanup_api_data  # API 数据清理


__all__ = [
    # 注意: 框架自动提供以下 fixtures（无需在此导出）:
    # - runtime, http_client, database, redis_client
    # - http_mock, time_mock

    # 项目业务 fixtures（取消注释以启用）
    # "api_client",
    # "uow",
    # "cleanup_api_data",
]
"""

__all__ = ["FIXTURES_INIT_TEMPLATE"]
