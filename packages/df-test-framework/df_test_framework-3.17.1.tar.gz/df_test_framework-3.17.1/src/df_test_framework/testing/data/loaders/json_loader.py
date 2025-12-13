"""JSON数据加载器

支持从JSON文件加载测试数据

特性:
- 支持标准JSON和JSON Lines格式
- 自动处理编码
- 支持JSON5扩展（注释、尾逗号等，需要json5库）
- 支持JSONPath查询

使用示例:
    >>> from df_test_framework.testing.data.loaders import JSONLoader
    >>>
    >>> # 加载完整文件
    >>> users = JSONLoader.load("tests/data/users.json")
    >>>
    >>> # 加载单条数据
    >>> first_user = JSONLoader.load_one("tests/data/users.json", index=0)
    >>>
    >>> # 使用JSONPath查询
    >>> names = JSONLoader.query("tests/data/users.json", "$.users[*].name")
    >>>
    >>> # 加载JSON Lines
    >>> logs = JSONLoader.load_lines("tests/data/logs.jsonl")

v3.10.0 新增 - P2.2 测试数据工具增强
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .base import DataLoader


class JSONLoader(DataLoader):
    """JSON数据加载器

    支持标准JSON格式和扩展功能

    支持格式:
        - 标准JSON文件 (.json)
        - JSON Lines文件 (.jsonl)
        - JSON5文件 (.json5) - 需要json5库

    示例:
        >>> # 加载JSON数组
        >>> users = JSONLoader.load("users.json")
        >>> # [{"name": "Alice"}, {"name": "Bob"}]

        >>> # 加载JSON对象
        >>> config = JSONLoader.load("config.json")
        >>> # {"database": {...}, "redis": {...}}

        >>> # 从字符串解析
        >>> data = JSONLoader.loads('{"key": "value"}')
    """

    @classmethod
    def load(cls, file_path: str | Path, encoding: str = "utf-8", **kwargs) -> Any:
        """从JSON文件加载数据

        Args:
            file_path: JSON文件路径
            encoding: 文件编码，默认UTF-8
            **kwargs: json.load的额外参数

        Returns:
            解析后的Python对象

        Raises:
            FileNotFoundError: 文件不存在
            json.JSONDecodeError: JSON格式错误

        示例:
            >>> data = JSONLoader.load("tests/data/users.json")
            >>> data = JSONLoader.load("config.json", encoding="gbk")
        """
        path = cls._resolve_path(file_path)

        with open(path, encoding=encoding) as f:
            return json.load(f, **kwargs)

    @classmethod
    def loads(cls, content: str, **kwargs) -> Any:
        """从JSON字符串解析数据

        Args:
            content: JSON字符串
            **kwargs: json.loads的额外参数

        Returns:
            解析后的Python对象

        Raises:
            json.JSONDecodeError: JSON格式错误

        示例:
            >>> data = JSONLoader.loads('{"name": "Alice", "age": 25}')
            >>> print(data)  # {'name': 'Alice', 'age': 25}
        """
        return json.loads(content, **kwargs)

    @classmethod
    def load_lines(
        cls,
        file_path: str | Path,
        encoding: str = "utf-8",
        skip_empty: bool = True,
        skip_errors: bool = False,
    ) -> list[dict[str, Any]]:
        """从JSON Lines文件加载数据

        JSON Lines格式：每行一个独立的JSON对象

        Args:
            file_path: JSONL文件路径
            encoding: 文件编码
            skip_empty: 是否跳过空行
            skip_errors: 是否跳过解析错误的行

        Returns:
            JSON对象列表

        示例:
            >>> # logs.jsonl:
            >>> # {"level": "INFO", "msg": "started"}
            >>> # {"level": "ERROR", "msg": "failed"}
            >>> logs = JSONLoader.load_lines("logs.jsonl")
        """
        path = cls._resolve_path(file_path)
        result = []

        with open(path, encoding=encoding) as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()

                if not line and skip_empty:
                    continue

                try:
                    result.append(json.loads(line))
                except json.JSONDecodeError as e:
                    if skip_errors:
                        continue
                    raise ValueError(f"第{line_num}行JSON格式错误: {e}") from e

        return result

    @classmethod
    def query(cls, file_path: str | Path, jsonpath: str, encoding: str = "utf-8") -> list[Any]:
        """使用JSONPath查询数据

        需要安装jsonpath-ng库: pip install jsonpath-ng

        Args:
            file_path: JSON文件路径
            jsonpath: JSONPath表达式
            encoding: 文件编码

        Returns:
            匹配的结果列表

        Raises:
            ImportError: 未安装jsonpath-ng库

        示例:
            >>> # data.json: {"users": [{"name": "Alice"}, {"name": "Bob"}]}
            >>> names = JSONLoader.query("data.json", "$.users[*].name")
            >>> print(names)  # ['Alice', 'Bob']

        常用JSONPath语法:
            - $.store.book[*].author  获取所有书的作者
            - $..author               递归获取所有author
            - $.store.book[0]         第一本书
            - $.store.book[-1]        最后一本书
            - $.store.book[0,1]       第一和第二本书
            - $.store.book[:2]        前两本书
            - $.store.book[?@.price<10]  价格小于10的书
        """
        try:
            from jsonpath_ng import parse
        except ImportError:
            raise ImportError("JSONPath查询需要jsonpath-ng库，请安装: pip install jsonpath-ng")

        data = cls.load(file_path, encoding=encoding)
        jsonpath_expr = parse(jsonpath)
        matches = jsonpath_expr.find(data)

        return [match.value for match in matches]

    @classmethod
    def save(
        cls,
        data: Any,
        file_path: str | Path,
        encoding: str = "utf-8",
        indent: int = 2,
        ensure_ascii: bool = False,
        **kwargs,
    ) -> None:
        """保存数据到JSON文件

        Args:
            data: 要保存的数据
            file_path: 目标文件路径
            encoding: 文件编码
            indent: 缩进空格数
            ensure_ascii: 是否转义非ASCII字符
            **kwargs: json.dump的额外参数

        示例:
            >>> JSONLoader.save({"name": "测试"}, "output.json")
        """
        path = Path(file_path)

        # 确保目录存在
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding=encoding) as f:
            json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii, **kwargs)


__all__ = ["JSONLoader"]
