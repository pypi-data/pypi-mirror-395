"""测试 data_generator.py - 测试数据生成器

测试覆盖:
- DataGenerator类的所有方法
- 基础数据生成
- 个人信息生成
- 日期时间生成
- 业务数据生成
- 金融数据生成
- 网络数据生成
"""

import string
from datetime import datetime, timedelta
from decimal import Decimal

import pytest

from df_test_framework.utils.data_generator import DataGenerator


class TestDataGeneratorBasic:
    """测试基础数据生成"""

    @pytest.fixture
    def generator(self):
        """数据生成器实例"""
        return DataGenerator()

    def test_init_with_default_locale(self):
        """测试使用默认locale初始化"""
        gen = DataGenerator()
        assert gen.faker is not None

    def test_init_with_custom_locale(self):
        """测试使用自定义locale初始化"""
        gen = DataGenerator(locale="en_US")
        assert gen.faker is not None

    def test_random_string_default(self, generator):
        """测试生成默认长度的随机字符串"""
        result = generator.random_string()
        assert len(result) == 10
        assert all(c in string.ascii_letters + string.digits for c in result)

    def test_random_string_custom_length(self, generator):
        """测试生成自定义长度的随机字符串"""
        result = generator.random_string(length=20)
        assert len(result) == 20

    def test_random_string_custom_chars(self, generator):
        """测试使用自定义字符集"""
        result = generator.random_string(length=10, chars="ABC123")
        assert len(result) == 10
        assert all(c in "ABC123" for c in result)

    def test_random_int_default(self, generator):
        """测试生成默认范围的随机整数"""
        result = generator.random_int()
        assert isinstance(result, int)
        assert 0 <= result <= 100

    def test_random_int_custom_range(self, generator):
        """测试生成自定义范围的随机整数"""
        result = generator.random_int(min_value=50, max_value=100)
        assert 50 <= result <= 100

    def test_random_float_default(self, generator):
        """测试生成默认范围的随机浮点数"""
        result = generator.random_float()
        assert isinstance(result, float)
        assert 0.0 <= result <= 100.0
        # 验证小数位数
        assert len(str(result).split(".")[-1]) <= 2

    def test_random_float_custom_range(self, generator):
        """测试生成自定义范围的随机浮点数"""
        result = generator.random_float(min_value=10.0, max_value=20.0, decimals=3)
        assert 10.0 <= result <= 20.0

    def test_random_decimal(self, generator):
        """测试生成随机Decimal"""
        result = generator.random_decimal()
        assert isinstance(result, Decimal)
        assert Decimal("0") <= result <= Decimal("100")

    def test_random_bool(self, generator):
        """测试生成随机布尔值"""
        result = generator.random_bool()
        assert isinstance(result, bool)

    def test_random_choice(self, generator):
        """测试从列表中随机选择"""
        choices = ["apple", "banana", "orange"]
        result = generator.random_choice(choices)
        assert result in choices


class TestDataGeneratorPersonal:
    """测试个人信息生成"""

    @pytest.fixture
    def generator(self):
        """数据生成器实例"""
        return DataGenerator()

    def test_name(self, generator):
        """测试生成姓名"""
        result = generator.name()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_email(self, generator):
        """测试生成邮箱"""
        result = generator.email()
        assert isinstance(result, str)
        assert "@" in result

    def test_phone(self, generator):
        """测试生成手机号"""
        result = generator.phone()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_address(self, generator):
        """测试生成地址"""
        result = generator.address()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_company(self, generator):
        """测试生成公司名"""
        result = generator.company()
        assert isinstance(result, str)
        assert len(result) > 0


class TestDataGeneratorDateTime:
    """测试日期时间生成"""

    @pytest.fixture
    def generator(self):
        """数据生成器实例"""
        return DataGenerator()

    def test_date_default(self, generator):
        """测试生成默认范围的日期"""
        result = generator.date()
        assert isinstance(result, datetime)
        # 验证日期在过去30天到今天之间
        assert result <= datetime.now()

    def test_date_custom_range(self, generator):
        """测试生成自定义范围的日期"""
        result = generator.date(start_date="-7d", end_date="now")
        assert isinstance(result, datetime)

    def test_future_date_default(self, generator):
        """测试生成未来日期"""
        result = generator.future_date()
        assert isinstance(result, datetime)
        assert result > datetime.now()

    def test_future_date_custom_days(self, generator):
        """测试生成自定义天数的未来日期"""
        result = generator.future_date(days=60)
        assert isinstance(result, datetime)
        assert result > datetime.now()
        assert result <= datetime.now() + timedelta(days=60)

    def test_past_date_default(self, generator):
        """测试生成过去日期"""
        result = generator.past_date()
        assert isinstance(result, datetime)
        assert result < datetime.now()

    def test_past_date_custom_days(self, generator):
        """测试生成自定义天数的过去日期"""
        result = generator.past_date(days=60)
        assert isinstance(result, datetime)
        assert result < datetime.now()


class TestDataGeneratorBusiness:
    """测试业务数据生成"""

    @pytest.fixture
    def generator(self):
        """数据生成器实例"""
        return DataGenerator()

    def test_test_id_classmethod(self):
        """测试 test_id 类方法（无需实例化）"""
        result = DataGenerator.test_id("TEST_ORD")
        assert result.startswith("TEST_ORD")
        # 验证格式: prefix + timestamp(14位) + random(6位)
        assert len(result) == len("TEST_ORD") + 14 + 6

    def test_test_id_with_different_prefixes(self):
        """测试不同前缀的 test_id"""
        order_no = DataGenerator.test_id("TEST_ORD")
        user_id = DataGenerator.test_id("TEST_USER")
        payment_no = DataGenerator.test_id("TEST_PAY")

        assert order_no.startswith("TEST_ORD")
        assert user_id.startswith("TEST_USER")
        assert payment_no.startswith("TEST_PAY")

    def test_test_id_uniqueness(self):
        """测试 test_id 生成的唯一性"""
        ids = [DataGenerator.test_id("TEST") for _ in range(50)]
        assert len(ids) == len(set(ids))

    def test_card_number_default(self, generator):
        """测试生成默认长度的卡号"""
        result = generator.card_number()
        assert isinstance(result, str)
        assert len(result) == 16
        assert result.isdigit()

    def test_card_number_custom_length(self, generator):
        """测试生成自定义长度的卡号"""
        result = generator.card_number(length=20)
        assert len(result) == 20
        assert result.isdigit()

    def test_order_id_default_prefix(self, generator):
        """测试生成默认前缀的订单号"""
        result = generator.order_id()
        assert result.startswith("ORD")
        assert len(result) == 23  # ORD + 14位时间戳 + 6位随机数

    def test_order_id_custom_prefix(self, generator):
        """测试生成自定义前缀的订单号"""
        result = generator.order_id(prefix="TEST")
        assert result.startswith("TEST")

    def test_uuid(self, generator):
        """测试生成UUID"""
        result = generator.uuid()
        assert isinstance(result, str)
        # UUID格式验证
        parts = result.split("-")
        assert len(parts) == 5


class TestDataGeneratorFinancial:
    """测试金融数据生成"""

    @pytest.fixture
    def generator(self):
        """数据生成器实例"""
        return DataGenerator()

    def test_amount_default(self, generator):
        """测试生成默认范围的金额"""
        result = generator.amount()
        assert isinstance(result, Decimal)
        assert Decimal("1.0") <= result <= Decimal("1000.0")

    def test_amount_custom_range(self, generator):
        """测试生成自定义范围的金额"""
        result = generator.amount(min_value=100.0, max_value=500.0)
        assert Decimal("100.0") <= result <= Decimal("500.0")

    def test_currency_code(self, generator):
        """测试生成货币代码"""
        result = generator.currency_code()
        assert isinstance(result, str)
        assert len(result) == 3


class TestDataGeneratorNetwork:
    """测试网络数据生成"""

    @pytest.fixture
    def generator(self):
        """数据生成器实例"""
        return DataGenerator()

    def test_url(self, generator):
        """测试生成URL"""
        result = generator.url()
        assert isinstance(result, str)
        assert result.startswith("http")

    def test_ipv4(self, generator):
        """测试生成IPv4地址"""
        result = generator.ipv4()
        assert isinstance(result, str)
        # 验证IPv4格式
        parts = result.split(".")
        assert len(parts) == 4
        for part in parts:
            assert 0 <= int(part) <= 255

    def test_user_agent(self, generator):
        """测试生成User-Agent"""
        result = generator.user_agent()
        assert isinstance(result, str)
        assert len(result) > 0


__all__ = [
    "TestDataGeneratorBasic",
    "TestDataGeneratorPersonal",
    "TestDataGeneratorDateTime",
    "TestDataGeneratorBusiness",
    "TestDataGeneratorFinancial",
    "TestDataGeneratorNetwork",
]
