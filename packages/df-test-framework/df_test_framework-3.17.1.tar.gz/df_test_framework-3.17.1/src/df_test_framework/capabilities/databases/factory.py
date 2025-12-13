"""数据库工厂

提供统一的数据库客户端创建接口
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from df_test_framework.infrastructure.config.schema import DatabaseConfig, RedisConfig

if TYPE_CHECKING:
    from .database import Database
    from .redis.redis_client import RedisClient

DatabaseType = Literal["mysql", "postgresql", "sqlite", "redis", "mongodb", "elasticsearch"]


class DatabaseFactory:
    """数据库工厂

    根据配置创建合适的数据库客户端

    Examples:
        >>> # 创建MySQL数据库
        >>> db = DatabaseFactory.create_mysql("mysql://user:pass@localhost/db")
        >>>
        >>> # 创建Redis客户端
        >>> redis = DatabaseFactory.create_redis(host="localhost", port=6379)
        >>>
        >>> # 使用配置对象
        >>> config = DatabaseConfig(connection_string="mysql://...")
        >>> db = DatabaseFactory.create_database(config)
    """

    @staticmethod
    def create_mysql(
        connection_string: str,
        allowed_tables: set[str] | None = None,
    ) -> Database:
        """创建MySQL数据库客户端

        Args:
            connection_string: MySQL连接字符串
            allowed_tables: 允许操作的表名白名单

        Returns:
            Database实例
        """
        # ✅ Bug修复: 正确的导入路径（database.py在databases/目录下）
        from .database import Database

        # ✅ Bug修复: Database接受allowed_tables但DatabaseConfig不接受
        # 直接调用Database构造函数
        return Database(
            connection_string=connection_string,
            allowed_tables=allowed_tables,
        )

    @staticmethod
    def create_postgresql(
        connection_string: str,
        allowed_tables: set[str] | None = None,
    ) -> Database:
        """创建PostgreSQL数据库客户端

        Args:
            connection_string: PostgreSQL连接字符串
            allowed_tables: 允许操作的表名白名单

        Returns:
            Database实例
        """
        # ✅ Bug修复: 正确的导入路径（database.py在databases/目录下）
        from .database import Database

        # ✅ Bug修复: Database接受allowed_tables但DatabaseConfig不接受
        # 直接调用Database构造函数
        return Database(
            connection_string=connection_string,
            allowed_tables=allowed_tables,
        )

    @staticmethod
    def create_sqlite(
        database_path: str = ":memory:",
        allowed_tables: set[str] | None = None,
    ) -> Database:
        """创建SQLite数据库客户端

        Args:
            database_path: 数据库文件路径，默认为内存数据库
            allowed_tables: 允许操作的表名白名单

        Returns:
            Database实例
        """
        # ✅ Bug修复: 正确的导入路径（database.py在databases/目录下）
        from .database import Database

        # ✅ Bug修复: Database接受allowed_tables但DatabaseConfig不接受
        # 直接调用Database构造函数
        connection_string = f"sqlite:///{database_path}"
        return Database(
            connection_string=connection_string,
            allowed_tables=allowed_tables,
        )

    @staticmethod
    def create_redis(
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: str | None = None,
        **kwargs,
    ) -> RedisClient:
        """创建Redis客户端

        Args:
            host: Redis主机
            port: Redis端口
            db: 数据库编号
            password: 密码
            **kwargs: 其他Redis配置

        Returns:
            RedisClient实例
        """
        # ✅ Bug修复: 正确的导入路径（redis/目录下）
        from df_test_framework.infrastructure.config.schema import RedisConfig

        from .redis.redis_client import RedisClient

        config = RedisConfig(
            host=host,
            port=port,
            db=db,
            password=password,
            **kwargs,
        )
        return RedisClient(config)

    @staticmethod
    def create_mongodb(connection_string: str, **kwargs):
        """创建MongoDB客户端（预留）

        Args:
            connection_string: MongoDB连接字符串
            **kwargs: 其他配置

        Returns:
            MongoClient实例

        Raises:
            NotImplementedError: 功能尚未实现
        """
        raise NotImplementedError("MongoDB客户端尚未实现。请提交PR实现MongoDB适配器。")

    @staticmethod
    def create_elasticsearch(hosts: list, **kwargs):
        """创建Elasticsearch客户端（预留）

        Args:
            hosts: ES主机列表
            **kwargs: 其他配置

        Returns:
            ElasticsearchClient实例

        Raises:
            NotImplementedError: 功能尚未实现
        """
        raise NotImplementedError("Elasticsearch客户端尚未实现。请提交PR实现Elasticsearch适配器。")

    @staticmethod
    def create_database(config: DatabaseConfig) -> Database:
        """使用配置对象创建SQL数据库客户端

        Args:
            config: 数据库配置

        Returns:
            Database实例
        """
        # ✅ Bug修复: 正确的导入路径（database.py在databases/目录下）
        from .database import Database

        return Database(config)

    @staticmethod
    def create_redis_client(config: RedisConfig) -> RedisClient:
        """使用配置对象创建Redis客户端

        Args:
            config: Redis配置

        Returns:
            RedisClient实例
        """
        # ✅ Bug修复: 正确的导入路径（redis/目录下）
        from .redis.redis_client import RedisClient

        return RedisClient(config)
