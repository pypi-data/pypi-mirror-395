# 消息队列示例

演示如何使用df-test-framework的Kafka、RabbitMQ和RocketMQ客户端。

---

## 📦 安装依赖

```bash
# Kafka示例
pip install 'df-test-framework[kafka]'

# RabbitMQ示例
pip install 'df-test-framework[rabbitmq]'

# RocketMQ示例
pip install 'df-test-framework[rocketmq]'

# 全部安装
pip install 'df-test-framework[mq]'
```

---

## 🐳 启动服务

### Kafka

```bash
# 使用Docker Compose启动Kafka
docker-compose -f docker-compose-kafka.yml up -d

# 验证服务
docker ps | grep kafka
```

### RabbitMQ

```bash
# 使用Docker Compose启动RabbitMQ
docker-compose -f docker-compose-rabbitmq.yml up -d

# 访问管理界面
# http://localhost:15672 (guest/guest)
```

### RocketMQ

```bash
# 使用Docker Compose启动RocketMQ
docker-compose -f docker-compose-rocketmq.yml up -d

# 访问管理控制台
# http://localhost:8080
```

---

## 📂 示例列表

### Kafka示例

| 文件 | 说明 |
|------|------|
| `kafka_basic.py` | 基本发送和消费 |
| `kafka_batch.py` | 批量发送 |
| `kafka_partitions.py` | 使用分区和key |

### RabbitMQ示例

| 文件 | 说明 |
|------|------|
| `rabbitmq_basic.py` | 基本发布和消费 |
| `rabbitmq_direct.py` | Direct Exchange |
| `rabbitmq_topic.py` | Topic Exchange |
| `rabbitmq_fanout.py` | Fanout Exchange |
| `rabbitmq_work_queue.py` | 工作队列模式 |

### RocketMQ示例

| 文件 | 说明 |
|------|------|
| `rocketmq_basic.py` | 基本发送(同步/批量/单向) |
| `docker-compose-rocketmq.yml` | RocketMQ Docker环境 |
| `rocketmq-broker.conf` | Broker配置文件 |

---

## 🚀 运行示例

### Kafka

```bash
# 基本示例
python kafka_basic.py

# 批量发送
python kafka_batch.py
```

### RabbitMQ

```bash
# 基本示例
python rabbitmq_basic.py

# Topic Exchange
python rabbitmq_topic.py
```

### RocketMQ

```bash
# 基本示例
python rocketmq_basic.py
```

---

## 🧹 清理

```bash
# 停止Kafka
docker-compose -f docker-compose-kafka.yml down -v

# 停止RabbitMQ
docker-compose -f docker-compose-rabbitmq.yml down -v

# 停止RocketMQ
docker-compose -f docker-compose-rocketmq.yml down -v
```

---

## 📚 相关文档

- [消息队列使用指南](../../docs/guides/message_queue.md)
- [Kafka API参考](../../docs/api-reference/)
- [RabbitMQ API参考](../../docs/api-reference/)
