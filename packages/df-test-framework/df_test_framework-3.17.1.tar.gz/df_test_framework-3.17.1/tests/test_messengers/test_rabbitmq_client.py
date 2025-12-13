"""测试RabbitMQClient

测试RabbitMQ消息队列客户端的功能。

注意: 这些测试使用Mock对象,不需要实际的RabbitMQ服务器。
集成测试需要在examples/中使用真实的RabbitMQ实例。
"""

from unittest.mock import MagicMock, patch

import pytest
from pydantic import SecretStr

# 尝试导入,如果失败则跳过所有测试
try:
    from df_test_framework.capabilities.messengers.queue.rabbitmq import (
        RabbitMQClient,
        RabbitMQConfig,
        RabbitMQConnectionConfig,
        RabbitMQConsumeConfig,
        RabbitMQPublishConfig,
    )

    RABBITMQ_AVAILABLE = True
except ImportError:
    RABBITMQ_AVAILABLE = False

    # 创建占位符以避免NameError
    RabbitMQClient = None
    RabbitMQConfig = None
    RabbitMQConnectionConfig = None
    RabbitMQPublishConfig = None
    RabbitMQConsumeConfig = None


pytestmark = pytest.mark.skipif(not RABBITMQ_AVAILABLE, reason="pika未安装")


class TestRabbitMQConfig:
    """测试RabbitMQ配置模型"""

    def test_default_config(self):
        """测试默认配置"""
        config = RabbitMQConfig()

        assert config.connection.host == "localhost"
        assert config.connection.port == 5672
        assert config.connection.username == "guest"
        assert config.connection.password.get_secret_value() == "guest"
        assert config.connection.heartbeat == 600

        assert config.publish.delivery_mode == 2
        assert config.consume.auto_ack is False
        assert config.timeout == 10

    def test_custom_config(self):
        """测试自定义配置"""
        config = RabbitMQConfig(
            connection=RabbitMQConnectionConfig(
                host="rabbitmq.example.com",
                port=5673,
                username="admin",
                password=SecretStr("secret"),
            ),
            publish=RabbitMQPublishConfig(delivery_mode=1, mandatory=True),
            consume=RabbitMQConsumeConfig(auto_ack=True, prefetch_count=10),
        )

        assert config.connection.host == "rabbitmq.example.com"
        assert config.connection.port == 5673
        assert config.connection.username == "admin"
        assert config.connection.password.get_secret_value() == "secret"

        assert config.publish.delivery_mode == 1
        assert config.publish.mandatory is True

        assert config.consume.auto_ack is True
        assert config.consume.prefetch_count == 10


@pytest.mark.skipif(
    True,  # 默认跳过,因为需要mock pika
    reason="需要mock pika库",
)
class TestRabbitMQClient:
    """测试RabbitMQClient

    使用Mock对象模拟pika的行为
    """

    @pytest.fixture
    def rabbitmq_config(self):
        """RabbitMQ配置fixture"""
        return RabbitMQConfig()

    @pytest.fixture
    def mock_connection(self):
        """Mock pika.BlockingConnection"""
        with patch(
            "df_test_framework.capabilities.messengers.queue.rabbitmq.client.pika.BlockingConnection"
        ) as mock:
            connection = MagicMock()
            connection.is_closed = False

            # Mock channel
            channel = MagicMock()
            channel.is_closed = False
            connection.channel.return_value = channel

            mock.return_value = connection
            yield mock, connection, channel

    def test_client_creation(self, rabbitmq_config):
        """测试创建客户端"""
        client = RabbitMQClient(rabbitmq_config)

        assert client.config == rabbitmq_config
        assert client._connection is None
        assert client._channel is None

    def test_connection_lazy_creation(self, rabbitmq_config, mock_connection):
        """测试连接延迟创建"""
        mock_cls, mock_conn, mock_ch = mock_connection

        client = RabbitMQClient(rabbitmq_config)

        # 首次访问时创建
        connection = client.connection

        assert connection is not None
        mock_cls.assert_called_once()

        # 第二次访问不会重新创建
        connection2 = client.connection
        assert connection == connection2
        assert mock_cls.call_count == 1

    def test_channel_lazy_creation(self, rabbitmq_config, mock_connection):
        """测试通道延迟创建"""
        mock_cls, mock_conn, mock_ch = mock_connection

        client = RabbitMQClient(rabbitmq_config)

        # 首次访问时创建
        channel = client.channel

        assert channel is not None
        mock_conn.channel.assert_called_once()

        # 验证设置了QoS
        mock_ch.basic_qos.assert_called_once_with(prefetch_count=1)

    def test_declare_exchange(self, rabbitmq_config, mock_connection):
        """测试声明exchange"""
        mock_cls, mock_conn, mock_ch = mock_connection

        client = RabbitMQClient(rabbitmq_config)

        client.declare_exchange("test-exchange", exchange_type="topic", durable=True)

        mock_ch.exchange_declare.assert_called_once_with(
            exchange="test-exchange",
            exchange_type="topic",
            durable=True,
            auto_delete=False,
        )

    def test_declare_queue(self, rabbitmq_config, mock_connection):
        """测试声明队列"""
        mock_cls, mock_conn, mock_ch = mock_connection

        # Mock queue_declare返回值
        result = MagicMock()
        result.method.message_count = 5
        mock_ch.queue_declare.return_value = result

        client = RabbitMQClient(rabbitmq_config)

        queue_result = client.declare_queue("test-queue", durable=True)

        mock_ch.queue_declare.assert_called_once_with(
            queue="test-queue",
            durable=True,
            exclusive=False,
            auto_delete=False,
            arguments={},
        )

        assert queue_result.method.message_count == 5

    def test_bind_queue(self, rabbitmq_config, mock_connection):
        """测试绑定队列"""
        mock_cls, mock_conn, mock_ch = mock_connection

        client = RabbitMQClient(rabbitmq_config)

        client.bind_queue(
            queue="test-queue",
            exchange="test-exchange",
            routing_key="test.routing.key",
        )

        mock_ch.queue_bind.assert_called_once_with(
            queue="test-queue",
            exchange="test-exchange",
            routing_key="test.routing.key",
            arguments={},
        )

    def test_publish_message(self, rabbitmq_config, mock_connection):
        """测试发布消息"""
        mock_cls, mock_conn, mock_ch = mock_connection

        client = RabbitMQClient(rabbitmq_config)

        message = {"user_id": 123, "action": "login"}
        client.publish(
            exchange="test-exchange",
            routing_key="test.key",
            message=message,
        )

        mock_ch.basic_publish.assert_called_once()
        call_args = mock_ch.basic_publish.call_args

        assert call_args[1]["exchange"] == "test-exchange"
        assert call_args[1]["routing_key"] == "test.key"
        assert call_args[1]["mandatory"] is False

    def test_publish_batch(self, rabbitmq_config, mock_connection):
        """测试批量发布"""
        mock_cls, mock_conn, mock_ch = mock_connection

        client = RabbitMQClient(rabbitmq_config)

        messages = [
            {"user_id": 1, "action": "login"},
            {"user_id": 2, "action": "logout"},
            {"user_id": 3, "action": "purchase"},
        ]

        count = client.publish_batch(
            exchange="test-exchange", routing_key="test.key", messages=messages
        )

        assert count == 3
        assert mock_ch.basic_publish.call_count == 3

    def test_get_message(self, rabbitmq_config, mock_connection):
        """测试获取单条消息"""
        mock_cls, mock_conn, mock_ch = mock_connection

        # Mock basic_get返回值
        method_frame = MagicMock()
        method_frame.delivery_tag = 123
        properties = MagicMock()
        body = b'{"user_id": 123, "action": "login"}'

        mock_ch.basic_get.return_value = (method_frame, properties, body)

        client = RabbitMQClient(rabbitmq_config)

        message = client.get_message("test-queue")

        assert message == {"user_id": 123, "action": "login"}
        mock_ch.basic_get.assert_called_once_with(queue="test-queue", auto_ack=False)

    def test_get_message_empty_queue(self, rabbitmq_config, mock_connection):
        """测试从空队列获取消息"""
        mock_cls, mock_conn, mock_ch = mock_connection

        # 空队列返回None
        mock_ch.basic_get.return_value = (None, None, None)

        client = RabbitMQClient(rabbitmq_config)

        message = client.get_message("test-queue")

        assert message is None

    def test_purge_queue(self, rabbitmq_config, mock_connection):
        """测试清空队列"""
        mock_cls, mock_conn, mock_ch = mock_connection

        # Mock purge返回值
        result = MagicMock()
        result.method.message_count = 10
        mock_ch.queue_purge.return_value = result

        client = RabbitMQClient(rabbitmq_config)

        count = client.purge_queue("test-queue")

        assert count == 10
        mock_ch.queue_purge.assert_called_once_with(queue="test-queue")

    def test_delete_queue(self, rabbitmq_config, mock_connection):
        """测试删除队列"""
        mock_cls, mock_conn, mock_ch = mock_connection

        # Mock delete返回值
        result = MagicMock()
        result.method.message_count = 5
        mock_ch.queue_delete.return_value = result

        client = RabbitMQClient(rabbitmq_config)

        count = client.delete_queue("test-queue", if_unused=True)

        assert count == 5
        mock_ch.queue_delete.assert_called_once_with(queue="test-queue", if_unused=True)

    def test_delete_exchange(self, rabbitmq_config, mock_connection):
        """测试删除exchange"""
        mock_cls, mock_conn, mock_ch = mock_connection

        client = RabbitMQClient(rabbitmq_config)

        client.delete_exchange("test-exchange", if_unused=False)

        mock_ch.exchange_delete.assert_called_once_with(exchange="test-exchange", if_unused=False)

    def test_close_client(self, rabbitmq_config, mock_connection):
        """测试关闭客户端"""
        mock_cls, mock_conn, mock_ch = mock_connection

        client = RabbitMQClient(rabbitmq_config)

        # 创建连接和通道
        _ = client.connection
        _ = client.channel

        # 关闭
        client.close()

        mock_ch.close.assert_called_once()
        mock_conn.close.assert_called_once()


class TestRabbitMQClientIntegration:
    """RabbitMQ客户端集成测试骨架

    这些测试需要真实的RabbitMQ实例,应在examples/中实现。
    这里只是提供测试框架。
    """

    @pytest.mark.skip(reason="需要真实的RabbitMQ实例")
    def test_real_rabbitmq_publish_and_consume(self):
        """真实环境下的发布和消费测试"""
        config = RabbitMQConfig()
        client = RabbitMQClient(config)

        # 声明
        client.declare_exchange("test-exchange", "direct")
        client.declare_queue("test-queue")
        client.bind_queue("test-queue", "test-exchange", "test-key")

        # 发布消息
        test_message = {"user_id": 123, "action": "login"}
        client.publish("test-exchange", "test-key", test_message)

        # 消费消息
        messages = []
        client.consume(
            queue="test-queue",
            handler=lambda msg: messages.append(msg),
            max_messages=1,
        )

        assert len(messages) == 1
        assert messages[0] == test_message

        # 清理
        client.delete_queue("test-queue")
        client.delete_exchange("test-exchange")
        client.close()


__all__ = [
    "TestRabbitMQConfig",
    "TestRabbitMQClient",
    "TestRabbitMQClientIntegration",
]
