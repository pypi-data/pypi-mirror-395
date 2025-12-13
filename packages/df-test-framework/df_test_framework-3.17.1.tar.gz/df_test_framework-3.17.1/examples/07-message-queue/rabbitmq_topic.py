"""RabbitMQ Topic Exchange示例

演示如何使用Topic Exchange实现基于模式匹配的消息路由。

Topic Exchange使用通配符:
- * 匹配一个单词
- # 匹配零个或多个单词

前置条件:
1. 安装依赖: pip install 'df-test-framework[rabbitmq]'
2. 启动RabbitMQ服务
"""

from df_test_framework.messengers.queue.rabbitmq import (
    RabbitMQClient,
    RabbitMQConfig,
)


def main():
    """主函数"""
    print("📡 连接RabbitMQ...")
    client = RabbitMQClient(RabbitMQConfig())

    # 1. 声明Topic Exchange
    print("\n🔧 声明Topic Exchange...")
    exchange = "logs"
    client.declare_exchange(exchange, exchange_type="topic")

    # 2. 声明队列并绑定不同的routing pattern
    print("\n🔧 声明队列并绑定...")

    # 所有日志
    client.declare_queue("all-logs")
    client.bind_queue("all-logs", exchange, routing_key="#")
    print("  ✅ all-logs 绑定 '#' (所有消息)")

    # 只有错误日志
    client.declare_queue("error-logs")
    client.bind_queue("error-logs", exchange, routing_key="*.error")
    print("  ✅ error-logs 绑定 '*.error'")

    # 只有数据库相关日志
    client.declare_queue("db-logs")
    client.bind_queue("db-logs", exchange, routing_key="db.*")
    print("  ✅ db-logs 绑定 'db.*'")

    # 3. 发布不同routing key的消息
    print(f"\n📤 发布消息到 {exchange}...")

    test_logs = [
        ("app.info", {"level": "info", "msg": "Application started"}),
        ("app.error", {"level": "error", "msg": "Unexpected error"}),
        ("db.info", {"level": "info", "msg": "Connected to database"}),
        ("db.error", {"level": "error", "msg": "Connection timeout"}),
        ("api.warning", {"level": "warning", "msg": "Rate limit exceeded"}),
    ]

    for routing_key, message in test_logs:
        client.publish(exchange, routing_key, message)
        print(f"  ✅ [{routing_key}] {message['msg']}")

    # 4. 消费各个队列的消息
    print("\n📥 消费消息...")

    # all-logs应该收到所有5条消息
    all_logs_count = 0
    while True:
        msg = client.get_message("all-logs")
        if msg is None:
            break
        all_logs_count += 1
        print(f"  📋 [all-logs] {msg['msg']}")

    # error-logs应该收到2条(app.error, db.error)
    error_logs_count = 0
    while True:
        msg = client.get_message("error-logs")
        if msg is None:
            break
        error_logs_count += 1
        print(f"  ❌ [error-logs] {msg['msg']}")

    # db-logs应该收到2条(db.info, db.error)
    db_logs_count = 0
    while True:
        msg = client.get_message("db-logs")
        if msg is None:
            break
        db_logs_count += 1
        print(f"  💾 [db-logs] {msg['msg']}")

    # 5. 验证结果
    print("\n📊 统计:")
    print(f"  - 发布消息数: {len(test_logs)}")
    print(f"  - all-logs 收到: {all_logs_count} (预期 5)")
    print(f"  - error-logs 收到: {error_logs_count} (预期 2)")
    print(f"  - db-logs 收到: {db_logs_count} (预期 2)")

    assert all_logs_count == 5, "all-logs应收到5条消息"
    assert error_logs_count == 2, "error-logs应收到2条消息"
    assert db_logs_count == 2, "db-logs应收到2条消息"

    print("\n✅ Topic Exchange路由正确!")

    # 6. 清理
    print("\n🧹 清理资源...")
    client.delete_queue("all-logs")
    client.delete_queue("error-logs")
    client.delete_queue("db-logs")
    client.delete_exchange(exchange)

    client.close()
    print("\n👋 完成")


if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请运行: pip install 'df-test-framework[rabbitmq]'")
    except Exception as e:
        print(f"❌ 错误: {e}")
