"""
测试RedisClient

验证Redis客户端的各种操作方法。
v3.18.0: 新增 EventBus 集成测试
"""

from unittest.mock import Mock, patch

import pytest

from df_test_framework.capabilities.databases.redis.redis_client import RedisClient
from df_test_framework.core.events import (
    CacheOperationEndEvent,
    CacheOperationErrorEvent,
    CacheOperationStartEvent,
)
from df_test_framework.infrastructure.events import EventBus


class TestRedisClientInit:
    """测试RedisClient初始化"""

    @patch("redis.ConnectionPool")
    @patch("redis.Redis")
    def test_client_creation_default(self, mock_redis, mock_pool):
        """测试使用默认配置创建"""
        client = RedisClient()

        assert client.host == "localhost"
        assert client.port == 6379
        assert client.db == 0

        # 验证连接池被创建
        mock_pool.assert_called_once()

        client.close()

    @patch("redis.ConnectionPool")
    @patch("redis.Redis")
    def test_client_creation_custom(self, mock_redis, mock_pool):
        """测试使用自定义配置创建"""
        client = RedisClient(
            host="redis.example.com",
            port=6380,
            db=1,
            password="secret",
            max_connections=100,
        )

        assert client.host == "redis.example.com"
        assert client.port == 6380
        assert client.db == 1

        # 验证连接池被创建时使用了正确的参数
        mock_pool.assert_called_once()
        call_kwargs = mock_pool.call_args[1]
        assert call_kwargs["host"] == "redis.example.com"
        assert call_kwargs["port"] == 6380
        assert call_kwargs["db"] == 1
        assert call_kwargs["password"] == "secret"
        assert call_kwargs["max_connections"] == 100

        client.close()


class TestRedisClientPing:
    """测试ping方法"""

    @patch("redis.ConnectionPool")
    @patch("redis.Redis")
    def test_ping_success(self, mock_redis, mock_pool):
        """测试ping成功"""
        mock_client = Mock()
        mock_client.ping.return_value = True
        mock_redis.return_value = mock_client

        client = RedisClient()
        result = client.ping()

        assert result is True
        mock_client.ping.assert_called_once()

        client.close()

    @patch("redis.ConnectionPool")
    @patch("redis.Redis")
    def test_ping_failure(self, mock_redis, mock_pool):
        """测试ping失败"""
        mock_client = Mock()
        mock_client.ping.side_effect = Exception("Connection failed")
        mock_redis.return_value = mock_client

        client = RedisClient()
        result = client.ping()

        assert result is False

        client.close()


class TestRedisClientStringOperations:
    """测试字符串操作"""

    def setup_method(self):
        """每个测试前创建mock client"""
        with patch("redis.ConnectionPool"), patch("redis.Redis") as mock_redis:
            self.mock_client = Mock()
            mock_redis.return_value = self.mock_client
            self.client = RedisClient()

    def test_set(self):
        """测试set方法"""
        self.mock_client.set.return_value = True

        result = self.client.set("key1", "value1")

        assert result is True
        self.mock_client.set.assert_called_once_with("key1", "value1", ex=None, nx=False)

    def test_set_with_expiration(self):
        """测试带过期时间的set"""
        self.mock_client.set.return_value = True

        result = self.client.set("key1", "value1", ex=60)

        assert result is True
        self.mock_client.set.assert_called_once_with("key1", "value1", ex=60, nx=False)

    def test_set_with_nx(self):
        """测试带nx标志的set"""
        self.mock_client.set.return_value = True

        result = self.client.set("key1", "value1", nx=True)

        assert result is True
        self.mock_client.set.assert_called_once_with("key1", "value1", ex=None, nx=True)

    def test_get(self):
        """测试get方法"""
        self.mock_client.get.return_value = "value1"

        result = self.client.get("key1")

        assert result == "value1"
        self.mock_client.get.assert_called_once_with("key1")

    def test_get_nonexistent(self):
        """测试获取不存在的键"""
        self.mock_client.get.return_value = None

        result = self.client.get("nonexistent")

        assert result is None

    def test_delete(self):
        """测试delete方法"""
        self.mock_client.delete.return_value = 1

        result = self.client.delete("key1")

        assert result == 1
        self.mock_client.delete.assert_called_once_with("key1")

    def test_delete_multiple(self):
        """测试删除多个键"""
        self.mock_client.delete.return_value = 2

        result = self.client.delete("key1", "key2")

        assert result == 2
        self.mock_client.delete.assert_called_once_with("key1", "key2")

    def test_exists(self):
        """测试exists方法"""
        self.mock_client.exists.return_value = 1

        result = self.client.exists("key1")

        assert result == 1
        self.mock_client.exists.assert_called_once_with("key1")

    def test_expire(self):
        """测试expire方法"""
        self.mock_client.expire.return_value = True

        result = self.client.expire("key1", 60)

        assert result is True
        self.mock_client.expire.assert_called_once_with("key1", 60)

    def test_ttl(self):
        """测试ttl方法"""
        self.mock_client.ttl.return_value = 60

        result = self.client.ttl("key1")

        assert result == 60
        self.mock_client.ttl.assert_called_once_with("key1")


class TestRedisClientHashOperations:
    """测试哈希操作"""

    def setup_method(self):
        """每个测试前创建mock client"""
        with patch("redis.ConnectionPool"), patch("redis.Redis") as mock_redis:
            self.mock_client = Mock()
            mock_redis.return_value = self.mock_client
            self.client = RedisClient()

    def test_hset(self):
        """测试hset方法"""
        self.mock_client.hset.return_value = 1

        result = self.client.hset("hash1", "field1", "value1")

        assert result == 1
        self.mock_client.hset.assert_called_once_with("hash1", "field1", "value1")

    def test_hget(self):
        """测试hget方法"""
        self.mock_client.hget.return_value = "value1"

        result = self.client.hget("hash1", "field1")

        assert result == "value1"
        self.mock_client.hget.assert_called_once_with("hash1", "field1")

    def test_hgetall(self):
        """测试hgetall方法"""
        self.mock_client.hgetall.return_value = {"field1": "value1", "field2": "value2"}

        result = self.client.hgetall("hash1")

        assert result == {"field1": "value1", "field2": "value2"}
        self.mock_client.hgetall.assert_called_once_with("hash1")

    def test_hdel(self):
        """测试hdel方法"""
        self.mock_client.hdel.return_value = 1

        result = self.client.hdel("hash1", "field1")

        assert result == 1
        self.mock_client.hdel.assert_called_once_with("hash1", "field1")


class TestRedisClientListOperations:
    """测试列表操作"""

    def setup_method(self):
        """每个测试前创建mock client"""
        with patch("redis.ConnectionPool"), patch("redis.Redis") as mock_redis:
            self.mock_client = Mock()
            mock_redis.return_value = self.mock_client
            self.client = RedisClient()

    def test_lpush(self):
        """测试lpush方法"""
        self.mock_client.lpush.return_value = 1

        result = self.client.lpush("list1", "value1")

        assert result == 1
        self.mock_client.lpush.assert_called_once_with("list1", "value1")

    def test_rpush(self):
        """测试rpush方法"""
        self.mock_client.rpush.return_value = 2

        result = self.client.rpush("list1", "value1", "value2")

        assert result == 2
        self.mock_client.rpush.assert_called_once_with("list1", "value1", "value2")

    def test_lpop(self):
        """测试lpop方法"""
        self.mock_client.lpop.return_value = "value1"

        result = self.client.lpop("list1")

        assert result == "value1"
        self.mock_client.lpop.assert_called_once_with("list1")

    def test_rpop(self):
        """测试rpop方法"""
        self.mock_client.rpop.return_value = "value1"

        result = self.client.rpop("list1")

        assert result == "value1"
        self.mock_client.rpop.assert_called_once_with("list1")

    def test_lrange(self):
        """测试lrange方法"""
        self.mock_client.lrange.return_value = ["value1", "value2", "value3"]

        result = self.client.lrange("list1", 0, -1)

        assert result == ["value1", "value2", "value3"]
        self.mock_client.lrange.assert_called_once_with("list1", 0, -1)


class TestRedisClientSetOperations:
    """测试集合操作"""

    def setup_method(self):
        """每个测试前创建mock client"""
        with patch("redis.ConnectionPool"), patch("redis.Redis") as mock_redis:
            self.mock_client = Mock()
            mock_redis.return_value = self.mock_client
            self.client = RedisClient()

    def test_sadd(self):
        """测试sadd方法"""
        self.mock_client.sadd.return_value = 2

        result = self.client.sadd("set1", "value1", "value2")

        assert result == 2
        self.mock_client.sadd.assert_called_once_with("set1", "value1", "value2")

    def test_smembers(self):
        """测试smembers方法"""
        self.mock_client.smembers.return_value = {"value1", "value2"}

        result = self.client.smembers("set1")

        assert result == {"value1", "value2"}
        self.mock_client.smembers.assert_called_once_with("set1")

    def test_srem(self):
        """测试srem方法"""
        self.mock_client.srem.return_value = 1

        result = self.client.srem("set1", "value1")

        assert result == 1
        self.mock_client.srem.assert_called_once_with("set1", "value1")


class TestRedisClientSortedSetOperations:
    """测试有序集合操作"""

    def setup_method(self):
        """每个测试前创建mock client"""
        with patch("redis.ConnectionPool"), patch("redis.Redis") as mock_redis:
            self.mock_client = Mock()
            mock_redis.return_value = self.mock_client
            self.client = RedisClient()

    def test_zadd(self):
        """测试zadd方法"""
        self.mock_client.zadd.return_value = 2

        result = self.client.zadd("zset1", {"value1": 1.0, "value2": 2.0})

        assert result == 2
        self.mock_client.zadd.assert_called_once_with("zset1", {"value1": 1.0, "value2": 2.0})

    def test_zrange(self):
        """测试zrange方法"""
        self.mock_client.zrange.return_value = ["value1", "value2"]

        result = self.client.zrange("zset1", 0, -1)

        assert result == ["value1", "value2"]
        self.mock_client.zrange.assert_called_once_with("zset1", 0, -1, withscores=False)

    def test_zrange_with_scores(self):
        """测试带分数的zrange"""
        self.mock_client.zrange.return_value = [("value1", 1.0), ("value2", 2.0)]

        result = self.client.zrange("zset1", 0, -1, withscores=True)

        assert result == [("value1", 1.0), ("value2", 2.0)]
        self.mock_client.zrange.assert_called_once_with("zset1", 0, -1, withscores=True)


class TestRedisClientGenericOperations:
    """测试通用操作"""

    def setup_method(self):
        """每个测试前创建mock client"""
        with patch("redis.ConnectionPool"), patch("redis.Redis") as mock_redis:
            self.mock_client = Mock()
            mock_redis.return_value = self.mock_client
            self.client = RedisClient()

    def test_keys_all(self):
        """测试keys获取所有键"""
        self.mock_client.keys.return_value = ["key1", "key2", "key3"]

        result = self.client.keys()

        assert result == ["key1", "key2", "key3"]
        self.mock_client.keys.assert_called_once_with("*")

    def test_keys_with_pattern(self):
        """测试keys使用模式匹配"""
        self.mock_client.keys.return_value = ["user:1", "user:2"]

        result = self.client.keys("user:*")

        assert result == ["user:1", "user:2"]
        self.mock_client.keys.assert_called_once_with("user:*")

    def test_flushdb(self):
        """测试flushdb清空数据库"""
        self.mock_client.flushdb.return_value = True

        result = self.client.flushdb()

        assert result is True
        self.mock_client.flushdb.assert_called_once()

    def test_close(self):
        """测试close关闭连接"""
        self.client.close()

        self.mock_client.close.assert_called_once()


# =============================================================================
# EventBus 集成测试 (v3.18.0)
# =============================================================================


class TestRedisClientEventBusIntegration:
    """测试 Redis 客户端 EventBus 事件发布"""

    @pytest.fixture
    def event_bus_and_events(self):
        """创建事件总线和事件收集器"""
        event_bus = EventBus()
        collected_events = []

        # 订阅所有缓存事件
        async def collect_event(event):
            collected_events.append(event)

        event_bus.subscribe(CacheOperationStartEvent, collect_event)
        event_bus.subscribe(CacheOperationEndEvent, collect_event)
        event_bus.subscribe(CacheOperationErrorEvent, collect_event)

        return event_bus, collected_events

    @pytest.fixture
    def redis_client_with_eventbus(self, event_bus_and_events):
        """创建带 EventBus 的 Redis 客户端"""
        event_bus, _ = event_bus_and_events

        with patch("redis.ConnectionPool"), patch("redis.Redis") as mock_redis:
            mock_client = Mock()
            mock_redis.return_value = mock_client
            client = RedisClient(event_bus=event_bus)
            client._mock_client = mock_client  # 保存 mock 引用
            yield client
            client.close()

    def test_set_publishes_events(self, redis_client_with_eventbus, event_bus_and_events):
        """测试 set 操作发布开始和结束事件"""
        _, collected_events = event_bus_and_events
        redis_client_with_eventbus._mock_client.set.return_value = True

        redis_client_with_eventbus.set("test_key", "test_value")

        # 验证发布了开始和结束事件
        assert len(collected_events) == 2

        start_event = collected_events[0]
        end_event = collected_events[1]

        assert isinstance(start_event, CacheOperationStartEvent)
        assert start_event.operation == "SET"
        assert start_event.key == "test_key"

        assert isinstance(end_event, CacheOperationEndEvent)
        assert end_event.operation == "SET"
        assert end_event.key == "test_key"
        assert end_event.success is True

        # 验证 correlation_id 关联
        assert start_event.correlation_id == end_event.correlation_id

    def test_get_hit_publishes_events(self, redis_client_with_eventbus, event_bus_and_events):
        """测试 get 命中发布事件（hit=True）"""
        _, collected_events = event_bus_and_events
        redis_client_with_eventbus._mock_client.get.return_value = "cached_value"

        result = redis_client_with_eventbus.get("hit_key")

        assert result == "cached_value"
        assert len(collected_events) == 2

        end_event = collected_events[1]
        assert isinstance(end_event, CacheOperationEndEvent)
        assert end_event.hit is True

    def test_get_miss_publishes_events(self, redis_client_with_eventbus, event_bus_and_events):
        """测试 get 未命中发布事件（hit=False）"""
        _, collected_events = event_bus_and_events
        redis_client_with_eventbus._mock_client.get.return_value = None

        result = redis_client_with_eventbus.get("miss_key")

        assert result is None
        assert len(collected_events) == 2

        end_event = collected_events[1]
        assert isinstance(end_event, CacheOperationEndEvent)
        assert end_event.hit is False

    def test_delete_publishes_events(self, redis_client_with_eventbus, event_bus_and_events):
        """测试 delete 操作发布事件"""
        _, collected_events = event_bus_and_events
        redis_client_with_eventbus._mock_client.delete.return_value = 1

        redis_client_with_eventbus.delete("del_key")

        assert len(collected_events) == 2

        start_event = collected_events[0]
        assert start_event.operation == "DELETE"

    def test_hset_publishes_events(self, redis_client_with_eventbus, event_bus_and_events):
        """测试 hset 操作发布事件（包含 field）"""
        _, collected_events = event_bus_and_events
        redis_client_with_eventbus._mock_client.hset.return_value = 1

        redis_client_with_eventbus.hset("hash_key", "field1", "value1")

        assert len(collected_events) == 2

        start_event = collected_events[0]
        assert start_event.operation == "HSET"
        assert start_event.key == "hash_key"
        assert start_event.field == "field1"

    def test_lpush_publishes_events(self, redis_client_with_eventbus, event_bus_and_events):
        """测试 lpush 操作发布事件"""
        _, collected_events = event_bus_and_events
        redis_client_with_eventbus._mock_client.lpush.return_value = 1

        redis_client_with_eventbus.lpush("list_key", "value1")

        assert len(collected_events) == 2

        start_event = collected_events[0]
        assert start_event.operation == "LPUSH"
        assert start_event.key == "list_key"

    def test_sadd_publishes_events(self, redis_client_with_eventbus, event_bus_and_events):
        """测试 sadd 操作发布事件"""
        _, collected_events = event_bus_and_events
        redis_client_with_eventbus._mock_client.sadd.return_value = 2

        redis_client_with_eventbus.sadd("set_key", "member1", "member2")

        assert len(collected_events) == 2

        start_event = collected_events[0]
        assert start_event.operation == "SADD"

    def test_zadd_publishes_events(self, redis_client_with_eventbus, event_bus_and_events):
        """测试 zadd 操作发布事件"""
        _, collected_events = event_bus_and_events
        redis_client_with_eventbus._mock_client.zadd.return_value = 2

        redis_client_with_eventbus.zadd("zset_key", {"m1": 1.0, "m2": 2.0})

        assert len(collected_events) == 2

        start_event = collected_events[0]
        assert start_event.operation == "ZADD"

    def test_error_publishes_error_event(self, redis_client_with_eventbus, event_bus_and_events):
        """测试操作失败发布错误事件"""
        _, collected_events = event_bus_and_events
        redis_client_with_eventbus._mock_client.get.side_effect = Exception(
            "Redis connection error"
        )

        with pytest.raises(Exception, match="Redis connection error"):
            redis_client_with_eventbus.get("error_key")

        # 应该有开始事件和错误事件
        assert len(collected_events) == 2

        start_event = collected_events[0]
        error_event = collected_events[1]

        assert isinstance(start_event, CacheOperationStartEvent)
        assert isinstance(error_event, CacheOperationErrorEvent)
        assert error_event.operation == "GET"
        assert error_event.key == "error_key"
        assert error_event.error_type == "Exception"
        assert "Redis connection error" in error_event.error_message

        # 验证 correlation_id 关联
        assert start_event.correlation_id == error_event.correlation_id

    def test_no_events_without_eventbus(self):
        """测试没有 EventBus 时不发布事件"""
        with patch("redis.ConnectionPool"), patch("redis.Redis") as mock_redis:
            mock_client = Mock()
            mock_client.get.return_value = "value"
            mock_redis.return_value = mock_client

            # 不传入 event_bus
            client = RedisClient()
            result = client.get("key")

            assert result == "value"
            # 不应该抛出异常
            client.close()


class TestRedisClientNewMethods:
    """测试 v3.18.0 新增的方法"""

    def setup_method(self):
        """每个测试前创建 mock client"""
        with patch("redis.ConnectionPool"), patch("redis.Redis") as mock_redis:
            self.mock_client = Mock()
            mock_redis.return_value = self.mock_client
            self.client = RedisClient()

    def test_incr(self):
        """测试 incr 方法"""
        self.mock_client.incr.return_value = 2

        result = self.client.incr("counter")

        assert result == 2
        self.mock_client.incr.assert_called_once_with("counter", 1)

    def test_incr_with_amount(self):
        """测试带增量的 incr"""
        self.mock_client.incr.return_value = 10

        result = self.client.incr("counter", 5)

        assert result == 10
        self.mock_client.incr.assert_called_once_with("counter", 5)

    def test_decr(self):
        """测试 decr 方法"""
        self.mock_client.decr.return_value = 0

        result = self.client.decr("counter")

        assert result == 0
        self.mock_client.decr.assert_called_once_with("counter", 1)

    def test_hexists(self):
        """测试 hexists 方法"""
        self.mock_client.hexists.return_value = True

        result = self.client.hexists("hash", "field")

        assert result is True
        self.mock_client.hexists.assert_called_once_with("hash", "field")

    def test_hkeys(self):
        """测试 hkeys 方法"""
        self.mock_client.hkeys.return_value = ["field1", "field2"]

        result = self.client.hkeys("hash")

        assert result == ["field1", "field2"]
        self.mock_client.hkeys.assert_called_once_with("hash")

    def test_hvals(self):
        """测试 hvals 方法"""
        self.mock_client.hvals.return_value = ["value1", "value2"]

        result = self.client.hvals("hash")

        assert result == ["value1", "value2"]
        self.mock_client.hvals.assert_called_once_with("hash")

    def test_hlen(self):
        """测试 hlen 方法"""
        self.mock_client.hlen.return_value = 5

        result = self.client.hlen("hash")

        assert result == 5
        self.mock_client.hlen.assert_called_once_with("hash")

    def test_llen(self):
        """测试 llen 方法"""
        self.mock_client.llen.return_value = 10

        result = self.client.llen("list")

        assert result == 10
        self.mock_client.llen.assert_called_once_with("list")

    def test_lindex(self):
        """测试 lindex 方法"""
        self.mock_client.lindex.return_value = "item"

        result = self.client.lindex("list", 0)

        assert result == "item"
        self.mock_client.lindex.assert_called_once_with("list", 0)

    def test_sismember(self):
        """测试 sismember 方法"""
        self.mock_client.sismember.return_value = True

        result = self.client.sismember("set", "member")

        assert result is True
        self.mock_client.sismember.assert_called_once_with("set", "member")

    def test_scard(self):
        """测试 scard 方法"""
        self.mock_client.scard.return_value = 3

        result = self.client.scard("set")

        assert result == 3
        self.mock_client.scard.assert_called_once_with("set")

    def test_zrevrange(self):
        """测试 zrevrange 方法"""
        self.mock_client.zrevrange.return_value = ["c", "b", "a"]

        result = self.client.zrevrange("zset", 0, -1)

        assert result == ["c", "b", "a"]
        self.mock_client.zrevrange.assert_called_once_with("zset", 0, -1, withscores=False)

    def test_zscore(self):
        """测试 zscore 方法"""
        self.mock_client.zscore.return_value = 1.5

        result = self.client.zscore("zset", "member")

        assert result == 1.5
        self.mock_client.zscore.assert_called_once_with("zset", "member")

    def test_zcard(self):
        """测试 zcard 方法"""
        self.mock_client.zcard.return_value = 10

        result = self.client.zcard("zset")

        assert result == 10
        self.mock_client.zcard.assert_called_once_with("zset")

    def test_zrank(self):
        """测试 zrank 方法"""
        self.mock_client.zrank.return_value = 2

        result = self.client.zrank("zset", "member")

        assert result == 2
        self.mock_client.zrank.assert_called_once_with("zset", "member")

    def test_zrem(self):
        """测试 zrem 方法"""
        self.mock_client.zrem.return_value = 1

        result = self.client.zrem("zset", "member")

        assert result == 1
        self.mock_client.zrem.assert_called_once_with("zset", "member")

    def test_scan(self):
        """测试 scan 方法"""
        self.mock_client.scan.return_value = (0, ["key1", "key2"])

        cursor, keys = self.client.scan(0)

        assert cursor == 0
        assert keys == ["key1", "key2"]
        self.mock_client.scan.assert_called_once_with(cursor=0, match=None, count=None)

    def test_scan_with_pattern(self):
        """测试带模式的 scan"""
        self.mock_client.scan.return_value = (5, ["user:1", "user:2"])

        cursor, keys = self.client.scan(0, match="user:*", count=50)

        assert cursor == 5
        assert keys == ["user:1", "user:2"]
        self.mock_client.scan.assert_called_once_with(cursor=0, match="user:*", count=50)

    def test_type(self):
        """测试 type 方法"""
        self.mock_client.type.return_value = "string"

        result = self.client.type("key")

        assert result == "string"
        self.mock_client.type.assert_called_once_with("key")

    def test_rename(self):
        """测试 rename 方法"""
        self.mock_client.rename.return_value = True

        result = self.client.rename("old_key", "new_key")

        assert result is True
        self.mock_client.rename.assert_called_once_with("old_key", "new_key")
