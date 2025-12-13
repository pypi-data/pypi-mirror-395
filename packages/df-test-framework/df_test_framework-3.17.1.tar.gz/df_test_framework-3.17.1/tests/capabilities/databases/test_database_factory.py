"""测试DatabaseFactory

验证Factory类正确创建Database和RedisClient实例，修复导入路径bug
"""

from unittest.mock import patch

import pytest

from df_test_framework.capabilities.databases.factory import DatabaseFactory
from df_test_framework.infrastructure.config.schema import (
    DatabaseConfig,
    RedisConfig,
)


class TestDatabaseFactory:
    """测试DatabaseFactory"""

    def test_create_mysql(self):
        """测试创建MySQL数据库客户端"""
        # ✅ Bug修复验证: 确保可以正确导入Database类
        connection_string = "mysql+pymysql://user:pass@localhost:3306/testdb"

        with patch(
            "df_test_framework.capabilities.databases.database.Database.__init__",
            return_value=None,
        ) as mock_init:
            DatabaseFactory.create_mysql(connection_string)

            # 验证Database构造函数被调用
            mock_init.assert_called_once()
            # ✅ Bug修复验证: 确保connection_string正确传递
            call_args = mock_init.call_args
            assert call_args[1]["connection_string"] == connection_string
            assert call_args[1]["allowed_tables"] is None

    def test_create_mysql_with_allowed_tables(self):
        """测试创建MySQL数据库客户端（带表名白名单）"""
        connection_string = "mysql+pymysql://user:pass@localhost:3306/testdb"
        allowed_tables = {"users", "orders"}

        with patch(
            "df_test_framework.capabilities.databases.database.Database.__init__",
            return_value=None,
        ) as mock_init:
            DatabaseFactory.create_mysql(connection_string, allowed_tables=allowed_tables)

            # 验证allowed_tables正确传递
            call_args = mock_init.call_args
            assert call_args[1]["connection_string"] == connection_string
            assert call_args[1]["allowed_tables"] == allowed_tables

    def test_create_postgresql(self):
        """测试创建PostgreSQL数据库客户端"""
        # ✅ Bug修复验证: 确保可以正确导入Database类
        connection_string = "postgresql://user:pass@localhost:5432/testdb"

        with patch(
            "df_test_framework.capabilities.databases.database.Database.__init__",
            return_value=None,
        ) as mock_init:
            DatabaseFactory.create_postgresql(connection_string)

            # 验证Database构造函数被调用
            mock_init.assert_called_once()
            call_args = mock_init.call_args
            assert call_args[1]["connection_string"] == connection_string

    def test_create_sqlite_default_memory(self):
        """测试创建SQLite数据库客户端（默认内存数据库）"""
        # ✅ Bug修复验证: 确保可以正确导入Database类
        with patch(
            "df_test_framework.capabilities.databases.database.Database.__init__",
            return_value=None,
        ) as mock_init:
            DatabaseFactory.create_sqlite()

            # 验证Database构造函数被调用
            mock_init.assert_called_once()
            call_args = mock_init.call_args
            # 默认使用内存数据库
            assert call_args[1]["connection_string"] == "sqlite:///:memory:"

    def test_create_sqlite_with_file_path(self):
        """测试创建SQLite数据库客户端（文件数据库）"""
        database_path = "/tmp/test.db"

        with patch(
            "df_test_framework.capabilities.databases.database.Database.__init__",
            return_value=None,
        ) as mock_init:
            DatabaseFactory.create_sqlite(database_path)

            # 验证connection_string正确构建
            call_args = mock_init.call_args
            assert call_args[1]["connection_string"] == f"sqlite:///{database_path}"

    def test_create_redis_default(self):
        """测试创建Redis客户端（默认配置）"""
        # ✅ Bug修复验证: 确保可以正确导入RedisClient类
        with patch(
            "df_test_framework.capabilities.databases.redis.redis_client.RedisClient.__init__",
            return_value=None,
        ) as mock_init:
            DatabaseFactory.create_redis()

            # 验证RedisClient构造函数被调用
            mock_init.assert_called_once()
            call_args = mock_init.call_args[0]
            config = call_args[0]

            # 验证默认配置
            assert isinstance(config, RedisConfig)
            assert config.host == "localhost"
            assert config.port == 6379
            assert config.db == 0

    def test_create_redis_custom(self):
        """测试创建Redis客户端（自定义配置）"""
        with patch(
            "df_test_framework.capabilities.databases.redis.redis_client.RedisClient.__init__",
            return_value=None,
        ) as mock_init:
            DatabaseFactory.create_redis(
                host="redis.example.com",
                port=6380,
                db=5,
                password="secret",
            )

            # 验证自定义配置
            call_args = mock_init.call_args[0]
            config = call_args[0]

            assert config.host == "redis.example.com"
            assert config.port == 6380
            assert config.db == 5
            assert config.password.get_secret_value() == "secret"

    def test_create_database_with_config(self):
        """测试使用DatabaseConfig创建数据库客户端"""
        config = DatabaseConfig(
            connection_string="mysql+pymysql://user:pass@localhost:3306/testdb",
            pool_size=20,
        )

        with patch(
            "df_test_framework.capabilities.databases.database.Database.__init__",
            return_value=None,
        ) as mock_init:
            DatabaseFactory.create_database(config)

            # 验证Database构造函数被调用，且config正确传递
            mock_init.assert_called_once_with(config)

    def test_create_redis_client_with_config(self):
        """测试使用RedisConfig创建Redis客户端"""
        config = RedisConfig(
            host="redis.example.com",
            port=6380,
            db=3,
        )

        with patch(
            "df_test_framework.capabilities.databases.redis.redis_client.RedisClient.__init__",
            return_value=None,
        ) as mock_init:
            DatabaseFactory.create_redis_client(config)

            # 验证RedisClient构造函数被调用，且config正确传递
            mock_init.assert_called_once_with(config)

    def test_create_mongodb_not_implemented(self):
        """测试MongoDB客户端未实现"""
        with pytest.raises(NotImplementedError, match="MongoDB客户端尚未实现"):
            DatabaseFactory.create_mongodb("mongodb://localhost:27017/testdb")

    def test_create_elasticsearch_not_implemented(self):
        """测试Elasticsearch客户端未实现"""
        with pytest.raises(NotImplementedError, match="Elasticsearch客户端尚未实现"):
            DatabaseFactory.create_elasticsearch(["localhost:9200"])


class TestImportPaths:
    """测试导入路径修复"""

    def test_database_import_path(self):
        """测试Database类导入路径正确"""
        # ✅ Bug修复验证: 确保从正确的路径导入Database
        try:
            from df_test_framework.capabilities.databases.database import Database

            assert Database is not None
        except ImportError as e:
            pytest.fail(f"Database import failed: {e}")

    def test_redis_client_import_path(self):
        """测试RedisClient类导入路径正确"""
        # ✅ Bug修复验证: 确保从正确的路径导入RedisClient
        try:
            from df_test_framework.capabilities.databases.redis.redis_client import RedisClient

            assert RedisClient is not None
        except ImportError as e:
            pytest.fail(f"RedisClient import failed: {e}")

    def test_factory_can_import_database(self):
        """测试Factory内部可以导入Database"""
        # 这个测试验证factory.py中的import语句是否正确
        from df_test_framework.capabilities.databases import factory

        # 通过调用create_mysql来触发import
        with patch(
            "df_test_framework.capabilities.databases.database.Database.__init__",
            return_value=None,
        ):
            try:
                factory.DatabaseFactory.create_mysql("mysql+pymysql://user:pass@localhost/db")
            except ImportError as e:
                pytest.fail(f"Factory failed to import Database: {e}")

    def test_factory_can_import_redis_client(self):
        """测试Factory内部可以导入RedisClient"""
        # 这个测试验证factory.py中的import语句是否正确
        from df_test_framework.capabilities.databases import factory

        # 通过调用create_redis来触发import
        with patch(
            "df_test_framework.capabilities.databases.redis.redis_client.RedisClient.__init__",
            return_value=None,
        ):
            try:
                factory.DatabaseFactory.create_redis()
            except ImportError as e:
                pytest.fail(f"Factory failed to import RedisClient: {e}")
