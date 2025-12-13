"""Kafka消息队列客户端

提供Kafka Producer和Consumer的封装。

v3.9.0新增 - 基于confluent-kafka (librdkafka) 实现

版本说明 (v3.10.0+): 使用 confluent-kafka>=2.12.0
- Windows 预编译 wheel 支持，Python 3.12+ 可直接安装
- SSL 问题: 2.0+ 在某些环境可能遇到错误，可使用 KafkaSSLConfig workaround 配置

使用示例::

    from df_test_framework.capabilities.messengers.queue.kafka import KafkaClient, KafkaConfig

    # 创建客户端
    config = KafkaConfig(bootstrap_servers=["localhost:9092"])
    client = KafkaClient(config)

    # 发送消息
    client.send("test-topic", {"user_id": 123, "action": "login"})

    # 消费消息
    client.consume(
        topics=["test-topic"],
        group_id="test-group",
        handler=lambda msg: print(msg),
        max_messages=10
    )

    client.close()
"""

from .client import KafkaClient
from .config import (
    KafkaConfig,
    KafkaConsumerConfig,
    KafkaProducerConfig,
    KafkaSSLConfig,
)

__all__ = [
    "KafkaClient",
    "KafkaConfig",
    "KafkaProducerConfig",
    "KafkaConsumerConfig",
    "KafkaSSLConfig",
]
