"""预置工厂单元测试

测试预置数据工厂的功能

v3.10.0 - P2.2 测试数据工具增强
"""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from df_test_framework.testing.factories import (
    AddressFactory,
    ApiResponseFactory,
    CardFactory,
    OrderFactory,
    PaginationFactory,
    PaymentFactory,
    ProductFactory,
    Sequence,
    UserFactory,
)


class TestUserFactory:
    """UserFactory测试"""

    def setup_method(self):
        """每个测试前重置序列"""
        Sequence.reset()

    def test_build_single_user(self):
        """测试构建单个用户"""
        user = UserFactory.build()

        assert user["id"] == 1
        assert user["username"] == "user_1"
        assert user["email"] == "user_1@example.com"
        assert user["status"] == "active"
        assert user["role"] == "user"
        assert user["is_verified"] is True
        assert isinstance(user["created_at"], datetime)

    def test_build_batch_users(self):
        """测试批量构建用户"""
        users = UserFactory.build_batch(5)

        assert len(users) == 5
        assert users[0]["id"] == 1
        assert users[4]["id"] == 5
        assert users[0]["username"] == "user_1"
        assert users[4]["username"] == "user_5"

    def test_build_with_override(self):
        """测试覆盖默认值"""
        user = UserFactory.build(username="admin", role="admin", is_superuser=True)

        assert user["username"] == "admin"
        assert user["role"] == "admin"
        assert user["is_superuser"] is True

    def test_user_id_is_uuid(self):
        """测试user_id是有效UUID"""
        user = UserFactory.build()

        # 验证是有效的UUID字符串
        UUID(user["user_id"])

    def test_email_derived_from_username(self):
        """测试邮箱从用户名派生"""
        user = UserFactory.build(username="alice")

        assert user["email"] == "alice@example.com"


class TestOrderFactory:
    """OrderFactory测试"""

    def setup_method(self):
        Sequence.reset()

    def test_build_single_order(self):
        """测试构建单个订单"""
        order = OrderFactory.build()

        assert order["id"] == 1
        assert order["order_no"].startswith("ORD-")
        assert order["status"] == "pending"
        assert isinstance(order["total_amount"], Decimal)
        assert order["paid_at"] is None

    def test_order_amount_calculation(self):
        """测试订单金额计算"""
        order = OrderFactory.build()

        # 实付金额 = 总金额 - 折扣金额
        expected = order["total_amount"] - order["discount_amount"]
        assert order["payment_amount"] == expected

    def test_build_paid_order(self):
        """测试构建已支付订单"""
        paid_at = datetime.now()
        order = OrderFactory.build(status="paid", paid_at=paid_at)

        assert order["status"] == "paid"
        assert order["paid_at"] == paid_at


class TestProductFactory:
    """ProductFactory测试"""

    def setup_method(self):
        Sequence.reset()

    def test_build_single_product(self):
        """测试构建单个商品"""
        product = ProductFactory.build()

        assert product["id"] == 1
        assert product["sku"].startswith("SKU-")
        assert product["status"] == "on_sale"
        assert isinstance(product["price"], Decimal)
        assert isinstance(product["images"], list)

    def test_sale_price_calculation(self):
        """测试售价计算（9折）"""
        product = ProductFactory.build()

        expected = product["price"] * Decimal("0.9")
        assert product["sale_price"] == expected

    def test_product_images_generated(self):
        """测试商品图片生成"""
        product = ProductFactory.build()

        assert len(product["images"]) == 3
        assert all(product["sku"] in img for img in product["images"])


class TestAddressFactory:
    """AddressFactory测试"""

    def setup_method(self):
        Sequence.reset()

    def test_build_single_address(self):
        """测试构建单个地址"""
        addr = AddressFactory.build()

        assert addr["id"] == 1
        assert addr["is_default"] is False
        assert "name" in addr
        assert "phone" in addr

    def test_build_default_address(self):
        """测试构建默认地址"""
        addr = AddressFactory.build(is_default=True)

        assert addr["is_default"] is True


class TestPaymentFactory:
    """PaymentFactory测试"""

    def setup_method(self):
        Sequence.reset()

    def test_build_single_payment(self):
        """测试构建单个支付记录"""
        payment = PaymentFactory.build()

        assert payment["id"] == 1
        assert payment["payment_no"].startswith("PAY-")
        assert payment["status"] == "pending"
        assert isinstance(payment["amount"], Decimal)

    def test_build_success_payment(self):
        """测试构建成功支付"""
        paid_at = datetime.now()
        payment = PaymentFactory.build(status="success", paid_at=paid_at)

        assert payment["status"] == "success"
        assert payment["paid_at"] == paid_at


class TestCardFactory:
    """CardFactory测试"""

    def setup_method(self):
        Sequence.reset()

    def test_build_single_card(self):
        """测试构建单张卡"""
        card = CardFactory.build()

        assert card["id"] == 1
        assert card["card_no"].startswith("CARD")
        assert card["card_type"] == "gift_card"
        assert card["status"] == "inactive"
        assert card["balance"] == card["face_value"]

    def test_build_activated_card(self):
        """测试构建已激活卡"""
        activated_at = datetime.now()
        card = CardFactory.build(status="active", activated_at=activated_at)

        assert card["status"] == "active"
        assert card["activated_at"] == activated_at


class TestApiResponseFactory:
    """ApiResponseFactory测试"""

    def test_build_success_response(self):
        """测试构建成功响应"""
        resp = ApiResponseFactory.build()

        assert resp["code"] == 0
        assert resp["message"] == "success"
        assert isinstance(resp["timestamp"], int)
        assert "request_id" in resp

    def test_build_error_response(self):
        """测试构建错误响应"""
        resp = ApiResponseFactory.build(code=400, message="参数错误", data=None)

        assert resp["code"] == 400
        assert resp["message"] == "参数错误"
        assert resp["data"] is None


class TestPaginationFactory:
    """PaginationFactory测试"""

    def test_build_empty_page(self):
        """测试构建空分页"""
        page = PaginationFactory.build()

        assert page["items"] == []
        assert page["total"] == 0
        assert page["page"] == 1
        assert page["has_next"] is False
        assert page["has_prev"] is False

    def test_build_with_data(self):
        """测试构建有数据分页"""
        page = PaginationFactory.build(total=100, page=2, page_size=10)

        assert page["total"] == 100
        assert page["page"] == 2
        assert page["page_size"] == 10
        assert page["total_pages"] == 10
        assert page["has_next"] is True
        assert page["has_prev"] is True

    def test_pagination_edge_cases(self):
        """测试分页边界情况"""
        # 第一页
        first_page = PaginationFactory.build(total=50, page=1, page_size=10)
        assert first_page["has_prev"] is False
        assert first_page["has_next"] is True

        # 最后一页
        last_page = PaginationFactory.build(total=50, page=5, page_size=10)
        assert last_page["has_prev"] is True
        assert last_page["has_next"] is False
