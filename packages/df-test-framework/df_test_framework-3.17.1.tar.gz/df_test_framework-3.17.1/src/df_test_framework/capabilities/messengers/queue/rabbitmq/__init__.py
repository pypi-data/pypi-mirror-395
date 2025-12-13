"""RabbitMQ消息队列客户端

提供RabbitMQ Publisher和Consumer的封装。

v3.9.0新增

使用示例::

    from df_test_framework.capabilities.messengers.queue.rabbitmq import (
        RabbitMQClient, RabbitMQConfig
    )

    # 创建客户端
    config = RabbitMQConfig()
    client = RabbitMQClient(config)

    # 声明exchange、queue并绑定
    client.declare_exchange("test-exchange", "direct")
    client.declare_queue("test-queue")
    client.bind_queue("test-queue", "test-exchange", "test-key")

    # 发布消息
    client.publish(
        exchange="test-exchange",
        routing_key="test-key",
        message={"user_id": 123}
    )

    # 消费消息
    client.consume(
        queue="test-queue",
        handler=lambda msg: print(msg),
        max_messages=10
    )

    client.close()
"""

from .client import RabbitMQClient
from .config import (
    RabbitMQConfig,
    RabbitMQConnectionConfig,
    RabbitMQConsumeConfig,
    RabbitMQPublishConfig,
)

__all__ = [
    "RabbitMQClient",
    "RabbitMQConfig",
    "RabbitMQConnectionConfig",
    "RabbitMQPublishConfig",
    "RabbitMQConsumeConfig",
]
