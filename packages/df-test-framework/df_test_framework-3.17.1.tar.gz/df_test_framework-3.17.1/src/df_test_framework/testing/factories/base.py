"""数据工厂基类

提供强大的测试数据构建能力，基于Factory Pattern

核心特性:
- 声明式定义数据结构
- 支持序列化字段（自增ID、序列值等）
- 支持Lazy属性（延迟计算）
- 支持Faker集成（生成假数据）
- 支持关联对象
- 支持Trait（预设配置）

使用场景:
- 快速构建测试数据
- 保持测试数据一致性
- 减少样板代码
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, TypeVar

try:
    from faker import Faker

    FAKER_AVAILABLE = True
    _faker = Faker(locale="zh_CN")  # 默认中文
except ImportError:
    FAKER_AVAILABLE = False
    _faker = None


T = TypeVar("T")


class LazyAttribute:
    """延迟计算属性

    属性值在build时动态计算，而非定义时

    Example:
        >>> class UserFactory(Factory):
        ...     username = LazyAttribute(lambda obj: f"user_{obj.id}")
        ...     email = LazyAttribute(lambda obj: f"{obj.username}@example.com")
    """

    def __init__(self, func: Callable):
        """初始化延迟属性

        Args:
            func: 计算函数，接收当前对象作为参数
        """
        self.func = func

    def evaluate(self, obj):
        """评估属性值

        Args:
            obj: 当前对象（包含其他已生成的属性）

        Returns:
            属性值
        """
        return self.func(obj)


class Sequence:
    """序列生成器

    生成递增的序列值，支持自定义格式

    Example:
        >>> class UserFactory(Factory):
        ...     id = Sequence()  # 1, 2, 3, ...
        ...     username = Sequence(lambda n: f"user_{n}")  # user_1, user_2, ...
    """

    _counters: dict[str, int] = {}  # 全局计数器

    def __init__(self, func: Callable[[int], Any] | None = None):
        """初始化序列生成器

        Args:
            func: 格式化函数，接收序列号作为参数，返回最终值
                  如果为None，直接返回序列号
        """
        self.func = func or (lambda n: n)
        self.counter_name = None  # 在Factory中设置

    def next(self) -> Any:
        """获取下一个值

        Returns:
            下一个序列值
        """
        if self.counter_name is None:
            # 未绑定到Factory，使用默认计数器
            counter_name = "__default__"
        else:
            counter_name = self.counter_name

        # 递增计数器
        if counter_name not in self._counters:
            self._counters[counter_name] = 0
        self._counters[counter_name] += 1

        return self.func(self._counters[counter_name])

    @classmethod
    def reset(cls, name: str | None = None):
        """重置计数器

        Args:
            name: 计数器名称（None表示重置所有）
        """
        if name is None:
            cls._counters.clear()
        elif name in cls._counters:
            cls._counters[name] = 0


class FakerAttribute:
    """Faker属性（生成假数据）

    Example:
        >>> class UserFactory(Factory):
        ...     name = FakerAttribute("name")
        ...     email = FakerAttribute("email")
        ...     phone = FakerAttribute("phone_number")
    """

    def __init__(self, provider: str, *args, **kwargs):
        """初始化Faker属性

        Args:
            provider: Faker provider名称（如"name", "email"）
            *args: provider参数
            **kwargs: provider关键字参数
        """
        if not FAKER_AVAILABLE:
            raise ImportError("faker is not installed. Please install it: pip install faker")
        self.provider = provider
        self.args = args
        self.kwargs = kwargs

    def generate(self) -> Any:
        """生成假数据

        Returns:
            生成的假数据
        """
        method = getattr(_faker, self.provider)
        return method(*self.args, **self.kwargs)


@dataclass
class FactoryOptions:
    """Factory配置选项"""

    model: type | None = None  # 目标Model类（可选）
    abstract: bool = False  # 是否为抽象Factory


class FactoryMeta(type):
    """Factory元类

    负责处理类定义时的声明式属性
    """

    def __new__(mcs, name, bases, namespace):
        # 提取Factory选项
        meta = namespace.get("Meta", None)
        if meta:
            options = FactoryOptions(
                model=getattr(meta, "model", None),
                abstract=getattr(meta, "abstract", False),
            )
        else:
            options = FactoryOptions()

        namespace["_options"] = options

        # 提取字段定义
        fields = {}
        for key, value in namespace.items():
            if key.startswith("_") or key == "Meta":
                continue
            if isinstance(value, (LazyAttribute, Sequence, FakerAttribute)):
                fields[key] = value
            elif callable(value):
                # 跳过方法
                continue
            else:
                # 普通值
                fields[key] = value

        namespace["_fields"] = fields

        # 为Sequence绑定counter名称
        for field_name, field_value in fields.items():
            if isinstance(field_value, Sequence):
                field_value.counter_name = f"{name}.{field_name}"

        return super().__new__(mcs, name, bases, namespace)


class Factory[T](metaclass=FactoryMeta):
    """数据工厂基类

    使用声明式语法定义测试数据结构

    Example:
        >>> class UserFactory(Factory):
        ...     class Meta:
        ...         model = User  # 可选：关联Model类
        ...
        ...     id = Sequence()
        ...     username = Sequence(lambda n: f"user_{n}")
        ...     email = LazyAttribute(lambda obj: f"{obj.username}@example.com")
        ...     name = FakerAttribute("name")  # 需要安装faker
        ...     age = 25  # 固定值
        ...     is_active = True

        >>> # 构建单个对象
        >>> user = UserFactory.build()
        >>> print(user)  # {"id": 1, "username": "user_1", "email": "user_1@example.com", ...}

        >>> # 构建多个对象
        >>> users = UserFactory.build_batch(10)
        >>> print(len(users))  # 10

        >>> # 覆盖默认值
        >>> user = UserFactory.build(username="alice", age=30)

        >>> # Trait预设
        >>> admin_user = UserFactory.build(is_admin=True, role="admin")
    """

    _options: FactoryOptions
    _fields: dict[str, Any]

    @classmethod
    def build(cls, **overrides) -> dict[str, Any]:
        """构建单个对象

        Args:
            **overrides: 覆盖默认值

        Returns:
            构建的对象（字典）
        """
        obj = {}

        # 1. 处理普通字段和覆盖
        for field_name, field_value in cls._fields.items():
            if field_name in overrides:
                # 使用覆盖值
                obj[field_name] = overrides[field_name]
            elif isinstance(field_value, Sequence):
                # 序列字段
                obj[field_name] = field_value.next()
            elif isinstance(field_value, FakerAttribute):
                # Faker字段
                obj[field_name] = field_value.generate()
            elif isinstance(field_value, LazyAttribute):
                # 延迟字段：稍后评估
                pass
            else:
                # 普通值
                obj[field_name] = field_value

        # 2. 评估LazyAttribute（依赖其他字段）
        for field_name, field_value in cls._fields.items():
            if isinstance(field_value, LazyAttribute) and field_name not in overrides:
                # 创建临时对象供LazyAttribute访问
                temp_obj = type("TempObj", (), obj)()
                obj[field_name] = field_value.evaluate(temp_obj)

        # 3. 如果有Model类，转换为Model实例
        if cls._options.model:
            return cls._options.model(**obj)

        return obj

    @classmethod
    def build_batch(cls, size: int, **overrides) -> list:
        """批量构建对象

        Args:
            size: 数量
            **overrides: 覆盖默认值（应用到所有对象）

        Returns:
            对象列表
        """
        return [cls.build(**overrides) for _ in range(size)]

    @classmethod
    def build_dict(cls, **overrides) -> dict[str, Any]:
        """构建字典（确保返回字典）

        Args:
            **overrides: 覆盖默认值

        Returns:
            字典对象
        """
        obj = cls.build(**overrides)
        if isinstance(obj, dict):
            return obj
        # 如果是Model实例，转换为字典
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        if hasattr(obj, "model_dump"):  # Pydantic
            return obj.model_dump()
        if hasattr(obj, "dict"):  # Pydantic v1
            return obj.dict()
        return obj

    @classmethod
    def reset_sequences(cls):
        """重置所有序列计数器"""
        Sequence.reset()


# 便捷函数


def fake(provider: str, *args, **kwargs):
    """快捷函数：生成假数据

    Args:
        provider: Faker provider名称
        *args: provider参数
        **kwargs: provider关键字参数

    Returns:
        生成的假数据

    Example:
        >>> name = fake("name")
        >>> email = fake("email")
    """
    if not FAKER_AVAILABLE:
        raise ImportError("faker is not installed. Please install it: pip install faker")
    method = getattr(_faker, provider)
    return method(*args, **kwargs)


__all__ = [
    "Factory",
    "LazyAttribute",
    "Sequence",
    "FakerAttribute",
    "fake",
    "FAKER_AVAILABLE",
]
