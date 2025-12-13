"""消息传递能力层 - Layer 1

提供消息队列和发布/订阅模式的消息传递能力

v3.9.0 新增:
- queue/: 消息队列客户端
  - Kafka: 基于 confluent-kafka 1.9.2 (高性能,企业级)
  - RabbitMQ: 基于 pika (AMQP 0-9-1)
  - RocketMQ: 基于 rocketmq-python-client (Apache官方)

未来计划:
- pubsub/: 发布订阅模式（Redis Pub/Sub、MQTT等）
"""

__all__ = []
