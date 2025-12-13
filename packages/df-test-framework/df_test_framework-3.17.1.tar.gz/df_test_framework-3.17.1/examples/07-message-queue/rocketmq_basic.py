"""RocketMQ基本使用示例

演示如何使用RocketMQClient发送和消费消息。

前置条件:
1. 安装依赖: pip install 'df-test-framework[rocketmq]'
2. 启动RocketMQ服务: docker-compose -f docker-compose-rocketmq.yml up -d
"""

from df_test_framework.messengers.queue.rocketmq import (
    RocketMQClient,
    RocketMQConfig,
    RocketMQProducerConfig,
)


def main():
    """主函数"""
    # 1. 创建RocketMQ客户端
    print("📡 连接RocketMQ...")
    config = RocketMQConfig(
        namesrv_addr="localhost:9876",
        producer=RocketMQProducerConfig(group_name="test-producer"),
    )
    client = RocketMQClient(config)

    # 2. 发送消息
    print("\n📤 发送消息...")
    topic = "demo-topic"

    test_messages = [
        {"user_id": 1, "action": "login", "timestamp": "2025-11-25T10:00:00Z"},
        {"user_id": 2, "action": "view_product", "product_id": "P001"},
        {"user_id": 1, "action": "add_to_cart", "product_id": "P001"},
        {"user_id": 1, "action": "checkout", "order_id": "ORD-001"},
    ]

    msg_ids = []
    for message in test_messages:
        msg_id = client.send(
            topic=topic,
            message=message,
            tags="test",  # 标签用于消息过滤
        )
        msg_ids.append(msg_id)
        print(f"  ✅ 发送: {message} (MsgID: {msg_id})")

    # 3. 批量发送
    print("\n📤 批量发送消息...")
    batch_messages = [
        {"order_id": f"ORD-{i}", "amount": 100 * i} for i in range(1, 4)
    ]

    count = client.send_batch(topic, batch_messages, tags="batch")
    print(f"  ✅ 批量发送成功: {count} 条消息")

    # 4. 单向发送(高性能,不等待响应)
    print("\n⚡ 单向发送...")
    client.send_oneway(topic, {"type": "metric", "value": 99}, tags="fast")
    print("  ✅ 单向发送成功")

    print("\n📊 统计:")
    print(f"  - 同步发送消息数: {len(msg_ids)}")
    print(f"  - 批量发送消息数: {count}")
    print("  - 单向发送消息数: 1")
    print(f"  - 总计: {len(msg_ids) + count + 1}")

    # 5. 关闭客户端
    client.close()
    print("\n👋 连接已关闭")

    # 注意: 消息消费需要单独进程,详见rocketmq_consumer.py


if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请运行: pip install 'df-test-framework[rocketmq]'")
    except Exception as e:
        print(f"❌ 错误: {e}")
        print(
            "请确保RocketMQ服务已启动: docker-compose -f docker-compose-rocketmq.yml up -d"
        )
