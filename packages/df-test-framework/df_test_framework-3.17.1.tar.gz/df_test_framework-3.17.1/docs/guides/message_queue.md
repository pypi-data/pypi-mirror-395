# 消息队列使用指南

> **版本**: v3.17.0 | **更新**: 2025-12-05
> **引入版本**: v3.9.0
> **特性**: Kafka + RabbitMQ + RocketMQ客户端

df-test-framework提供了Kafka、RabbitMQ和RocketMQ的封装客户端,简化消息队列的测试场景。

---

## 📦 安装

消息队列客户端是**可选依赖**,需要单独安装:

```bash
# 安装Kafka支持
pip install 'df-test-framework[kafka]'

# 安装RabbitMQ支持
pip install 'df-test-framework[rabbitmq]'

# 安装RocketMQ支持
pip install 'df-test-framework[rocketmq]'

# 同时安装全部
pip install 'df-test-framework[mq]'
```

---

## 🚀 Kafka客户端

### 基本用法

```python
from df_test_framework.messengers.queue.kafka import KafkaClient, KafkaConfig

# 创建客户端
config = KafkaConfig(
    bootstrap_servers=["localhost:9092"],
    timeout=10
)
client = KafkaClient(config)

# 发送消息
client.send(
    topic="user-events",
    message={"user_id": 123, "action": "login"},
    key="user-123"  # 可选,用于分区
)

# 批量发送
messages = [
    {"user_id": 1, "action": "login"},
    {"user_id": 2, "action": "logout"},
]
count = client.send_batch("user-events", messages)
print(f"发送了 {count} 条消息")

# 消费消息
messages_received = []
client.consume(
    topics=["user-events"],
    group_id="test-consumer-group",
    handler=lambda msg: messages_received.append(msg),
    max_messages=10,  # 最多消费10条
    max_idle_seconds=5.0  # 空闲超过5秒自动退出
)

# 关闭客户端
client.close()
```

### 高级配置

#### 技术栈说明

**当前版本**: `confluent-kafka 1.9.2` (基于 librdkafka)

**性能优势**:
- 生产性能提升 **3倍** (相比 kafka-python3)
- 消费性能提升 **50%**
- 基于高性能 C 库 librdkafka

**版本说明** (v3.10.0+): 使用 confluent-kafka>=2.12.0
- Windows 预编译 wheel 支持，Python 3.12+ 可直接安装
- SSL 问题: 2.0+ 在某些环境可能遇到 SSL_HANDSHAKE 错误，框架提供 workaround 配置

#### Producer配置

```python
from df_test_framework.messengers.queue.kafka import (
    KafkaConfig,
    KafkaProducerConfig
)

config = KafkaConfig(
    bootstrap_servers=["kafka1:9092", "kafka2:9092"],
    producer=KafkaProducerConfig(
        acks="all",  # 等待所有副本确认
        retries=5,  # 重试次数
        compression_type="gzip",  # 压缩类型: gzip, snappy, lz4, zstd
        batch_num_messages=10000,  # 批量消息数 (librdkafka: batch.num.messages)
        queue_buffering_max_ms=10,  # 批量等待时间(毫秒)
        queue_buffering_max_kbytes=32768,  # 缓冲区大小(KB)
        enable_idempotence=True,  # 启用幂等性(确保消息不重复)
    )
)
```

#### Consumer配置

```python
from df_test_framework.messengers.queue.kafka import (
    KafkaConfig,
    KafkaConsumerConfig
)

config = KafkaConfig(
    bootstrap_servers=["localhost:9092"],
    consumer=KafkaConsumerConfig(
        group_id="my-consumer-group",
        auto_offset_reset="earliest",  # 从最早的消息开始
        enable_auto_commit=False,  # 手动提交offset
    )
)
```

#### SSL/TLS 配置

**SSL 问题 Workaround** (v3.10.0+):
- confluent-kafka 2.0+ 在某些环境可能遇到 SSL_HANDSHAKE 错误
- 框架提供 workaround 配置项解决此问题
- 关键: `enable_ssl_certificate_verification` 必须是字符串("true"/"false")，不是布尔值

##### 方式1: 使用证书(生产环境推荐)

```python
from df_test_framework.messengers.queue.kafka import (
    KafkaConfig,
    KafkaSSLConfig,
    KafkaProducerConfig
)

config = KafkaConfig(
    bootstrap_servers=["kafka.example.com:9093"],
    producer=KafkaProducerConfig(),
    ssl=KafkaSSLConfig(
        security_protocol="SSL",  # 或 SASL_SSL
        ssl_ca_location="/path/to/ca-cert.pem",  # CA证书
        ssl_certificate_location="/path/to/client-cert.pem",  # 客户端证书
        ssl_key_location="/path/to/client-key.pem",  # 客户端私钥
        ssl_key_password="your-key-password"  # 私钥密码(可选)
    )
)
client = KafkaClient(config)
```

##### 方式2: SASL认证

```python
config = KafkaConfig(
    bootstrap_servers=["kafka.example.com:9093"],
    producer=KafkaProducerConfig(),
    ssl=KafkaSSLConfig(
        security_protocol="SASL_SSL",
        sasl_mechanism="PLAIN",  # 或 SCRAM-SHA-256, SCRAM-SHA-512, GSSAPI
        sasl_username="your-username",
        sasl_password="your-password",
        ssl_ca_location="/path/to/ca-cert.pem"
    )
)
```

##### 方式3: 禁用SSL验证(仅测试环境!)

```python
config = KafkaConfig(
    bootstrap_servers=["kafka-test.example.com:9092"],
    producer=KafkaProducerConfig(),
    ssl=KafkaSSLConfig(
        security_protocol="PLAINTEXT",  # 或 SSL
        # 针对 2.0+ 版本的 workaround (1.9.2 通常不需要)
        enable_ssl_certificate_verification="false",  # 注意: 必须是字符串!
        ssl_endpoint_identification_algorithm="none"
    )
)
```

**安全警告**: 生产环境切勿禁用证书验证!

#### 同步发送(等待确认)

```python
# send() 是异步发送,返回后消息可能还在队列中
client.send("user-events", {"user_id": 123})

# send_sync() 会等待broker确认,返回消息元数据
result = client.send_sync("user-events", {"user_id": 123}, timeout=10.0)
print(f"发送成功: topic={result['topic']}, "
      f"partition={result['partition']}, offset={result['offset']}")
```

#### AdminClient - 主题管理

```python
# 创建主题
client.create_topic(
    topic="new-topic",
    num_partitions=3,  # 3个分区
    replication_factor=2,  # 2个副本
    config={"retention.ms": "86400000"}  # 保留1天
)

# 删除主题
client.delete_topic("old-topic")
```

### 在测试中使用

使用pytest fixtures:

```python
# conftest.py
from df_test_framework.testing.fixtures.message_queue import (
    kafka_client, kafka_config
)

# test_kafka.py
def test_send_and_consume(kafka_client):
    # 发送消息
    test_message = {"user_id": 123, "action": "login"}
    kafka_client.send("test-topic", test_message)

    # 消费消息
    messages = []
    kafka_client.consume(
        topics=["test-topic"],
        group_id="test-group",
        handler=lambda msg: messages.append(msg),
        max_messages=1
    )

    assert len(messages) == 1
    assert messages[0] == test_message
```

---

## 🐰 RabbitMQ客户端

### 协议选择说明

#### 技术栈: Pika (AMQP 0-9-1)

**当前版本**: `pika >= 1.3.0` (基于 AMQP 0-9-1 协议)

**为什么选择 AMQP 0-9-1 而非 AMQP 1.0**:

| 对比维度 | AMQP 0-9-1 (Pika) | AMQP 1.0 (rabbitmq-amqp-python-client) |
|---------|-------------------|----------------------------------------|
| **协议关系** | RabbitMQ原生协议 | 完全不同的协议标准 |
| **Python客户端** | `pika` v1.3.2 (2022年10月) | `rabbitmq-amqp-python-client` v0.3.0 (2024年11月) |
| **成熟度** | ✅ 生产就绪 | ⚠️ **Alpha阶段** |
| **文档完整性** | ✅ 完整文档和最佳实践 | ⚠️ 文档不完整 |
| **社区支持** | ✅ 活跃社区,丰富案例 | ⚠️ 社区资源有限 |
| **功能支持** | ✅ 完整Exchange/Queue/Binding | 🔄 功能逐步完善中 |
| **维护状态** | ✅ Stable (仅bug修复) | 🚧 Alpha (API可能变化) |
| **适用场景** | 生产环境 | 实验和未来迁移准备 |

**协议差异**:
- **AMQP 0-9-1**: RabbitMQ的核心设计协议,支持Exchange、Queue、Binding等核心概念,**永久支持**
- **AMQP 1.0**: OASIS标准协议,是一个完全不同的协议(不是版本升级!),更通用但更复杂

**决策理由**:
1. **生产稳定性**: 测试框架需要稳定可靠的依赖,不能使用Alpha阶段的库
2. **RabbitMQ原生支持**: AMQP 0-9-1是RabbitMQ的核心协议,不会被废弃
3. **功能完整性**: Pika已支持所有RabbitMQ特性(Exchange、Queue、Binding、死信队列等)
4. **社区成熟度**: 丰富的文档、案例和生产实践经验

**未来计划**:
- 持续关注 `rabbitmq-amqp-python-client` 的成熟度进展
- 当其达到 Stable 版本时,考虑提供 AMQP 1.0 支持作为可选方案
- 保持对 AMQP 0-9-1 的长期支持(RabbitMQ永久支持该协议)

### 基本用法

```python
from df_test_framework.messengers.queue.rabbitmq import (
    RabbitMQClient,
    RabbitMQConfig
)

# 创建客户端
config = RabbitMQConfig()  # 默认localhost:5672, guest/guest
client = RabbitMQClient(config)

# 1. 声明exchange和queue
client.declare_exchange("user-exchange", exchange_type="direct")
client.declare_queue("user-queue")
client.bind_queue("user-queue", "user-exchange", routing_key="user.login")

# 2. 发布消息
client.publish(
    exchange="user-exchange",
    routing_key="user.login",
    message={"user_id": 123, "timestamp": "2025-11-25"}
)

# 3. 消费消息
messages_received = []
client.consume(
    queue="user-queue",
    handler=lambda msg: messages_received.append(msg),
    max_messages=10
)

# 4. 清理资源
client.delete_queue("user-queue")
client.delete_exchange("user-exchange")
client.close()
```

### 高级配置

#### 连接配置

```python
from df_test_framework.messengers.queue.rabbitmq import (
    RabbitMQConfig,
    RabbitMQConnectionConfig
)
from pydantic import SecretStr

config = RabbitMQConfig(
    connection=RabbitMQConnectionConfig(
        host="rabbitmq.example.com",
        port=5672,
        virtual_host="/production",
        username="admin",
        password=SecretStr("secret"),
        heartbeat=600,
        connection_attempts=3,
        retry_delay=2
    )
)
```

#### 发布配置

```python
from df_test_framework.messengers.queue.rabbitmq import (
    RabbitMQConfig,
    RabbitMQPublishConfig
)

config = RabbitMQConfig(
    publish=RabbitMQPublishConfig(
        delivery_mode=2,  # 持久化
        mandatory=True,  # 路由失败时返回
        content_type="application/json"
    )
)
```

#### 消费配置

```python
from df_test_framework.messengers.queue.rabbitmq import (
    RabbitMQConfig,
    RabbitMQConsumeConfig
)

config = RabbitMQConfig(
    consume=RabbitMQConsumeConfig(
        auto_ack=False,  # 手动确认
        prefetch_count=10,  # 预取10条消息
    )
)
```

### Exchange类型

RabbitMQ支持4种exchange类型:

#### 1. Direct Exchange

```python
# 精确匹配routing key
client.declare_exchange("logs", exchange_type="direct")
client.declare_queue("error-logs")
client.bind_queue("error-logs", "logs", routing_key="error")

# 只有routing_key="error"的消息才会路由到error-logs队列
client.publish("logs", "error", {"level": "error", "msg": "Database connection failed"})
```

#### 2. Topic Exchange

```python
# 支持通配符匹配
client.declare_exchange("events", exchange_type="topic")
client.declare_queue("user-events")
client.bind_queue("user-events", "events", routing_key="user.*")

# 匹配 user.* 的消息都会路由过来
client.publish("events", "user.login", {"user_id": 123})
client.publish("events", "user.logout", {"user_id": 123})
```

#### 3. Fanout Exchange

```python
# 广播模式,忽略routing key
client.declare_exchange("notifications", exchange_type="fanout")
client.declare_queue("email-queue")
client.declare_queue("sms-queue")
client.bind_queue("email-queue", "notifications", routing_key="")
client.bind_queue("sms-queue", "notifications", routing_key="")

# 消息会同时发送到所有绑定的队列
client.publish("notifications", "", {"message": "System maintenance at 2AM"})
```

#### 4. Headers Exchange

```python
# 根据消息头匹配
client.declare_exchange("tasks", exchange_type="headers")
```

### 队列操作

```python
# 声明持久化队列
client.declare_queue("orders", durable=True)

# 声明带TTL的队列(消息30秒后过期)
client.declare_queue(
    "temp-messages",
    arguments={"x-message-ttl": 30000}
)

# 声明死信队列
client.declare_queue(
    "main-queue",
    arguments={
        "x-dead-letter-exchange": "dlx",
        "x-dead-letter-routing-key": "dead"
    }
)

# 获取单条消息(非阻塞)
message = client.get_message("orders")
if message:
    print(f"Got message: {message}")

# 清空队列
count = client.purge_queue("temp-messages")
print(f"清空了 {count} 条消息")

# 删除队列
client.delete_queue("temp-messages")
```

### 在测试中使用

使用pytest fixtures:

```python
# conftest.py
from df_test_framework.testing.fixtures.message_queue import (
    rabbitmq_client, rabbitmq_config
)

# test_rabbitmq.py
def test_fanout_exchange(rabbitmq_client):
    # 声明fanout exchange和多个队列
    rabbitmq_client.declare_exchange("broadcast", "fanout")
    rabbitmq_client.declare_queue("queue1")
    rabbitmq_client.declare_queue("queue2")
    rabbitmq_client.bind_queue("queue1", "broadcast", "")
    rabbitmq_client.bind_queue("queue2", "broadcast", "")

    # 发布一条消息
    test_message = {"text": "Hello all!"}
    rabbitmq_client.publish("broadcast", "", test_message)

    # 验证两个队列都收到了
    msg1 = rabbitmq_client.get_message("queue1")
    msg2 = rabbitmq_client.get_message("queue2")

    assert msg1 == test_message
    assert msg2 == test_message

    # 清理
    rabbitmq_client.delete_queue("queue1")
    rabbitmq_client.delete_queue("queue2")
    rabbitmq_client.delete_exchange("broadcast")
```

---

## 📋 测试场景示例

### 场景1: 订单创建事件

```python
def test_order_created_event(kafka_client):
    # 模拟订单服务发送订单创建事件
    order_event = {
        "event_type": "order.created",
        "order_id": "ORD-12345",
        "user_id": 123,
        "amount": 99.99,
        "timestamp": "2025-11-25T10:00:00Z"
    }

    kafka_client.send("order-events", order_event, key="ORD-12345")

    # 模拟库存服务消费事件
    inventory_messages = []
    kafka_client.consume(
        topics=["order-events"],
        group_id="inventory-service",
        handler=lambda msg: inventory_messages.append(msg),
        max_messages=1
    )

    assert len(inventory_messages) == 1
    assert inventory_messages[0]["order_id"] == "ORD-12345"
```

### 场景2: 任务队列

```python
def test_task_queue(rabbitmq_client):
    # 声明任务队列
    rabbitmq_client.declare_queue("tasks", durable=True)

    # 发布3个任务
    tasks = [
        {"task_id": 1, "action": "send_email"},
        {"task_id": 2, "action": "generate_report"},
        {"task_id": 3, "action": "backup_database"},
    ]

    for task in tasks:
        rabbitmq_client.publish(
            exchange="",  # 默认exchange
            routing_key="tasks",
            message=task
        )

    # Worker消费任务
    completed_tasks = []
    rabbitmq_client.consume(
        queue="tasks",
        handler=lambda task: completed_tasks.append(task),
        max_messages=3
    )

    assert len(completed_tasks) == 3
    assert completed_tasks[0]["action"] == "send_email"
```

### 场景3: 日志聚合

```python
def test_log_aggregation(rabbitmq_client):
    # Topic exchange: 不同级别的日志路由到不同队列
    rabbitmq_client.declare_exchange("logs", "topic")

    rabbitmq_client.declare_queue("all-logs")
    rabbitmq_client.bind_queue("all-logs", "logs", routing_key="#")

    rabbitmq_client.declare_queue("error-logs")
    rabbitmq_client.bind_queue("error-logs", "logs", routing_key="*.error")

    # 发送不同级别的日志
    rabbitmq_client.publish("logs", "app.info", {"msg": "Server started"})
    rabbitmq_client.publish("logs", "db.error", {"msg": "Connection failed"})
    rabbitmq_client.publish("logs", "api.error", {"msg": "Timeout"})

    # 验证all-logs收到3条
    all_count = 0
    while True:
        msg = rabbitmq_client.get_message("all-logs")
        if msg is None:
            break
        all_count += 1
    assert all_count == 3

    # 验证error-logs只收到2条
    error_count = 0
    while True:
        msg = rabbitmq_client.get_message("error-logs")
        if msg is None:
            break
        error_count += 1
    assert error_count == 2
```

---

## ⚡ 性能建议

### Kafka性能优化

1. **批量发送**: 使用`send_batch()`而不是多次调用`send()`
2. **压缩**: 启用gzip或lz4压缩减少网络传输
3. **异步发送**: 不等待确认,提高吞吐量(设置`acks=0`)
4. **分区策略**: 使用key保证相关消息进入同一分区

```python
# 高吞吐量配置
config = KafkaConfig(
    producer=KafkaProducerConfig(
        acks="0",  # 不等待确认
        compression_type="lz4",  # LZ4压缩
        batch_size=65536,  # 64KB批量
        linger_ms=100,  # 等待100ms凑批
    )
)
```

### RabbitMQ性能优化

1. **预取数量**: 增大`prefetch_count`提高消费速度
2. **批量发布**: 使用`publish_batch()`
3. **持久化**: 非关键消息不持久化(delivery_mode=1)
4. **手动确认**: 使用auto_ack=False,批量确认

```python
# 高性能消费配置
config = RabbitMQConfig(
    consume=RabbitMQConsumeConfig(
        prefetch_count=100,  # 预取100条
        auto_ack=True,  # 自动确认
    ),
    publish=RabbitMQPublishConfig(
        delivery_mode=1,  # 非持久化
    )
)
```

---

## 🐛 故障排查

### Kafka常见问题

1. **连接超时**
   ```
   KafkaError: [Errno -1] UNKNOWN: Connection refused
   ```
   - 检查bootstrap_servers配置是否正确
   - 确认Kafka服务已启动
   - 检查网络防火墙规则

2. **消费不到消息**
   - 检查group_id是否正确
   - 确认offset设置(earliest vs latest)
   - 验证topic是否存在

3. **消息丢失**
   - 确保acks="all"
   - 检查replication factor >= 2
   - 启用producer重试

### RabbitMQ常见问题

1. **连接被拒绝**
   ```
   AMQPConnectionError: Connection refused
   ```
   - 检查host和port配置
   - 验证username/password
   - 确认virtual_host存在

2. **消息未路由**
   - 检查exchange和queue是否已声明
   - 验证binding关系和routing_key
   - 确认exchange类型匹配

3. **消息堆积**
   - 增加consumer数量
   - 提高prefetch_count
   - 检查消息处理逻辑性能

---

## 🚀 RocketMQ客户端

### 基本用法

```python
from df_test_framework.messengers.queue.rocketmq import (
    RocketMQClient,
    RocketMQConfig,
    RocketMQProducerConfig,
    RocketMQConsumerConfig,
)

# 创建客户端
config = RocketMQConfig(
    namesrv_addr="localhost:9876",
    producer=RocketMQProducerConfig(group_name="test-producer"),
)
client = RocketMQClient(config)

# 发送消息
msg_id = client.send(
    topic="user-events",
    message={"user_id": 123, "action": "login"},
    tags="login",  # 标签用于消息过滤
    keys="user-123"  # 消息键用于索引
)
print(f"消息ID: {msg_id}")

# 批量发送
messages = [
    {"user_id": 1, "action": "login"},
    {"user_id": 2, "action": "logout"},
]
count = client.send_batch("user-events", messages, tags="user")
print(f"发送了 {count} 条消息")

# 单向发送(不等待broker响应,性能最高)
client.send_oneway("user-events", {"user_id": 456}, tags="fast")

# 关闭客户端
client.close()
```

### 消息消费

```python
from df_test_framework.messengers.queue.rocketmq import (
    RocketMQClient,
    RocketMQConfig,
    RocketMQConsumerConfig,
)

# 创建客户端
config = RocketMQConfig(
    namesrv_addr="localhost:9876",
    consumer=RocketMQConsumerConfig(
        group_name="test-consumer",
        message_model="CLUSTERING",  # 集群消费
    ),
)
client = RocketMQClient(config)

# 订阅消息
def message_handler(msg):
    """消息处理函数"""
    print(f"收到消息: {msg}")
    # 返回True表示消费成功,False表示重新消费
    return True

# 订阅(会阻塞)
client.subscribe(
    topic="user-events",
    handler=message_handler,
    tags="login"  # 只消费login标签的消息,*表示所有
)

# 停止消费
client.shutdown()
```

### 高级配置

#### Producer配置

```python
from df_test_framework.messengers.queue.rocketmq import (
    RocketMQConfig,
    RocketMQProducerConfig,
)

config = RocketMQConfig(
    namesrv_addr="namesrv1:9876;namesrv2:9876",  # 多个NameServer用分号分隔
    producer=RocketMQProducerConfig(
        group_name="my-producer",
        send_msg_timeout=5000,  # 发送超时5秒
        max_message_size=8388608,  # 最大消息8MB
        retry_times_when_send_failed=3,  # 重试次数
    ),
    # ACL认证
    access_key="your_access_key",
    secret_key="your_secret_key",
)
```

#### Consumer配置

```python
from df_test_framework.messengers.queue.rocketmq import (
    RocketMQConfig,
    RocketMQConsumerConfig,
)

config = RocketMQConfig(
    namesrv_addr="localhost:9876",
    consumer=RocketMQConsumerConfig(
        group_name="my-consumer",
        message_model="BROADCASTING",  # 广播模式(每个Consumer都收到消息)
        consume_from_where="CONSUME_FROM_FIRST_OFFSET",  # 从最早消息开始
        consume_thread_max=128,  # 最大消费线程数
        pull_batch_size=64,  # 单次拉取64条
    ),
)
```

### 延迟消息

RocketMQ支持18个延迟级别:

```python
# 延迟级别: 1s 5s 10s 30s 1m 2m 3m 4m 5m 6m 7m 8m 9m 10m 20m 30m 1h 2h
client.send(
    topic="delayed-tasks",
    message={"task": "send_email"},
    delay_level=3  # 延迟10秒
)
```

### 消息过滤

#### 使用Tags过滤

```python
# 生产者发送不同标签的消息
client.send("orders", {"order_id": "001"}, tags="PAID")
client.send("orders", {"order_id": "002"}, tags="PENDING")
client.send("orders", {"order_id": "003"}, tags="PAID")

# 消费者只消费PAID标签
client.subscribe(
    topic="orders",
    handler=lambda msg: print(msg) or True,
    tags="PAID"  # 只消费已支付订单
)
```

#### 多标签订阅

```python
# 消费PAID或SHIPPED标签的消息
client.subscribe(
    topic="orders",
    handler=handler,
    tags="PAID || SHIPPED"
)
```

### 在测试中使用

使用pytest fixtures:

```python
# conftest.py
from df_test_framework.testing.fixtures.message_queue import (
    rocketmq_client, rocketmq_config
)

# test_rocketmq.py
def test_send_and_receive(rocketmq_client):
    # 发送消息
    test_message = {"user_id": 123, "action": "login"}
    msg_id = rocketmq_client.send("test-topic", test_message, tags="test")

    assert msg_id is not None
```

---

## 🎯 消息队列对比

| 特性 | Kafka | RabbitMQ | RocketMQ |
|------|-------|----------|----------|
| **性能** | 极高(百万级QPS) | 中等(万级QPS) | 高(十万级QPS) |
| **延迟** | 毫秒级 | 微秒级 | 毫秒级 |
| **消息顺序** | 分区内有序 | 队列内有序 | 分区内有序 |
| **消息持久化** | ✅ 强 | ✅ 可选 | ✅ 强 |
| **分布式事务** | ❌ | ❌ | ✅ |
| **延迟消息** | ❌ | ✅ (插件) | ✅ (18个级别) |
| **消息过滤** | ❌ | ✅ (Headers) | ✅ (Tags/SQL) |
| **适用场景** | 日志收集、流处理 | 任务队列、RPC | 电商、金融 |

**选择建议**:
- **Kafka**: 大数据量、日志采集、实时流处理
- **RabbitMQ**: 复杂路由、任务队列、微服务通信
- **RocketMQ**: 电商订单、分布式事务、金融系统

---

## 📚 相关文档

- [Kafka官方文档](https://kafka.apache.org/documentation/)
- [RabbitMQ官方文档](https://www.rabbitmq.com/documentation.html)
- [RocketMQ官方文档](https://rocketmq.apache.org/docs/quick-start/)
- [示例代码](../../examples/07-message-queue/)
- [API参考](../api-reference/)

---

**最后更新**: 2025-11-25
**适用版本**: v3.9.0+
