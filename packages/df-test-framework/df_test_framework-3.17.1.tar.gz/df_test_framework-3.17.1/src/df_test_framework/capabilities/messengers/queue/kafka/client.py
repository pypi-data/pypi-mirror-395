"""Kafka消息队列客户端

提供Kafka Producer和Consumer的封装。

v3.9.0新增 - 基于confluent-kafka (librdkafka) 实现

版本说明 (v3.10.0+): 使用 confluent-kafka>=2.12.0
- Windows 预编译 wheel 支持，Python 3.12+ 可直接安装
- SSL 问题说明: 2.0+ 版本在某些环境可能遇到 SSL_HANDSHAKE 错误
  → 使用 KafkaSSLConfig 的 workaround 配置可解决（见 config.py）

v3.14.0 新增:
- 集成 EventBus 发布消息事件
- 支持 event_bus 参数

使用示例::

    from df_test_framework.capabilities.messengers.queue.kafka import (
        KafkaClient, KafkaConfig, KafkaProducerConfig
    )

    # 基本配置
    config = KafkaConfig(
        bootstrap_servers=["localhost:9092"],
        producer=KafkaProducerConfig()
    )
    client = KafkaClient(config)

    # 发送消息
    client.send("test-topic", {"user_id": 123, "action": "login"})

    # 消费消息
    messages = []
    client.consume(
        topics=["test-topic"],
        group_id="test-group",
        handler=lambda msg: messages.append(msg),
        max_messages=10
    )

    # 关闭客户端
    client.close()
"""

from __future__ import annotations

import json
import logging
import time
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from df_test_framework.core.events import MessageConsumeEvent, MessagePublishEvent

from .config import KafkaConfig, KafkaConsumerConfig

if TYPE_CHECKING:
    from df_test_framework.infrastructure.events import EventBus

try:
    from confluent_kafka import Consumer, KafkaError, KafkaException, Producer
    from confluent_kafka.admin import AdminClient, NewTopic
except ImportError:
    raise ImportError("confluent-kafka 未安装。请运行: pip install 'df-test-framework[kafka]'")

logger = logging.getLogger(__name__)


class KafkaClient:
    """Kafka消息队列客户端

    基于confluent-kafka (librdkafka) 的Producer和Consumer封装,
    提供简化的消息发送和消费接口。

    相比kafka-python3的优势:
    - 性能提升: 生产性能提升3倍,消费性能提升50%
    - 企业级特性: 支持事务、幂等性、Avro序列化
    - 活跃维护: Confluent官方支持,持续更新

    Attributes:
        config: Kafka配置
    """

    def __init__(self, config: KafkaConfig, event_bus: EventBus | None = None):
        """初始化Kafka客户端

        Args:
            config: Kafka配置对象
            event_bus: 🆕 v3.14.0 事件总线（可选，用于发布消息事件）
        """
        self.config = config
        self._event_bus = event_bus
        self._producer: Producer | None = None
        self._consumer: Consumer | None = None
        self._admin_client: AdminClient | None = None

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
        """发布事件到 EventBus（同步模式）

        v3.18.0: 改用 publish_sync() 确保事件完整性
        """
        event_bus = self._get_event_bus()
        if event_bus:
            try:
                event_bus.publish_sync(event)
            except Exception:
                pass  # 静默失败，不影响主流程

    def _get_producer(self) -> Producer:
        """获取或创建Producer实例"""
        if self._producer is None:
            # 构建Producer配置
            producer_config = self.config.to_confluent_dict(include_producer=True)

            # 添加delivery报告回调
            def delivery_report(err, msg):
                """Producer delivery报告回调"""
                if err is not None:
                    logger.error(f"消息发送失败: {err}")
                else:
                    logger.debug(
                        f"消息发送成功: topic={msg.topic()}, "
                        f"partition={msg.partition()}, "
                        f"offset={msg.offset()}"
                    )

            self._producer = Producer(producer_config)
            logger.info(f"KafkaProducer创建成功: {self.config.bootstrap_servers}")

        return self._producer

    def send(
        self,
        topic: str,
        message: dict[str, Any],
        key: str | None = None,
        partition: int | None = None,
        headers: dict[str, str] | None = None,
        on_delivery: Callable | None = None,
    ) -> None:
        """发送消息到Kafka主题

        Args:
            topic: 主题名称
            message: 消息内容(字典)
            key: 消息key(可选,用于分区)
            partition: 指定分区(可选)
            headers: 消息头(可选,字典形式)
            on_delivery: 自定义delivery回调(可选)

        Raises:
            KafkaException: 发送失败时抛出
        """
        try:
            producer = self._get_producer()

            # 序列化消息
            value_bytes = json.dumps(message).encode("utf-8")
            key_bytes = key.encode("utf-8") if key else None

            # 转换headers格式: confluent-kafka需要list of tuples
            headers_list = None
            if headers:
                headers_list = [(k, v.encode("utf-8")) for k, v in headers.items()]

            # 发送消息(异步)
            producer.produce(
                topic=topic,
                value=value_bytes,
                key=key_bytes,
                partition=partition if partition is not None else -1,
                headers=headers_list,
                on_delivery=on_delivery,
            )

            # 触发发送(非阻塞)
            producer.poll(0)

            # v3.14.0: 发布消息发送事件
            self._publish_event(
                MessagePublishEvent(
                    queue_type="kafka",
                    topic=topic,
                    message=message,
                )
            )

        except BufferError as e:
            # 本地队列满了,需要flush
            logger.warning(f"本地队列满,等待flush: {e}")
            producer.flush()
            # 重试
            producer.produce(topic, value_bytes, key_bytes, partition, headers_list, on_delivery)
            producer.poll(0)

        except Exception as e:
            logger.error(f"发送消息失败: {e}")
            raise

    def send_sync(
        self,
        topic: str,
        message: dict[str, Any],
        key: str | None = None,
        partition: int | None = None,
        headers: dict[str, str] | None = None,
        timeout: float = 10.0,
    ) -> dict[str, Any]:
        """同步发送消息(等待确认)

        Args:
            topic: 主题名称
            message: 消息内容(字典)
            key: 消息key(可选)
            partition: 指定分区(可选)
            headers: 消息头(可选)
            timeout: 超时时间(秒)

        Returns:
            发送结果: {"topic": str, "partition": int, "offset": int}

        Raises:
            KafkaException: 发送失败时抛出
        """
        result = {"topic": None, "partition": None, "offset": None}

        def sync_callback(err, msg):
            """同步回调,记录结果"""
            if err is not None:
                raise KafkaException(err)
            result["topic"] = msg.topic()
            result["partition"] = msg.partition()
            result["offset"] = msg.offset()

        # 发送消息
        self.send(topic, message, key, partition, headers, on_delivery=sync_callback)

        # 等待发送完成
        producer = self._get_producer()
        remaining = producer.flush(timeout=timeout)

        if remaining > 0:
            raise TimeoutError(f"发送超时: {remaining} 条消息未确认")

        return result

    def send_batch(
        self,
        topic: str,
        messages: list[dict[str, Any]],
        key_func: Callable[[dict], str] | None = None,
    ) -> int:
        """批量发送消息(异步)

        Args:
            topic: 主题名称
            messages: 消息列表
            key_func: 可选的key提取函数

        Returns:
            成功发送的消息数量
        """
        success_count = 0

        for message in messages:
            try:
                key = key_func(message) if key_func else None
                self.send(topic, message, key=key)
                success_count += 1
            except Exception as e:
                logger.error(f"批量发送失败: {e}, message={message}")

        # Flush确保所有消息发送
        producer = self._get_producer()
        remaining = producer.flush(timeout=30)

        if remaining > 0:
            logger.warning(f"批量发送有 {remaining} 条消息未确认")

        logger.info(f"批量发送完成: {success_count}/{len(messages)}")
        return success_count

    def consume(
        self,
        topics: list[str],
        group_id: str,
        handler: Callable[[dict[str, Any]], None],
        max_messages: int | None = None,
        consumer_config: KafkaConsumerConfig | None = None,
        timeout: float = 1.0,
        max_idle_seconds: float | None = None,
    ) -> int:
        """消费Kafka消息

        Args:
            topics: 主题列表
            group_id: 消费者组ID
            handler: 消息处理函数
            max_messages: 最大消费消息数(None表示持续消费)
            consumer_config: Consumer配置(可选)
            timeout: poll超时时间(秒)
            max_idle_seconds: 最长空闲等待时间(秒)，超过则退出消费

        Returns:
            已消费的消息数量
        """
        # 构建Consumer配置
        if consumer_config is None:
            if self.config.consumer is None:
                consumer_config = KafkaConsumerConfig(group_id=group_id)
            else:
                consumer_config = self.config.consumer
                consumer_config.group_id = group_id
        else:
            consumer_config.group_id = group_id

        config = self.config.to_confluent_dict(include_consumer=True)
        config.update(consumer_config.to_confluent_dict())

        # 创建Consumer
        consumer = Consumer(config)
        consumer.subscribe(topics)
        self._consumer = consumer

        logger.info(f"开始消费: topics={topics}, group_id={group_id}")

        message_count = 0
        last_message_time = time.monotonic()
        try:
            while True:
                msg = consumer.poll(timeout=timeout)

                if msg is None:
                    # 没有消息,继续等待
                    if max_idle_seconds is not None:
                        idle = time.monotonic() - last_message_time
                        if idle >= max_idle_seconds:
                            logger.info(f"空闲超过 {max_idle_seconds}s，停止消费")
                            break
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # 到达分区末尾
                        logger.debug(f"到达分区末尾: {msg.topic()}[{msg.partition()}]")
                        continue
                    else:
                        # 错误
                        logger.error(f"消费错误: {msg.error()}")
                        raise KafkaException(msg.error())

                # 处理消息
                try:
                    value = json.loads(msg.value().decode("utf-8"))
                    handler(value)
                    message_count += 1
                    last_message_time = time.monotonic()

                    # 手动提交offset (当auto_commit禁用时)
                    if not consumer_config.enable_auto_commit:
                        consumer.commit(message=msg, asynchronous=False)

                    # v3.14.0: 发布消息消费事件
                    self._publish_event(
                        MessageConsumeEvent(
                            queue_type="kafka",
                            topic=msg.topic(),
                            message=value,
                            consumer_group=group_id,
                        )
                    )

                    logger.debug(
                        f"消息处理成功: topic={msg.topic()}, "
                        f"partition={msg.partition()}, "
                        f"offset={msg.offset()}"
                    )

                    # 检查是否达到最大消费数
                    if max_messages and message_count >= max_messages:
                        logger.info(f"达到最大消费数量: {max_messages}")
                        break

                except Exception as e:
                    logger.error(f"消息处理失败: {e}, message={msg.value()}")

        except KeyboardInterrupt:
            logger.info("消费被中断")
        finally:
            consumer.close()
            self._consumer = None
            logger.info(f"消费完成: {message_count} 条消息")

        return message_count

    def create_topic(
        self,
        topic: str,
        num_partitions: int = 1,
        replication_factor: int = 1,
        config: dict[str, str] | None = None,
        timeout: float = 10.0,
    ) -> None:
        """创建Kafka主题

        Args:
            topic: 主题名称
            num_partitions: 分区数
            replication_factor: 副本因子
            config: 主题配置(可选)
            timeout: 超时时间(秒)

        Raises:
            KafkaException: 创建失败时抛出
        """
        if self._admin_client is None:
            admin_config = self.config.to_confluent_dict()
            self._admin_client = AdminClient(admin_config)

        new_topic = NewTopic(
            topic=topic,
            num_partitions=num_partitions,
            replication_factor=replication_factor,
            config=config or {},
        )

        # 创建主题
        fs = self._admin_client.create_topics([new_topic])

        # 等待结果
        for topic_name, f in fs.items():
            try:
                f.result(timeout=timeout)
                logger.info(f"主题创建成功: {topic_name}")
            except Exception as e:
                logger.error(f"主题创建失败: {topic_name}, error={e}")
                raise

    def delete_topic(self, topic: str, timeout: float = 10.0) -> None:
        """删除Kafka主题

        Args:
            topic: 主题名称
            timeout: 超时时间(秒)

        Raises:
            KafkaException: 删除失败时抛出
        """
        if self._admin_client is None:
            admin_config = self.config.to_confluent_dict()
            self._admin_client = AdminClient(admin_config)

        fs = self._admin_client.delete_topics([topic])

        for topic_name, f in fs.items():
            try:
                f.result(timeout=timeout)
                logger.info(f"主题删除成功: {topic_name}")
            except Exception as e:
                logger.error(f"主题删除失败: {topic_name}, error={e}")
                raise

    def flush(self, timeout: float = 10.0) -> int:
        """刷新Producer队列,等待所有消息发送完成

        Args:
            timeout: 超时时间(秒)

        Returns:
            未发送完成的消息数量(0表示全部发送完成)
        """
        if self._producer:
            remaining = self._producer.flush(timeout=timeout)
            logger.info(f"Producer flush完成: {remaining} 条消息未发送")
            return remaining
        return 0

    def close(self) -> None:
        """关闭客户端,释放资源"""
        # Flush Producer队列
        if self._producer:
            self._producer.flush()
            logger.info("KafkaProducer已关闭")
            self._producer = None

        # 关闭Consumer
        if self._consumer:
            self._consumer.close()
            logger.info("KafkaConsumer已关闭")
            self._consumer = None


__all__ = ["KafkaClient"]
