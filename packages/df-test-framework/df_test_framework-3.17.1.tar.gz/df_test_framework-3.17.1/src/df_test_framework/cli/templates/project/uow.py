"""UnitOfWork 配置说明模板

v3.13.0 更新：配置驱动，无需自定义 UoW 类。
"""

UOW_TEMPLATE = '''"""Unit of Work 配置说明 (v3.13.0)

v3.13.0 重大变更：
- ✅ 无需创建自定义 UoW 类
- ✅ 无需创建自定义 uow fixture
- ✅ 只需在 .env 中配置即可

配置方式：
    在 .env 文件中添加：
    TEST__REPOSITORY_PACKAGE={project_name_snake}.repositories

使用示例：
    >>> def test_example(uow):
    ...     # uow 自动具有所有 Repository
    ...     user = uow.users.find_by_id(1)
    ...     order = uow.orders.create({{"user_id": 1, "amount": 100}})
    ...     # ✅ 测试结束自动回滚

数据保留配置：
    - @pytest.mark.keep_data - 测试标记
    - --keep-test-data - 命令行参数
    - TEST__KEEP_TEST_DATA=1 - .env 文件配置

Repository 命名规则：
    - UserRepository -> uow.users
    - OrderRepository -> uow.orders
    - PaymentRepository -> uow.payments

如需 IDE 类型提示，可创建类型存根（可选）：
    if TYPE_CHECKING:
        class UnitOfWork:
            users: UserRepository
            orders: OrderRepository
"""

# v3.13.0: 框架 uow fixture 自动读取 TEST__REPOSITORY_PACKAGE 配置
# 无需在此定义自定义 UoW 类
'''

__all__ = ["UOW_TEMPLATE"]
