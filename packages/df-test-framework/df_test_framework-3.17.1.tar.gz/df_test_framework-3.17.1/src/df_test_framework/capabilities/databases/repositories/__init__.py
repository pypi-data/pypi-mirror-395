"""Repository模块 - 数据访问层抽象

v1.3.0 新增:
- Repository模式封装数据访问逻辑
- 提高可测试性和代码可维护性

使用示例:
    from df_test_framework.repositories import BaseRepository
    from df_test_framework.core.database import Database

    class CardRepository(BaseRepository):
        '''卡片数据仓库'''

        def __init__(self, db: Database):
            super().__init__(db, table_name="card_inventory")

        def find_by_card_no(self, card_no: str):
            '''根据卡号查找卡片'''
            return self.find_one({"card_no": card_no})

        def find_active_cards(self):
            '''查找所有激活的卡片'''
            return self.find_all({"status": "ACTIVE"})

        def activate_card(self, card_no: str):
            '''激活卡片'''
            return self.update(
                {"card_no": card_no},
                {"status": "ACTIVE", "activated_at": "NOW()"}
            )

    # 在测试中使用
    def test_card_operations(db_fixture):
        repo = CardRepository(db_fixture)

        # 查找卡片
        card = repo.find_by_card_no("CARD001")

        # 激活卡片
        repo.activate_card("CARD001")

        # 查找所有激活的卡片
        active_cards = repo.find_active_cards()

更多示例请参考文档: docs/guides/使用示例.md
"""

from .base import BaseRepository
from .query_spec import (
    CompoundCondition,
    Operator,
    QueryCondition,
    QuerySpec,
    SimpleCondition,
    WhereClause,
)

__all__ = [
    "BaseRepository",
    # Query Builder (v1.4.0 新增)
    "QuerySpec",
    "QueryCondition",
    "SimpleCondition",
    "CompoundCondition",
    "Operator",
    "WhereClause",
]
