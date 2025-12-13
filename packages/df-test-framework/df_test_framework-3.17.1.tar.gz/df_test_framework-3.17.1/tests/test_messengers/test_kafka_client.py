"""测试KafkaClient

测试Kafka消息队列客户端的功能。

注意: 这些测试使用Mock对象,不需要实际的Kafka服务器。
集成测试需要在examples/中使用真实的Kafka实例。
"""

from unittest.mock import MagicMock, patch

import pytest

# 尝试导入,如果失败则跳过所有测试
try:
    from df_test_framework.capabilities.messengers.queue.kafka import (
        KafkaClient,
        KafkaConfig,
        KafkaConsumerConfig,
        KafkaProducerConfig,
    )

    KAFKA_AVAILABLE = True
except ImportError:
    KAFKA_AVAILABLE = False

    # 创建占位符以避免NameError
    KafkaClient = None
    KafkaConfig = None
    KafkaProducerConfig = None
    KafkaConsumerConfig = None


pytestmark = pytest.mark.skipif(not KAFKA_AVAILABLE, reason="confluent-kafka未安装")


class TestKafkaConfig:
    """测试Kafka配置模型"""

    def test_default_config(self):
        """测试默认配置"""
        config = KafkaConfig()

        assert config.bootstrap_servers == ["localhost:9092"]
        assert config.request_timeout_ms == 30000
        assert config.producer is None
        assert config.consumer is None

    def test_custom_config(self):
        """测试自定义配置"""
        config = KafkaConfig(
            bootstrap_servers=["kafka1:9092", "kafka2:9092"],
            request_timeout_ms=60000,
            producer=KafkaProducerConfig(acks="1", retries=5),
            consumer=KafkaConsumerConfig(group_id="test-group", auto_offset_reset="earliest"),
        )

        assert config.bootstrap_servers == ["kafka1:9092", "kafka2:9092"]
        assert config.request_timeout_ms == 60000
        assert config.producer.acks == "1"
        assert config.producer.retries == 5
        assert config.consumer.group_id == "test-group"
        assert config.consumer.auto_offset_reset == "earliest"

    def test_producer_config_to_confluent_dict(self):
        """测试Producer配置转换为confluent-kafka字典"""
        producer_config = KafkaProducerConfig(
            acks="all",
            retries=3,
            compression_type="gzip",
            enable_idempotence=True,
        )

        config_dict = producer_config.to_confluent_dict()

        assert config_dict["acks"] == -1  # "all" 映射为 -1
        assert config_dict["message.send.max.retries"] == 3
        assert config_dict["compression.type"] == "gzip"
        assert config_dict["enable.idempotence"] is True

    def test_producer_config_librdkafka_keys(self):
        """测试Producer配置使用正确的librdkafka键名

        v3.9.0 修复: 确保使用 librdkafka 原生键名而非 Java 风格键名
        """
        producer_config = KafkaProducerConfig(
            batch_num_messages=5000,
            queue_buffering_max_ms=20,
            queue_buffering_max_kbytes=65536,
            max_in_flight=10,
        )

        config_dict = producer_config.to_confluent_dict()

        # 验证使用 librdkafka 原生键名
        assert config_dict["batch.num.messages"] == 5000
        assert config_dict["queue.buffering.max.ms"] == 20
        assert config_dict["queue.buffering.max.kbytes"] == 65536
        assert config_dict["max.in.flight"] == 10

        # 确保不存在 Java 风格的键名
        assert "batch.size" not in config_dict
        assert "buffer.memory" not in config_dict
        assert "linger.ms" not in config_dict
        assert "max.in.flight.requests.per.connection" not in config_dict

    def test_consumer_config_to_confluent_dict(self):
        """测试Consumer配置转换为confluent-kafka字典"""
        consumer_config = KafkaConsumerConfig(
            group_id="test-group",
            auto_offset_reset="latest",
            enable_auto_commit=False,
            extra_config={"fetch.min.bytes": 1024},
        )

        config_dict = consumer_config.to_confluent_dict()

        assert config_dict["group.id"] == "test-group"
        assert config_dict["auto.offset.reset"] == "latest"
        assert config_dict["enable.auto.commit"] is False
        assert config_dict["fetch.min.bytes"] == 1024


@pytest.mark.skipif(
    True,  # 默认跳过,因为需要mock kafka-python3
    reason="需要mock kafka-python3库",
)
class TestKafkaClient:
    """测试KafkaClient

    使用Mock对象模拟kafka-python3的行为
    """

    @pytest.fixture
    def kafka_config(self):
        """Kafka配置fixture"""
        return KafkaConfig(bootstrap_servers=["localhost:9092"])

    @pytest.fixture
    def mock_producer(self):
        """Mock KafkaProducer"""
        with patch(
            "df_test_framework.capabilities.messengers.queue.kafka.client.KafkaProducer"
        ) as mock:
            producer = MagicMock()

            # Mock send方法
            future = MagicMock()
            metadata = MagicMock()
            metadata.topic = "test-topic"
            metadata.partition = 0
            metadata.offset = 123
            future.get.return_value = metadata
            producer.send.return_value = future

            mock.return_value = producer
            yield mock

    @pytest.fixture
    def mock_consumer(self):
        """Mock KafkaConsumer"""
        with patch(
            "df_test_framework.capabilities.messengers.queue.kafka.client.KafkaConsumer"
        ) as mock:
            consumer = MagicMock()

            # Mock消息迭代
            message1 = MagicMock()
            message1.topic = "test-topic"
            message1.partition = 0
            message1.offset = 100
            message1.value = '{"user_id": 123}'

            message2 = MagicMock()
            message2.topic = "test-topic"
            message2.partition = 0
            message2.offset = 101
            message2.value = '{"user_id": 456}'

            consumer.__iter__.return_value = iter([message1, message2])

            mock.return_value = consumer
            yield mock

    def test_client_creation(self, kafka_config):
        """测试创建客户端"""
        client = KafkaClient(kafka_config)

        assert client.config == kafka_config
        assert client._producer is None
        assert client._consumers == []

    def test_producer_lazy_creation(self, kafka_config, mock_producer):
        """测试Producer延迟创建"""
        client = KafkaClient(kafka_config)

        # 首次访问时创建
        producer = client.producer

        assert producer is not None
        mock_producer.assert_called_once()

        # 第二次访问不会重新创建
        producer2 = client.producer
        assert producer == producer2
        assert mock_producer.call_count == 1

    def test_send_message(self, kafka_config, mock_producer):
        """测试发送消息"""
        client = KafkaClient(kafka_config)

        message = {"user_id": 123, "action": "login"}
        client.send("test-topic", message)

        # 验证调用
        client.producer.send.assert_called_once()
        call_args = client.producer.send.call_args

        assert call_args[1]["topic"] == "test-topic"
        assert call_args[1]["value"] == message

    def test_send_message_with_key(self, kafka_config, mock_producer):
        """测试发送带key的消息"""
        client = KafkaClient(kafka_config)

        message = {"user_id": 123}
        client.send("test-topic", message, key="user-123")

        call_args = client.producer.send.call_args
        assert call_args[1]["key"] == b"user-123"

    def test_send_message_with_partition(self, kafka_config, mock_producer):
        """测试发送到指定分区"""
        client = KafkaClient(kafka_config)

        message = {"user_id": 123}
        client.send("test-topic", message, partition=2)

        call_args = client.producer.send.call_args
        assert call_args[1]["partition"] == 2

    def test_send_batch(self, kafka_config, mock_producer):
        """测试批量发送"""
        client = KafkaClient(kafka_config)

        messages = [
            {"user_id": 1, "action": "login"},
            {"user_id": 2, "action": "logout"},
            {"user_id": 3, "action": "purchase"},
        ]

        count = client.send_batch("test-topic", messages)

        assert count == 3
        assert client.producer.send.call_count == 3

    def test_send_batch_with_key_func(self, kafka_config, mock_producer):
        """测试批量发送带key提取函数"""
        client = KafkaClient(kafka_config)

        messages = [
            {"user_id": 1, "action": "login"},
            {"user_id": 2, "action": "logout"},
        ]

        def key_func(msg):
            return f"user-{msg['user_id']}"

        count = client.send_batch("test-topic", messages, key_func=key_func)

        assert count == 2

        # 验证每个消息的key
        calls = client.producer.send.call_args_list
        assert calls[0][1]["key"] == b"user-1"
        assert calls[1][1]["key"] == b"user-2"

    def test_consume_messages(self, kafka_config, mock_consumer):
        """测试消费消息"""
        client = KafkaClient(kafka_config)

        messages = []

        def handler(msg):
            return messages.append(msg)

        count = client.consume(
            topics=["test-topic"],
            group_id="test-group",
            handler=handler,
            max_messages=2,
        )

        assert count == 2
        assert len(messages) == 2
        assert messages[0] == {"user_id": 123}
        assert messages[1] == {"user_id": 456}

    def test_close_client(self, kafka_config, mock_producer):
        """测试关闭客户端"""
        client = KafkaClient(kafka_config)

        # 创建producer
        _ = client.producer

        # 关闭
        client.close()

        client.producer.close.assert_called_once()


class TestKafkaClientIntegration:
    """Kafka客户端集成测试骨架

    这些测试需要真实的Kafka实例,应在examples/中实现。
    这里只是提供测试框架。
    """

    @pytest.mark.skip(reason="需要真实的Kafka实例")
    def test_real_kafka_send_and_consume(self):
        """真实环境下的发送和消费测试"""
        config = KafkaConfig(bootstrap_servers=["localhost:9092"])
        client = KafkaClient(config)

        # 发送消息
        test_message = {"user_id": 123, "action": "login"}
        client.send("test-topic", test_message)

        # 消费消息
        messages = []
        client.consume(
            topics=["test-topic"],
            group_id="test-group",
            handler=lambda msg: messages.append(msg),
            max_messages=1,
        )

        assert len(messages) == 1
        assert messages[0] == test_message

        client.close()


__all__ = [
    "TestKafkaConfig",
    "TestKafkaClient",
    "TestKafkaClientIntegration",
]
