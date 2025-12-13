"""Redis 客户端封装

v3.17.1 重构:
- 添加 EventBus 事件发布（所有操作）
- 完善 Allure 报告集成（所有操作）
- 统一操作执行包装器 _execute_operation()
- 支持 correlation_id 事件关联
"""

import time
from collections.abc import Callable
from typing import Any, TypeVar

import redis
from loguru import logger

from df_test_framework.core.events import (
    CacheOperationEndEvent,
    CacheOperationErrorEvent,
    CacheOperationStartEvent,
)

T = TypeVar("T")


class RedisClient:
    """Redis 客户端封装

    功能:
    - 提供 Redis 连接管理
    - 封装常用的 Redis 操作
    - 支持连接池
    - EventBus 事件发布（v3.17.1）
    - Allure 报告集成（v3.17.1 增强）

    v3.17.1 新特性:
    - 所有操作发布 EventBus 事件
    - 所有操作记录到 Allure 报告
    - 支持 correlation_id 事件关联
    - 统一的操作执行包装器
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: str | None = None,
        max_connections: int = 50,
        decode_responses: bool = True,
        event_bus: Any | None = None,
    ):
        """初始化 Redis 客户端

        Args:
            host: Redis 主机地址
            port: Redis 端口
            db: 数据库编号
            password: 密码
            max_connections: 连接池最大连接数
            decode_responses: 是否自动解码响应为字符串
            event_bus: EventBus 实例（可选，v3.17.1）
        """
        self.host = host
        self.port = port
        self.db = db
        self._event_bus = event_bus

        # 创建连接池
        self.pool = redis.ConnectionPool(
            host=host,
            port=port,
            db=db,
            password=password,
            max_connections=max_connections,
            decode_responses=decode_responses,
        )

        # 创建 Redis 客户端
        self.client = redis.Redis(connection_pool=self.pool)

        # v3.5: ObservabilityLogger
        from df_test_framework.infrastructure.logging.observability import redis_logger

        self.obs_logger = redis_logger()

        logger.info(f"Redis 连接已建立: {host}:{port}/{db}")

    def _get_event_bus(self):
        """获取 EventBus 实例"""
        if self._event_bus is not None:
            return self._event_bus
        try:
            from df_test_framework.infrastructure.events import get_event_bus

            return get_event_bus()
        except Exception:
            return None

    def _publish_event(self, event: Any) -> None:
        """发布事件到 EventBus（同步模式）"""
        event_bus = self._get_event_bus()
        if event_bus:
            try:
                event_bus.publish_sync(event)
            except Exception:
                pass  # 静默失败，不影响主流程

    def _execute_operation(
        self,
        operation: str,
        key: str,
        func: Callable[[], T],
        field: str | None = None,
        is_read: bool = False,
        value: Any | None = None,
    ) -> T:
        """统一的操作执行包装器

        提供 EventBus 事件发布、Allure 报告、可观测性日志的统一处理。

        Args:
            operation: 操作类型（SET, GET, HSET 等）
            key: 缓存键
            func: 实际执行的操作函数
            field: Hash 操作的字段名（可选）
            is_read: 是否为读取操作（用于计算 hit）
            value: 写入的值（用于 Allure 记录）

        Returns:
            操作结果
        """
        # 1. 发布开始事件
        start_event, correlation_id = CacheOperationStartEvent.create(
            operation=operation, key=key, field=field
        )
        self._publish_event(start_event)

        # 2. 记录可观测性日志
        self.obs_logger.cache_operation(operation, key)

        # 3. 执行操作
        start_time = time.perf_counter()
        try:
            result = func()
            duration_ms = (time.perf_counter() - start_time) * 1000

            # 4. 计算 hit 状态（读取操作）
            hit = None
            if is_read:
                hit = result is not None

            # 5. 发布结束事件（Allure 通过 EventBus 订阅自动记录）
            end_event = CacheOperationEndEvent.create(
                correlation_id=correlation_id,
                operation=operation,
                key=key,
                duration_ms=duration_ms,
                hit=hit,
            )
            self._publish_event(end_event)

            return result

        except Exception as e:
            duration_ms = (time.perf_counter() - start_time) * 1000

            # 发布错误事件（Allure 通过 EventBus 订阅自动记录）
            error_event = CacheOperationErrorEvent.create(
                correlation_id=correlation_id,
                operation=operation,
                key=key,
                error=e,
                duration_ms=duration_ms,
            )
            self._publish_event(error_event)

            raise

    def ping(self) -> bool:
        """测试连接

        Returns:
            连接是否正常
        """
        try:
            return self.client.ping()
        except Exception as e:
            logger.error(f"Redis 连接测试失败: {str(e)}")
            return False

    # ========== 字符串操作 ==========

    def set(
        self,
        key: str,
        value: Any,
        ex: int | None = None,
        nx: bool = False,
    ) -> bool:
        """设置键值

        Args:
            key: 键
            value: 值
            ex: 过期时间(秒)
            nx: 如果键不存在才设置

        Returns:
            是否成功
        """
        return self._execute_operation(
            operation="SET",
            key=key,
            func=lambda: self.client.set(key, value, ex=ex, nx=nx),
            value=value,
        )

    def get(self, key: str) -> str | None:
        """获取值

        Args:
            key: 键

        Returns:
            值，如果不存在返回 None
        """
        return self._execute_operation(
            operation="GET",
            key=key,
            func=lambda: self.client.get(key),
            is_read=True,
        )

    def delete(self, *keys: str) -> int:
        """删除键

        Args:
            *keys: 要删除的键

        Returns:
            删除的键数量
        """
        # 对于多键删除，使用第一个键作为主键记录
        primary_key = keys[0] if keys else ""
        return self._execute_operation(
            operation="DELETE",
            key=primary_key if len(keys) == 1 else f"{primary_key},...({len(keys)} keys)",
            func=lambda: self.client.delete(*keys),
        )

    def exists(self, *keys: str) -> int:
        """检查键是否存在

        Args:
            *keys: 要检查的键

        Returns:
            存在的键数量
        """
        primary_key = keys[0] if keys else ""
        return self._execute_operation(
            operation="EXISTS",
            key=primary_key if len(keys) == 1 else f"{primary_key},...({len(keys)} keys)",
            func=lambda: self.client.exists(*keys),
            is_read=True,
        )

    def expire(self, key: str, seconds: int) -> bool:
        """设置键的过期时间

        Args:
            key: 键
            seconds: 过期时间(秒)

        Returns:
            是否成功
        """
        return self._execute_operation(
            operation="EXPIRE",
            key=key,
            func=lambda: self.client.expire(key, seconds),
            value=f"{seconds}s",
        )

    def ttl(self, key: str) -> int:
        """获取键的剩余过期时间

        Args:
            key: 键

        Returns:
            剩余秒数，-1 表示永久，-2 表示不存在
        """
        return self._execute_operation(
            operation="TTL",
            key=key,
            func=lambda: self.client.ttl(key),
            is_read=True,
        )

    def incr(self, key: str, amount: int = 1) -> int:
        """自增

        Args:
            key: 键
            amount: 增量

        Returns:
            增后的值
        """
        return self._execute_operation(
            operation="INCR",
            key=key,
            func=lambda: self.client.incr(key, amount),
            value=amount,
        )

    def decr(self, key: str, amount: int = 1) -> int:
        """自减

        Args:
            key: 键
            amount: 减量

        Returns:
            减后的值
        """
        return self._execute_operation(
            operation="DECR",
            key=key,
            func=lambda: self.client.decr(key, amount),
            value=amount,
        )

    # ========== 哈希操作 ==========

    def hset(self, name: str, key: str, value: Any) -> int:
        """设置哈希字段

        Args:
            name: 哈希名
            key: 字段名
            value: 字段值

        Returns:
            新创建的字段数量
        """
        return self._execute_operation(
            operation="HSET",
            key=name,
            field=key,
            func=lambda: self.client.hset(name, key, value),
            value=value,
        )

    def hget(self, name: str, key: str) -> str | None:
        """获取哈希字段

        Args:
            name: 哈希名
            key: 字段名

        Returns:
            字段值
        """
        return self._execute_operation(
            operation="HGET",
            key=name,
            field=key,
            func=lambda: self.client.hget(name, key),
            is_read=True,
        )

    def hgetall(self, name: str) -> dict:
        """获取哈希所有字段

        Args:
            name: 哈希名

        Returns:
            所有字段的字典
        """
        return self._execute_operation(
            operation="HGETALL",
            key=name,
            func=lambda: self.client.hgetall(name),
            is_read=True,
        )

    def hdel(self, name: str, *keys: str) -> int:
        """删除哈希字段

        Args:
            name: 哈希名
            *keys: 要删除的字段

        Returns:
            删除的字段数量
        """
        return self._execute_operation(
            operation="HDEL",
            key=name,
            field=keys[0] if len(keys) == 1 else f"{keys[0]},...({len(keys)} fields)",
            func=lambda: self.client.hdel(name, *keys),
        )

    def hexists(self, name: str, key: str) -> bool:
        """检查哈希字段是否存在

        Args:
            name: 哈希名
            key: 字段名

        Returns:
            是否存在
        """
        return self._execute_operation(
            operation="HEXISTS",
            key=name,
            field=key,
            func=lambda: self.client.hexists(name, key),
            is_read=True,
        )

    def hkeys(self, name: str) -> list:
        """获取哈希所有字段名

        Args:
            name: 哈希名

        Returns:
            字段名列表
        """
        return self._execute_operation(
            operation="HKEYS",
            key=name,
            func=lambda: self.client.hkeys(name),
            is_read=True,
        )

    def hvals(self, name: str) -> list:
        """获取哈希所有字段值

        Args:
            name: 哈希名

        Returns:
            字段值列表
        """
        return self._execute_operation(
            operation="HVALS",
            key=name,
            func=lambda: self.client.hvals(name),
            is_read=True,
        )

    def hlen(self, name: str) -> int:
        """获取哈希字段数量

        Args:
            name: 哈希名

        Returns:
            字段数量
        """
        return self._execute_operation(
            operation="HLEN",
            key=name,
            func=lambda: self.client.hlen(name),
            is_read=True,
        )

    # ========== 列表操作 ==========

    def lpush(self, name: str, *values: Any) -> int:
        """从左边推入列表

        Args:
            name: 列表名
            *values: 要推入的值

        Returns:
            列表长度
        """
        return self._execute_operation(
            operation="LPUSH",
            key=name,
            func=lambda: self.client.lpush(name, *values),
            value=values[0] if len(values) == 1 else f"[{len(values)} items]",
        )

    def rpush(self, name: str, *values: Any) -> int:
        """从右边推入列表

        Args:
            name: 列表名
            *values: 要推入的值

        Returns:
            列表长度
        """
        return self._execute_operation(
            operation="RPUSH",
            key=name,
            func=lambda: self.client.rpush(name, *values),
            value=values[0] if len(values) == 1 else f"[{len(values)} items]",
        )

    def lpop(self, name: str) -> str | None:
        """从左边弹出

        Args:
            name: 列表名

        Returns:
            弹出的值
        """
        return self._execute_operation(
            operation="LPOP",
            key=name,
            func=lambda: self.client.lpop(name),
            is_read=True,
        )

    def rpop(self, name: str) -> str | None:
        """从右边弹出

        Args:
            name: 列表名

        Returns:
            弹出的值
        """
        return self._execute_operation(
            operation="RPOP",
            key=name,
            func=lambda: self.client.rpop(name),
            is_read=True,
        )

    def lrange(self, name: str, start: int, end: int) -> list:
        """获取列表范围

        Args:
            name: 列表名
            start: 起始索引
            end: 结束索引

        Returns:
            元素列表
        """
        return self._execute_operation(
            operation="LRANGE",
            key=name,
            func=lambda: self.client.lrange(name, start, end),
            is_read=True,
        )

    def llen(self, name: str) -> int:
        """获取列表长度

        Args:
            name: 列表名

        Returns:
            列表长度
        """
        return self._execute_operation(
            operation="LLEN",
            key=name,
            func=lambda: self.client.llen(name),
            is_read=True,
        )

    def lindex(self, name: str, index: int) -> str | None:
        """获取列表指定索引的元素

        Args:
            name: 列表名
            index: 索引

        Returns:
            元素值
        """
        return self._execute_operation(
            operation="LINDEX",
            key=name,
            func=lambda: self.client.lindex(name, index),
            is_read=True,
        )

    # ========== 集合操作 ==========

    def sadd(self, name: str, *values: Any) -> int:
        """添加到集合

        Args:
            name: 集合名
            *values: 要添加的值

        Returns:
            新添加的元素数量
        """
        return self._execute_operation(
            operation="SADD",
            key=name,
            func=lambda: self.client.sadd(name, *values),
            value=values[0] if len(values) == 1 else f"[{len(values)} items]",
        )

    def smembers(self, name: str) -> set:
        """获取集合所有成员

        Args:
            name: 集合名

        Returns:
            成员集合
        """
        return self._execute_operation(
            operation="SMEMBERS",
            key=name,
            func=lambda: self.client.smembers(name),
            is_read=True,
        )

    def srem(self, name: str, *values: Any) -> int:
        """从集合移除

        Args:
            name: 集合名
            *values: 要移除的值

        Returns:
            移除的元素数量
        """
        return self._execute_operation(
            operation="SREM",
            key=name,
            func=lambda: self.client.srem(name, *values),
            value=values[0] if len(values) == 1 else f"[{len(values)} items]",
        )

    def sismember(self, name: str, value: Any) -> bool:
        """检查是否为集合成员

        Args:
            name: 集合名
            value: 要检查的值

        Returns:
            是否为成员
        """
        return self._execute_operation(
            operation="SISMEMBER",
            key=name,
            func=lambda: self.client.sismember(name, value),
            is_read=True,
        )

    def scard(self, name: str) -> int:
        """获取集合大小

        Args:
            name: 集合名

        Returns:
            集合大小
        """
        return self._execute_operation(
            operation="SCARD",
            key=name,
            func=lambda: self.client.scard(name),
            is_read=True,
        )

    # ========== 有序集合操作 ==========

    def zadd(self, name: str, mapping: dict) -> int:
        """添加到有序集合

        Args:
            name: 有序集合名
            mapping: {member: score} 字典

        Returns:
            新添加的元素数量
        """
        return self._execute_operation(
            operation="ZADD",
            key=name,
            func=lambda: self.client.zadd(name, mapping),
            value=f"[{len(mapping)} items]",
        )

    def zrange(self, name: str, start: int, end: int, withscores: bool = False) -> list:
        """获取有序集合范围

        Args:
            name: 有序集合名
            start: 起始索引
            end: 结束索引
            withscores: 是否返回分数

        Returns:
            元素列表
        """
        return self._execute_operation(
            operation="ZRANGE",
            key=name,
            func=lambda: self.client.zrange(name, start, end, withscores=withscores),
            is_read=True,
        )

    def zrevrange(self, name: str, start: int, end: int, withscores: bool = False) -> list:
        """获取有序集合逆序范围

        Args:
            name: 有序集合名
            start: 起始索引
            end: 结束索引
            withscores: 是否返回分数

        Returns:
            元素列表
        """
        return self._execute_operation(
            operation="ZREVRANGE",
            key=name,
            func=lambda: self.client.zrevrange(name, start, end, withscores=withscores),
            is_read=True,
        )

    def zscore(self, name: str, value: Any) -> float | None:
        """获取有序集合成员的分数

        Args:
            name: 有序集合名
            value: 成员

        Returns:
            分数
        """
        return self._execute_operation(
            operation="ZSCORE",
            key=name,
            func=lambda: self.client.zscore(name, value),
            is_read=True,
        )

    def zcard(self, name: str) -> int:
        """获取有序集合大小

        Args:
            name: 有序集合名

        Returns:
            集合大小
        """
        return self._execute_operation(
            operation="ZCARD",
            key=name,
            func=lambda: self.client.zcard(name),
            is_read=True,
        )

    def zrank(self, name: str, value: Any) -> int | None:
        """获取有序集合成员的排名

        Args:
            name: 有序集合名
            value: 成员

        Returns:
            排名（从 0 开始）
        """
        return self._execute_operation(
            operation="ZRANK",
            key=name,
            func=lambda: self.client.zrank(name, value),
            is_read=True,
        )

    def zrem(self, name: str, *values: Any) -> int:
        """从有序集合移除

        Args:
            name: 有序集合名
            *values: 要移除的成员

        Returns:
            移除的元素数量
        """
        return self._execute_operation(
            operation="ZREM",
            key=name,
            func=lambda: self.client.zrem(name, *values),
            value=values[0] if len(values) == 1 else f"[{len(values)} items]",
        )

    # ========== 通用操作 ==========

    def keys(self, pattern: str = "*") -> list:
        """获取匹配的键列表

        Args:
            pattern: 匹配模式

        Returns:
            键列表
        """
        return self._execute_operation(
            operation="KEYS",
            key=pattern,
            func=lambda: self.client.keys(pattern),
            is_read=True,
        )

    def scan(
        self,
        cursor: int = 0,
        match: str | None = None,
        count: int | None = None,
    ) -> tuple[int, list]:
        """增量迭代键

        Args:
            cursor: 游标
            match: 匹配模式
            count: 每次返回数量提示

        Returns:
            (新游标, 键列表)
        """
        return self._execute_operation(
            operation="SCAN",
            key=match or "*",
            func=lambda: self.client.scan(cursor=cursor, match=match, count=count),
            is_read=True,
        )

    def type(self, key: str) -> str:
        """获取键的类型

        Args:
            key: 键

        Returns:
            类型（string, list, set, zset, hash, none）
        """
        return self._execute_operation(
            operation="TYPE",
            key=key,
            func=lambda: self.client.type(key),
            is_read=True,
        )

    def rename(self, src: str, dst: str) -> bool:
        """重命名键

        Args:
            src: 源键名
            dst: 目标键名

        Returns:
            是否成功
        """
        return self._execute_operation(
            operation="RENAME",
            key=f"{src} -> {dst}",
            func=lambda: self.client.rename(src, dst),
        )

    def flushdb(self) -> bool:
        """清空当前数据库"""
        logger.warning(f"清空 Redis 数据库: DB{self.db}")
        return self.client.flushdb()

    def close(self) -> None:
        """关闭连接"""
        self.client.close()
        logger.info("Redis 连接已关闭")


__all__ = ["RedisClient"]
