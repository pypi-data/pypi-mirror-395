"""
测试Builder模式

验证BaseBuilder和DictBuilder的功能。
"""

from dataclasses import dataclass

import pytest

from df_test_framework.testing.data.builders import BaseBuilder, DictBuilder

# ========== 测试用的自定义Builder ==========


@dataclass
class User:
    """测试用的User模型"""

    user_id: str
    name: str
    age: int
    email: str = ""
    is_active: bool = True


class UserBuilder(BaseBuilder[User]):
    """自定义UserBuilder用于测试"""

    def __init__(self):
        self._user_id = "default_user"
        self._name = "Default Name"
        self._age = 18
        self._email = ""
        self._is_active = True

    def with_id(self, user_id: str) -> "UserBuilder":
        self._user_id = user_id
        return self

    def with_name(self, name: str) -> "UserBuilder":
        self._name = name
        return self

    def with_age(self, age: int) -> "UserBuilder":
        self._age = age
        return self

    def with_email(self, email: str) -> "UserBuilder":
        self._email = email
        return self

    def active(self) -> "UserBuilder":
        self._is_active = True
        return self

    def inactive(self) -> "UserBuilder":
        self._is_active = False
        return self

    def build(self) -> User:
        return User(
            user_id=self._user_id,
            name=self._name,
            age=self._age,
            email=self._email,
            is_active=self._is_active,
        )


class TestBaseBuilder:
    """测试BaseBuilder基类"""

    def test_builder_requires_build_method(self):
        """测试BaseBuilder强制要求实现build方法"""
        # BaseBuilder是抽象基类，不能直接实例化
        with pytest.raises(TypeError):
            BaseBuilder()  # type: ignore

    def test_custom_builder_build(self):
        """测试自定义Builder的build方法"""
        user = UserBuilder().build()

        assert isinstance(user, User)
        assert user.user_id == "default_user"
        assert user.name == "Default Name"
        assert user.age == 18
        assert user.is_active is True

    def test_custom_builder_fluent_api(self):
        """测试流式API"""
        user = (
            UserBuilder()
            .with_id("user_001")
            .with_name("Alice")
            .with_age(25)
            .with_email("alice@example.com")
            .inactive()
            .build()
        )

        assert user.user_id == "user_001"
        assert user.name == "Alice"
        assert user.age == 25
        assert user.email == "alice@example.com"
        assert user.is_active is False

    def test_builder_reset(self):
        """测试reset方法重置builder到初始状态"""
        builder = UserBuilder().with_id("user_001").with_name("Alice").with_age(30)

        # 重置
        builder.reset()

        # 验证回到初始状态
        user = builder.build()
        assert user.user_id == "default_user"
        assert user.name == "Default Name"
        assert user.age == 18

    def test_builder_reuse(self):
        """测试Builder可以重复使用"""
        builder = UserBuilder()

        # 第一次构建
        user1 = builder.with_id("user_001").with_name("Alice").build()

        # 重置后第二次构建
        builder.reset()
        user2 = builder.with_id("user_002").with_name("Bob").build()

        assert user1.user_id == "user_001"
        assert user1.name == "Alice"
        assert user2.user_id == "user_002"
        assert user2.name == "Bob"


class TestDictBuilder:
    """测试DictBuilder"""

    def test_dict_builder_creation(self):
        """测试创建DictBuilder"""
        builder = DictBuilder()
        assert isinstance(builder, DictBuilder)
        assert builder._data == {}

    def test_dict_builder_with_initial_data(self):
        """测试使用初始数据创建"""
        initial = {"name": "Alice", "age": 25}
        builder = DictBuilder(initial)

        # 验证数据被深拷贝
        result = builder.build()
        assert result == initial
        assert result is not initial  # 不是同一个对象

    def test_set_single_field(self):
        """测试set设置单个字段"""
        builder = DictBuilder()
        builder.set("user_id", "user_001")

        result = builder.build()
        assert result == {"user_id": "user_001"}

    def test_set_fluent_chaining(self):
        """测试set流式链式调用"""
        result = (
            DictBuilder().set("user_id", "user_001").set("name", "Alice").set("age", 25).build()
        )

        assert result == {"user_id": "user_001", "name": "Alice", "age": 25}

    def test_set_many(self):
        """测试set_many批量设置字段"""
        result = DictBuilder().set_many(user_id="user_001", name="Alice", age=25).build()

        assert result == {"user_id": "user_001", "name": "Alice", "age": 25}

    def test_set_many_with_existing_data(self):
        """测试set_many覆盖已有字段"""
        result = (
            DictBuilder()
            .set("user_id", "old_id")
            .set("name", "Old Name")
            .set_many(user_id="new_id", age=30)
            .build()
        )

        assert result == {"user_id": "new_id", "name": "Old Name", "age": 30}

    def test_remove_field(self):
        """测试remove移除字段"""
        result = (
            DictBuilder()
            .set("user_id", "user_001")
            .set("name", "Alice")
            .set("temp_field", "temp")
            .remove("temp_field")
            .build()
        )

        assert result == {"user_id": "user_001", "name": "Alice"}
        assert "temp_field" not in result

    def test_remove_nonexistent_field(self):
        """测试移除不存在的字段不抛出异常"""
        builder = DictBuilder().set("user_id", "user_001")
        builder.remove("nonexistent")  # 不应该抛出异常

        result = builder.build()
        assert result == {"user_id": "user_001"}

    def test_get_field(self):
        """测试get获取字段值"""
        builder = DictBuilder().set("user_id", "user_001").set("name", "Alice")

        assert builder.get("user_id") == "user_001"
        assert builder.get("name") == "Alice"
        assert builder.get("nonexistent") is None
        assert builder.get("nonexistent", "default") == "default"

    def test_has_field(self):
        """测试has检查字段是否存在"""
        builder = DictBuilder().set("user_id", "user_001")

        assert builder.has("user_id") is True
        assert builder.has("nonexistent") is False

    def test_merge(self):
        """测试merge合并其他字典"""
        result = (
            DictBuilder()
            .set("user_id", "user_001")
            .set("name", "Alice")
            .merge({"age": 25, "email": "alice@example.com"})
            .build()
        )

        assert result == {
            "user_id": "user_001",
            "name": "Alice",
            "age": 25,
            "email": "alice@example.com",
        }

    def test_merge_overwrites_existing(self):
        """测试merge覆盖同名字段"""
        result = (
            DictBuilder()
            .set("user_id", "old_id")
            .set("name", "Alice")
            .merge({"user_id": "new_id", "age": 25})
            .build()
        )

        assert result == {"user_id": "new_id", "name": "Alice", "age": 25}

    def test_build_returns_deep_copy(self):
        """测试build返回深拷贝"""
        builder = DictBuilder().set("user_id", "user_001")

        result1 = builder.build()
        result2 = builder.build()

        # 应该是不同的对象
        assert result1 is not result2
        # 但内容相同
        assert result1 == result2

    def test_build_does_not_affect_builder(self):
        """测试build后修改返回值不影响builder"""
        builder = DictBuilder().set("user_id", "user_001")
        result = builder.build()

        # 修改返回值
        result["user_id"] = "modified"

        # builder应该不受影响
        new_result = builder.build()
        assert new_result["user_id"] == "user_001"

    def test_clone(self):
        """测试clone克隆builder"""
        builder1 = DictBuilder().set("user_id", "user_001").set("name", "Alice")

        builder2 = builder1.clone()

        # 验证是不同的实例
        assert builder1 is not builder2

        # 验证数据相同
        assert builder1.build() == builder2.build()

        # 修改builder2不影响builder1
        builder2.set("age", 25)

        assert builder1.has("age") is False
        assert builder2.has("age") is True

    def test_clone_and_modify(self):
        """测试克隆后修改"""
        base_builder = DictBuilder().set("template", "base").set("version", "1.0")

        builder1 = base_builder.clone().set("user_id", "user_001")
        builder2 = base_builder.clone().set("user_id", "user_002")

        result1 = builder1.build()
        result2 = builder2.build()

        assert result1 == {"template": "base", "version": "1.0", "user_id": "user_001"}
        assert result2 == {"template": "base", "version": "1.0", "user_id": "user_002"}


class TestDictBuilderComplexScenarios:
    """测试DictBuilder复杂场景"""

    def test_nested_dict(self):
        """测试嵌套字典"""
        result = (
            DictBuilder()
            .set("user_id", "user_001")
            .set("profile", {"name": "Alice", "age": 25})
            .set("preferences", {"theme": "dark", "language": "zh-CN"})
            .build()
        )

        assert result["profile"]["name"] == "Alice"
        assert result["preferences"]["theme"] == "dark"

    def test_list_values(self):
        """测试列表值"""
        result = (
            DictBuilder()
            .set("user_id", "user_001")
            .set("tags", ["premium", "verified"])
            .set("permissions", ["read", "write", "delete"])
            .build()
        )

        assert len(result["tags"]) == 2
        assert "premium" in result["tags"]

    def test_complex_data_structure(self):
        """测试复杂数据结构"""
        result = (
            DictBuilder()
            .set_many(
                user_id="user_001",
                name="Alice",
                age=25,
            )
            .set(
                "address",
                {
                    "city": "Beijing",
                    "country": "China",
                },
            )
            .set(
                "orders",
                [
                    {"order_id": "ord_001", "amount": 100},
                    {"order_id": "ord_002", "amount": 200},
                ],
            )
            .merge({"is_vip": True, "points": 1000})
            .build()
        )

        assert result["user_id"] == "user_001"
        assert result["address"]["city"] == "Beijing"
        assert len(result["orders"]) == 2
        assert result["is_vip"] is True

    def test_template_pattern(self):
        """测试模板模式用法"""
        # 创建模板builder
        template = DictBuilder().set_many(
            template_id="tpl_001",
            version="1.0",
            created_by="system",
        )

        # 基于模板创建多个实例
        instance1 = template.clone().set("instance_id", "inst_001").build()
        instance2 = template.clone().set("instance_id", "inst_002").build()

        assert instance1["template_id"] == "tpl_001"
        assert instance2["template_id"] == "tpl_001"
        assert instance1["instance_id"] == "inst_001"
        assert instance2["instance_id"] == "inst_002"
