"""Redis Mock 工具

提供 Redis 操作的 Mock 功能
"""

from __future__ import annotations

import fnmatch
import time
from typing import Any
from unittest.mock import MagicMock, Mock

from loguru import logger

# 检查 fakeredis 是否可用
try:
    import fakeredis

    FAKEREDIS_AVAILABLE = True
except ImportError:
    FAKEREDIS_AVAILABLE = False


class RedisMocker:
    """Redis Mock 工具

    优先使用 fakeredis（如果可用），否则使用简单的内存Mock

    Examples:
        >>> # 使用上下文管理器
        >>> with RedisMocker() as redis_mock:
        ...     redis_mock.set("key", "value")
        ...     assert redis_mock.get("key") == "value"
        >>>
        >>> # 使用 fakeredis（完整的 Redis 功能）
        >>> redis_mock = RedisMocker(use_fakeredis=True)
        >>> redis_mock.start()
        >>> redis_mock.mock_client.set("counter", 0)
        >>> redis_mock.mock_client.incr("counter")
        >>> assert redis_mock.mock_client.get("counter") == 1
    """

    def __init__(self, use_fakeredis: bool = True) -> None:
        """初始化 Redis Mock

        Args:
            use_fakeredis: 是否使用 fakeredis（如果可用）
        """
        self.use_fakeredis = use_fakeredis and FAKEREDIS_AVAILABLE
        self._mock_client: Any = None
        self._memory_store: dict[str, Any] = {}
        self._expiry_times: dict[str, float] = {}  # 键过期时间

    def start(self) -> RedisMocker:
        """启动 Mock"""
        if self.use_fakeredis:
            self._mock_client = fakeredis.FakeRedis(decode_responses=True)
            logger.debug("Started Redis mock with fakeredis")
        else:
            self._mock_client = self._create_simple_mock()
            logger.debug("Started Redis mock with simple mock")

        return self

    def stop(self) -> None:
        """停止 Mock"""
        if self.use_fakeredis and self._mock_client:
            self._mock_client.flushall()

        self._memory_store.clear()
        self._mock_client = None
        logger.debug("Stopped Redis mock")

    def _create_simple_mock(self) -> Mock:
        """创建简单的 Redis Mock（内存实现）"""
        mock_client = MagicMock()

        # 实现常用方法
        mock_client.get.side_effect = lambda key: self._memory_store.get(key)
        mock_client.set.side_effect = self._set
        mock_client.delete.side_effect = lambda *keys: sum(
            1 for key in keys if self._memory_store.pop(key, None) is not None
        )
        mock_client.exists.side_effect = lambda *keys: sum(
            1 for key in keys if key in self._memory_store
        )
        mock_client.keys.side_effect = self._keys
        mock_client.flushall.side_effect = self._memory_store.clear

        # Hash 操作
        mock_client.hget.side_effect = self._hget
        mock_client.hset.side_effect = self._hset
        mock_client.hgetall.side_effect = self._hgetall
        mock_client.hdel.side_effect = self._hdel
        mock_client.hexists.side_effect = self._hexists
        mock_client.hlen.side_effect = self._hlen
        mock_client.hkeys.side_effect = self._hkeys
        mock_client.hvals.side_effect = self._hvals

        # List 操作
        mock_client.lpush.side_effect = self._lpush
        mock_client.rpush.side_effect = self._rpush
        mock_client.lpop.side_effect = self._lpop
        mock_client.rpop.side_effect = self._rpop
        mock_client.lrange.side_effect = self._lrange
        mock_client.llen.side_effect = self._llen

        # Set 操作
        mock_client.sadd.side_effect = self._sadd
        mock_client.smembers.side_effect = self._smembers
        mock_client.srem.side_effect = self._srem
        mock_client.sismember.side_effect = self._sismember
        mock_client.scard.side_effect = self._scard

        # 计数器操作
        mock_client.incr.side_effect = self._incr
        mock_client.decr.side_effect = self._decr
        mock_client.incrby.side_effect = self._incrby
        mock_client.decrby.side_effect = self._decrby
        mock_client.incrbyfloat.side_effect = self._incrbyfloat

        # 过期时间操作
        mock_client.setex.side_effect = self._setex
        mock_client.expire.side_effect = self._expire
        mock_client.ttl.side_effect = self._ttl
        mock_client.pttl.side_effect = self._pttl
        mock_client.persist.side_effect = self._persist

        # 批量操作
        mock_client.mget.side_effect = self._mget
        mock_client.mset.side_effect = self._mset

        # 其他操作
        mock_client.type.side_effect = self._type
        mock_client.append.side_effect = self._append
        mock_client.strlen.side_effect = self._strlen
        mock_client.getset.side_effect = self._getset
        mock_client.setnx.side_effect = self._setnx

        return mock_client

    def _set(self, key: str, value: Any, **kwargs: Any) -> bool:
        """SET 命令"""
        self._memory_store[key] = value
        return True

    def _hget(self, name: str, key: str) -> Any:
        """HGET 命令"""
        hash_value = self._memory_store.get(name, {})
        return hash_value.get(key) if isinstance(hash_value, dict) else None

    def _hset(self, name: str, key: str, value: Any) -> int:
        """HSET 命令"""
        if name not in self._memory_store:
            self._memory_store[name] = {}

        is_new = key not in self._memory_store[name]  # type: ignore
        self._memory_store[name][key] = value  # type: ignore
        return 1 if is_new else 0

    def _hgetall(self, name: str) -> dict[str, Any]:
        """HGETALL 命令"""
        return self._memory_store.get(name, {})  # type: ignore

    def _hdel(self, name: str, *keys: str) -> int:
        """HDEL 命令"""
        if name not in self._memory_store:
            return 0

        count = 0
        hash_value = self._memory_store[name]
        if isinstance(hash_value, dict):
            for key in keys:
                if hash_value.pop(key, None) is not None:
                    count += 1

        return count

    def _lpush(self, key: str, *values: Any) -> int:
        """LPUSH 命令"""
        if key not in self._memory_store:
            self._memory_store[key] = []

        list_value = self._memory_store[key]
        if isinstance(list_value, list):
            for value in reversed(values):
                list_value.insert(0, value)
            return len(list_value)

        return 0

    def _rpush(self, key: str, *values: Any) -> int:
        """RPUSH 命令"""
        if key not in self._memory_store:
            self._memory_store[key] = []

        list_value = self._memory_store[key]
        if isinstance(list_value, list):
            list_value.extend(values)
            return len(list_value)

        return 0

    def _lpop(self, key: str) -> Any:
        """LPOP 命令"""
        list_value = self._memory_store.get(key, [])
        if isinstance(list_value, list) and len(list_value) > 0:
            return list_value.pop(0)
        return None

    def _rpop(self, key: str) -> Any:
        """RPOP 命令"""
        list_value = self._memory_store.get(key, [])
        if isinstance(list_value, list) and len(list_value) > 0:
            return list_value.pop()
        return None

    def _lrange(self, key: str, start: int, end: int) -> list[Any]:
        """LRANGE 命令"""
        list_value = self._memory_store.get(key, [])
        if isinstance(list_value, list):
            # Redis 的 end 是包含的，Python 的切片是不包含的
            if end == -1:
                return list_value[start:]
            return list_value[start : end + 1]
        return []

    def _llen(self, key: str) -> int:
        """LLEN 命令"""
        list_value = self._memory_store.get(key, [])
        return len(list_value) if isinstance(list_value, list) else 0

    def _sadd(self, key: str, *members: Any) -> int:
        """SADD 命令"""
        if key not in self._memory_store:
            self._memory_store[key] = set()

        set_value = self._memory_store[key]
        if isinstance(set_value, set):
            initial_size = len(set_value)
            set_value.update(members)
            return len(set_value) - initial_size

        return 0

    def _smembers(self, key: str) -> set[Any]:
        """SMEMBERS 命令"""
        set_value = self._memory_store.get(key, set())
        return set_value if isinstance(set_value, set) else set()

    def _srem(self, key: str, *members: Any) -> int:
        """SREM 命令"""
        set_value = self._memory_store.get(key, set())
        if isinstance(set_value, set):
            count = 0
            for member in members:
                if member in set_value:
                    set_value.remove(member)
                    count += 1
            return count

        return 0

    def _sismember(self, key: str, member: Any) -> bool:
        """SISMEMBER 命令"""
        set_value = self._memory_store.get(key, set())
        return member in set_value if isinstance(set_value, set) else False

    def _scard(self, key: str) -> int:
        """SCARD 命令 - 获取集合大小"""
        set_value = self._memory_store.get(key, set())
        return len(set_value) if isinstance(set_value, set) else 0

    # ========== Hash 扩展操作 ==========

    def _hexists(self, name: str, key: str) -> bool:
        """HEXISTS 命令"""
        hash_value = self._memory_store.get(name, {})
        return key in hash_value if isinstance(hash_value, dict) else False

    def _hlen(self, name: str) -> int:
        """HLEN 命令"""
        hash_value = self._memory_store.get(name, {})
        return len(hash_value) if isinstance(hash_value, dict) else 0

    def _hkeys(self, name: str) -> list[str]:
        """HKEYS 命令"""
        hash_value = self._memory_store.get(name, {})
        return list(hash_value.keys()) if isinstance(hash_value, dict) else []

    def _hvals(self, name: str) -> list[Any]:
        """HVALS 命令"""
        hash_value = self._memory_store.get(name, {})
        return list(hash_value.values()) if isinstance(hash_value, dict) else []

    # ========== 计数器操作 ==========

    def _incr(self, key: str) -> int:
        """INCR 命令"""
        return self._incrby(key, 1)

    def _decr(self, key: str) -> int:
        """DECR 命令"""
        return self._decrby(key, 1)

    def _incrby(self, key: str, amount: int = 1) -> int:
        """INCRBY 命令"""
        current = self._memory_store.get(key, 0)
        if isinstance(current, str):
            current = int(current)
        new_value = current + amount
        self._memory_store[key] = new_value
        return new_value

    def _decrby(self, key: str, amount: int = 1) -> int:
        """DECRBY 命令"""
        return self._incrby(key, -amount)

    def _incrbyfloat(self, key: str, amount: float) -> float:
        """INCRBYFLOAT 命令"""
        current = self._memory_store.get(key, 0.0)
        if isinstance(current, str):
            current = float(current)
        new_value = float(current) + amount
        self._memory_store[key] = new_value
        return new_value

    # ========== 过期时间操作 ==========

    def _setex(self, key: str, seconds: int, value: Any) -> bool:
        """SETEX 命令 - 设置值和过期时间"""
        self._memory_store[key] = value
        self._expiry_times[key] = time.time() + seconds
        return True

    def _expire(self, key: str, seconds: int) -> bool:
        """EXPIRE 命令 - 设置过期时间"""
        if key not in self._memory_store:
            return False
        self._expiry_times[key] = time.time() + seconds
        return True

    def _ttl(self, key: str) -> int:
        """TTL 命令 - 获取剩余生存时间（秒）"""
        if key not in self._memory_store:
            return -2  # 键不存在
        if key not in self._expiry_times:
            return -1  # 键存在但没有过期时间
        remaining = self._expiry_times[key] - time.time()
        if remaining <= 0:
            # 键已过期，清理
            self._memory_store.pop(key, None)
            self._expiry_times.pop(key, None)
            return -2
        return int(remaining)

    def _pttl(self, key: str) -> int:
        """PTTL 命令 - 获取剩余生存时间（毫秒）"""
        ttl = self._ttl(key)
        if ttl < 0:
            return ttl
        return ttl * 1000

    def _persist(self, key: str) -> bool:
        """PERSIST 命令 - 移除过期时间"""
        if key in self._expiry_times:
            del self._expiry_times[key]
            return True
        return False

    # ========== 批量操作 ==========

    def _mget(self, *keys: str) -> list[Any]:
        """MGET 命令 - 批量获取"""
        return [self._memory_store.get(key) for key in keys]

    def _mset(self, mapping: dict[str, Any]) -> bool:
        """MSET 命令 - 批量设置"""
        self._memory_store.update(mapping)
        return True

    # ========== 其他操作 ==========

    def _type(self, key: str) -> str:
        """TYPE 命令 - 获取键类型"""
        if key not in self._memory_store:
            return "none"
        value = self._memory_store[key]
        if isinstance(value, str):
            return "string"
        elif isinstance(value, list):
            return "list"
        elif isinstance(value, set):
            return "set"
        elif isinstance(value, dict):
            return "hash"
        elif isinstance(value, (int, float)):
            return "string"  # Redis 将数字存储为字符串
        return "string"

    def _append(self, key: str, value: str) -> int:
        """APPEND 命令 - 追加字符串"""
        current = self._memory_store.get(key, "")
        if not isinstance(current, str):
            current = str(current)
        new_value = current + value
        self._memory_store[key] = new_value
        return len(new_value)

    def _strlen(self, key: str) -> int:
        """STRLEN 命令 - 获取字符串长度"""
        value = self._memory_store.get(key, "")
        if not isinstance(value, str):
            value = str(value)
        return len(value)

    def _getset(self, key: str, value: Any) -> Any:
        """GETSET 命令 - 设置新值并返回旧值"""
        old_value = self._memory_store.get(key)
        self._memory_store[key] = value
        return old_value

    def _setnx(self, key: str, value: Any) -> bool:
        """SETNX 命令 - 仅当键不存在时设置"""
        if key in self._memory_store:
            return False
        self._memory_store[key] = value
        return True

    def _keys(self, pattern: str = "*") -> list[str]:
        """KEYS 命令 - 支持 glob 模式匹配"""
        if pattern == "*":
            return list(self._memory_store.keys())
        # 转换 Redis glob 模式为 fnmatch 模式
        return [key for key in self._memory_store.keys() if fnmatch.fnmatch(key, pattern)]

    def reset(self) -> None:
        """重置 Mock 状态"""
        if self.use_fakeredis and self._mock_client:
            self._mock_client.flushall()

        self._memory_store.clear()
        self._expiry_times.clear()
        logger.debug("Redis mock reset")

    def __enter__(self) -> RedisMocker:
        """上下文管理器入口"""
        return self.start()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore
        """上下文管理器退出"""
        self.stop()

    @property
    def mock_client(self) -> Any:
        """获取 Mock Redis 客户端"""
        if not self._mock_client:
            raise RuntimeError("Mock not started. Call start() first.")
        return self._mock_client
