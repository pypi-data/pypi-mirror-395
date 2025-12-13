"""数据清理Fixtures模板"""

DATA_CLEANERS_TEMPLATE = """\"\"\"数据清理Fixtures

提供项目自定义的数据清理功能。

v3.11.1说明:
- ✅ 推荐使用 Unit of Work 模式（uow fixture 管理事务和 Repository）
- ✅ 框架已内置 http_mock（HTTP请求Mock）
- ✅ 框架已内置 time_mock（时间Mock）
- 🆕 v3.11.1 API测试数据清理（CleanupManager, ListCleanup, should_keep_test_data）
- 🆕 v3.11.1 DataGenerator.test_id() - 无需实例化生成测试标识符

本文件用于定义项目特定的清理fixtures，例如:
- API测试数据清理（订单、用户、支付等通过API创建的数据）
- 文件清理（临时文件、上传文件）
- 外部资源清理（S3、OSS等）
- 缓存清理（Redis特定key清理）

配置控制（v3.11.1）:
- pytest --keep-test-data      # 命令行参数，保留所有测试数据
- KEEP_TEST_DATA=1             # 环境变量，保留所有测试数据
- @pytest.mark.keep_data       # 测试标记，保留该测试的数据
\"\"\"

import pytest
from pathlib import Path
from typing import List, Callable

from df_test_framework import DataGenerator, CleanupManager, ListCleanup, should_keep_test_data


@pytest.fixture
def cleanup_files() -> Callable[[Path], Path]:
    \"\"\"文件自动清理fixture

    测试中创建的文件会在测试结束后自动删除。

    使用示例:
        ```python
        def test_file_upload(cleanup_files, http_client):
            # 创建临时文件
            test_file = Path("test_upload.txt")
            test_file.write_text("test content")
            cleanup_files(test_file)  # 注册清理

            # 上传文件
            response = http_client.post(
                "/upload",
                files={{"file": test_file.open("rb")}}
            )
            assert response.status_code == 200

            # ✅ 测试结束后自动删除 test_upload.txt
        ```

    Yields:
        Callable: 文件注册函数
    \"\"\"
    created_files: List[Path] = []

    def register_file(filepath: Path) -> Path:
        \"\"\"注册需要清理的文件

        Args:
            filepath: 文件路径

        Returns:
            Path: 原始路径（支持链式调用）
        \"\"\"
        created_files.append(filepath)
        return filepath

    yield register_file

    # 测试结束后清理所有注册的文件
    for filepath in created_files:
        if filepath.exists():
            try:
                if filepath.is_file():
                    filepath.unlink()
                elif filepath.is_dir():
                    import shutil
                    shutil.rmtree(filepath)
            except Exception as e:
                print(f"清理文件失败: {{filepath}} - {{e}}")


@pytest.fixture
def cleanup_redis_keys(redis_client) -> Callable[[str], None]:
    \"\"\"Redis Key自动清理fixture

    测试中创建的Redis key会在测试结束后自动删除。

    使用示例:
        ```python
        def test_cache(cleanup_redis_keys, redis_client):
            # 设置缓存
            test_key = "test:user:123"
            redis_client.set(test_key, "test_value")
            cleanup_redis_keys(test_key)  # 注册清理

            # 验证缓存
            value = redis_client.get(test_key)
            assert value == "test_value"

            # ✅ 测试结束后自动删除 test:user:123
        ```

    Yields:
        Callable: Key注册函数
    \"\"\"
    keys_to_delete: List[str] = []

    def register_key(key: str) -> None:
        \"\"\"注册需要清理的Redis key

        Args:
            key: Redis key
        \"\"\"
        keys_to_delete.append(key)

    yield register_key

    # 测试结束后清理所有注册的keys
    if keys_to_delete:
        try:
            redis_client.delete(*keys_to_delete)
        except Exception as e:
            print(f"清理Redis keys失败: {{e}}")


# ========== v3.11.1 API测试数据清理 ==========

class OrderCleanupManager(CleanupManager):
    \"\"\"订单数据清理管理器示例

    继承 CleanupManager，实现 _do_cleanup() 方法。
    自动根据 --keep-test-data 配置决定是否清理。

    使用方式:
        @pytest.fixture
        def cleanup_orders(request, database):
            manager = OrderCleanupManager(request, database)
            yield manager
            manager.cleanup()  # 自动检查配置
    \"\"\"
    def _do_cleanup(self):
        # 按依赖关系倒序清理（先子表后主表）
        for order_no in self.get_items("orders"):
            # 1. 先删除订单明细
            self.db.execute(
                "DELETE FROM order_items WHERE order_no = :no",
                {{"no": order_no}}
            )
            # 2. 再删除订单主表
            self.db.execute(
                "DELETE FROM orders WHERE order_no = :no",
                {{"no": order_no}}
            )


@pytest.fixture
def cleanup_orders(request, database):
    \"\"\"订单数据清理fixture（v3.11.1）

    使用 CleanupManager 模式清理 API 创建的订单数据。

    使用示例:
        ```python
        def test_create_order(http_client, cleanup_orders):
            # 生成测试订单号
            order_no = DataGenerator.test_id("TEST_ORD")

            # 调用 API 创建订单
            response = http_client.post("/orders", json={{"order_no": order_no}})
            assert response.status_code == 200

            # 注册清理
            cleanup_orders.add("orders", order_no)

            # ... 后续测试断言 ...
            # ✅ 测试结束后自动清理（除非 --keep-test-data）
        ```

    运行测试:
        pytest tests/                   # 正常运行，自动清理数据
        pytest tests/ --keep-test-data  # 保留测试数据用于调试
    \"\"\"
    manager = OrderCleanupManager(request, database)
    yield manager
    manager.cleanup()


@pytest.fixture
def cleanup_order_nos(request, database):
    \"\"\"订单号列表清理fixture（v3.11.1）

    使用 ListCleanup 模式，适合简单的单表清理场景。

    使用示例:
        ```python
        def test_create_order(http_client, cleanup_order_nos, database):
            order_no = DataGenerator.test_id("TEST_ORD")
            response = http_client.post("/orders", json={{"order_no": order_no}})
            cleanup_order_nos.append(order_no)  # 添加到清理列表

            # ... 测试断言 ...

            # ✅ 测试结束后执行清理（fixture teardown）
        ```
    \"\"\"
    order_nos = ListCleanup(request)
    yield order_nos

    # 根据配置决定是否清理
    if order_nos.should_do_cleanup():
        for order_no in order_nos:
            try:
                database.execute(
                    "DELETE FROM orders WHERE order_no = :no",
                    {{"no": order_no}}
                )
            except Exception as e:
                print(f"清理订单失败 {{order_no}}: {{e}}")


__all__ = [
    # 文件和Redis清理
    "cleanup_files",
    "cleanup_redis_keys",
    # API测试数据清理（v3.11.1）
    "OrderCleanupManager",
    "cleanup_orders",
    "cleanup_order_nos",
]
"""

__all__ = ["DATA_CLEANERS_TEMPLATE"]
