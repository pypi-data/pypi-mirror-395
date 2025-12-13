"""JSON到Pydantic模型生成器

从JSON响应自动生成Pydantic模型定义。

Features:
- 自动类型推断 (str, int, float, bool, list, dict, Optional)
- 支持嵌套对象 (自动生成子模型)
- 支持数组类型 (List[T])
- 支持可选字段 (Optional[T])
- 自动驼峰转蛇形 (camelCase -> snake_case)
- 支持alias映射 (JSON字段名与Python字段名不同)
- 生成BaseResponse[T]包装类

v3.6+ 特性:
- ⚠️ 浮点数字段推断为 float (不推荐用于金额)
- 💡 金额字段建议手动改为 Decimal 类型
- ✅ HttpClient 自动处理 Decimal 序列化
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def infer_python_type(value: Any, field_name: str = "") -> tuple[str, bool]:
    """推断Python类型

    Args:
        value: JSON值
        field_name: 字段名(用于生成嵌套类名)

    Returns:
        (type_str, is_optional): 类型字符串和是否可选
    """
    if value is None:
        return ("Any", True)

    if isinstance(value, bool):
        return ("bool", False)

    if isinstance(value, int):
        return ("int", False)

    if isinstance(value, float):
        return ("float", False)

    if isinstance(value, str):
        return ("str", False)

    if isinstance(value, list):
        if not value:  # 空数组
            return ("List[Any]", False)

        # 推断数组元素类型
        first_item = value[0]
        if isinstance(first_item, dict):
            # 嵌套对象数组
            nested_class_name = _to_pascal_case(field_name) if field_name else "Item"
            return (f"List[{nested_class_name}]", False)
        else:
            # 基础类型数组
            item_type, _ = infer_python_type(first_item)
            return (f"List[{item_type}]", False)

    if isinstance(value, dict):
        # 嵌套对象
        nested_class_name = _to_pascal_case(field_name) if field_name else "NestedObject"
        return (nested_class_name, False)

    return ("Any", False)


def _to_snake_case(name: str) -> str:
    """驼峰转蛇形

    Examples:
        >>> _to_snake_case("userId")
        'user_id'
        >>> _to_snake_case("orderNo")
        'order_no'
        >>> _to_snake_case("ID")
        'id'
    """
    import re

    # 处理连续大写字母 (如 "ID" -> "id")
    name = re.sub("([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    # 处理驼峰 (如 "userId" -> "user_id")
    name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.lower()


def _to_pascal_case(name: str) -> str:
    """蛇形转帕斯卡

    Examples:
        >>> _to_pascal_case("user_id")
        'UserId'
        >>> _to_pascal_case("order_items")
        'OrderItems'
    """
    return "".join(word.capitalize() for word in name.split("_"))


def generate_model_class(
    class_name: str,
    data: dict[str, Any],
    *,
    parent_data_classes: set[str] = None,
) -> tuple[str, list[str]]:
    """生成单个模型类

    Args:
        class_name: 类名
        data: JSON数据
        parent_data_classes: 已生成的数据类名集合(避免重复)

    Returns:
        (class_code, nested_classes): 类代码和嵌套类列表
    """
    if parent_data_classes is None:
        parent_data_classes = set()

    lines = []
    nested_classes = []
    imports = set()

    # 类定义
    lines.append(f"class {class_name}(BaseModel):")
    lines.append('    """自动生成的数据模型"""')

    if not data:
        lines.append("    pass")
        return "\n".join(lines), []

    # 字段定义
    for json_field, value in data.items():
        python_field = _to_snake_case(json_field)
        type_str, is_optional = infer_python_type(value, python_field)

        # 处理嵌套对象
        if isinstance(value, dict) and value:
            nested_class_name = _to_pascal_case(python_field)
            if nested_class_name not in parent_data_classes:
                parent_data_classes.add(nested_class_name)
                nested_code, sub_nested = generate_model_class(
                    nested_class_name, value, parent_data_classes=parent_data_classes
                )
                nested_classes.extend(sub_nested)
                nested_classes.append(nested_code)
            type_str = nested_class_name

        # 处理数组中的嵌套对象
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            nested_class_name = _to_pascal_case(python_field.rstrip("s"))  # users -> User
            if nested_class_name not in parent_data_classes:
                parent_data_classes.add(nested_class_name)
                nested_code, sub_nested = generate_model_class(
                    nested_class_name, value[0], parent_data_classes=parent_data_classes
                )
                nested_classes.extend(sub_nested)
                nested_classes.append(nested_code)
            type_str = f"List[{nested_class_name}]"
            imports.add("List")

        # 类型导入
        if "List[" in type_str:
            imports.add("List")
        if "Optional[" in type_str or is_optional:
            imports.add("Optional")

        # 字段定义
        if is_optional:
            type_annotation = f"Optional[{type_str}]"
            default = "None"
        else:
            type_annotation = type_str
            default = "..."

        # alias配置
        if python_field != json_field:
            field_config = f'Field({default}, alias="{json_field}", description="{json_field}字段")'
        else:
            field_config = f'Field({default}, description="{python_field}字段")'

        lines.append(f"    {python_field}: {type_annotation} = {field_config}")

    return "\n".join(lines), nested_classes


def generate_pydantic_model_from_json(
    json_data: str | dict[str, Any],
    *,
    model_name: str = "ResponseData",
    wrap_in_base_response: bool = True,
    output_file: Path = None,
) -> str:
    """从JSON生成Pydantic模型

    Args:
        json_data: JSON字符串或字典
        model_name: 模型名称
        wrap_in_base_response: 是否包装为BaseResponse[T]
        output_file: 输出文件路径(如果提供则写入文件)

    Returns:
        生成的Python代码

    Example:
        >>> json_str = '''
        ... {
        ...     "code": 200,
        ...     "message": "success",
        ...     "data": {
        ...         "userId": "123",
        ...         "userName": "张三",
        ...         "age": 25,
        ...         "orders": [
        ...             {"orderId": "001", "amount": 100.0}
        ...         ]
        ...     }
        ... }
        ... '''
        >>> code = generate_pydantic_model_from_json(json_str, model_name="UserResponse")
        >>> print(code)
        # 生成的代码...
    """
    # 解析JSON
    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data

    # 提取data字段(如果存在标准响应格式)
    if wrap_in_base_response and "data" in data:
        inner_data = data["data"]
    else:
        inner_data = data

    # 生成模型类
    data_class_name = f"{model_name}Data" if wrap_in_base_response else model_name
    main_class_code, nested_classes = generate_model_class(data_class_name, inner_data)

    # 组装完整代码
    lines = []

    # 文件头注释
    lines.append('"""自动生成的Pydantic模型')
    lines.append("")
    lines.append("使用 df-test gen models 命令生成")
    lines.append("")
    lines.append("⚠️ 重要提示:")
    lines.append("- 浮点数字段 (float) 推断自 JSON 数值")
    lines.append("- 金额/价格字段建议手动改为 Decimal 类型")
    lines.append("- 示例: amount: float → amount: Decimal")
    lines.append("- HttpClient 会自动将 Decimal 序列化为字符串")
    lines.append('"""')
    lines.append("")

    # 导入语句
    lines.append("from __future__ import annotations")
    lines.append("")
    lines.append("from typing import List, Optional, Any")
    lines.append("# from decimal import Decimal  # 如果有金额字段,取消注释")
    lines.append("from pydantic import BaseModel, Field")

    if wrap_in_base_response:
        lines.append("from df_test_framework.models.responses import BaseResponse")

    lines.append("")
    lines.append("")

    # 嵌套类(按依赖顺序)
    for nested_class in reversed(nested_classes):
        lines.append(nested_class)
        lines.append("")
        lines.append("")

    # 主数据类
    lines.append(main_class_code)
    lines.append("")
    lines.append("")

    # 响应包装类
    if wrap_in_base_response:
        lines.append(f"class {model_name}(BaseResponse[{data_class_name}]):")
        lines.append('    """响应模型"""')
        lines.append("    pass")

    code = "\n".join(lines)

    # 写入文件
    if output_file:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(code, encoding="utf-8")
        print("\n✅ 模型文件生成成功！")
        print(f"📁 文件路径: {output_file}")

    return code


__all__ = [
    "generate_pydantic_model_from_json",
    "infer_python_type",
    "generate_model_class",
]
