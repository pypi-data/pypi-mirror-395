"""数据访问能力层 - Layer 1

提供SQL、NoSQL等数据库访问能力
按数据库类型扁平化组织：mysql/、postgresql/、redis/、mongodb/等

v3.13.0 变更:
- UnitOfWork 支持配置驱动（repository_package 通过配置指定）
- 移除 BaseUnitOfWork（直接使用 UnitOfWork）

v3.11.1 新增:
- QueryBuilder：流式查询构建器（P2-2）
"""

# 工厂类
# 通用Database类（支持MySQL/PostgreSQL/SQLite等）
from .database import Database
from .factory import DatabaseFactory

# Query Builder（v3.11.1 P2-2）
from .query_builder import QueryBuilder

# Redis客户端
from .redis.redis_client import RedisClient

# Repository模式
from .repositories.base import BaseRepository
from .repositories.query_spec import QuerySpec

# Unit of Work 模式
from .uow import UnitOfWork

__all__ = [
    # 工厂
    "DatabaseFactory",
    # 通用Database
    "Database",
    # Unit of Work
    "UnitOfWork",
    # Repository模式
    "BaseRepository",
    "QuerySpec",
    # Query Builder
    "QueryBuilder",
    # Redis
    "RedisClient",
]
