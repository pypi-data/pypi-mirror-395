"""数据加载器基类

提供数据加载的通用接口和工具方法

v3.10.0 新增 - P2.2 测试数据工具增强
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class DataLoader(ABC):
    """数据加载器基类

    定义数据加载的标准接口

    子类需要实现:
        - load(): 加载文件数据
        - loads(): 从字符串加载数据

    示例:
        >>> class MyLoader(DataLoader):
        ...     @classmethod
        ...     def load(cls, file_path, **kwargs):
        ...         with open(file_path) as f:
        ...             return parse(f.read())
    """

    @classmethod
    @abstractmethod
    def load(cls, file_path: str | Path, **kwargs) -> Any:
        """从文件加载数据

        Args:
            file_path: 文件路径
            **kwargs: 额外参数

        Returns:
            加载的数据

        Raises:
            FileNotFoundError: 文件不存在
            ValueError: 数据格式错误
        """
        pass

    @classmethod
    @abstractmethod
    def loads(cls, content: str, **kwargs) -> Any:
        """从字符串加载数据

        Args:
            content: 数据字符串
            **kwargs: 额外参数

        Returns:
            解析后的数据

        Raises:
            ValueError: 数据格式错误
        """
        pass

    @classmethod
    def load_one(cls, file_path: str | Path, index: int = 0, **kwargs) -> dict[str, Any]:
        """加载单条数据

        从文件中加载指定索引的数据（适用于列表数据）

        Args:
            file_path: 文件路径
            index: 数据索引，默认第一条
            **kwargs: 额外参数

        Returns:
            指定索引的数据

        Raises:
            IndexError: 索引超出范围
            TypeError: 数据不是列表类型
        """
        data = cls.load(file_path, **kwargs)

        if not isinstance(data, list):
            if index == 0:
                return data if isinstance(data, dict) else {"value": data}
            raise TypeError(f"数据不是列表类型，无法使用索引访问: {type(data)}")

        if index < 0 or index >= len(data):
            raise IndexError(f"索引 {index} 超出范围 [0, {len(data) - 1}]")

        return data[index]

    @classmethod
    def load_all(cls, file_path: str | Path, **kwargs) -> list[dict[str, Any]]:
        """加载所有数据（确保返回列表）

        Args:
            file_path: 文件路径
            **kwargs: 额外参数

        Returns:
            数据列表
        """
        data = cls.load(file_path, **kwargs)

        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return [data]
        else:
            return [{"value": data}]

    @classmethod
    def exists(cls, file_path: str | Path) -> bool:
        """检查文件是否存在

        Args:
            file_path: 文件路径

        Returns:
            文件是否存在
        """
        return Path(file_path).exists()

    @classmethod
    def _resolve_path(cls, file_path: str | Path) -> Path:
        """解析文件路径

        支持相对路径和绝对路径

        Args:
            file_path: 文件路径

        Returns:
            解析后的Path对象

        Raises:
            FileNotFoundError: 文件不存在
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")

        return path


__all__ = ["DataLoader"]
