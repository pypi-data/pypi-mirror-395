"""基础Builder类

v1.3.0 新增 - Builder模式实现
提供流畅的API构建测试数据
"""

from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any, TypeVar

T = TypeVar("T")


class BaseBuilder[T](ABC):
    """Builder基类

    提供流畅的API用于构建测试数据

    示例:
        class CardRequestBuilder(BaseBuilder[CardRequest]):
            def __init__(self):
                self._user_id = "default_user"
                self._template_id = "default_template"
                self._quantity = 1

            def with_user(self, user_id: str) -> "CardRequestBuilder":
                self._user_id = user_id
                return self

            def with_quantity(self, quantity: int) -> "CardRequestBuilder":
                self._quantity = quantity
                return self

            def build(self) -> CardRequest:
                return CardRequest(
                    user_id=self._user_id,
                    template_id=self._template_id,
                    quantity=self._quantity
                )

        # 使用
        request = CardRequestBuilder() \\
            .with_user("user_001") \\
            .with_quantity(5) \\
            .build()

    v1.3.0 新增
    """

    @abstractmethod
    def build(self) -> T:
        """构建最终对象

        子类必须实现此方法

        Returns:
            构建的对象

        示例:
            def build(self) -> CardRequest:
                return CardRequest(
                    user_id=self._user_id,
                    template_id=self._template_id,
                    quantity=self._quantity
                )
        """
        pass

    def reset(self) -> "BaseBuilder":
        """重置Builder到初始状态

        子类可以覆盖此方法实现自定义重置逻辑

        Returns:
            self,支持链式调用
        """
        self.__init__()  # type: ignore
        return self


class DictBuilder(BaseBuilder[dict[str, Any]]):
    """字典Builder - 简化版Builder

    直接构建字典对象,适用于简单的测试数据构建场景

    示例:
        builder = DictBuilder() \\
            .set("user_id", "user_001") \\
            .set("template_id", "tpl_001") \\
            .set("quantity", 5) \\
            .build()

        # 结果: {"user_id": "user_001", "template_id": "tpl_001", "quantity": 5}

    v1.3.0 新增
    """

    def __init__(self, initial_data: dict[str, Any] | None = None):
        """初始化DictBuilder

        Args:
            initial_data: 初始数据字典,会被深拷贝
        """
        self._data: dict[str, Any] = deepcopy(initial_data) if initial_data else {}

    def set(self, key: str, value: Any) -> "DictBuilder":
        """设置字段值

        Args:
            key: 字段名
            value: 字段值

        Returns:
            self,支持链式调用

        示例:
            builder.set("user_id", "user_001").set("quantity", 5)
        """
        self._data[key] = value
        return self

    def set_many(self, **kwargs: Any) -> "DictBuilder":
        """批量设置字段值

        Args:
            **kwargs: 字段名和值的键值对

        Returns:
            self,支持链式调用

        示例:
            builder.set_many(user_id="user_001", quantity=5)
        """
        self._data.update(kwargs)
        return self

    def remove(self, key: str) -> "DictBuilder":
        """移除字段

        Args:
            key: 要移除的字段名

        Returns:
            self,支持链式调用

        示例:
            builder.remove("optional_field")
        """
        self._data.pop(key, None)
        return self

    def get(self, key: str, default: Any = None) -> Any:
        """获取字段值

        Args:
            key: 字段名
            default: 默认值

        Returns:
            字段值,如果不存在返回default

        示例:
            user_id = builder.get("user_id", "default_user")
        """
        return self._data.get(key, default)

    def has(self, key: str) -> bool:
        """检查字段是否存在

        Args:
            key: 字段名

        Returns:
            是否存在

        示例:
            if builder.has("optional_field"):
                ...
        """
        return key in self._data

    def merge(self, other_data: dict[str, Any]) -> "DictBuilder":
        """合并其他字典数据

        Args:
            other_data: 要合并的字典,会覆盖同名字段

        Returns:
            self,支持链式调用

        示例:
            builder.merge({"status": "ACTIVE", "balance": 100.0})
        """
        self._data.update(other_data)
        return self

    def build(self) -> dict[str, Any]:
        """构建字典对象

        Returns:
            构建的字典,是深拷贝的副本

        示例:
            data = builder.build()
        """
        return deepcopy(self._data)

    def clone(self) -> "DictBuilder":
        """克隆当前Builder

        Returns:
            新的DictBuilder实例,包含当前数据的深拷贝

        示例:
            builder2 = builder.clone().set("user_id", "user_002")
        """
        return DictBuilder(self._data)


__all__ = ["BaseBuilder", "DictBuilder"]
