"""测试数据生成器"""

import random
import string
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any

from faker import Faker


class DataGenerator:
    """
    测试数据生成器

    提供各种类型的测试数据生成功能。

    实例方法用法:
        gen = DataGenerator()
        order_no = gen.order_id(prefix="TEST_ORD")

    类方法用法（无需实例化）:
        order_no = DataGenerator.test_id("TEST_ORD")
    """

    def __init__(self, locale: str = "zh_CN"):
        """
        初始化数据生成器

        Args:
            locale: 本地化设置 (zh_CN, en_US等)
        """
        self.faker = Faker(locale)

    # ========== 类方法（无需实例化）==========

    @classmethod
    def test_id(cls, prefix: str = "TEST") -> str:
        """生成测试数据标识符（无需实例化）

        快捷方法，用于生成带前缀的唯一测试数据标识符。

        Args:
            prefix: 前缀字符串，如 "TEST_ORD", "TEST_USER"

        Returns:
            格式: "{prefix}{timestamp}{random}"
            示例: "TEST_ORD20251128123456789012"

        Usage:
            order_no = DataGenerator.test_id("TEST_ORD")
            user_id = DataGenerator.test_id("TEST_USER")
            payment_no = DataGenerator.test_id("TEST_PAY")
        """
        return cls().order_id(prefix=prefix)

    # ========== 基础数据 ==========

    def random_string(
        self,
        length: int = 10,
        chars: str = string.ascii_letters + string.digits,
    ) -> str:
        """生成随机字符串"""
        return "".join(random.choice(chars) for _ in range(length))

    def random_int(self, min_value: int = 0, max_value: int = 100) -> int:
        """生成随机整数"""
        return random.randint(min_value, max_value)

    def random_float(
        self,
        min_value: float = 0.0,
        max_value: float = 100.0,
        decimals: int = 2,
    ) -> float:
        """生成随机浮点数"""
        value = random.uniform(min_value, max_value)
        return round(value, decimals)

    def random_decimal(
        self,
        min_value: float = 0.0,
        max_value: float = 100.0,
        decimals: int = 2,
    ) -> Decimal:
        """生成随机Decimal"""
        value = self.random_float(min_value, max_value, decimals)
        return Decimal(str(value))

    def random_bool(self) -> bool:
        """生成随机布尔值"""
        return random.choice([True, False])

    def random_choice(self, choices: list[Any]) -> Any:
        """从列表中随机选择"""
        return random.choice(choices)

    # ========== 个人信息 ==========

    def name(self) -> str:
        """生成随机姓名"""
        return self.faker.name()

    def email(self) -> str:
        """生成随机邮箱"""
        return self.faker.email()

    def phone(self) -> str:
        """生成随机手机号"""
        return self.faker.phone_number()

    def address(self) -> str:
        """生成随机地址"""
        return self.faker.address()

    def company(self) -> str:
        """生成随机公司名"""
        return self.faker.company()

    # ========== 日期时间 ==========

    def date(
        self,
        start_date: str = "-30d",
        end_date: str = "now",
    ) -> datetime:
        """
        生成随机日期

        Args:
            start_date: 开始日期 (支持相对日期如"-30d")
            end_date: 结束日期 (支持相对日期如"now")

        Returns:
            随机日期时间
        """
        return self.faker.date_time_between(start_date=start_date, end_date=end_date)

    def datetime_str(self, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
        """生成日期时间字符串

        Args:
            fmt: 日期格式，默认 "%Y-%m-%d %H:%M:%S"

        Returns:
            格式化的日期时间字符串

        Example:
            dt = gen.datetime_str()  # "2025-11-28 12:34:56"
            dt = gen.datetime_str("%Y%m%d")  # "20251128"
        """
        return datetime.now().strftime(fmt)

    def future_date(self, days: int = 30) -> datetime:
        """生成未来日期

        Args:
            days: 未来多少天内，默认 30

        Returns:
            未来的随机日期

        Example:
            future = gen.future_date(7)  # 未来7天内的随机日期
        """
        return datetime.now() + timedelta(days=random.randint(1, days))

    def past_date(self, days: int = 30) -> datetime:
        """生成过去日期

        Args:
            days: 过去多少天内，默认 30

        Returns:
            过去的随机日期

        Example:
            past = gen.past_date(7)  # 过去7天内的随机日期
        """
        return datetime.now() - timedelta(days=random.randint(1, days))

    def timestamp(self, milliseconds: bool = False) -> int:
        """生成当前时间戳

        Args:
            milliseconds: 是否返回毫秒时间戳，默认 False（返回秒）

        Returns:
            时间戳（秒或毫秒）

        Example:
            ts = gen.timestamp()  # 1732780800（秒）
            ts = gen.timestamp(milliseconds=True)  # 1732780800123（毫秒）
        """
        if milliseconds:
            return int(datetime.now().timestamp() * 1000)
        return int(datetime.now().timestamp())

    # ========== 业务数据 ==========

    def card_number(self, length: int = 16) -> str:
        """生成卡号"""
        return "".join(random.choice(string.digits) for _ in range(length))

    def order_id(self, prefix: str = "ORD") -> str:
        """生成订单号

        Args:
            prefix: 订单号前缀，默认 "ORD"

        Returns:
            格式: "{prefix}{timestamp}{random}"
            示例: "ORD20251128123456789012"
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = self.random_string(6, string.digits)
        return f"{prefix}{timestamp}{random_suffix}"

    def order_no(self, prefix: str = "TEST_ORD") -> str:
        """生成订单号（别名）

        便捷方法，与 order_id() 功能相同，但使用更常见的方法名。

        Args:
            prefix: 订单号前缀，默认 "TEST_ORD"

        Returns:
            格式: "{prefix}_{timestamp}{random}"
            示例: "TEST_ORD_20251128123456789"

        Example:
            order_no = gen.order_no()  # TEST_ORD_20251128...
            order_no = gen.order_no("PAY")  # PAY_20251128...
        """
        timestamp = int(datetime.now().timestamp() * 1000)  # 毫秒时间戳
        return f"{prefix}_{timestamp}"

    def user_id(self, prefix: str = "TEST_USER") -> str:
        """生成用户ID

        Args:
            prefix: 用户ID前缀，默认 "TEST_USER"

        Returns:
            格式: "{prefix}_{timestamp}{random}"
            示例: "TEST_USER_1732780800123"

        Example:
            user_id = gen.user_id()  # TEST_USER_1732780800123
            user_id = gen.user_id("VIP")  # VIP_1732780800123
        """
        timestamp = int(datetime.now().timestamp() * 1000)
        return f"{prefix}_{timestamp}"

    def payment_no(self, prefix: str = "PAY") -> str:
        """生成支付订单号

        Args:
            prefix: 支付订单号前缀，默认 "PAY"

        Returns:
            格式: "{prefix}_{timestamp}"
            示例: "PAY_1732780800123"
        """
        timestamp = int(datetime.now().timestamp() * 1000)
        return f"{prefix}_{timestamp}"

    def transaction_id(self, prefix: str = "TXN") -> str:
        """生成交易ID

        Args:
            prefix: 交易ID前缀，默认 "TXN"

        Returns:
            格式: "{prefix}_{timestamp}{random}"
            示例: "TXN_1732780800123456"
        """
        timestamp = int(datetime.now().timestamp() * 1000)
        random_suffix = self.random_string(3, string.digits)
        return f"{prefix}_{timestamp}{random_suffix}"

    def uuid(self) -> str:
        """生成UUID"""
        return self.faker.uuid4()

    def chinese_phone(self) -> str:
        """生成中国手机号

        生成符合中国手机号格式的11位号码。

        Returns:
            11位手机号，格式: 1[3-9]xxxxxxxxx

        Example:
            phone = gen.chinese_phone()  # 13812345678
        """
        # 中国手机号前缀（主流运营商）
        prefixes = [
            "130",
            "131",
            "132",
            "133",
            "134",
            "135",
            "136",
            "137",
            "138",
            "139",  # 移动
            "145",
            "147",
            "148",
            "150",
            "151",
            "152",
            "157",
            "158",
            "159",  # 移动
            "165",
            "166",
            "167",
            "172",
            "178",
            "182",
            "183",
            "184",
            "187",
            "188",
            "198",  # 移动
            "130",
            "131",
            "132",
            "140",
            "145",
            "146",
            "155",
            "156",
            "166",
            "167",
            "171",  # 联通
            "175",
            "176",
            "185",
            "186",
            "196",  # 联通
            "133",
            "149",
            "153",
            "173",
            "174",
            "177",
            "180",
            "181",
            "189",
            "191",
            "193",
            "199",  # 电信
        ]
        prefix = random.choice(prefixes)
        suffix = "".join(random.choice(string.digits) for _ in range(8))
        return f"{prefix}{suffix}"

    # ========== 金融数据 ==========

    def amount(
        self,
        min_value: float = 1.0,
        max_value: float = 1000.0,
        decimals: int = 2,
    ) -> Decimal:
        """生成金额

        Args:
            min_value: 最小值，默认 1.0
            max_value: 最大值，默认 1000.0
            decimals: 小数位数，默认 2

        Returns:
            Decimal 类型的金额

        Example:
            amount = gen.amount()  # 1.00 ~ 1000.00
            amount = gen.amount(10, 100)  # 10.00 ~ 100.00
        """
        return self.random_decimal(min_value, max_value, decimals)

    def decimal(
        self,
        min_value: float = 0.0,
        max_value: float = 100.0,
        decimals: int = 2,
    ) -> Decimal:
        """生成 Decimal 数值（别名）

        便捷方法，与 random_decimal() 功能相同。

        Args:
            min_value: 最小值，默认 0.0
            max_value: 最大值，默认 100.0
            decimals: 小数位数，默认 2

        Returns:
            Decimal 类型的数值

        Example:
            price = gen.decimal(10, 100)  # Decimal('45.67')
            balance = gen.decimal(0, 1000)  # Decimal('567.89')
        """
        return self.random_decimal(min_value, max_value, decimals)

    def currency_code(self) -> str:
        """生成货币代码"""
        return self.faker.currency_code()

    # ========== 网络数据 ==========

    def url(self) -> str:
        """生成URL"""
        return self.faker.url()

    def ipv4(self) -> str:
        """生成IPv4地址"""
        return self.faker.ipv4()

    def user_agent(self) -> str:
        """生成User-Agent"""
        return self.faker.user_agent()


__all__ = ["DataGenerator"]
