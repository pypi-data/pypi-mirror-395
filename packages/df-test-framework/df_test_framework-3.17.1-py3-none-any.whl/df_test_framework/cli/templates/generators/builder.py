"""Builder类生成模板"""

GEN_BUILDER_TEMPLATE = """\"\"\"Builder: {entity_name}

使用Builder模式构建{entity_name}测试数据。
\"\"\"

from df_test_framework import DictBuilder
from typing import Any, Dict


class {EntityName}Builder(DictBuilder):
    \"\"\"{EntityName}数据构建器

    使用链式调用构建{entity_name}数据。

    Example:
        >>> builder = {EntityName}Builder()
        >>> data = (
        ...     builder
        ...     .with_name("示例名称")
        ...     .with_status("active")
        ...     .build()
        ... )
    \"\"\"

    def __init__(self):
        \"\"\"初始化Builder，设置默认值\"\"\"
        super().__init__()
        self._data = {{
            "name": "{entity_name}_default",
            "status": "active",
            "created_at": None,
            "updated_at": None,
        }}

    def with_name(self, name: str) -> "{EntityName}Builder":
        \"\"\"设置名称

        Args:
            name: 名称

        Returns:
            self: 支持链式调用
        \"\"\"
        self._data["name"] = name
        return self

    def with_status(self, status: str) -> "{EntityName}Builder":
        \"\"\"设置状态

        Args:
            status: 状态（如: active, inactive）

        Returns:
            self: 支持链式调用
        \"\"\"
        self._data["status"] = status
        return self

    # TODO: 添加更多字段的设置方法
    # def with_xxx(self, xxx: Any) -> "{EntityName}Builder":
    #     \"\"\"设置xxx\"\"\"
    #     self._data["xxx"] = xxx
    #     return self


__all__ = ["{EntityName}Builder"]
"""

__all__ = ["GEN_BUILDER_TEMPLATE"]
