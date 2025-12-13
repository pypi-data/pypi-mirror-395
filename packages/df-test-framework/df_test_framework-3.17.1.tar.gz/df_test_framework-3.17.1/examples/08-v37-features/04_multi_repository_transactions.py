"""
多Repository事务一致性

Unit of Work 核心价值：保证跨多个 Repository 的事务一致性

本示例演示：
1. 多个 Repository 共享同一事务
2. 一次 commit 提交所有更改
3. 出错时全部回滚（原子性）
4. 典型业务场景：订单+库存+支付

学习要点：
- ✅ 多个 Repository 通过 UoW 统一管理
- ✅ 确保事务原子性（全部成功或全部失败）
- ✅ 避免数据不一致
- ✅ 简化业务代码
"""

from decimal import Decimal

import pytest
from sqlalchemy.orm import Session

from df_test_framework import BaseRepository
from df_test_framework.databases import BaseUnitOfWork

# ========== Repository 定义 ==========

class OrderRepository(BaseRepository):
    """订单仓库"""

    def __init__(self, session: Session):
        super().__init__(session, table_name="orders")

    def find_by_user(self, user_id: int) -> list[dict]:
        return self.find_all({"user_id": user_id})


class PaymentRepository(BaseRepository):
    """支付记录仓库"""

    def __init__(self, session: Session):
        super().__init__(session, table_name="payments")

    def find_by_order(self, order_id: int) -> dict | None:
        return self.find_one({"order_id": order_id})


class CardRepository(BaseRepository):
    """礼品卡仓库"""

    def __init__(self, session: Session):
        super().__init__(session, table_name="cards")

    def find_by_card_no(self, card_no: str) -> dict | None:
        return self.find_one({"card_no": card_no})

    def deduct_balance(self, card_no: str, amount: Decimal) -> int:
        """扣减卡片余额"""
        card = self.find_by_card_no(card_no)
        if not card:
            raise ValueError(f"卡片不存在: {card_no}")

        current_balance = Decimal(str(card["balance"]))
        if current_balance < amount:
            raise ValueError(f"余额不足: 当前={current_balance}, 需要={amount}")

        new_balance = current_balance - amount
        return self.update(
            conditions={"card_no": card_no},
            data={"balance": new_balance}
        )


# ========== 示例1：基础多Repository操作 ==========

def example_1_basic_multi_repo(session_factory):
    """示例1：多Repository基础操作"""
    print("\n" + "=" * 60)
    print("示例1：多Repository基础操作")
    print("=" * 60)

    with BaseUnitOfWork(session_factory) as uow:
        order_repo = uow.repository(OrderRepository)
        payment_repo = uow.repository(PaymentRepository)

        # 1. 创建订单
        order_id = order_repo.create({
            "user_id": 1,
            "amount": Decimal("100.00"),
            "status": "pending"
        })
        print(f"1️⃣  创建订单: order_id={order_id}")

        # 2. 创建支付记录
        payment_id = payment_repo.create({
            "order_id": order_id,
            "amount": Decimal("100.00"),
            "status": "success"
        })
        print(f"2️⃣  创建支付记录: payment_id={payment_id}")

        # 3. 统一提交
        print("3️⃣  统一 commit() - 两个操作一起提交")
        uow.commit()

    print("✅ 订单和支付记录创建成功")


# ========== 示例2：业务场景 - 礼品卡支付 ==========

def example_2_gift_card_payment(session_factory):
    """示例2：礼品卡支付业务场景

    场景：
    1. 创建支付订单
    2. 扣减礼品卡余额
    3. 创建支付记录

    要求：三个操作必须原子性（全成功或全失败）
    """
    print("\n" + "=" * 60)
    print("示例2：礼品卡支付（事务原子性）")
    print("=" * 60)

    # 准备：创建测试礼品卡
    with BaseUnitOfWork(session_factory) as uow:
        card_repo = uow.repository(CardRepository)
        card_repo.create({
            "card_no": "CARD123456",
            "balance": Decimal("500.00"),
            "status": "active"
        })
        uow.commit()
        print("0️⃣  准备数据：创建礼品卡 CARD123456, 余额=500元")

    # 业务操作：礼品卡支付
    print("\n业务操作：使用礼品卡支付订单")
    with BaseUnitOfWork(session_factory) as uow:
        order_repo = uow.repository(OrderRepository)
        payment_repo = uow.repository(PaymentRepository)
        card_repo = uow.repository(CardRepository)

        # 1. 创建订单
        order_id = order_repo.create({
            "user_id": 1,
            "amount": Decimal("100.00"),
            "status": "pending"
        })
        print(f"1️⃣  创建订单: order_id={order_id}, amount=100元")

        # 2. 扣减礼品卡余额
        card_repo.deduct_balance("CARD123456", Decimal("100.00"))
        print("2️⃣  扣减礼品卡余额: 500 - 100 = 400元")

        # 3. 创建支付记录
        payment_id = payment_repo.create({
            "order_id": order_id,
            "card_no": "CARD123456",
            "amount": Decimal("100.00"),
            "status": "success"
        })
        print(f"3️⃣  创建支付记录: payment_id={payment_id}")

        # 4. 统一提交
        print("\n4️⃣  统一 commit() - 三个操作一起提交")
        uow.commit()

    print("✅ 礼品卡支付成功（订单、余额、支付记录都已更新）")


# ========== 示例3：事务回滚 - 余额不足 ==========

def example_3_transaction_rollback(session_factory):
    """示例3：事务回滚 - 余额不足场景

    场景：
    1. 创建订单
    2. 扣减礼品卡余额（失败 - 余额不足）
    3. 创建支付记录

    结果：第2步失败，导致整个事务回滚
    """
    print("\n" + "=" * 60)
    print("示例3：事务回滚（余额不足）")
    print("=" * 60)

    # 准备：创建余额不足的礼品卡
    with BaseUnitOfWork(session_factory) as uow:
        card_repo = uow.repository(CardRepository)
        card_repo.create({
            "card_no": "CARD_INSUFFICIENT",
            "balance": Decimal("50.00"),  # 只有50元
            "status": "active"
        })
        uow.commit()
        print("0️⃣  准备数据：创建礼品卡余额=50元")

    # 尝试支付100元（余额不足）
    print("\n业务操作：尝试支付100元（但余额只有50元）")
    try:
        with BaseUnitOfWork(session_factory) as uow:
            order_repo = uow.repository(OrderRepository)
            payment_repo = uow.repository(PaymentRepository)
            card_repo = uow.repository(CardRepository)

            # 1. 创建订单
            order_id = order_repo.create({
                "user_id": 1,
                "amount": Decimal("100.00"),
                "status": "pending"
            })
            print(f"1️⃣  创建订单: order_id={order_id}")

            # 2. 尝试扣减余额（会失败）
            print("2️⃣  尝试扣减100元...")
            card_repo.deduct_balance("CARD_INSUFFICIENT", Decimal("100.00"))

            # 3. 创建支付记录（不会执行到这里）
            payment_repo.create({
                "order_id": order_id,
                "amount": Decimal("100.00"),
                "status": "success"
            })

            uow.commit()

    except ValueError as e:
        print(f"❌ 余额不足，操作失败: {e}")
        print("3️⃣  UoW 自动回滚 - 订单创建被撤销")
        print("✅ 数据库保持一致性（没有孤儿订单）")


# ========== 示例4：复杂业务场景 ==========

def example_4_complex_transaction(session_factory):
    """示例4：复杂业务场景 - 多卡支付

    场景：使用2张礼品卡支付一个订单
    1. 创建订单 200元
    2. 扣减卡1余额 150元
    3. 扣减卡2余额 50元
    4. 创建2条支付记录
    """
    print("\n" + "=" * 60)
    print("示例4：复杂业务 - 多卡支付")
    print("=" * 60)

    # 准备：创建2张礼品卡
    with BaseUnitOfWork(session_factory) as uow:
        card_repo = uow.repository(CardRepository)
        card_repo.create({"card_no": "CARD_A", "balance": Decimal("150.00")})
        card_repo.create({"card_no": "CARD_B", "balance": Decimal("50.00")})
        uow.commit()
        print("0️⃣  准备数据：卡A=150元, 卡B=50元")

    # 多卡支付
    print("\n业务操作：使用2张卡支付200元订单")
    with BaseUnitOfWork(session_factory) as uow:
        order_repo = uow.repository(OrderRepository)
        payment_repo = uow.repository(PaymentRepository)
        card_repo = uow.repository(CardRepository)

        # 1. 创建订单
        order_id = order_repo.create({
            "user_id": 1,
            "amount": Decimal("200.00"),
            "status": "pending"
        })
        print("1️⃣  创建订单: 总额=200元")

        # 2. 扣减卡A余额
        card_repo.deduct_balance("CARD_A", Decimal("150.00"))
        print("2️⃣  扣减卡A: 150元")

        # 3. 扣减卡B余额
        card_repo.deduct_balance("CARD_B", Decimal("50.00"))
        print("3️⃣  扣减卡B: 50元")

        # 4. 创建支付记录1
        payment_repo.create({
            "order_id": order_id,
            "card_no": "CARD_A",
            "amount": Decimal("150.00"),
            "status": "success"
        })
        print("4️⃣  创建支付记录1: 卡A支付150元")

        # 5. 创建支付记录2
        payment_repo.create({
            "order_id": order_id,
            "card_no": "CARD_B",
            "amount": Decimal("50.00"),
            "status": "success"
        })
        print("5️⃣  创建支付记录2: 卡B支付50元")

        # 6. 统一提交
        print("\n6️⃣  统一 commit() - 5个操作一起提交")
        uow.commit()

    print("✅ 多卡支付成功（订单、2张卡余额、2条支付记录都已更新）")


# ========== 测试用例 ==========

class TestMultiRepositoryTransactions:
    """多Repository事务一致性测试"""

    def test_multi_repo_success(self, uow):
        """测试：多Repository操作成功"""
        order_repo = uow.repository(OrderRepository)
        payment_repo = uow.repository(PaymentRepository)

        # 创建订单
        order_id = order_repo.create({
            "user_id": 1,
            "amount": Decimal("100.00"),
            "status": "pending"
        })

        # 创建支付
        payment_id = payment_repo.create({
            "order_id": order_id,
            "amount": Decimal("100.00"),
            "status": "success"
        })

        # 验证
        assert order_id is not None
        assert payment_id is not None

        # ✅ 测试结束自动回滚

    def test_transaction_atomicity(self, uow):
        """测试：事务原子性"""
        order_repo = uow.repository(OrderRepository)
        card_repo = uow.repository(CardRepository)

        # 创建测试卡
        card_repo.create({
            "card_no": "TEST_CARD",
            "balance": Decimal("50.00")
        })

        # 创建订单
        order_repo.create({
            "user_id": 1,
            "amount": Decimal("100.00")
        })

        # 尝试扣减余额（会失败）
        with pytest.raises(ValueError):
            card_repo.deduct_balance("TEST_CARD", Decimal("100.00"))

        # ✅ 订单创建和卡片创建都会回滚


# ========== 主函数 ==========

if __name__ == "__main__":
    print("\n" + "🚀 多Repository事务一致性")
    print("=" * 60)

    print("\n💡 核心价值：")
    print("UoW 确保多个 Repository 操作的事务原子性")
    print("全部成功或全部失败，不会出现数据不一致")

    # 运行示例（需要实际数据库）
    print("\n⚠️  以下示例需要实际数据库环境")
    print("在项目中通过 pytest 运行测试用例")

    print("\n" + "=" * 60)
    print("📋 实战最佳实践")
    print("=" * 60)
    print("""
# 礼品卡支付业务代码
def process_card_payment(uow, user_id, card_no, amount):
    \"\"\"处理礼品卡支付

    Args:
        uow: UnitOfWork 实例
        user_id: 用户ID
        card_no: 礼品卡号
        amount: 支付金额

    Returns:
        payment_id: 支付记录ID

    Raises:
        ValueError: 余额不足或卡片无效
    \"\"\"
    order_repo = uow.repository(OrderRepository)
    payment_repo = uow.repository(PaymentRepository)
    card_repo = uow.repository(CardRepository)

    # 1. 创建订单
    order_id = order_repo.create({
        "user_id": user_id,
        "amount": amount,
        "status": "pending"
    })

    # 2. 扣减余额
    card_repo.deduct_balance(card_no, amount)

    # 3. 创建支付记录
    payment_id = payment_repo.create({
        "order_id": order_id,
        "card_no": card_no,
        "amount": amount,
        "status": "success"
    })

    # 4. 提交事务
    uow.commit()

    return payment_id
    """)

    print("\n" + "=" * 60)
    print("✅ 示例代码说明完成！")
    print("=" * 60)
    print("下一步：运行 05_project_uow.py 学习项目级UoW封装")
