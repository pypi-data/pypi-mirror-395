"""RabbitMQ消息队列客户端

提供RabbitMQ Publisher和Consumer的封装。

v3.9.0新增

v3.14.0 新增:
- 集成 EventBus 发布消息事件
- 支持 event_bus 参数

使用示例::

    from df_test_framework.capabilities.messengers.queue.rabbitmq import (
        RabbitMQClient, RabbitMQConfig
    )

    # 创建客户端
    config = RabbitMQConfig()
    client = RabbitMQClient(config)

    # 声明exchange和queue
    client.declare_exchange("test-exchange", "direct")
    client.declare_queue("test-queue")
    client.bind_queue("test-queue", "test-exchange", "test-key")

    # 发布消息
    client.publish(
        exchange="test-exchange",
        routing_key="test-key",
        message={"user_id": 123, "action": "login"}
    )

    # 消费消息
    messages = []
    client.consume(
        queue="test-queue",
        handler=lambda msg: messages.append(msg),
        max_messages=10
    )

    client.close()
"""

from __future__ import annotations

import json
import logging
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from .config import RabbitMQConfig

if TYPE_CHECKING:
    from df_test_framework.infrastructure.events import EventBus

try:
    import pika
    from pika.exceptions import AMQPError
except ImportError:
    raise ImportError("pika 未安装。请运行: pip install 'df-test-framework[rabbitmq]'")

logger = logging.getLogger(__name__)


class RabbitMQClient:
    """RabbitMQ消息队列客户端

    封装pika的基本操作,提供简化的消息发布和消费接口。

    Attributes:
        config: RabbitMQ配置
        connection: pika连接对象
        channel: pika通道对象
    """

    def __init__(self, config: RabbitMQConfig, event_bus: EventBus | None = None):
        """初始化RabbitMQ客户端

        Args:
            config: RabbitMQ配置对象
            event_bus: 🆕 v3.14.0 事件总线（可选）
        """
        self.config = config
        self._event_bus = event_bus
        self._connection: pika.BlockingConnection | None = None
        self._channel: pika.channel.Channel | None = None

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

    @property
    def connection(self) -> pika.BlockingConnection:
        """获取或创建连接"""
        if self._connection is None or self._connection.is_closed:
            credentials = pika.PlainCredentials(
                self.config.connection.username,
                self.config.connection.password.get_secret_value(),
            )

            parameters = pika.ConnectionParameters(
                host=self.config.connection.host,
                port=self.config.connection.port,
                virtual_host=self.config.connection.virtual_host,
                credentials=credentials,
                heartbeat=self.config.connection.heartbeat,
                blocked_connection_timeout=self.config.connection.blocked_connection_timeout,
                connection_attempts=self.config.connection.connection_attempts,
                retry_delay=self.config.connection.retry_delay,
            )

            self._connection = pika.BlockingConnection(parameters)
            logger.info(
                f"RabbitMQ连接成功: {self.config.connection.host}:{self.config.connection.port}"
            )

        return self._connection

    @property
    def channel(self) -> pika.channel.Channel:
        """获取或创建通道"""
        if self._channel is None or self._channel.is_closed:
            self._channel = self.connection.channel()
            # 设置QoS
            self._channel.basic_qos(prefetch_count=self.config.consume.prefetch_count)
            logger.info("RabbitMQ通道创建成功")

        return self._channel

    def declare_exchange(
        self,
        exchange: str,
        exchange_type: str = "direct",
        durable: bool = True,
        auto_delete: bool = False,
    ) -> None:
        """声明exchange

        Args:
            exchange: exchange名称
            exchange_type: exchange类型(direct, topic, fanout, headers)
            durable: 是否持久化
            auto_delete: 无消费者时是否自动删除
        """
        self.channel.exchange_declare(
            exchange=exchange,
            exchange_type=exchange_type,
            durable=durable,
            auto_delete=auto_delete,
        )
        logger.info(f"Exchange声明成功: {exchange} (type={exchange_type}, durable={durable})")

    def declare_queue(
        self,
        queue: str,
        durable: bool = True,
        exclusive: bool = False,
        auto_delete: bool = False,
        arguments: dict | None = None,
    ) -> pika.frame.Method:
        """声明队列

        Args:
            queue: 队列名称
            durable: 是否持久化
            exclusive: 是否独占
            auto_delete: 无消费者时是否自动删除
            arguments: 队列参数(如TTL、死信队列等)

        Returns:
            队列声明结果
        """
        result = self.channel.queue_declare(
            queue=queue,
            durable=durable,
            exclusive=exclusive,
            auto_delete=auto_delete,
            arguments=arguments or {},
        )
        logger.info(
            f"Queue声明成功: {queue} (durable={durable}, "
            f"message_count={result.method.message_count})"
        )
        return result

    def bind_queue(
        self,
        queue: str,
        exchange: str,
        routing_key: str = "",
        arguments: dict | None = None,
    ) -> None:
        """绑定队列到exchange

        Args:
            queue: 队列名称
            exchange: exchange名称
            routing_key: 路由键
            arguments: 绑定参数
        """
        self.channel.queue_bind(
            queue=queue,
            exchange=exchange,
            routing_key=routing_key,
            arguments=arguments or {},
        )
        logger.info(f"Queue绑定成功: {queue} -> {exchange} (routing_key={routing_key})")

    def publish(
        self,
        exchange: str,
        routing_key: str,
        message: dict[str, Any],
        headers: dict | None = None,
    ) -> None:
        """发布消息

        Args:
            exchange: exchange名称
            routing_key: 路由键
            message: 消息内容(字典)
            headers: 消息头(可选)

        Raises:
            AMQPError: 发布失败时抛出
        """
        try:
            properties = pika.BasicProperties(
                delivery_mode=self.config.publish.delivery_mode,
                content_type=self.config.publish.content_type,
                content_encoding=self.config.publish.content_encoding,
                headers=headers or {},
            )

            self.channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=json.dumps(message).encode("utf-8"),
                properties=properties,
                mandatory=self.config.publish.mandatory,
            )

            logger.debug(f"消息发布成功: exchange={exchange}, routing_key={routing_key}")

        except AMQPError as e:
            logger.error(f"发布消息失败: {e}")
            raise

    def publish_batch(
        self,
        exchange: str,
        routing_key: str,
        messages: list[dict[str, Any]],
    ) -> int:
        """批量发布消息

        Args:
            exchange: exchange名称
            routing_key: 路由键
            messages: 消息列表

        Returns:
            成功发布的消息数量
        """
        success_count = 0

        for message in messages:
            try:
                self.publish(exchange, routing_key, message)
                success_count += 1
            except AMQPError as e:
                logger.error(f"批量发布失败: {e}, message={message}")

        logger.info(f"批量发布完成: {success_count}/{len(messages)}")
        return success_count

    def consume(
        self,
        queue: str,
        handler: Callable[[dict[str, Any]], None],
        max_messages: int | None = None,
        auto_ack: bool | None = None,
    ) -> int:
        """消费消息

        Args:
            queue: 队列名称
            handler: 消息处理函数
            max_messages: 最大消费消息数(None表示持续消费)
            auto_ack: 是否自动确认(None使用配置中的设置)

        Returns:
            已消费的消息数量
        """
        if auto_ack is None:
            auto_ack = self.config.consume.auto_ack

        message_count = 0

        logger.info(f"开始消费: queue={queue}, auto_ack={auto_ack}")

        try:
            for method_frame, properties, body in self.channel.consume(
                queue=queue, auto_ack=auto_ack
            ):
                if method_frame is None:
                    break

                try:
                    message = json.loads(body.decode("utf-8"))
                    handler(message)
                    message_count += 1

                    # 手动确认
                    if not auto_ack:
                        self.channel.basic_ack(method_frame.delivery_tag)

                    logger.debug(f"消息处理成功: delivery_tag={method_frame.delivery_tag}")

                    if max_messages and message_count >= max_messages:
                        logger.info(f"达到最大消费数量: {max_messages}")
                        break

                except Exception as e:
                    logger.error(f"消息处理失败: {e}, body={body}")
                    # 拒绝消息
                    if not auto_ack:
                        self.channel.basic_nack(method_frame.delivery_tag, requeue=False)

        except KeyboardInterrupt:
            logger.info("消费被中断")
        finally:
            self.channel.cancel()
            logger.info(f"消费完成: {message_count} 条消息")

        return message_count

    def get_message(self, queue: str) -> dict[str, Any] | None:
        """从队列获取单条消息(非阻塞)

        Args:
            queue: 队列名称

        Returns:
            消息内容,如果队列为空则返回None
        """
        method_frame, properties, body = self.channel.basic_get(
            queue=queue, auto_ack=self.config.consume.auto_ack
        )

        if method_frame is None:
            return None

        message = json.loads(body.decode("utf-8"))

        # 手动确认
        if not self.config.consume.auto_ack:
            self.channel.basic_ack(method_frame.delivery_tag)

        logger.debug(f"获取消息成功: delivery_tag={method_frame.delivery_tag}")

        return message

    def purge_queue(self, queue: str) -> int:
        """清空队列

        Args:
            queue: 队列名称

        Returns:
            清空的消息数量
        """
        result = self.channel.queue_purge(queue=queue)
        logger.info(f"队列清空成功: {queue}, 清空{result.method.message_count}条消息")
        return result.method.message_count

    def delete_queue(self, queue: str, if_unused: bool = False) -> int:
        """删除队列

        Args:
            queue: 队列名称
            if_unused: 仅在无消费者时删除

        Returns:
            删除的消息数量
        """
        result = self.channel.queue_delete(queue=queue, if_unused=if_unused)
        logger.info(f"队列删除成功: {queue}")
        return result.method.message_count

    def delete_exchange(self, exchange: str, if_unused: bool = False) -> None:
        """删除exchange

        Args:
            exchange: exchange名称
            if_unused: 仅在无绑定时删除
        """
        self.channel.exchange_delete(exchange=exchange, if_unused=if_unused)
        logger.info(f"Exchange删除成功: {exchange}")

    def close(self) -> None:
        """关闭客户端,释放资源"""
        if self._channel and not self._channel.is_closed:
            self._channel.close()
            logger.info("RabbitMQ通道已关闭")

        if self._connection and not self._connection.is_closed:
            self._connection.close()
            logger.info("RabbitMQ连接已关闭")


__all__ = ["RabbitMQClient"]
