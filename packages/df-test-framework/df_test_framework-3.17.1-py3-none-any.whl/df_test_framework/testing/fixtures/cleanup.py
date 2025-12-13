"""测试数据清理 - 通用基础设施

v3.11.1 重新设计:
- 统一配置：使用 --keep-test-data 控制所有数据保留（UoW + API 数据）
- 基类内置配置检查：项目无需重复检查

v3.12.1 改进:
- 支持通过 Settings 配置（.env 文件中 KEEP_TEST_DATA=1）

配置方式（优先级从高到低）:
1. @pytest.mark.keep_data - 测试标记
2. --keep-test-data - 命令行参数
3. Settings 配置 - .env 文件或环境变量 KEEP_TEST_DATA=1

使用示例:
    # 正常运行（默认清理数据）
    pytest tests/

    # 调试模式（保留所有数据）
    pytest tests/ --keep-test-data

    # .env 文件配置（本地开发推荐）
    KEEP_TEST_DATA=1

    # 单个测试保留数据
    @pytest.mark.keep_data
    def test_debug():
        ...

测试数据生成:
    使用 DataGenerator 生成测试数据标识符:
    from df_test_framework import DataGenerator

    gen = DataGenerator()
    order_no = gen.order_id(prefix="TEST_ORD")
    # 或使用类方法（无需实例化）
    order_no = DataGenerator.test_id("TEST_ORD")
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from loguru import logger

if TYPE_CHECKING:
    import pytest


# ============================================================
# 配置检查
# ============================================================


def should_keep_test_data(request: pytest.FixtureRequest) -> bool:
    """检查是否应该保留测试数据（不清理）

    统一检查函数，用于 UoW 回滚和 API 数据清理。

    优先级（从高到低）:
    1. @pytest.mark.keep_data 标记
    2. --keep-test-data 命令行参数
    3. Settings 配置（通过 .env 文件或环境变量 KEEP_TEST_DATA=1）

    Args:
        request: pytest fixture request 对象

    Returns:
        bool: True 表示保留数据（不清理），False 表示清理数据

    Usage:
        @pytest.fixture
        def cleanup_data(request, database):
            items = []
            yield items

            if should_keep_test_data(request):
                logger.info("保留测试数据（调试模式）")
                return

            # 执行清理...
    """
    # 1. 检查测试标记（最高优先级）
    if request.node.get_closest_marker("keep_data"):
        logger.debug("检测到 @pytest.mark.keep_data 标记")
        return True

    # 2. 检查命令行参数
    if hasattr(request.config.option, "keep_test_data") and request.config.option.keep_test_data:
        logger.debug("检测到 --keep-test-data 参数")
        return True

    # 3. 从 Settings 读取配置（通过 .env 或环境变量 KEEP_TEST_DATA=1）
    try:
        from df_test_framework.infrastructure.config import get_settings

        settings = get_settings()
        if settings and settings.test and settings.test.keep_test_data:
            logger.debug("检测到 Settings 配置 keep_test_data=True")
            return True
    except Exception as e:
        logger.debug(f"读取 Settings 配置失败: {e}")

    return False


# ============================================================
# 清理管理器基类
# ============================================================


class CleanupManager(ABC):
    """测试数据清理管理器基类

    内置配置检查，自动根据 --keep-test-data 等配置决定是否清理。

    Usage:
        class MyCleanupManager(CleanupManager):
            def _do_cleanup(self):
                for order_no in self.get_items("orders"):
                    self.db.execute("DELETE FROM orders WHERE order_no = ?", order_no)

        @pytest.fixture
        def cleanup(request, database):
            manager = MyCleanupManager(request, database)
            yield manager
            manager.cleanup()  # 自动检查配置，决定是否清理
    """

    def __init__(self, request: pytest.FixtureRequest, db: Any = None):
        """初始化清理管理器

        Args:
            request: pytest fixture request 对象（用于检查配置）
            db: 数据库连接（可选）
        """
        self._request = request
        self._db = db
        self._items: dict[str, list[Any]] = {}

    @property
    def db(self) -> Any:
        """数据库连接"""
        return self._db

    def add(self, item_type: str, item_id: Any) -> None:
        """添加需要清理的项目

        Args:
            item_type: 项目类型（如 "orders", "payments"）
            item_id: 项目标识符
        """
        if item_type not in self._items:
            self._items[item_type] = []
        self._items[item_type].append(item_id)
        logger.debug(f"注册清理项: {item_type} = {item_id}")

    def add_many(self, item_type: str, item_ids: list[Any]) -> None:
        """批量添加需要清理的项目"""
        for item_id in item_ids:
            self.add(item_type, item_id)

    def get_items(self, item_type: str) -> list[Any]:
        """获取指定类型的所有项目"""
        return self._items.get(item_type, [])

    def all_items(self) -> dict[str, list[Any]]:
        """获取所有项目"""
        return self._items.copy()

    def has_items(self) -> bool:
        """是否有需要清理的项目"""
        return any(items for items in self._items.values())

    def cleanup(self) -> None:
        """执行清理（自动检查配置）

        如果配置了保留数据，则跳过清理并打印保留的数据。
        """
        if not self.has_items():
            return

        if should_keep_test_data(self._request):
            self._log_kept_items()
            return

        logger.info("开始清理测试数据...")
        try:
            self._do_cleanup()
            logger.info("测试数据清理完成")
        except Exception as e:
            logger.error(f"清理失败: {e}")

    def _log_kept_items(self) -> None:
        """打印保留的数据项"""
        logger.info("保留测试数据（调试模式）:")
        for item_type, items in self._items.items():
            if items:
                logger.info(f"  {item_type}: {items}")

    @abstractmethod
    def _do_cleanup(self) -> None:
        """执行实际清理逻辑（子类实现）"""
        pass


class SimpleCleanupManager(CleanupManager):
    """简单清理管理器 - 使用回调函数（P1-3 增强版）

    适用于不想创建子类的场景。

    P1-3 新增便捷方法:
    - add_api_data() - 自动清理 API 数据
    - add_db_row() - 自动清理数据库行

    Usage:
        @pytest.fixture
        def cleanup(request, database):
            manager = SimpleCleanupManager(request, database)

            # 传统方式：注册清理函数
            manager.register_cleanup("orders", lambda ids: database.execute(
                "DELETE FROM orders WHERE order_no IN :ids", {"ids": tuple(ids)}
            ))

            # P1-3 便捷方式：自动清理
            manager.add_db_row(database, "orders", order_no="ORD001")

            yield manager
            manager.cleanup()
    """

    def __init__(self, request: pytest.FixtureRequest, db: Any = None):
        super().__init__(request, db)
        self._cleanup_funcs: dict[str, Callable[[list[Any]], None]] = {}
        self._http_client: Any = None  # P1-3: 存储 http_client

    def register_cleanup(self, item_type: str, cleanup_func: Callable[[list[Any]], None]) -> None:
        """注册清理函数

        Args:
            item_type: 项目类型
            cleanup_func: 清理函数，接收项目ID列表
        """
        self._cleanup_funcs[item_type] = cleanup_func

    def add_api_data(
        self,
        http_client: Any,
        endpoint: str,
        identifier: Any,
        method: str = "DELETE",
    ) -> None:
        """添加 API 数据清理（P1-3 新增）

        自动注册 API 数据清理，测试结束后自动调用删除接口。

        Args:
            http_client: HTTP 客户端
            endpoint: API 端点模板，支持 {id} 占位符
                     例如: "/orders/{id}", "/cards/{card_no}"
            identifier: 数据标识符（如 order_id, card_no）
            method: HTTP 方法，默认 DELETE

        Example:
            >>> # 测试中创建订单
            >>> response = http_client.post("/orders", json={...})
            >>> order_id = response.json()["id"]
            >>>
            >>> # 注册清理（测试结束后自动删除）
            >>> cleanup.add_api_data(http_client, "/orders/{id}", order_id)
            >>> # 等价于：测试结束后调用 http_client.delete(f"/orders/{order_id}")
        """
        self._http_client = http_client

        # 构建完整的 API 路径
        import re

        if isinstance(identifier, dict):
            # 字典方式：支持多个占位符
            # 例如: "/orders/{type}/{id}" + {"type": "online", "id": "123"}
            api_path = endpoint.format(**identifier)
        else:
            # 单个值：替换第一个占位符或拼接到末尾
            # 例如: "/orders/{id}" + "123" -> "/orders/123"
            # 或者: "/orders" + "123" -> "/orders/123"
            if "{" in endpoint:
                # 有占位符，替换第一个
                api_path = re.sub(r"\{[^}]+\}", str(identifier), endpoint, count=1)
            else:
                # 无占位符，拼接到末尾
                api_path = f"{endpoint.rstrip('/')}/{identifier}"

        # 添加到清理列表
        item_type = f"api_{method.lower()}"
        self.add(item_type, api_path)

        # 自动注册清理函数（如果还没注册）
        if item_type not in self._cleanup_funcs:
            self.register_cleanup(item_type, lambda paths: self._cleanup_api_paths(method, paths))

        logger.debug(f"[P1-3] 注册 API 数据清理: {method} {api_path}")

    def add_db_row(self, database: Any, table: str, **conditions) -> None:
        """添加数据库行清理（P1-3 新增）

        自动注册数据库行清理，测试结束后自动删除对应行。

        Args:
            database: 数据库连接对象
            table: 表名
            **conditions: WHERE 条件（字段=值）

        Example:
            >>> # 测试中创建卡片
            >>> database.execute(
            ...     "INSERT INTO cards (card_no, status) VALUES (:card_no, :status)",
            ...     {"card_no": "CARD001", "status": 0}
            ... )
            >>>
            >>> # 注册清理（测试结束后自动删除）
            >>> cleanup.add_db_row(database, "cards", card_no="CARD001")
            >>> # 等价于：测试结束后执行 DELETE FROM cards WHERE card_no = 'CARD001'
        """
        if not self._db:
            self._db = database

        # 构建清理项标识
        item_type = f"db_table_{table}"
        self.add(item_type, conditions)

        # 自动注册清理函数（如果还没注册）
        if item_type not in self._cleanup_funcs:
            self.register_cleanup(item_type, lambda items: self._cleanup_db_rows(table, items))

        logger.debug(f"[P1-3] 注册数据库行清理: {table} WHERE {conditions}")

    def _cleanup_api_paths(self, method: str, paths: list[str]) -> None:
        """清理 API 数据（P1-3 内部方法）"""
        if not self._http_client:
            logger.warning("未设置 http_client，无法清理 API 数据")
            return

        for path in paths:
            try:
                if method.upper() == "DELETE":
                    self._http_client.delete(path)
                elif method.upper() == "POST":
                    self._http_client.post(path)
                else:
                    logger.warning(f"不支持的 HTTP 方法: {method}")
                logger.debug(f"已清理 API 数据: {method} {path}")
            except Exception as e:
                logger.warning(f"清理 API 数据失败 ({path}): {e}")

    def _cleanup_db_rows(self, table: str, condition_list: list[dict]) -> None:
        """清理数据库行（P1-3 内部方法）"""
        if not self._db:
            logger.warning("未设置数据库连接，无法清理数据库数据")
            return

        for conditions in condition_list:
            try:
                # 构建 WHERE 子句
                where_parts = []
                params = {}
                for i, (key, value) in enumerate(conditions.items()):
                    param_name = f"{key}_{i}"
                    where_parts.append(f"{key} = :{param_name}")
                    params[param_name] = value

                where_clause = " AND ".join(where_parts)
                sql = f"DELETE FROM {table} WHERE {where_clause}"

                self._db.execute(sql, params)
                logger.debug(f"已清理数据库行: {table} WHERE {conditions}")
            except Exception as e:
                logger.warning(f"清理数据库行失败 ({table}, {conditions}): {e}")

    def _do_cleanup(self) -> None:
        """执行所有注册的清理函数"""
        for item_type, items in self._items.items():
            if not items:
                continue

            cleanup_func = self._cleanup_funcs.get(item_type)
            if cleanup_func:
                try:
                    cleanup_func(items)
                    logger.info(f"已清理 {item_type}: {len(items)} 项")
                except Exception as e:
                    logger.warning(f"清理 {item_type} 失败: {e}")
            else:
                logger.warning(f"未注册 {item_type} 的清理函数，跳过")


# ============================================================
# 列表式清理（最简单用法）
# ============================================================


class ListCleanup(list):
    """列表式清理器 - 最简单的用法

    继承自 list，可以直接 append，同时支持清理控制。

    Usage:
        @pytest.fixture
        def cleanup_orders(request, database):
            orders = ListCleanup(request)

            yield orders

            # 方式1: 使用 should_do_cleanup() (推荐)
            if orders.should_do_cleanup():
                for order_no in orders:
                    database.execute(
                        "DELETE FROM orders WHERE order_no = :order_no",
                        {"order_no": order_no}
                    )

            # 方式2: 使用 should_keep() 检查
            if orders.should_keep():
                return
            # 执行清理...
    """

    def __init__(self, request: pytest.FixtureRequest):
        super().__init__()
        self._request = request
        self._keep_logged = False

    def should_keep(self) -> bool:
        """是否应该保留数据（不清理）"""
        return should_keep_test_data(self._request)

    def should_do_cleanup(self) -> bool:
        """是否应该执行清理（推荐使用）

        如果需要保留数据，会自动打印日志（只打印一次）。

        Returns:
            True: 应该清理
            False: 不清理（已打印保留日志）
        """
        if should_keep_test_data(self._request):
            if self and not self._keep_logged:
                logger.info(f"保留测试数据: {list(self)}")
                self._keep_logged = True
            return False
        return True


# ============================================================
# 导出
# ============================================================

__all__ = [
    # 配置检查
    "should_keep_test_data",
    # 清理管理器
    "CleanupManager",
    "SimpleCleanupManager",
    "ListCleanup",
]
