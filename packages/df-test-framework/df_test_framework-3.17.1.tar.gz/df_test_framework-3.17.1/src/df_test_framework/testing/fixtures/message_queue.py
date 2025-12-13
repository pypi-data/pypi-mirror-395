"""消息队列Fixtures

提供Kafka和RabbitMQ客户端的pytest fixtures。

v3.9.0新增

使用示例::

    # conftest.py
    from df_test_framework.testing.fixtures.message_queue import (
        kafka_client,
        rabbitmq_client
    )

    # test_mq.py
    def test_kafka_send(kafka_client):
        kafka_client.send("test-topic", {"user_id": 123})

    def test_rabbitmq_publish(rabbitmq_client):
        rabbitmq_client.publish("exchange", "key", {"user_id": 123})
"""

from collections.abc import Generator

import pytest

# 延迟导入,避免在没有安装可选依赖时报错
try:
    from df_test_framework.capabilities.messengers.queue.kafka import (
        KafkaClient,
        KafkaConfig,
        KafkaProducerConfig,
    )

    KAFKA_AVAILABLE = True
except ImportError:
    KAFKA_AVAILABLE = False

try:
    from df_test_framework.capabilities.messengers.queue.rabbitmq import (
        RabbitMQClient,
        RabbitMQConfig,
    )

    RABBITMQ_AVAILABLE = True
except ImportError:
    RABBITMQ_AVAILABLE = False

try:
    from df_test_framework.capabilities.messengers.queue.rocketmq import (
        RocketMQClient,
        RocketMQConfig,
        RocketMQProducerConfig,
    )

    ROCKETMQ_AVAILABLE = True
except ImportError:
    ROCKETMQ_AVAILABLE = False


@pytest.fixture(scope="session")
def kafka_config() -> "KafkaConfig":
    """Kafka配置fixture

    默认连接到 localhost:9092

    可在conftest.py中覆盖::

        @pytest.fixture(scope="session")
        def kafka_config():
            return KafkaConfig(
                bootstrap_servers=["kafka.example.com:9092"]
            )
    """
    if not KAFKA_AVAILABLE:
        pytest.skip("confluent-kafka未安装,请运行: pip install 'df-test-framework[kafka]'")

    return KafkaConfig(bootstrap_servers=["localhost:9092"], producer=KafkaProducerConfig())


@pytest.fixture(scope="function")
def kafka_client(kafka_config: "KafkaConfig") -> Generator["KafkaClient", None, None]:
    """Kafka客户端fixture

    每个测试函数都会创建新的客户端实例,测试结束后自动关闭。

    使用示例::

        def test_send_message(kafka_client):
            kafka_client.send("test-topic", {"user_id": 123})

            messages = []
            kafka_client.consume(
                topics=["test-topic"],
                group_id="test-group",
                handler=lambda msg: messages.append(msg),
                max_messages=1
            )

            assert len(messages) == 1
    """
    if not KAFKA_AVAILABLE:
        pytest.skip("confluent-kafka未安装")

    client = KafkaClient(kafka_config)
    yield client
    client.close()


@pytest.fixture(scope="session")
def rabbitmq_config() -> "RabbitMQConfig":
    """RabbitMQ配置fixture

    默认连接到 localhost:5672 (guest/guest)

    可在conftest.py中覆盖::

        @pytest.fixture(scope="session")
        def rabbitmq_config():
            from pydantic import SecretStr
            return RabbitMQConfig(
                connection=RabbitMQConnectionConfig(
                    host="rabbitmq.example.com",
                    username="admin",
                    password=SecretStr("secret")
                )
            )
    """
    if not RABBITMQ_AVAILABLE:
        pytest.skip("pika未安装,请运行: pip install 'df-test-framework[rabbitmq]'")

    return RabbitMQConfig()


@pytest.fixture(scope="function")
def rabbitmq_client(
    rabbitmq_config: "RabbitMQConfig",
) -> Generator["RabbitMQClient", None, None]:
    """RabbitMQ客户端fixture

    每个测试函数都会创建新的客户端实例,测试结束后自动关闭。

    使用示例::

        def test_publish_message(rabbitmq_client):
            # 声明
            rabbitmq_client.declare_exchange("test-exchange", "direct")
            rabbitmq_client.declare_queue("test-queue")
            rabbitmq_client.bind_queue("test-queue", "test-exchange", "test-key")

            # 发布
            rabbitmq_client.publish(
                exchange="test-exchange",
                routing_key="test-key",
                message={"user_id": 123}
            )

            # 获取
            message = rabbitmq_client.get_message("test-queue")
            assert message == {"user_id": 123}
    """
    if not RABBITMQ_AVAILABLE:
        pytest.skip("pika未安装")

    client = RabbitMQClient(rabbitmq_config)
    yield client
    client.close()


@pytest.fixture(scope="session")
def rocketmq_config() -> "RocketMQConfig":
    """RocketMQ配置fixture

    默认连接到 localhost:9876

    可在conftest.py中覆盖::

        @pytest.fixture(scope="session")
        def rocketmq_config():
            return RocketMQConfig(
                namesrv_addr="rocketmq.example.com:9876",
                producer=RocketMQProducerConfig(group_name="my-producer")
            )
    """
    if not ROCKETMQ_AVAILABLE:
        pytest.skip(
            "rocketmq-python-client未安装,请运行: pip install 'df-test-framework[rocketmq]'"
        )

    return RocketMQConfig(
        namesrv_addr="localhost:9876", producer=RocketMQProducerConfig(group_name="test-producer")
    )


@pytest.fixture(scope="function")
def rocketmq_client(
    rocketmq_config: "RocketMQConfig",
) -> Generator["RocketMQClient", None, None]:
    """RocketMQ客户端fixture

    每个测试函数都会创建新的客户端实例,测试结束后自动关闭。

    使用示例::

        def test_send_message(rocketmq_client):
            # 发送消息
            msg_id = rocketmq_client.send(
                "test-topic",
                {"user_id": 123, "action": "login"},
                tags="login"
            )
            assert msg_id is not None
    """
    if not ROCKETMQ_AVAILABLE:
        pytest.skip("rocketmq-python-client未安装")

    client = RocketMQClient(rocketmq_config)
    yield client
    client.close()


__all__ = [
    "kafka_config",
    "kafka_client",
    "rabbitmq_config",
    "rabbitmq_client",
    "rocketmq_config",
    "rocketmq_client",
]
