"""RocketMQ消息队列客户端

提供RocketMQ Producer和Consumer的封装。

v3.9.0新增

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
    client.send("test-topic", {"user_id": 123, "action": "login"}, tags="login")

    # 订阅消息
    client.subscribe(
        topic="test-topic",
        handler=lambda msg: print(msg) or True,  # 返回True表示消费成功
        tags="*"
    )

    client.close()
"""

from .client import RocketMQClient
from .config import (
    RocketMQConfig,
    RocketMQConsumerConfig,
    RocketMQProducerConfig,
)

__all__ = [
    "RocketMQClient",
    "RocketMQConfig",
    "RocketMQProducerConfig",
    "RocketMQConsumerConfig",
]
