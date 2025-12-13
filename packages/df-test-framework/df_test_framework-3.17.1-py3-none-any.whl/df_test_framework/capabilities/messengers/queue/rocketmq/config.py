"""RocketMQ配置模型

定义RocketMQClient的配置参数。

v3.9.0新增

注意: RocketMQ Python客户端使用rocketmq-python-client库(apache/rocketmq-client-python官方客户端)
"""

from typing import Any

from pydantic import BaseModel, Field


class RocketMQProducerConfig(BaseModel):
    """RocketMQ Producer配置"""

    group_name: str = Field(description="Producer组名")
    send_msg_timeout: int = Field(default=3000, description="发送超时时间(毫秒)")
    compress_msg_body_over_howmuch: int = Field(default=4096, description="消息体压缩阈值(字节)")
    max_message_size: int = Field(default=4194304, description="最大消息大小(字节,默认4MB)")
    retry_times_when_send_failed: int = Field(default=2, description="同步发送失败重试次数")
    retry_times_when_send_async_failed: int = Field(default=2, description="异步发送失败重试次数")

    # 自定义配置
    custom_config: dict[str, Any] = Field(default_factory=dict, description="自定义Producer配置")


class RocketMQConsumerConfig(BaseModel):
    """RocketMQ Consumer配置"""

    group_name: str = Field(description="Consumer组名")
    message_model: str = Field(
        default="CLUSTERING", description="消费模式: CLUSTERING(集群), BROADCASTING(广播)"
    )
    consume_from_where: str = Field(
        default="CONSUME_FROM_LAST_OFFSET",
        description="消费起始位置: CONSUME_FROM_LAST_OFFSET, CONSUME_FROM_FIRST_OFFSET, CONSUME_FROM_TIMESTAMP",
    )
    consume_thread_min: int = Field(default=20, description="最小消费线程数")
    consume_thread_max: int = Field(default=64, description="最大消费线程数")
    pull_batch_size: int = Field(default=32, description="单次拉取消息数量")

    # 自定义配置
    custom_config: dict[str, Any] = Field(default_factory=dict, description="自定义Consumer配置")


class RocketMQConfig(BaseModel):
    """RocketMQ客户端配置"""

    namesrv_addr: str = Field(
        default="localhost:9876", description="NameServer地址(多个用分号分隔)"
    )
    timeout: int = Field(default=10, description="操作超时时间(秒)")

    # Producer配置(可选)
    producer: RocketMQProducerConfig | None = Field(default=None, description="Producer配置")

    # Consumer配置(可选)
    consumer: RocketMQConsumerConfig | None = Field(default=None, description="Consumer配置")

    # 认证配置
    access_key: str | None = Field(default=None, description="AccessKey(ACL认证)")
    secret_key: str | None = Field(default=None, description="SecretKey(ACL认证)")


__all__ = ["RocketMQConfig", "RocketMQProducerConfig", "RocketMQConsumerConfig"]
