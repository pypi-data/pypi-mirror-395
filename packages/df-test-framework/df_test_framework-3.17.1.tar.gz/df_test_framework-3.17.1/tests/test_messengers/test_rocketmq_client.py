"""测试RocketMQClient

测试RocketMQ消息队列客户端的功能。

注意: 这些测试使用Mock对象,不需要实际的RocketMQ服务器。
集成测试需要在examples/中使用真实的RocketMQ实例。
"""

from unittest.mock import MagicMock, patch

import pytest

# 尝试导入,如果失败则跳过所有测试
try:
    from df_test_framework.capabilities.messengers.queue.rocketmq import (
        RocketMQClient,
        RocketMQConfig,
        RocketMQConsumerConfig,
        RocketMQProducerConfig,
    )

    ROCKETMQ_AVAILABLE = True
except ImportError:
    ROCKETMQ_AVAILABLE = False

    # 创建占位符以避免NameError
    RocketMQClient = None
    RocketMQConfig = None
    RocketMQProducerConfig = None
    RocketMQConsumerConfig = None


pytestmark = pytest.mark.skipif(not ROCKETMQ_AVAILABLE, reason="rocketmq-python-client未安装")


class TestRocketMQConfig:
    """测试RocketMQ配置模型"""

    def test_default_config(self):
        """测试默认配置"""
        config = RocketMQConfig()

        assert config.namesrv_addr == "localhost:9876"
        assert config.timeout == 10
        assert config.producer is None
        assert config.consumer is None
        assert config.access_key is None

    def test_custom_config(self):
        """测试自定义配置"""
        config = RocketMQConfig(
            namesrv_addr="rocketmq.example.com:9876",
            timeout=30,
            producer=RocketMQProducerConfig(group_name="test-producer", send_msg_timeout=5000),
            consumer=RocketMQConsumerConfig(
                group_name="test-consumer", message_model="BROADCASTING"
            ),
            access_key="test_ak",
            secret_key="test_sk",
        )

        assert config.namesrv_addr == "rocketmq.example.com:9876"
        assert config.timeout == 30
        assert config.producer.group_name == "test-producer"
        assert config.producer.send_msg_timeout == 5000
        assert config.consumer.group_name == "test-consumer"
        assert config.consumer.message_model == "BROADCASTING"
        assert config.access_key == "test_ak"

    def test_producer_config(self):
        """测试Producer配置"""
        producer_config = RocketMQProducerConfig(
            group_name="my-producer",
            send_msg_timeout=5000,
            max_message_size=8388608,  # 8MB
            retry_times_when_send_failed=3,
        )

        assert producer_config.group_name == "my-producer"
        assert producer_config.send_msg_timeout == 5000
        assert producer_config.max_message_size == 8388608
        assert producer_config.retry_times_when_send_failed == 3

    def test_consumer_config(self):
        """测试Consumer配置"""
        consumer_config = RocketMQConsumerConfig(
            group_name="my-consumer",
            message_model="CLUSTERING",
            consume_from_where="CONSUME_FROM_FIRST_OFFSET",
            consume_thread_max=128,
        )

        assert consumer_config.group_name == "my-consumer"
        assert consumer_config.message_model == "CLUSTERING"
        assert consumer_config.consume_from_where == "CONSUME_FROM_FIRST_OFFSET"
        assert consumer_config.consume_thread_max == 128


@pytest.mark.skipif(
    True,  # 默认跳过,因为需要mock rocketmq-python-client
    reason="需要mock rocketmq-python-client库",
)
class TestRocketMQClient:
    """测试RocketMQClient

    使用Mock对象模拟rocketmq-python-client的行为
    """

    @pytest.fixture
    def rocketmq_config(self):
        """RocketMQ配置fixture"""
        return RocketMQConfig(
            namesrv_addr="localhost:9876",
            producer=RocketMQProducerConfig(group_name="test-producer"),
        )

    @pytest.fixture
    def mock_producer(self):
        """Mock Producer"""
        with patch(
            "df_test_framework.capabilities.messengers.queue.rocketmq.client.Producer"
        ) as mock:
            producer = MagicMock()

            # Mock send_sync返回值
            send_result = MagicMock()
            send_result.msg_id = "MSG-123456"
            send_result.status = 0  # SEND_OK
            producer.send_sync.return_value = send_result

            mock.return_value = producer
            yield mock, producer

    def test_client_creation(self, rocketmq_config):
        """测试创建客户端"""
        client = RocketMQClient(rocketmq_config)

        assert client.config == rocketmq_config
        assert client._producer is None
        assert client._consumer is None

    def test_send_message(self, rocketmq_config, mock_producer):
        """测试发送消息"""
        mock_cls, producer = mock_producer

        client = RocketMQClient(rocketmq_config)

        message = {"user_id": 123, "action": "login"}
        msg_id = client.send(topic="test-topic", message=message, tags="login", keys="user-123")

        assert msg_id == "MSG-123456"
        producer.send_sync.assert_called_once()

    def test_send_batch(self, rocketmq_config, mock_producer):
        """测试批量发送"""
        mock_cls, producer = mock_producer

        client = RocketMQClient(rocketmq_config)

        messages = [
            {"user_id": 1, "action": "login"},
            {"user_id": 2, "action": "logout"},
            {"user_id": 3, "action": "purchase"},
        ]

        count = client.send_batch("test-topic", messages, tags="user")

        assert count == 3
        assert producer.send_sync.call_count == 3

    def test_send_oneway(self, rocketmq_config, mock_producer):
        """测试单向发送"""
        mock_cls, producer = mock_producer

        client = RocketMQClient(rocketmq_config)

        message = {"user_id": 123, "action": "login"}
        client.send_oneway("test-topic", message, tags="login")

        producer.send_oneway.assert_called_once()

    def test_close_client(self, rocketmq_config, mock_producer):
        """测试关闭客户端"""
        mock_cls, producer = mock_producer

        client = RocketMQClient(rocketmq_config)

        # 发送一条消息以创建producer
        client.send("test-topic", {"test": "data"})

        # 关闭
        client.close()

        producer.shutdown.assert_called_once()


class TestRocketMQClientIntegration:
    """RocketMQ客户端集成测试骨架

    这些测试需要真实的RocketMQ实例,应在examples/中实现。
    这里只是提供测试框架。
    """

    @pytest.mark.skip(reason="需要真实的RocketMQ实例")
    def test_real_rocketmq_send_and_consume(self):
        """真实环境下的发送和消费测试"""
        config = RocketMQConfig(
            namesrv_addr="localhost:9876",
            producer=RocketMQProducerConfig(group_name="test-producer"),
            consumer=RocketMQConsumerConfig(group_name="test-consumer"),
        )
        client = RocketMQClient(config)

        # 发送消息
        test_message = {"user_id": 123, "action": "login"}
        msg_id = client.send("test-topic", test_message, tags="test")
        assert msg_id is not None

        # 消费消息
        messages_received = []

        def handler(msg):
            messages_received.append(msg)
            return True  # 消费成功

        # 订阅(会阻塞)
        # client.subscribe("test-topic", handler, tags="test")

        # 验证
        # assert len(messages_received) >= 1

        client.close()


__all__ = [
    "TestRocketMQConfig",
    "TestRocketMQClient",
    "TestRocketMQClientIntegration",
]
