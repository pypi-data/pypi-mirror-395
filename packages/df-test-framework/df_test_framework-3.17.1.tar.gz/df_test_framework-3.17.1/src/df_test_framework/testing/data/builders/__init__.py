"""Builder模块 - 测试数据构建器

v1.3.0 新增:
- Builder模式简化测试数据构建
- 提供流畅的API,提升测试可读性

使用示例:
    from df_test_framework.builders import BaseBuilder, DictBuilder

    # 方式1: 继承BaseBuilder
    class CardRequestBuilder(BaseBuilder):
        def __init__(self):
            self.data = {
                "user_id": "default_user",
                "template_id": "default_template",
                "quantity": 1
            }

        def with_user(self, user_id: str):
            self.data["user_id"] = user_id
            return self

        def with_quantity(self, quantity: int):
            self.data["quantity"] = quantity
            return self

        def build(self) -> dict:
            return self.data

    # 使用继承方式
    request = CardRequestBuilder().with_user("user_001").with_quantity(5).build()

    # 方式2: 直接使用DictBuilder (更简单)
    request = (
        DictBuilder()
        .set("user_id", "user_001")
        .set("template_id", "template_001")
        .set("quantity", 5)
        .build()
    )

更多示例请参考文档: docs/guides/使用示例.md
"""

from .base import BaseBuilder, DictBuilder

__all__ = [
    "BaseBuilder",
    "DictBuilder",
]
