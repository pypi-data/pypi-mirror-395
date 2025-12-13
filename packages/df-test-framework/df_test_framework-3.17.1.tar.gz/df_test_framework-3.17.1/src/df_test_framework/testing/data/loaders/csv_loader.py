"""CSV数据加载器

支持从CSV文件加载测试数据

特性:
- 自动检测分隔符
- 支持自定义列映射
- 类型转换支持
- 支持有/无表头

使用示例:
    >>> from df_test_framework.testing.data.loaders import CSVLoader
    >>>
    >>> # 加载CSV（带表头）
    >>> users = CSVLoader.load("tests/data/users.csv")
    >>>
    >>> # 指定分隔符
    >>> data = CSVLoader.load("data.tsv", delimiter="\\t")
    >>>
    >>> # 类型转换
    >>> data = CSVLoader.load("data.csv", type_hints={"age": int, "price": float})

v3.10.0 新增 - P2.2 测试数据工具增强
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from .base import DataLoader


class CSVLoader(DataLoader):
    """CSV数据加载器

    支持CSV和类似格式（TSV等）

    示例:
        >>> # users.csv:
        >>> # name,age,email
        >>> # Alice,25,alice@example.com
        >>> # Bob,30,bob@example.com

        >>> users = CSVLoader.load("users.csv")
        >>> # [{'name': 'Alice', 'age': '25', 'email': 'alice@example.com'}, ...]

        >>> # 带类型转换
        >>> users = CSVLoader.load("users.csv", type_hints={"age": int})
        >>> # [{'name': 'Alice', 'age': 25, 'email': 'alice@example.com'}, ...]
    """

    @classmethod
    def load(
        cls,
        file_path: str | Path,
        encoding: str = "utf-8",
        delimiter: str = ",",
        has_header: bool = True,
        fieldnames: list[str] | None = None,
        type_hints: dict[str, type] | None = None,
        skip_rows: int = 0,
        **kwargs,
    ) -> list[dict[str, Any]]:
        """从CSV文件加载数据

        Args:
            file_path: CSV文件路径
            encoding: 文件编码，默认UTF-8
            delimiter: 字段分隔符，默认逗号
            has_header: 是否有表头行
            fieldnames: 自定义字段名（覆盖表头）
            type_hints: 类型转换映射 {"字段名": 类型}
            skip_rows: 跳过的行数（在表头之后）
            **kwargs: csv.DictReader的额外参数

        Returns:
            字典列表

        Raises:
            FileNotFoundError: 文件不存在

        示例:
            >>> data = CSVLoader.load("data.csv")
            >>> data = CSVLoader.load("data.tsv", delimiter="\\t")
            >>> data = CSVLoader.load("data.csv", type_hints={"age": int, "score": float})
        """
        path = cls._resolve_path(file_path)
        result = []

        with open(path, encoding=encoding, newline="") as f:
            if has_header:
                reader = csv.DictReader(f, delimiter=delimiter, fieldnames=fieldnames, **kwargs)
            else:
                # 无表头时使用fieldnames或生成默认列名
                if not fieldnames:
                    # 读取第一行确定列数
                    first_line = f.readline()
                    f.seek(0)
                    col_count = len(first_line.split(delimiter))
                    fieldnames = [f"col_{i}" for i in range(col_count)]
                reader = csv.DictReader(f, delimiter=delimiter, fieldnames=fieldnames, **kwargs)

            # 跳过指定行数
            for _ in range(skip_rows):
                next(reader, None)

            for row in reader:
                # 应用类型转换
                if type_hints:
                    row = cls._apply_type_hints(row, type_hints)
                result.append(dict(row))

        return result

    @classmethod
    def loads(cls, content: str, **kwargs) -> list[dict[str, Any]]:
        """从CSV字符串解析数据

        Args:
            content: CSV字符串
            **kwargs: 传递给load的参数

        Returns:
            字典列表

        示例:
            >>> csv_str = "name,age\\nAlice,25\\nBob,30"
            >>> data = CSVLoader.loads(csv_str)
        """
        import io

        delimiter = kwargs.pop("delimiter", ",")
        has_header = kwargs.pop("has_header", True)
        fieldnames = kwargs.pop("fieldnames", None)
        type_hints = kwargs.pop("type_hints", None)

        result = []
        f = io.StringIO(content)

        if has_header:
            reader = csv.DictReader(f, delimiter=delimiter, fieldnames=fieldnames, **kwargs)
        else:
            if not fieldnames:
                first_line = content.split("\n")[0] if content else ""
                col_count = len(first_line.split(delimiter))
                fieldnames = [f"col_{i}" for i in range(col_count)]
            reader = csv.DictReader(f, delimiter=delimiter, fieldnames=fieldnames, **kwargs)

        for row in reader:
            if type_hints:
                row = cls._apply_type_hints(row, type_hints)
            result.append(dict(row))

        return result

    @classmethod
    def load_as_tuples(
        cls,
        file_path: str | Path,
        encoding: str = "utf-8",
        delimiter: str = ",",
        skip_header: bool = True,
        **kwargs,
    ) -> list[tuple]:
        """加载为元组列表（适合pytest参数化）

        Args:
            file_path: CSV文件路径
            encoding: 文件编码
            delimiter: 分隔符
            skip_header: 是否跳过表头
            **kwargs: csv.reader额外参数

        Returns:
            元组列表

        示例:
            >>> # test_data.csv:
            >>> # input,expected
            >>> # 1,2
            >>> # 2,4
            >>> test_cases = CSVLoader.load_as_tuples("test_data.csv")
            >>> # [('1', '2'), ('2', '4')]
        """
        path = cls._resolve_path(file_path)
        result = []

        with open(path, encoding=encoding, newline="") as f:
            reader = csv.reader(f, delimiter=delimiter, **kwargs)

            if skip_header:
                next(reader, None)

            for row in reader:
                result.append(tuple(row))

        return result

    @classmethod
    def _apply_type_hints(cls, row: dict[str, str], type_hints: dict[str, type]) -> dict[str, Any]:
        """应用类型转换

        Args:
            row: 原始行数据
            type_hints: 类型映射

        Returns:
            类型转换后的行数据
        """
        result = dict(row)

        for field, target_type in type_hints.items():
            if field in result and result[field] is not None:
                try:
                    value = result[field]

                    # 处理空字符串
                    if value == "":
                        if target_type in (int, float):
                            result[field] = 0 if target_type is int else 0.0
                        elif target_type is bool:
                            result[field] = False
                        else:
                            result[field] = None
                        continue

                    # 布尔类型特殊处理
                    if target_type is bool:
                        result[field] = value.lower() in ("true", "1", "yes", "y", "on")
                    else:
                        result[field] = target_type(value)

                except (ValueError, TypeError):
                    # 转换失败保留原值
                    pass

        return result

    @classmethod
    def save(
        cls,
        data: list[dict[str, Any]],
        file_path: str | Path,
        encoding: str = "utf-8",
        delimiter: str = ",",
        fieldnames: list[str] | None = None,
        **kwargs,
    ) -> None:
        """保存数据到CSV文件

        Args:
            data: 要保存的数据列表
            file_path: 目标文件路径
            encoding: 文件编码
            delimiter: 分隔符
            fieldnames: 字段名列表（默认从第一条数据获取）
            **kwargs: csv.DictWriter额外参数

        示例:
            >>> data = [{"name": "Alice", "age": 25}]
            >>> CSVLoader.save(data, "output.csv")
        """
        if not data:
            return

        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        if fieldnames is None:
            fieldnames = list(data[0].keys())

        with open(path, "w", encoding=encoding, newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter, **kwargs)
            writer.writeheader()
            writer.writerows(data)


__all__ = ["CSVLoader"]
