"""RabbitMQ配置模型

定义RabbitMQClient的配置参数。

技术选型: Pika (AMQP 0-9-1)
--------------------------
- 协议: AMQP 0-9-1 (RabbitMQ核心协议)
- 客户端: pika >= 1.3.0 (生产就绪)
- 状态: Stable (仅bug修复维护)

为什么不使用 AMQP 1.0:
- rabbitmq-amqp-python-client v0.3.0 仍处于Alpha阶段
- AMQP 0-9-1 和 AMQP 1.0 是完全不同的协议,非版本升级
- Pika提供完整的Exchange/Queue/Binding支持,满足测试框架需求
- RabbitMQ永久支持AMQP 0-9-1协议

未来计划:
- 当 rabbitmq-amqp-python-client 达到Stable版本时,考虑提供AMQP 1.0支持

v3.9.0新增
"""

from pydantic import BaseModel, Field, SecretStr


class RabbitMQConnectionConfig(BaseModel):
    """RabbitMQ连接配置"""

    host: str = Field(default="localhost", description="RabbitMQ服务器地址")
    port: int = Field(default=5672, description="RabbitMQ端口")
    virtual_host: str = Field(default="/", description="虚拟主机")
    username: str = Field(default="guest", description="用户名")
    password: SecretStr = Field(default=SecretStr("guest"), description="密码")

    # 连接参数
    heartbeat: int = Field(default=600, description="心跳间隔(秒)")
    blocked_connection_timeout: int = Field(default=300, description="阻塞连接超时(秒)")
    connection_attempts: int = Field(default=3, description="连接重试次数")
    retry_delay: int = Field(default=2, description="重试延迟(秒)")


class RabbitMQPublishConfig(BaseModel):
    """RabbitMQ发布配置"""

    mandatory: bool = Field(default=False, description="消息路由失败时是否返回给发送者")
    delivery_mode: int = Field(default=2, description="投递模式: 1非持久化, 2持久化")
    content_type: str = Field(default="application/json", description="内容类型")
    content_encoding: str = Field(default="utf-8", description="内容编码")


class RabbitMQConsumeConfig(BaseModel):
    """RabbitMQ消费配置"""

    auto_ack: bool = Field(default=False, description="是否自动确认")
    prefetch_count: int = Field(default=1, description="预取消息数量")
    consumer_timeout: int | None = Field(default=None, description="消费者超时(毫秒)")


class RabbitMQConfig(BaseModel):
    """RabbitMQ客户端配置"""

    # 连接配置
    connection: RabbitMQConnectionConfig = Field(
        default_factory=RabbitMQConnectionConfig, description="连接配置"
    )

    # 发布配置
    publish: RabbitMQPublishConfig = Field(
        default_factory=RabbitMQPublishConfig, description="发布配置"
    )

    # 消费配置
    consume: RabbitMQConsumeConfig = Field(
        default_factory=RabbitMQConsumeConfig, description="消费配置"
    )

    # 超时配置
    timeout: int = Field(default=10, description="操作超时时间(秒)")


__all__ = [
    "RabbitMQConfig",
    "RabbitMQConnectionConfig",
    "RabbitMQPublishConfig",
    "RabbitMQConsumeConfig",
]
