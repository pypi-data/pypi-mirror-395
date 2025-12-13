"""测试 Redis Mock"""

import pytest

from df_test_framework.testing.mocking import FAKEREDIS_AVAILABLE, RedisMocker


class TestRedisMocker:
    """测试 RedisMocker"""

    def test_context_manager(self) -> None:
        """测试上下文管理器"""
        with RedisMocker(use_fakeredis=False) as redis_mock:
            assert redis_mock.mock_client is not None

    def test_simple_mock_get_set(self) -> None:
        """测试简单 Mock 的 GET/SET"""
        with RedisMocker(use_fakeredis=False) as redis_mock:
            redis_mock.mock_client.set("key", "value")
            result = redis_mock.mock_client.get("key")
            assert result == "value"

    def test_simple_mock_delete(self) -> None:
        """测试简单 Mock 的 DELETE"""
        with RedisMocker(use_fakeredis=False) as redis_mock:
            redis_mock.mock_client.set("key1", "value1")
            redis_mock.mock_client.set("key2", "value2")

            count = redis_mock.mock_client.delete("key1")
            assert count == 1
            assert redis_mock.mock_client.get("key1") is None
            assert redis_mock.mock_client.get("key2") == "value2"

    def test_simple_mock_exists(self) -> None:
        """测试简单 Mock 的 EXISTS"""
        with RedisMocker(use_fakeredis=False) as redis_mock:
            redis_mock.mock_client.set("key", "value")

            assert redis_mock.mock_client.exists("key") == 1
            assert redis_mock.mock_client.exists("nonexistent") == 0

    def test_simple_mock_keys(self) -> None:
        """测试简单 Mock 的 KEYS"""
        with RedisMocker(use_fakeredis=False) as redis_mock:
            redis_mock.mock_client.set("key1", "value1")
            redis_mock.mock_client.set("key2", "value2")

            keys = redis_mock.mock_client.keys()
            assert set(keys) == {"key1", "key2"}

    def test_simple_mock_hash_operations(self) -> None:
        """测试简单 Mock 的 Hash 操作"""
        with RedisMocker(use_fakeredis=False) as redis_mock:
            # HSET
            redis_mock.mock_client.hset("user:1", "name", "Alice")
            redis_mock.mock_client.hset("user:1", "age", "30")

            # HGET
            assert redis_mock.mock_client.hget("user:1", "name") == "Alice"

            # HGETALL
            user_data = redis_mock.mock_client.hgetall("user:1")
            assert user_data == {"name": "Alice", "age": "30"}

            # HDEL
            count = redis_mock.mock_client.hdel("user:1", "age")
            assert count == 1
            assert redis_mock.mock_client.hget("user:1", "age") is None

    def test_simple_mock_list_operations(self) -> None:
        """测试简单 Mock 的 List 操作"""
        with RedisMocker(use_fakeredis=False) as redis_mock:
            # RPUSH
            redis_mock.mock_client.rpush("queue", "item1", "item2")
            assert redis_mock.mock_client.llen("queue") == 2

            # LPUSH
            redis_mock.mock_client.lpush("queue", "item0")
            assert redis_mock.mock_client.llen("queue") == 3

            # LRANGE
            items = redis_mock.mock_client.lrange("queue", 0, -1)
            assert items == ["item0", "item1", "item2"]

            # LPOP
            item = redis_mock.mock_client.lpop("queue")
            assert item == "item0"

            # RPOP
            item = redis_mock.mock_client.rpop("queue")
            assert item == "item2"

    def test_simple_mock_set_operations(self) -> None:
        """测试简单 Mock 的 Set 操作"""
        with RedisMocker(use_fakeredis=False) as redis_mock:
            # SADD
            count = redis_mock.mock_client.sadd("tags", "python", "testing")
            assert count == 2

            # SMEMBERS
            members = redis_mock.mock_client.smembers("tags")
            assert members == {"python", "testing"}

            # SREM
            count = redis_mock.mock_client.srem("tags", "python")
            assert count == 1

            members = redis_mock.mock_client.smembers("tags")
            assert members == {"testing"}

    def test_reset(self) -> None:
        """测试重置"""
        with RedisMocker(use_fakeredis=False) as redis_mock:
            redis_mock.mock_client.set("key", "value")

            redis_mock.reset()

            assert redis_mock.mock_client.get("key") is None

    @pytest.mark.skipif(not FAKEREDIS_AVAILABLE, reason="fakeredis not installed")
    def test_fakeredis_integration(self) -> None:
        """测试 fakeredis 集成（如果可用）"""
        with RedisMocker(use_fakeredis=True) as redis_mock:
            redis_mock.mock_client.set("counter", 0)
            redis_mock.mock_client.incr("counter")
            redis_mock.mock_client.incr("counter")

            assert int(redis_mock.mock_client.get("counter")) == 2

    # ========== 新增测试：计数器操作 ==========

    def test_incr_decr(self) -> None:
        """测试 INCR/DECR 命令"""
        with RedisMocker(use_fakeredis=False) as redis_mock:
            # 从 0 开始
            assert redis_mock.mock_client.incr("counter") == 1
            assert redis_mock.mock_client.incr("counter") == 2

            # DECR
            assert redis_mock.mock_client.decr("counter") == 1
            assert redis_mock.mock_client.decr("counter") == 0
            assert redis_mock.mock_client.decr("counter") == -1

    def test_incrby_decrby(self) -> None:
        """测试 INCRBY/DECRBY 命令"""
        with RedisMocker(use_fakeredis=False) as redis_mock:
            redis_mock.mock_client.set("counter", 10)

            assert redis_mock.mock_client.incrby("counter", 5) == 15
            assert redis_mock.mock_client.decrby("counter", 3) == 12

    def test_incrbyfloat(self) -> None:
        """测试 INCRBYFLOAT 命令"""
        with RedisMocker(use_fakeredis=False) as redis_mock:
            redis_mock.mock_client.set("price", 10.5)

            result = redis_mock.mock_client.incrbyfloat("price", 0.1)
            assert abs(result - 10.6) < 0.001

    # ========== 新增测试：过期时间操作 ==========

    def test_setex(self) -> None:
        """测试 SETEX 命令"""
        with RedisMocker(use_fakeredis=False) as redis_mock:
            redis_mock.mock_client.setex("temp_key", 3600, "temp_value")

            assert redis_mock.mock_client.get("temp_key") == "temp_value"
            ttl = redis_mock.mock_client.ttl("temp_key")
            assert 0 < ttl <= 3600

    def test_expire_ttl(self) -> None:
        """测试 EXPIRE/TTL 命令"""
        with RedisMocker(use_fakeredis=False) as redis_mock:
            redis_mock.mock_client.set("key", "value")

            # 没有过期时间
            assert redis_mock.mock_client.ttl("key") == -1

            # 设置过期时间
            result = redis_mock.mock_client.expire("key", 100)
            assert result is True

            ttl = redis_mock.mock_client.ttl("key")
            assert 0 < ttl <= 100

    def test_ttl_nonexistent_key(self) -> None:
        """测试不存在的键的 TTL"""
        with RedisMocker(use_fakeredis=False) as redis_mock:
            assert redis_mock.mock_client.ttl("nonexistent") == -2

    def test_persist(self) -> None:
        """测试 PERSIST 命令"""
        with RedisMocker(use_fakeredis=False) as redis_mock:
            redis_mock.mock_client.setex("key", 100, "value")

            # 移除过期时间
            result = redis_mock.mock_client.persist("key")
            assert result is True

            # 现在应该没有过期时间
            assert redis_mock.mock_client.ttl("key") == -1

    # ========== 新增测试：批量操作 ==========

    def test_mget(self) -> None:
        """测试 MGET 命令"""
        with RedisMocker(use_fakeredis=False) as redis_mock:
            redis_mock.mock_client.set("key1", "value1")
            redis_mock.mock_client.set("key2", "value2")

            values = redis_mock.mock_client.mget("key1", "key2", "key3")
            assert values == ["value1", "value2", None]

    def test_mset(self) -> None:
        """测试 MSET 命令"""
        with RedisMocker(use_fakeredis=False) as redis_mock:
            redis_mock.mock_client.mset({"key1": "value1", "key2": "value2"})

            assert redis_mock.mock_client.get("key1") == "value1"
            assert redis_mock.mock_client.get("key2") == "value2"

    # ========== 新增测试：Hash 扩展操作 ==========

    def test_hexists(self) -> None:
        """测试 HEXISTS 命令"""
        with RedisMocker(use_fakeredis=False) as redis_mock:
            redis_mock.mock_client.hset("user:1", "name", "Alice")

            assert redis_mock.mock_client.hexists("user:1", "name") is True
            assert redis_mock.mock_client.hexists("user:1", "age") is False

    def test_hlen(self) -> None:
        """测试 HLEN 命令"""
        with RedisMocker(use_fakeredis=False) as redis_mock:
            redis_mock.mock_client.hset("user:1", "name", "Alice")
            redis_mock.mock_client.hset("user:1", "age", "30")

            assert redis_mock.mock_client.hlen("user:1") == 2
            assert redis_mock.mock_client.hlen("nonexistent") == 0

    def test_hkeys_hvals(self) -> None:
        """测试 HKEYS/HVALS 命令"""
        with RedisMocker(use_fakeredis=False) as redis_mock:
            redis_mock.mock_client.hset("user:1", "name", "Alice")
            redis_mock.mock_client.hset("user:1", "age", "30")

            keys = redis_mock.mock_client.hkeys("user:1")
            assert set(keys) == {"name", "age"}

            vals = redis_mock.mock_client.hvals("user:1")
            assert set(vals) == {"Alice", "30"}

    # ========== 新增测试：Set 扩展操作 ==========

    def test_sismember(self) -> None:
        """测试 SISMEMBER 命令"""
        with RedisMocker(use_fakeredis=False) as redis_mock:
            redis_mock.mock_client.sadd("tags", "python", "testing")

            assert redis_mock.mock_client.sismember("tags", "python") is True
            assert redis_mock.mock_client.sismember("tags", "java") is False

    def test_scard(self) -> None:
        """测试 SCARD 命令"""
        with RedisMocker(use_fakeredis=False) as redis_mock:
            redis_mock.mock_client.sadd("tags", "python", "testing")

            assert redis_mock.mock_client.scard("tags") == 2
            assert redis_mock.mock_client.scard("nonexistent") == 0

    # ========== 新增测试：字符串扩展操作 ==========

    def test_append(self) -> None:
        """测试 APPEND 命令"""
        with RedisMocker(use_fakeredis=False) as redis_mock:
            redis_mock.mock_client.set("greeting", "Hello")
            length = redis_mock.mock_client.append("greeting", " World")

            assert length == 11
            assert redis_mock.mock_client.get("greeting") == "Hello World"

    def test_strlen(self) -> None:
        """测试 STRLEN 命令"""
        with RedisMocker(use_fakeredis=False) as redis_mock:
            redis_mock.mock_client.set("key", "Hello")

            assert redis_mock.mock_client.strlen("key") == 5
            assert redis_mock.mock_client.strlen("nonexistent") == 0

    def test_getset(self) -> None:
        """测试 GETSET 命令"""
        with RedisMocker(use_fakeredis=False) as redis_mock:
            redis_mock.mock_client.set("key", "old_value")

            old = redis_mock.mock_client.getset("key", "new_value")
            assert old == "old_value"
            assert redis_mock.mock_client.get("key") == "new_value"

    def test_setnx(self) -> None:
        """测试 SETNX 命令"""
        with RedisMocker(use_fakeredis=False) as redis_mock:
            # 键不存在时设置成功
            result = redis_mock.mock_client.setnx("key", "value")
            assert result is True
            assert redis_mock.mock_client.get("key") == "value"

            # 键存在时设置失败
            result = redis_mock.mock_client.setnx("key", "new_value")
            assert result is False
            assert redis_mock.mock_client.get("key") == "value"

    # ========== 新增测试：TYPE 命令 ==========

    def test_type(self) -> None:
        """测试 TYPE 命令"""
        with RedisMocker(use_fakeredis=False) as redis_mock:
            # string
            redis_mock.mock_client.set("string_key", "value")
            assert redis_mock.mock_client.type("string_key") == "string"

            # list
            redis_mock.mock_client.rpush("list_key", "item")
            assert redis_mock.mock_client.type("list_key") == "list"

            # set
            redis_mock.mock_client.sadd("set_key", "member")
            assert redis_mock.mock_client.type("set_key") == "set"

            # hash
            redis_mock.mock_client.hset("hash_key", "field", "value")
            assert redis_mock.mock_client.type("hash_key") == "hash"

            # nonexistent
            assert redis_mock.mock_client.type("nonexistent") == "none"

    # ========== 新增测试：KEYS 模式匹配 ==========

    def test_keys_pattern(self) -> None:
        """测试 KEYS 命令的模式匹配"""
        with RedisMocker(use_fakeredis=False) as redis_mock:
            redis_mock.mock_client.set("user:1", "Alice")
            redis_mock.mock_client.set("user:2", "Bob")
            redis_mock.mock_client.set("order:1", "Order1")

            # 匹配所有
            all_keys = redis_mock.mock_client.keys("*")
            assert set(all_keys) == {"user:1", "user:2", "order:1"}

            # 匹配 user:* 模式
            user_keys = redis_mock.mock_client.keys("user:*")
            assert set(user_keys) == {"user:1", "user:2"}

            # 匹配 order:* 模式
            order_keys = redis_mock.mock_client.keys("order:*")
            assert order_keys == ["order:1"]
