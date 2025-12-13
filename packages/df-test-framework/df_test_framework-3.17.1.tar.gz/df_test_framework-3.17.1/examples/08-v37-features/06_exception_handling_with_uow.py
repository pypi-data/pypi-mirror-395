"""
异常场景测试与 UoW

展示如何使用 UoW 测试异常场景（余额不足、卡片冻结等）

本示例演示：
1. 使用 Repository 直接修改数据库状态
2. 模拟异常场景（冻结卡片、清空余额）
3. 验证业务错误处理
4. 测试结束自动回滚，无污染

学习要点：
- ✅ Repository 可直接修改数据库状态
- ✅ 无需通过 API 模拟异常场景
- ✅ 测试更加灵活和可控
- ✅ 异常测试也支持自动回滚

本示例基于真实项目：gift-card-test
参考文件：tests/api/2_h5/test_payment_exceptions.py
"""

from decimal import Decimal

import pytest
from sqlalchemy.orm import Session

from df_test_framework import BaseRepository
from df_test_framework.clients.http.rest.httpx.base_api import BusinessError

# ========== Repository 定义 ==========

class CardRepository(BaseRepository):
    """礼品卡仓库"""

    def __init__(self, session: Session):
        super().__init__(session, table_name="gift_cards")

    def find_by_card_no(self, card_no: str) -> dict | None:
        """根据卡号查找"""
        return self.find_one({"card_no": card_no})

    def freeze_card(self, card_no: str) -> int:
        """冻结卡片"""
        return self.update(
            conditions={"card_no": card_no},
            data={"status": 2}  # 2=已冻结
        )

    def set_consumed(self, card_no: str) -> int:
        """设置为已核销"""
        return self.update(
            conditions={"card_no": card_no},
            data={"status": 3, "balance": Decimal("0")}  # 3=已核销
        )

    def set_balance(self, card_no: str, balance: Decimal) -> int:
        """设置余额"""
        return self.update(
            conditions={"card_no": card_no},
            data={"balance": balance}
        )


# ========== 测试用例：异常场景 ==========

class TestPaymentExceptions:
    """支付异常场景测试套件

    v3.7.0 特性：
    - ✅ 使用 Repository 直接修改卡片状态
    - ✅ 无需通过 API 模拟异常状态
    - ✅ 测试结束自动回滚
    """

    def test_payment_insufficient_balance(self, h5_card_api, master_card_api, uow, settings):
        """测试：余额不足场景

        步骤：
        1. 创建面值100元的测试卡片
        2. 使用 Repository 将余额改为10元
        3. 尝试支付100元
        4. 验证支付失败并返回余额不足错误
        """
        import time
        timestamp = int(time.time() * 1000)

        test_user_id = f"TEST_INSUF_{settings.business.test_user_id}"
        order_no = f"ORD_INSUF_{timestamp}"

        # 步骤1: 创建测试卡片（默认面值100元）
        from gift_card_test.models.requests.master_card import MasterCardCreateRequest

        create_request = MasterCardCreateRequest(
            customer_order_no=order_no,
            user_id=test_user_id,
            template_id=settings.business.test_template_id,
            quantity=1
        )
        create_response = master_card_api.create_cards(create_request)
        card_no = create_response.data.sample_card_nos[0]

        # 步骤2: 使用 Repository 修改余额（模拟余额不足）
        uow.cards.set_balance(card_no, Decimal("10.00"))

        # 验证余额已修改
        card = uow.cards.find_by_card_no(card_no)
        assert Decimal(str(card["balance"])) == Decimal("10.00")

        # 步骤3: 尝试支付100元（余额不足）
        from gift_card_test.models.requests.h5_card import H5PaymentRequest

        payment_request = H5PaymentRequest(
            user_id=test_user_id,
            customer_order_no=f"PAY_{timestamp}",
            total_amount=Decimal("100.00"),
            card_list=card_no
        )

        # 步骤4: 验证支付失败
        with pytest.raises(BusinessError) as exc_info:
            h5_card_api.pay(payment_request)

        error = exc_info.value
        assert error.code != 200, "余额不足应该返回错误码"

        # ✅ 测试结束自动回滚（卡片状态恢复）

    def test_payment_frozen_card(self, h5_card_api, master_card_api, uow, settings):
        """测试：卡片已冻结场景

        步骤：
        1. 创建测试卡片
        2. 使用 Repository 将卡片状态改为冻结
        3. 尝试使用冻结卡片支付
        4. 验证支付失败
        """
        import time
        timestamp = int(time.time() * 1000)

        test_user_id = f"TEST_FROZEN_{settings.business.test_user_id}"
        order_no = f"ORD_FROZEN_{timestamp}"

        # 步骤1: 创建测试卡片
        from gift_card_test.models.requests.master_card import MasterCardCreateRequest

        create_request = MasterCardCreateRequest(
            customer_order_no=order_no,
            user_id=test_user_id,
            template_id=settings.business.test_template_id,
            quantity=1
        )
        create_response = master_card_api.create_cards(create_request)
        card_no = create_response.data.sample_card_nos[0]

        # 步骤2: 使用 Repository 冻结卡片
        uow.cards.freeze_card(card_no)

        # 验证卡片已冻结
        card = uow.cards.find_by_card_no(card_no)
        assert card["status"] == 2, "卡片应该已冻结"

        # 步骤3: 尝试使用冻结卡片支付
        from gift_card_test.models.requests.h5_card import H5PaymentRequest

        payment_request = H5PaymentRequest(
            user_id=test_user_id,
            customer_order_no=f"PAY_{timestamp}",
            total_amount=Decimal("50.00"),
            card_list=card_no
        )

        # 步骤4: 验证支付失败
        with pytest.raises(BusinessError) as exc_info:
            h5_card_api.pay(payment_request)

        error = exc_info.value
        assert error.code != 200, "冻结卡片不应该允许支付"

        # ✅ 测试结束自动回滚

    def test_payment_consumed_card(self, h5_card_api, master_card_api, uow, settings):
        """测试：卡片已核销场景

        步骤：
        1. 创建测试卡片
        2. 使用 Repository 将卡片设置为已核销
        3. 尝试使用已核销卡片支付
        4. 验证支付失败
        """
        import time
        timestamp = int(time.time() * 1000)

        test_user_id = f"TEST_CONSUMED_{settings.business.test_user_id}"
        order_no = f"ORD_CONSUMED_{timestamp}"

        # 步骤1: 创建测试卡片
        from gift_card_test.models.requests.master_card import MasterCardCreateRequest

        create_request = MasterCardCreateRequest(
            customer_order_no=order_no,
            user_id=test_user_id,
            template_id=settings.business.test_template_id,
            quantity=1
        )
        create_response = master_card_api.create_cards(create_request)
        card_no = create_response.data.sample_card_nos[0]

        # 步骤2: 使用 Repository 设置为已核销
        uow.cards.set_consumed(card_no)

        # 验证卡片状态
        card = uow.cards.find_by_card_no(card_no)
        assert card["status"] == 3, "卡片应该已核销"
        assert Decimal(str(card["balance"])) == 0, "已核销卡片余额应为0"

        # 步骤3: 尝试使用已核销卡片支付
        from gift_card_test.models.requests.h5_card import H5PaymentRequest

        payment_request = H5PaymentRequest(
            user_id=test_user_id,
            customer_order_no=f"PAY_{timestamp}",
            total_amount=Decimal("50.00"),
            card_list=card_no
        )

        # 步骤4: 验证支付失败
        with pytest.raises(BusinessError) as exc_info:
            h5_card_api.pay(payment_request)

        error = exc_info.value
        assert error.code != 200, "已核销卡片不应该允许支付"

        # ✅ 测试结束自动回滚

    def test_payment_card_not_found(self, h5_card_api, settings):
        """测试：卡片不存在场景

        这个场景不需要 Repository，直接使用不存在的卡号即可
        """
        import time
        timestamp = int(time.time() * 1000)

        test_user_id = f"TEST_NOTFOUND_{settings.business.test_user_id}"
        fake_card_no = f"FAKE_CARD_{timestamp}"

        from gift_card_test.models.requests.h5_card import H5PaymentRequest

        payment_request = H5PaymentRequest(
            user_id=test_user_id,
            customer_order_no=f"PAY_{timestamp}",
            total_amount=Decimal("50.00"),
            card_list=fake_card_no
        )

        # 验证支付失败
        with pytest.raises(BusinessError) as exc_info:
            h5_card_api.pay(payment_request)

        error = exc_info.value
        assert error.code != 200, "不存在的卡片不应该允许支付"


# ========== 对比传统测试方式 ==========

class TestTraditionalExceptionTesting:
    """传统异常测试方式（不使用 Repository）"""

    def test_frozen_card_traditional_way(self, h5_card_api, admin_card_api, master_card_api, settings):
        """❌ 传统方式：需要调用管理端 API 冻结卡片

        问题：
        1. 需要额外的 admin_card_api 依赖
        2. 需要管理员权限
        3. 可能没有冻结卡片的 API
        4. 测试代码更复杂
        """
        import time
        timestamp = int(time.time() * 1000)

        # 1. 创建卡片
        create_test_card(master_card_api, settings, timestamp)

        # 2. ❌ 需要调用管理端 API 冻结卡片
        # admin_card_api.freeze_card(card_no)  # 可能不存在这个 API

        # 3. 尝试支付
        # ...

        # 问题：如果没有冻结 API，就无法测试这个场景！


# ========== 最佳实践示例 ==========

class TestExceptionBestPractices:
    """异常场景测试最佳实践"""

    def test_exception_with_clear_steps(self, h5_card_api, master_card_api, uow, settings):
        """最佳实践1：清晰的测试步骤

        使用步骤注释，让测试意图清晰
        """
        import time
        timestamp = int(time.time() * 1000)

        test_user_id = f"TEST_BEST_{settings.business.test_user_id}"
        order_no = f"ORD_BEST_{timestamp}"

        # ========== 准备阶段 ==========
        from gift_card_test.models.requests.master_card import MasterCardCreateRequest

        # 步骤1: 创建测试卡片
        create_request = MasterCardCreateRequest(
            customer_order_no=order_no,
            user_id=test_user_id,
            template_id=settings.business.test_template_id,
            quantity=1
        )
        create_response = master_card_api.create_cards(create_request)
        card_no = create_response.data.sample_card_nos[0]

        # 步骤2: 模拟异常状态（余额不足）
        uow.cards.set_balance(card_no, Decimal("5.00"))

        # ========== 执行阶段 ==========
        from gift_card_test.models.requests.h5_card import H5PaymentRequest

        # 步骤3: 尝试支付
        payment_request = H5PaymentRequest(
            user_id=test_user_id,
            customer_order_no=f"PAY_{timestamp}",
            total_amount=Decimal("100.00"),
            card_list=card_no
        )

        # ========== 验证阶段 ==========
        # 步骤4: 验证业务错误
        with pytest.raises(BusinessError) as exc_info:
            h5_card_api.pay(payment_request)

        # 步骤5: 验证错误详情
        error = exc_info.value
        assert error.code != 200
        assert "余额" in error.message or "insufficient" in error.message.lower()

    @pytest.mark.parametrize("status,status_name", [
        (2, "冻结"),
        (3, "已核销"),
    ])
    def test_invalid_card_status_parametrized(
        self,
        h5_card_api,
        master_card_api,
        uow,
        settings,
        status,
        status_name
    ):
        """最佳实践2：参数化测试多种异常状态

        使用 pytest.mark.parametrize 测试多种状态
        """
        import time
        timestamp = int(time.time() * 1000)

        test_user_id = f"TEST_STATUS_{status}_{settings.business.test_user_id}"
        order_no = f"ORD_STATUS_{status}_{timestamp}"

        # 创建卡片
        from gift_card_test.models.requests.master_card import MasterCardCreateRequest

        create_request = MasterCardCreateRequest(
            customer_order_no=order_no,
            user_id=test_user_id,
            template_id=settings.business.test_template_id,
            quantity=1
        )
        create_response = master_card_api.create_cards(create_request)
        card_no = create_response.data.sample_card_nos[0]

        # 设置异常状态
        uow.cards.update(
            conditions={"card_no": card_no},
            data={"status": status}
        )

        # 验证支付失败
        from gift_card_test.models.requests.h5_card import H5PaymentRequest

        payment_request = H5PaymentRequest(
            user_id=test_user_id,
            customer_order_no=f"PAY_{timestamp}",
            total_amount=Decimal("50.00"),
            card_list=card_no
        )

        with pytest.raises(BusinessError):
            h5_card_api.pay(payment_request)


# ========== 说明文档 ==========

def print_documentation():
    """打印使用说明"""
    print("\n" + "=" * 60)
    print("🎯 异常场景测试最佳实践")
    print("=" * 60)

    print("\n✅ v3.7 优势：Repository 直接修改状态")
    print("-" * 60)
    print("""
# ❌ v3.6: 需要通过 API 模拟异常状态
def test_frozen_card_v36(admin_api, h5_api):
    card_no = create_card()
    admin_api.freeze_card(card_no)  # 需要管理端 API
    # 如果没有这个 API，就无法测试！

# ✅ v3.7: 直接修改数据库状态
def test_frozen_card_v37(uow, h5_api):
    card_no = create_card()
    uow.cards.freeze_card(card_no)  # ✅ 直接修改状态
    # 灵活、简单、无依赖
    """)

    print("\n💡 适用场景")
    print("-" * 60)
    scenarios = [
        ("余额不足", "set_balance(card_no, low_amount)"),
        ("卡片冻结", "freeze_card(card_no)"),
        ("卡片已核销", "set_consumed(card_no)"),
        ("卡片过期", "update(conditions={...}, data={'expired_at': past_date})"),
        ("达到使用次数上限", "update(conditions={...}, data={'used_count': max_count})"),
    ]

    for scenario, code in scenarios:
        print(f"  • {scenario:<20} - {code}")

    print("\n⚠️  注意事项")
    print("-" * 60)
    print("  1. 只修改测试需要的字段，避免副作用")
    print("  2. 使用业务语义方法（freeze_card）而非通用方法（update）")
    print("  3. 验证状态修改成功后再执行业务操作")
    print("  4. 测试结束依赖 uow 自动回滚")


if __name__ == "__main__":
    print("\n" + "🚀 异常场景测试与 UoW")
    print("=" * 60)
    print("本文件是完整的 pytest 测试文件")
    print("展示如何使用 v3.7 UoW 测试异常场景")

    print_documentation()

    print("\n" + "=" * 60)
    print("🎯 核心价值")
    print("=" * 60)
    print("""
v3.7 使异常场景测试更加：

1. ✅ 灵活
   - 可以模拟任意异常状态
   - 不依赖管理端 API

2. ✅ 简单
   - 直接修改数据库状态
   - 代码更少更清晰

3. ✅ 可靠
   - 测试结束自动回滚
   - 不会污染数据库

4. ✅ 全面
   - 可以覆盖所有边界条件
   - 不受 API 限制
    """)

    print("\n" + "=" * 60)
    print("✅ 所有 v3.7 示例代码完成！")
    print("=" * 60)
    print("现在可以运行：pytest examples/08-v37-features/ -v")
