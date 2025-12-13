"""RocketMQ消息队列客户端

提供RocketMQ Producer和Consumer的封装。

v3.9.0新增

v3.14.0 新增:
- 集成 EventBus 发布消息事件
- 支持 event_bus 参数

基于apache/rocketmq-client-python (官方Python客户端)

使用示例::

    from df_test_framework.capabilities.messengers.queue.rocketmq import (
        RocketMQClient, RocketMQConfig, RocketMQProducerConfig
    )

    # 创建客户端
    config = RocketMQConfig(
        namesrv_addr="localhost:9876",
        producer=RocketMQProducerConfig(group_name="test-producer")
    )
    client = RocketMQClient(config)

    # 发送消息
    client.send(
        topic="test-topic",
        message={"user_id": 123, "action": "login"},
        tags="login"
    )

    client.close()
"""

from __future__ import annotations

import json
import logging
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from .config import RocketMQConfig

if TYPE_CHECKING:
    from df_test_framework.infrastructure.events import EventBus

try:
    from rocketmq.client import ConsumeStatus, Message, Producer, PushConsumer
except ImportError:
    raise ImportError(
        "rocketmq-python-client 未安装。请运行: pip install 'df-test-framework[rocketmq]'"
    )

logger = logging.getLogger(__name__)


class RocketMQClient:
    """RocketMQ消息队列客户端

    封装apache/rocketmq-client-python的Producer和Consumer,提供简化的消息发送和消费接口。

    Attributes:
        config: RocketMQ配置
    """

    def __init__(self, config: RocketMQConfig, event_bus: EventBus | None = None):
        """初始化RocketMQ客户端

        Args:
            config: RocketMQ配置对象
            event_bus: 🆕 v3.14.0 事件总线（可选）
        """
        self.config = config
        self._event_bus = event_bus
        self._producer: Producer | None = None
        self._consumer: PushConsumer | None = None

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

    def _get_producer(self, group_name: str | None = None) -> Producer:
        """获取或创建Producer实例

        Args:
            group_name: Producer组名,如果为None则使用配置中的group_name

        Returns:
            Producer实例
        """
        if self._producer is None:
            if group_name is None:
                if self.config.producer is None:
                    raise ValueError("必须提供producer配置或group_name参数")
                group_name = self.config.producer.group_name

            producer = Producer(group_name)
            producer.set_name_server_address(self.config.namesrv_addr)

            # 设置ACL认证(如果配置)
            if self.config.access_key and self.config.secret_key:
                producer.set_session_credentials(
                    self.config.access_key,
                    self.config.secret_key,
                    "",  # channel参数
                )

            # 启动Producer
            producer.start()
            self._producer = producer
            logger.info(f"RocketMQ Producer启动成功: group={group_name}")

        return self._producer

    def send(
        self,
        topic: str,
        message: dict[str, Any],
        tags: str | None = None,
        keys: str | None = None,
        group_name: str | None = None,
    ) -> str:
        """同步发送消息到RocketMQ主题

        Args:
            topic: 主题名称
            message: 消息内容(字典)
            tags: 消息标签(可选,用于消息过滤)
            keys: 消息键(可选,用于索引)
            group_name: Producer组名(可选)

        Returns:
            消息ID

        Raises:
            Exception: 发送失败时抛出
        """
        try:
            producer = self._get_producer(group_name)

            # 创建消息
            msg = Message(topic)
            msg.set_body(json.dumps(message))

            if tags:
                msg.set_tags(tags)
            if keys:
                msg.set_keys(keys)

            # 同步发送
            ret = producer.send_sync(msg)

            logger.debug(
                f"消息发送成功: topic={topic}, msgId={ret.msg_id}, "
                f"status={ret.status}, offset={ret.offset}"
            )

            return ret.msg_id

        except Exception as e:
            logger.error(f"发送消息失败: {e}")
            raise

    def send_batch(
        self,
        topic: str,
        messages: list[dict[str, Any]],
        tags: str | None = None,
        group_name: str | None = None,
    ) -> int:
        """批量发送消息

        Args:
            topic: 主题名称
            messages: 消息列表
            tags: 消息标签
            group_name: Producer组名

        Returns:
            成功发送的消息数量
        """
        success_count = 0

        for message in messages:
            try:
                self.send(topic, message, tags=tags, group_name=group_name)
                success_count += 1
            except Exception as e:
                logger.error(f"批量发送失败: {e}, message={message}")

        logger.info(f"批量发送完成: {success_count}/{len(messages)}")
        return success_count

    def send_oneway(
        self,
        topic: str,
        message: dict[str, Any],
        tags: str | None = None,
        group_name: str | None = None,
    ) -> None:
        """单向发送消息(不等待broker响应,性能最高)

        Args:
            topic: 主题名称
            message: 消息内容
            tags: 消息标签
            group_name: Producer组名
        """
        try:
            producer = self._get_producer(group_name)

            # 创建消息
            msg = Message(topic)
            msg.set_body(json.dumps(message))

            if tags:
                msg.set_tags(tags)

            # 单向发送
            producer.send_oneway(msg)

            logger.debug(f"单向发送成功: topic={topic}")

        except Exception as e:
            logger.error(f"单向发送失败: {e}")
            raise

    def subscribe(
        self,
        topic: str,
        handler: Callable[[dict[str, Any]], bool],
        tags: str = "*",
        group_name: str | None = None,
    ) -> None:
        """订阅消息并启动消费

        Args:
            topic: 主题名称
            handler: 消息处理函数,返回True表示消费成功,False表示重新消费
            tags: 标签过滤表达式(默认"*"表示订阅所有)
            group_name: Consumer组名

        注意: 此方法会阻塞,直到调用shutdown()
        """
        if group_name is None:
            if self.config.consumer is None:
                raise ValueError("必须提供consumer配置或group_name参数")
            group_name = self.config.consumer.group_name

        consumer = PushConsumer(group_name)
        consumer.set_name_server_address(self.config.namesrv_addr)

        # 设置ACL认证
        if self.config.access_key and self.config.secret_key:
            consumer.set_session_credentials(self.config.access_key, self.config.secret_key, "")

        def callback(msg):
            """消息回调函数"""
            try:
                # 解析消息
                body = msg.body.decode("utf-8")
                message_dict = json.loads(body)

                # 调用用户处理函数
                success = handler(message_dict)

                logger.debug(
                    f"消息处理{'成功' if success else '失败'}: topic={msg.topic}, msgId={msg.id}"
                )

                return ConsumeStatus.CONSUME_SUCCESS if success else ConsumeStatus.RECONSUME_LATER

            except Exception as e:
                logger.error(f"消息处理异常: {e}")
                return ConsumeStatus.RECONSUME_LATER

        # 订阅主题
        consumer.subscribe(topic, callback, tags)
        consumer.start()

        self._consumer = consumer
        logger.info(f"开始消费: topic={topic}, tags={tags}, group={group_name}")

    def shutdown(self) -> None:
        """停止消费"""
        if self._consumer:
            self._consumer.shutdown()
            logger.info("Consumer已停止")

    def close(self) -> None:
        """关闭客户端,释放资源"""
        if self._producer:
            self._producer.shutdown()
            logger.info("RocketMQ Producer已关闭")

        if self._consumer:
            self._consumer.shutdown()
            logger.info("RocketMQ Consumer已关闭")


__all__ = ["RocketMQClient"]
