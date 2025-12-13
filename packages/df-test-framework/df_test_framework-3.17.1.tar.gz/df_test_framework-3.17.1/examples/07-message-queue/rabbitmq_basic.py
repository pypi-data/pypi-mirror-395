"""RabbitMQ基本使用示例

演示如何使用RabbitMQClient发布和消费消息。

前置条件:
1. 安装依赖: pip install 'df-test-framework[rabbitmq]'
2. 启动RabbitMQ服务: docker-compose -f docker-compose-rabbitmq.yml up -d
"""

from df_test_framework.messengers.queue.rabbitmq import (
    RabbitMQClient,
    RabbitMQConfig,
)


def main():
    """主函数"""
    # 1. 创建RabbitMQ客户端
    print("📡 连接RabbitMQ...")
    config = RabbitMQConfig()  # 默认localhost:5672, guest/guest
    client = RabbitMQClient(config)

    # 2. 声明exchange、queue并绑定
    print("\n🔧 声明资源...")
    exchange = "demo-exchange"
    queue = "demo-queue"
    routing_key = "demo.key"

    client.declare_exchange(exchange, exchange_type="direct")
    client.declare_queue(queue)
    client.bind_queue(queue, exchange, routing_key)
    print(f"  ✅ Exchange: {exchange}")
    print(f"  ✅ Queue: {queue}")
    print(f"  ✅ Binding: {routing_key}")

    # 3. 发布消息
    print(f"\n📤 发布消息到 {exchange}...")

    test_messages = [
        {"user_id": 1, "action": "login"},
        {"user_id": 2, "action": "view_product", "product_id": "P001"},
        {"user_id": 1, "action": "add_to_cart", "product_id": "P001"},
    ]

    for message in test_messages:
        client.publish(
            exchange=exchange, routing_key=routing_key, message=message
        )
        print(f"  ✅ 发布: {message}")

    # 4. 消费消息
    print(f"\n📥 从 {queue} 消费消息...")

    messages_received = []

    def message_handler(message):
        """消息处理函数"""
        messages_received.append(message)
        print(f"  ✅ 收到: {message}")

    # 消费所有消息
    count = client.consume(
        queue=queue, handler=message_handler, max_messages=3
    )

    print("\n📊 统计:")
    print(f"  - 发布消息数: {len(test_messages)}")
    print(f"  - 接收消息数: {count}")

    # 5. 验证
    assert count == len(test_messages), "消息数量不匹配"
    print("\n✅ 所有消息都成功接收!")

    # 6. 清理资源
    print("\n🧹 清理资源...")
    client.delete_queue(queue)
    client.delete_exchange(exchange)
    print("  ✅ 资源已删除")

    # 7. 关闭客户端
    client.close()
    print("\n👋 连接已关闭")


if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请运行: pip install 'df-test-framework[rabbitmq]'")
    except Exception as e:
        print(f"❌ 错误: {e}")
        print(
            "请确保RabbitMQ服务已启动: docker-compose -f docker-compose-rabbitmq.yml up -d"
        )
