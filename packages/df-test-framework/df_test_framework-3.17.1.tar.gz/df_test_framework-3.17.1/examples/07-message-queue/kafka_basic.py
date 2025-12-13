"""Kafka基本使用示例

演示如何使用KafkaClient发送和消费消息。

技术栈: confluent-kafka 1.9.2 (librdkafka)
- 生产性能提升3倍 (相比 kafka-python3)
- 消费性能提升50%

前置条件:
1. 安装依赖: pip install 'df-test-framework[kafka]'
2. 启动Kafka服务: docker-compose -f docker-compose-kafka.yml up -d
"""

from df_test_framework.messengers.queue.kafka import (
    KafkaClient,
    KafkaConfig,
    KafkaProducerConfig,
)


def main():
    """主函数"""
    # 1. 创建Kafka客户端
    print("📡 连接Kafka...")
    config = KafkaConfig(
        bootstrap_servers=["localhost:9092"],
        producer=KafkaProducerConfig(
            acks="all",  # 等待所有副本确认
            compression_type="gzip",  # 启用压缩
        ),
    )
    client = KafkaClient(config)

    # 2. 发送消息
    print("\n📤 发送消息...")
    topic = "demo-topic"

    test_messages = [
        {"user_id": 1, "action": "login", "timestamp": "2025-11-25T10:00:00Z"},
        {"user_id": 2, "action": "view_product", "product_id": "P001"},
        {"user_id": 1, "action": "add_to_cart", "product_id": "P001"},
        {"user_id": 1, "action": "checkout", "order_id": "ORD-001"},
    ]

    for message in test_messages:
        client.send(topic, message)
        print(f"  ✅ 发送: {message}")

    # 确保所有消息都发送完成
    client.flush(timeout=5.0)
    print("  📤 所有消息已发送")

    # 3. 消费消息
    print(f"\n📥 从 {topic} 消费消息...")

    messages_received = []

    def message_handler(message):
        """消息处理函数"""
        messages_received.append(message)
        print(f"  ✅ 收到: {message}")

    # 消费最多4条消息
    count = client.consume(
        topics=[topic],
        group_id="demo-consumer-group",
        handler=message_handler,
        max_messages=4,
    )

    print("\n📊 统计:")
    print(f"  - 发送消息数: {len(test_messages)}")
    print(f"  - 接收消息数: {count}")

    # 4. 验证
    assert count == len(test_messages), "消息数量不匹配"
    print("\n✅ 所有消息都成功接收!")

    # 5. 关闭客户端
    client.close()
    print("\n👋 连接已关闭")


if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请运行: pip install 'df-test-framework[kafka]'")
    except Exception as e:
        print(f"❌ 错误: {e}")
        print("请确保Kafka服务已启动: docker-compose -f docker-compose-kafka.yml up -d")
