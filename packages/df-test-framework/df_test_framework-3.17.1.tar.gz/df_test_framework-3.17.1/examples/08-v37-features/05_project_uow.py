"""
项目级 UoW 封装（最佳实践）

展示如何为项目创建专用的 UoW 类

本示例演示：
1. 继承 BaseUnitOfWork 创建项目 UoW
2. 使用 @property 暴露 Repository
3. 提供类型提示，IDE 友好
4. 简化测试代码

学习要点：
- ✅ 项目级 UoW 是最佳实践
- ✅ 使用属性方法暴露 Repository
- ✅ 提供完整类型提示
- ✅ IDE 自动补全和类型检查
"""

from sqlalchemy.orm import Session

from df_test_framework import BaseRepository
from df_test_framework.databases import BaseUnitOfWork

# ========== Repository 定义 ==========

class CardRepository(BaseRepository):
    """礼品卡仓库"""

    def __init__(self, session: Session):
        super().__init__(session, table_name="gift_cards")

    def find_by_card_no(self, card_no: str) -> dict | None:
        """根据卡号查找"""
        return self.find_one({"card_no": card_no})


class OrderRepository(BaseRepository):
    """订单仓库"""

    def __init__(self, session: Session):
        super().__init__(session, table_name="orders")


class PaymentRepository(BaseRepository):
    """支付记录仓库"""

    def __init__(self, session: Session):
        super().__init__(session, table_name="payments")


class ConsumptionRepository(BaseRepository):
    """消费记录仓库"""

    def __init__(self, session: Session):
        super().__init__(session, table_name="consumptions")


class TemplateRepository(BaseRepository):
    """模板仓库"""

    def __init__(self, session: Session):
        super().__init__(session, table_name="templates")


# ========== 项目级 UoW 封装 ==========

class GiftCardUoW(BaseUnitOfWork):
    """Gift Card 项目专用 Unit of Work

    提供类型安全的 Repository 访问接口。

    优势：
    1. ✅ IDE 自动补全
    2. ✅ 类型检查
    3. ✅ 代码简洁
    4. ✅ 易于维护

    使用示例：
        >>> with GiftCardUoW(session_factory) as uow:
        ...     # ✅ IDE 自动补全 cards/orders/payments
        ...     card = uow.cards.find_by_card_no("CARD123")
        ...     order = uow.orders.create({...})
        ...     uow.commit()
    """

    @property
    def cards(self) -> CardRepository:
        """卡片 Repository

        Returns:
            CardRepository: 卡片数据仓库
        """
        return self.repository(CardRepository)

    @property
    def orders(self) -> OrderRepository:
        """订单 Repository

        Returns:
            OrderRepository: 订单数据仓库
        """
        return self.repository(OrderRepository)

    @property
    def payments(self) -> PaymentRepository:
        """支付记录 Repository

        Returns:
            PaymentRepository: 支付记录数据仓库
        """
        return self.repository(PaymentRepository)

    @property
    def consumptions(self) -> ConsumptionRepository:
        """消费记录 Repository

        Returns:
            ConsumptionRepository: 消费记录数据仓库
        """
        return self.repository(ConsumptionRepository)

    @property
    def templates(self) -> TemplateRepository:
        """模板 Repository

        Returns:
            TemplateRepository: 模板数据仓库
        """
        return self.repository(TemplateRepository)


# ========== 使用示例 ==========

def example_1_basic_usage():
    """示例1：基础使用"""
    print("\n" + "=" * 60)
    print("示例1：基础使用 - 简洁的 API")
    print("=" * 60)

    print("""
# ❌ 使用 BaseUnitOfWork（繁琐）
with BaseUnitOfWork(session_factory) as uow:
    card_repo = uow.repository(CardRepository)
    order_repo = uow.repository(OrderRepository)

    card = card_repo.find_by_card_no("CARD123")
    order = order_repo.create({...})

# ✅ 使用 GiftCardUoW（简洁）
with GiftCardUoW(session_factory) as uow:
    card = uow.cards.find_by_card_no("CARD123")  # ✅ 直接访问
    order = uow.orders.create({...})              # ✅ 简洁清晰
    """)


def example_2_type_hints():
    """示例2：类型提示和 IDE 支持"""
    print("\n" + "=" * 60)
    print("示例2：类型提示 - IDE 自动补全")
    print("=" * 60)

    print("""
# conftest.py 中定义 fixture
@pytest.fixture
def uow(session_factory) -> GiftCardUoW:  # ✅ 明确类型
    with GiftCardUoW(session_factory) as uow:
        yield uow

# 测试中使用
def test_payment(uow: GiftCardUoW):  # ✅ 类型提示
    # ✅ IDE 会自动补全：cards, orders, payments, consumptions, templates
    card = uow.cards.find_by_card_no("CARD123")

    # ✅ IDE 会提示 CardRepository 的所有方法
    all_cards = uow.cards.find_all()

    # ✅ 类型检查会发现错误
    # uow.cardss.find_all()  # ❌ IDE 报错：没有 cardss 属性
    """)


def example_3_business_code():
    """示例3：业务代码中使用"""
    print("\n" + "=" * 60)
    print("示例3：业务代码中使用")
    print("=" * 60)

    print("""
from decimal import Decimal

def process_payment(uow: GiftCardUoW, card_no: str, amount: Decimal):
    \"\"\"处理支付业务

    Args:
        uow: GiftCardUoW 实例
        card_no: 礼品卡号
        amount: 支付金额

    Returns:
        payment_id: 支付记录ID
    \"\"\"
    # 1. 查询卡片
    card = uow.cards.find_by_card_no(card_no)
    if not card:
        raise ValueError(f"卡片不存在: {card_no}")

    # 2. 检查余额
    balance = Decimal(str(card["balance"]))
    if balance < amount:
        raise ValueError(f"余额不足: {balance} < {amount}")

    # 3. 创建订单
    order_id = uow.orders.create({
        "card_no": card_no,
        "amount": amount,
        "status": "pending"
    })

    # 4. 扣减余额
    new_balance = balance - amount
    uow.cards.update(
        conditions={"card_no": card_no},
        data={"balance": new_balance}
    )

    # 5. 创建支付记录
    payment_id = uow.payments.create({
        "order_id": order_id,
        "card_no": card_no,
        "amount": amount,
        "status": "success"
    })

    # 6. 创建消费记录
    uow.consumptions.create({
        "card_no": card_no,
        "amount": amount,
        "type": 0,  # 0=消费
        "balance": new_balance
    })

    # 7. 提交事务
    uow.commit()

    return payment_id
    """)


def example_4_pytest_fixture():
    """示例4：在 conftest.py 中配置"""
    print("\n" + "=" * 60)
    print("示例4：Pytest Fixture 配置")
    print("=" * 60)

    print("""
# src/gift_card_test/conftest.py

import pytest
from gift_card_test.uow import GiftCardUoW

@pytest.fixture
def uow(session_factory) -> GiftCardUoW:
    \"\"\"提供 GiftCardUoW fixture

    特性：
    - ✅ 自动回滚
    - ✅ 类型提示
    - ✅ 测试隔离
    \"\"\"
    with GiftCardUoW(session_factory) as uow:
        yield uow
        # 测试结束自动回滚

# 测试文件中使用
def test_create_card(uow: GiftCardUoW):
    \"\"\"测试创建卡片\"\"\"
    card_id = uow.cards.create({
        "card_no": "TEST123",
        "balance": Decimal("100.00")
    })

    assert card_id is not None

    # ✅ 测试结束自动回滚


def test_payment_flow(uow: GiftCardUoW):
    \"\"\"测试支付流程\"\"\"
    # 1. 创建卡片
    card_no = "FLOW_TEST_123"
    uow.cards.create({
        "card_no": card_no,
        "balance": Decimal("500.00")
    })

    # 2. 创建订单
    order_id = uow.orders.create({
        "card_no": card_no,
        "amount": Decimal("100.00")
    })

    # 3. 创建支付
    payment_id = uow.payments.create({
        "order_id": order_id,
        "amount": Decimal("100.00")
    })

    # 验证
    assert order_id is not None
    assert payment_id is not None

    # ✅ 测试结束自动回滚
    """)


# ========== 最佳实践总结 ==========

def best_practices_summary():
    """最佳实践总结"""
    print("\n" + "=" * 60)
    print("💡 最佳实践总结")
    print("=" * 60)

    print("\n✅ 1. 文件结构")
    print("-" * 60)
    print("""
src/gift_card_test/
├── uow.py              # ✅ 项目级 UoW 定义
├── repositories/       # Repository 定义
│   ├── card_repository.py
│   ├── order_repository.py
│   └── payment_repository.py
├── fixtures/
│   └── __init__.py     # pytest fixtures
└── conftest.py         # ✅ 配置 uow fixture
    """)

    print("\n✅ 2. UoW 类设计")
    print("-" * 60)
    print("""
class ProjectUoW(BaseUnitOfWork):
    \"\"\"项目级 UoW

    设计要点：
    1. 使用 @property 暴露 Repository
    2. 提供完整的类型提示
    3. 添加清晰的文档注释
    4. 命名符合业务领域
    \"\"\"

    @property
    def resource_name(self) -> ResourceRepository:
        \"\"\"资源仓库说明\"\"\"
        return self.repository(ResourceRepository)
    """)

    print("\n✅ 3. Fixture 配置")
    print("-" * 60)
    print("""
@pytest.fixture
def uow(session_factory) -> ProjectUoW:  # ✅ 类型提示
    \"\"\"项目 UoW fixture\"\"\"
    with ProjectUoW(session_factory) as uow:
        yield uow
        # 自动回滚
    """)

    print("\n✅ 4. 测试使用")
    print("-" * 60)
    print("""
def test_example(uow: ProjectUoW):  # ✅ 类型提示
    # ✅ IDE 自动补全
    resource = uow.resources.create({...})

    # ✅ 类型安全
    assert resource is not None
    """)


# ========== 完整示例：真实项目 ==========

def real_project_example():
    """完整示例：真实项目结构"""
    print("\n" + "=" * 60)
    print("📁 真实项目完整示例")
    print("=" * 60)

    print("\n1️⃣  src/gift_card_test/uow.py")
    print("-" * 60)
    print("""
from df_test_framework.databases import BaseUnitOfWork
from .repositories import (
    CardRepository,
    OrderRepository,
    PaymentRepository,
    ConsumptionRepository,
    TemplateRepository,
)

class GiftCardUoW(BaseUnitOfWork):
    \"\"\"Gift Card 项目 UoW\"\"\"

    @property
    def cards(self) -> CardRepository:
        return self.repository(CardRepository)

    @property
    def orders(self) -> OrderRepository:
        return self.repository(OrderRepository)

    @property
    def payments(self) -> PaymentRepository:
        return self.repository(PaymentRepository)

    @property
    def consumptions(self) -> ConsumptionRepository:
        return self.repository(ConsumptionRepository)

    @property
    def templates(self) -> TemplateRepository:
        return self.repository(TemplateRepository)
    """)

    print("\n2️⃣  tests/conftest.py")
    print("-" * 60)
    print("""
import pytest
from gift_card_test.uow import GiftCardUoW

@pytest.fixture
def uow(session_factory) -> GiftCardUoW:
    with GiftCardUoW(session_factory) as uow:
        yield uow
    """)

    print("\n3️⃣  tests/api/test_payment.py")
    print("-" * 60)
    print("""
from decimal import Decimal
from gift_card_test.uow import GiftCardUoW

def test_payment_flow(uow: GiftCardUoW, h5_card_api):
    # 创建测试卡片
    card_no = uow.cards.create({
        "card_no": "TEST123",
        "balance": Decimal("100.00")
    })

    # 调用支付 API
    response = h5_card_api.pay({
        "card_no": card_no,
        "amount": Decimal("50.00")
    })

    # 验证支付记录
    payment = uow.payments.find_by_order(response.data.order_id)
    assert payment is not None

    # ✅ 测试结束自动回滚
    """)


# ========== 主函数 ==========

if __name__ == "__main__":
    print("\n" + "🚀 项目级 UoW 封装（最佳实践）")
    print("=" * 60)

    example_1_basic_usage()
    example_2_type_hints()
    example_3_business_code()
    example_4_pytest_fixture()
    best_practices_summary()
    real_project_example()

    print("\n" + "=" * 60)
    print("🎯 核心优势")
    print("=" * 60)
    print("""
1. ✅ IDE 自动补全
   - 输入 uow. 立即看到所有 Repository

2. ✅ 类型安全
   - 编译时发现错误，而非运行时

3. ✅ 代码简洁
   - uow.cards 而非 uow.repository(CardRepository)

4. ✅ 易于维护
   - Repository 变更时只需修改 UoW 类

5. ✅ 团队协作
   - 新成员快速理解项目结构
    """)

    print("\n" + "=" * 60)
    print("✅ 示例代码说明完成！")
    print("=" * 60)
    print("下一步：运行 06_exception_handling_with_uow.py 学习异常测试")
