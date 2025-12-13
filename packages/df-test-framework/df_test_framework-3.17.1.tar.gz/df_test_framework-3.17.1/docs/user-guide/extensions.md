# 扩展系统使用指南

> **版本**: v2.0.0
> **最后更新**: 2025-11-02
> **难度**: ⭐⭐⭐ 中级

DF Test Framework v2基于[pluggy](https://pluggy.readthedocs.io/)提供强大的扩展机制，允许在框架的关键节点注入自定义逻辑，实现高度定制化。

---

## 📋 目录

- [扩展系统概述](#扩展系统概述)
- [快速开始](#快速开始)
- [Hook点详解](#hook点详解)
- [内置扩展](#内置扩展)
- [自定义扩展开发](#自定义扩展开发)
- [实战示例](#实战示例)
- [最佳实践](#最佳实践)
- [常见问题](#常见问题)

---

## 🎯 扩展系统概述

### 为什么需要扩展系统？

扩展系统允许你：
- ✅ **不修改框架代码**即可添加新功能
- ✅ **复用通用逻辑**跨多个测试项目
- ✅ **标准化团队实践**（监控、日志、配置等）
- ✅ **模块化开发**保持代码整洁

### 核心概念

```
┌─────────────────────────────────────┐
│     DF Test Framework Core          │
├─────────────────────────────────────┤
│  Hook Specification (扩展点)        │
│  • df_config_sources                │
│  • df_providers                     │
│  • df_post_bootstrap                │
└──────────┬──────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│  Extension Manager (pluggy)          │
│  • 管理插件注册                       │
│  • 调用Hook实现                       │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│  Custom Extensions (自定义扩展)      │
│  • 监控扩展                          │
│  • 性能分析扩展                       │
│  • 环境验证扩展                       │
│  • ...                               │
└──────────────────────────────────────┘
```

### 扩展系统架构

1. **Hook Specification (规范)**: 框架定义的扩展点
2. **Hook Implementation (实现)**: 插件对Hook的具体实现
3. **Extension Manager (管理器)**: 管理插件注册和调用
4. **Plugin (插件)**: 包含Hook实现的类或模块

---

## ⚡ 快速开始

### 1. 最简单的扩展

创建一个在Bootstrap完成后打印日志的扩展：

```python
# my_project/extensions/hello.py
from df_test_framework import hookimpl

@hookimpl
def df_post_bootstrap(runtime):
    """Bootstrap完成后执行"""
    runtime.logger.info("🎉 Hello from extension!")
    runtime.logger.info(f"当前环境: {runtime.settings.environment}")
```

**使用扩展：**

```python
# tests/conftest.py
from df_test_framework import Bootstrap

@pytest.fixture(scope="session")
def runtime():
    return (
        Bootstrap()
        .with_settings(MySettings)
        .with_plugin("my_project.extensions.hello")  # 注册扩展
        .build()
        .run()
    )
```

### 2. 添加自定义Provider

注册一个自定义服务到Runtime：

```python
# my_project/extensions/metrics.py
from df_test_framework import hookimpl
from df_test_framework.infrastructure.providers import SingletonProvider
from my_project.metrics import MetricsClient

@hookimpl
def df_providers(settings, logger):
    """注册自定义Provider"""
    return {
        "metrics": SingletonProvider(
            lambda ctx: MetricsClient(
                url=settings.extras.get("metrics_url", "http://localhost:9090")
            )
        )
    }
```

**使用Provider：**

```python
def test_with_metrics(runtime):
    metrics = runtime.get("metrics")
    metrics.increment("test.api.calls")

    # 你的测试代码...
```

### 3. 添加自定义配置源

从远程配置中心加载配置：

```python
# my_project/extensions/remote_config.py
from df_test_framework import hookimpl
from df_test_framework.infrastructure.config.sources import ConfigSource
import requests

class RemoteConfigSource(ConfigSource):
    def __init__(self, url: str):
        self.url = url

    def load(self, settings_cls):
        """从远程加载配置"""
        response = requests.get(self.url)
        return response.json()

@hookimpl
def df_config_sources(settings_cls):
    """添加远程配置源"""
    remote_url = os.getenv("CONFIG_CENTER_URL")
    if remote_url:
        return [RemoteConfigSource(remote_url)]
    return []
```

---

## 🔌 Hook点详解

框架提供3个Hook点，覆盖配置加载、资源注册和启动后处理。

### Hook 1: df_config_sources

**触发时机**: 配置加载阶段（在创建Settings之前）

**功能**: 提供额外的配置源（ConfigSource）

**签名**:
```python
@hookimpl
def df_config_sources(
    settings_cls: Type[FrameworkSettings]
) -> Iterable[ConfigSource]:
    """返回要添加到配置管道的ConfigSource对象列表"""
    pass
```

**参数**:
- `settings_cls`: Settings类（Type[FrameworkSettings]）

**返回**: `Iterable[ConfigSource]`

**使用场景**:
- ✅ 从配置中心加载配置（Apollo、Nacos等）
- ✅ 从数据库加载配置
- ✅ 从云存储加载配置（S3、OSS等）
- ✅ 合并多个环境的配置

**完整示例**:

```python
from df_test_framework import hookimpl
from df_test_framework.infrastructure.config.sources import ConfigSource
import boto3

class S3ConfigSource(ConfigSource):
    """从AWS S3加载配置"""

    def __init__(self, bucket: str, key: str):
        self.bucket = bucket
        self.key = key

    def load(self, settings_cls):
        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket=self.bucket, Key=self.key)
        data = obj['Body'].read().decode('utf-8')
        return json.loads(data)

class NacosConfigSource(ConfigSource):
    """从Nacos配置中心加载"""

    def __init__(self, server_addr: str, namespace: str, data_id: str):
        self.server_addr = server_addr
        self.namespace = namespace
        self.data_id = data_id

    def load(self, settings_cls):
        import nacos
        client = nacos.NacosClient(self.server_addr, namespace=self.namespace)
        config = client.get_config(self.data_id, "DEFAULT_GROUP")
        return yaml.safe_load(config)

@hookimpl
def df_config_sources(settings_cls):
    """根据环境选择配置源"""
    sources = []

    # 生产环境从Nacos加载
    if os.getenv("ENV") == "production":
        sources.append(NacosConfigSource(
            server_addr="nacos.example.com:8848",
            namespace="production",
            data_id="test-framework-config"
        ))

    # 测试环境从S3加载
    elif os.getenv("ENV") == "staging":
        sources.append(S3ConfigSource(
            bucket="test-configs",
            key="staging/framework-config.json"
        ))

    return sources
```

---

### Hook 2: df_providers

**触发时机**: RuntimeContext组装阶段

**功能**: 注册自定义Provider到ProviderRegistry

**签名**:
```python
@hookimpl
def df_providers(
    settings: FrameworkSettings,
    logger
) -> Dict[str, Provider]:
    """返回 {name: Provider} 映射"""
    pass
```

**参数**:
- `settings`: 已加载的Settings实例
- `logger`: 日志对象

**返回**: `Dict[str, Provider]`

**使用场景**:
- ✅ 注册自定义服务（消息队列、缓存等）
- ✅ 注册监控客户端
- ✅ 注册第三方SDK
- ✅ 创建共享资源池

**完整示例**:

```python
from df_test_framework import hookimpl
from df_test_framework.infrastructure.providers import SingletonProvider, Provider
from kafka import KafkaProducer, KafkaConsumer
from elasticsearch import Elasticsearch

class KafkaProducerProvider(SingletonProvider):
    """Kafka生产者Provider"""

    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers
        self._producer = None

    def get(self, context):
        if self._producer is None:
            self._producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
        return self._producer

@hookimpl
def df_providers(settings, logger):
    """注册多个自定义Provider"""
    providers = {}

    # Kafka生产者
    kafka_servers = settings.extras.get("kafka_servers")
    if kafka_servers:
        providers["kafka_producer"] = KafkaProducerProvider(kafka_servers)
        logger.info(f"注册Kafka Producer: {kafka_servers}")

    # Elasticsearch客户端
    es_hosts = settings.extras.get("elasticsearch_hosts")
    if es_hosts:
        providers["elasticsearch"] = SingletonProvider(
            lambda ctx: Elasticsearch(hosts=es_hosts)
        )
        logger.info(f"注册Elasticsearch: {es_hosts}")

    # 自定义监控客户端
    providers["app_monitor"] = SingletonProvider(
        lambda ctx: AppMonitor(
            service_name=settings.extras.get("service_name", "test-framework"),
            environment=settings.environment.value
        )
    )

    return providers
```

**在测试中使用**:

```python
def test_kafka_integration(runtime):
    # 获取Kafka生产者
    kafka = runtime.get("kafka_producer")
    kafka.send("test-topic", {"event": "user_created", "user_id": 123})

    # 获取ES客户端
    es = runtime.get("elasticsearch")
    es.index(index="test-logs", body={"message": "test log"})

    # 获取监控客户端
    monitor = runtime.get("app_monitor")
    monitor.record_metric("api.latency", 123)
```

---

### Hook 3: df_post_bootstrap

**触发时机**: RuntimeContext创建完成后

**功能**: 执行任意收尾逻辑

**签名**:
```python
@hookimpl
def df_post_bootstrap(runtime: RuntimeContext) -> None:
    """Runtime创建后执行的逻辑"""
    pass
```

**参数**:
- `runtime`: RuntimeContext实例

**返回**: None

**使用场景**:
- ✅ 环境验证（检查服务可用性）
- ✅ 初始化全局状态
- ✅ 注册pytest插件
- ✅ 打印环境信息
- ✅ 执行预热操作

**完整示例**:

```python
from df_test_framework import hookimpl
import pytest

@hookimpl
def df_post_bootstrap(runtime):
    """Bootstrap后执行多个初始化任务"""
    logger = runtime.logger

    # 1. 验证数据库连接
    try:
        db = runtime.database()
        db.execute_query("SELECT 1")
        logger.info("✅ 数据库连接正常")
    except Exception as e:
        logger.error(f"❌ 数据库连接失败: {e}")
        raise

    # 2. 验证Redis连接
    try:
        redis = runtime.redis_client()
        redis.ping()
        logger.info("✅ Redis连接正常")
    except Exception as e:
        logger.error(f"❌ Redis连接失败: {e}")
        raise

    # 3. 验证HTTP服务可用性
    try:
        http = runtime.http_client()
        response = http.get("/health")
        if response.status_code == 200:
            logger.info("✅ API服务健康检查通过")
        else:
            logger.warning(f"⚠️ API健康检查返回: {response.status_code}")
    except Exception as e:
        logger.error(f"❌ API服务不可用: {e}")

    # 4. 打印环境信息
    logger.info("=" * 60)
    logger.info(f"环境: {runtime.settings.environment.value}")
    logger.info(f"API地址: {runtime.settings.http.base_url}")
    logger.info(f"数据库: {runtime.settings.database.host}")
    logger.info("=" * 60)

    # 5. 注册pytest插件
    if hasattr(pytest, "config"):
        pytest.config.pluginmanager.register(MyCustomPlugin())

    # 6. 预热操作（可选）
    _warmup_services(runtime)

def _warmup_services(runtime):
    """预热服务，避免第一个测试超时"""
    try:
        http = runtime.http_client()
        http.get("/warmup", timeout=5)
        runtime.logger.info("✅ 服务预热完成")
    except:
        pass
```

---

## 📦 内置扩展

框架提供了一些开箱即用的扩展。

### 1. 监控扩展 (Monitoring)

**模块**: `df_test_framework.extensions.builtin.monitoring`

**功能**:
- API性能追踪
- 数据库慢查询监控
- 自动记录到Allure报告

**使用方法**:

```python
from df_test_framework import Bootstrap

runtime = (
    Bootstrap()
    .with_settings(MySettings)
    .with_plugin("df_test_framework.extensions.builtin.monitoring")
    .build()
    .run()
)

# 获取性能追踪器
tracker = runtime.get("api_performance_tracker")

# 在测试中使用
def test_api_performance(runtime):
    tracker = runtime.get("api_performance_tracker")
    http = runtime.http_client()

    with tracker.track("用户登录API"):
        response = http.post("/api/login", json={"username": "test"})

    # 追踪器会自动记录耗时
    stats = tracker.get_stats()
    print(f"平均耗时: {stats['用户登录API']['avg_ms']}ms")
```

**配置项**:

```python
class MySettings(FrameworkSettings):
    extras: dict = {
        "performance_slow_threshold": 500  # 慢请求阈值（毫秒）
    }
```

**输出示例**:

```
[INFO] API调用: 用户登录API
[INFO] └─ 耗时: 234ms ✅
[INFO] └─ 状态: 成功

[WARNING] API调用: 查询订单列表
[WARNING] └─ 耗时: 1250ms ⚠️ (超过阈值500ms)
```

---

## 🛠️ 自定义扩展开发

### 完整开发流程

#### 步骤1: 创建扩展模块

```python
# my_project/extensions/environment_validator.py
"""环境验证扩展 - 确保测试环境符合要求"""

from df_test_framework import hookimpl
import os
import sys

@hookimpl
def df_post_bootstrap(runtime):
    """验证测试环境"""
    logger = runtime.logger
    settings = runtime.settings

    logger.info("🔍 开始环境验证...")

    # 1. 检查必需的环境变量
    required_envs = ["API_KEY", "DATABASE_URL", "REDIS_URL"]
    missing = [env for env in required_envs if not os.getenv(env)]

    if missing:
        logger.error(f"❌ 缺少环境变量: {', '.join(missing)}")
        sys.exit(1)

    # 2. 检查Python版本
    if sys.version_info < (3, 10):
        logger.error(f"❌ Python版本过低: {sys.version}, 需要 >= 3.10")
        sys.exit(1)

    # 3. 检查网络连通性
    if not _check_network(settings.http.base_url):
        logger.error(f"❌ 无法连接到API: {settings.http.base_url}")
        sys.exit(1)

    # 4. 检查数据库权限
    try:
        db = runtime.database()
        db.execute_query("SELECT 1 FROM users LIMIT 1")
    except Exception as e:
        logger.error(f"❌ 数据库权限不足: {e}")
        sys.exit(1)

    logger.info("✅ 环境验证通过!")

def _check_network(url: str) -> bool:
    """检查网络连通性"""
    import socket
    from urllib.parse import urlparse

    try:
        hostname = urlparse(url).hostname
        socket.gethostbyname(hostname)
        return True
    except:
        return False
```

#### 步骤2: 注册扩展

**方式1: 在conftest.py中注册**

```python
# tests/conftest.py
import pytest
from df_test_framework import Bootstrap

@pytest.fixture(scope="session")
def runtime():
    return (
        Bootstrap()
        .with_settings(MySettings)
        .with_plugin("my_project.extensions.environment_validator")
        .build()
        .run()
    )
```

**方式2: 通过pytest.ini注册**

```ini
[pytest]
df_settings_class = my_project.settings.MySettings
df_plugins =
    my_project.extensions.environment_validator
    my_project.extensions.metrics
```

**方式3: 通过环境变量注册**

```bash
export DF_PLUGINS="my_project.extensions.environment_validator,my_project.extensions.metrics"
pytest
```

**方式4: 通过命令行参数**

```bash
pytest --df-plugin my_project.extensions.environment_validator
```

#### 步骤3: 测试扩展

```python
# tests/test_extension.py
def test_extension_loaded(runtime):
    """验证扩展是否正确加载"""
    # 如果环境验证失败，测试根本不会运行到这里
    assert runtime is not None
    assert runtime.settings.environment is not None
```

---

## 🎨 实战示例

### 示例1: Allure增强扩展

自动为所有测试添加环境信息到Allure报告。

```python
# my_project/extensions/allure_enhancer.py
from df_test_framework import hookimpl
import allure
import pytest

@hookimpl
def df_post_bootstrap(runtime):
    """增强Allure报告"""
    settings = runtime.settings

    # 添加环境信息到Allure
    allure.dynamic.environment(
        Environment=settings.environment.value,
        API_URL=settings.http.base_url,
        Database=settings.database.host,
        Redis=settings.redis.host,
    )

    # 添加Epic和Feature标签
    allure.dynamic.epic(f"{settings.extras.get('project_name', 'DF Test')}")

    runtime.logger.info("✅ Allure报告已增强")
```

### 示例2: 数据库备份扩展

测试前备份数据库，测试后恢复。

```python
# my_project/extensions/db_backup.py
from df_test_framework import hookimpl
from df_test_framework.infrastructure.providers import SingletonProvider
import subprocess
from datetime import datetime

class DatabaseBackupManager:
    """数据库备份管理器"""

    def __init__(self, db_config):
        self.db_config = db_config
        self.backup_file = None

    def backup(self):
        """备份数据库"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_file = f"/tmp/db_backup_{timestamp}.sql"

        cmd = f"mysqldump -h {self.db_config.host} -u {self.db_config.user} " \
              f"-p{self.db_config.password} {self.db_config.database} > {self.backup_file}"

        subprocess.run(cmd, shell=True, check=True)
        return self.backup_file

    def restore(self):
        """恢复数据库"""
        if not self.backup_file:
            return

        cmd = f"mysql -h {self.db_config.host} -u {self.db_config.user} " \
              f"-p{self.db_config.password} {self.db_config.database} < {self.backup_file}"

        subprocess.run(cmd, shell=True, check=True)

@hookimpl
def df_providers(settings, logger):
    """注册备份管理器"""
    return {
        "db_backup": SingletonProvider(
            lambda ctx: DatabaseBackupManager(settings.database)
        )
    }

@hookimpl
def df_post_bootstrap(runtime):
    """创建初始备份"""
    if runtime.settings.extras.get("enable_db_backup"):
        backup_mgr = runtime.get("db_backup")
        backup_file = backup_mgr.backup()
        runtime.logger.info(f"✅ 数据库已备份: {backup_file}")
```

**在conftest.py中使用**:

```python
@pytest.fixture(scope="session", autouse=True)
def restore_database_after_tests(runtime):
    """测试结束后恢复数据库"""
    yield

    if runtime.settings.extras.get("enable_db_backup"):
        backup_mgr = runtime.get("db_backup")
        backup_mgr.restore()
        print("✅ 数据库已恢复")
```

### 示例3: 测试数据工厂扩展

提供测试数据快速生成能力。

```python
# my_project/extensions/data_factory.py
from df_test_framework import hookimpl
from df_test_framework.infrastructure.providers import SingletonProvider
from faker import Faker
import random

class TestDataFactory:
    """测试数据工厂"""

    def __init__(self):
        self.faker = Faker('zh_CN')

    def create_user(self, **overrides):
        """创建测试用户数据"""
        user = {
            "username": self.faker.user_name(),
            "email": self.faker.email(),
            "phone": self.faker.phone_number(),
            "name": self.faker.name(),
            "address": self.faker.address(),
            "age": random.randint(18, 60),
        }
        user.update(overrides)
        return user

    def create_order(self, **overrides):
        """创建测试订单数据"""
        order = {
            "order_no": self.faker.uuid4(),
            "amount": round(random.uniform(10, 1000), 2),
            "status": random.choice(["pending", "paid", "shipped"]),
            "created_at": self.faker.date_time_this_year().isoformat(),
        }
        order.update(overrides)
        return order

    def create_batch_users(self, count: int):
        """批量创建用户"""
        return [self.create_user() for _ in range(count)]

@hookimpl
def df_providers(settings, logger):
    """注册数据工厂"""
    return {
        "data_factory": SingletonProvider(lambda ctx: TestDataFactory())
    }
```

**使用示例**:

```python
def test_create_users(runtime):
    factory = runtime.get("data_factory")

    # 创建单个用户
    user = factory.create_user(age=25)
    assert user["age"] == 25

    # 批量创建
    users = factory.create_batch_users(10)
    assert len(users) == 10

    # 使用生成的数据调用API
    http = runtime.http_client()
    response = http.post("/users", json=user)
    assert response.status_code == 201
```

### 示例4: 消息队列扩展

集成RabbitMQ或Kafka。

```python
# my_project/extensions/message_queue.py
from df_test_framework import hookimpl
from df_test_framework.infrastructure.providers import SingletonProvider
import pika
import json

class RabbitMQClient:
    """RabbitMQ客户端封装"""

    def __init__(self, host: str, port: int = 5672):
        self.host = host
        self.port = port
        self._connection = None
        self._channel = None

    def connect(self):
        """建立连接"""
        if not self._connection or self._connection.is_closed:
            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host, port=self.port)
            )
            self._channel = self._connection.channel()

    def publish(self, exchange: str, routing_key: str, message: dict):
        """发布消息"""
        self.connect()
        self._channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=json.dumps(message)
        )

    def consume(self, queue: str, callback, timeout: int = 5):
        """消费消息（带超时）"""
        self.connect()
        self._channel.queue_declare(queue=queue, durable=True)

        for method, properties, body in self._channel.consume(queue, inactivity_timeout=timeout):
            if method:
                callback(json.loads(body))
                self._channel.basic_ack(method.delivery_tag)
                break

    def close(self):
        """关闭连接"""
        if self._connection and not self._connection.is_closed:
            self._connection.close()

@hookimpl
def df_providers(settings, logger):
    """注册MQ客户端"""
    mq_host = settings.extras.get("rabbitmq_host")
    if not mq_host:
        logger.warning("未配置rabbitmq_host，跳过MQ Provider")
        return {}

    return {
        "mq": SingletonProvider(
            lambda ctx: RabbitMQClient(host=mq_host)
        )
    }

@hookimpl
def df_post_bootstrap(runtime):
    """验证MQ连接"""
    mq = runtime.get("mq")
    if mq:
        try:
            mq.connect()
            runtime.logger.info("✅ RabbitMQ连接正常")
        except Exception as e:
            runtime.logger.error(f"❌ RabbitMQ连接失败: {e}")
```

---

## 🎯 最佳实践

### 1. 扩展命名规范

```python
# ✅ 好的命名
my_project.extensions.monitoring
my_project.extensions.data_factory
my_project.extensions.allure_enhancer

# ❌ 不好的命名
my_project.ext
my_project.plugin1
my_project.utils
```

### 2. 单一职责原则

每个扩展只做一件事：

```python
# ✅ 好的设计 - 职责单一
@hookimpl
def df_providers(settings, logger):
    """只注册监控相关的Provider"""
    return {
        "api_tracker": SingletonProvider(...),
        "db_monitor": SingletonProvider(...),
    }

# ❌ 不好的设计 - 职责混乱
@hookimpl
def df_providers(settings, logger):
    """注册了各种不相关的东西"""
    return {
        "api_tracker": SingletonProvider(...),
        "kafka": SingletonProvider(...),
        "elasticsearch": SingletonProvider(...),
        "data_factory": SingletonProvider(...),
    }
```

### 3. 优雅的错误处理

```python
@hookimpl
def df_post_bootstrap(runtime):
    """验证环境时提供详细的错误信息"""
    try:
        # 验证逻辑
        _validate_services(runtime)
    except Exception as e:
        runtime.logger.error("=" * 60)
        runtime.logger.error("❌ 环境验证失败")
        runtime.logger.error(f"原因: {e}")
        runtime.logger.error("请检查：")
        runtime.logger.error("  1. 数据库是否启动")
        runtime.logger.error("  2. Redis是否启动")
        runtime.logger.error("  3. API服务是否可访问")
        runtime.logger.error("=" * 60)
        raise
```

### 4. 使用配置开关

让扩展可以通过配置启用/禁用：

```python
@hookimpl
def df_providers(settings, logger):
    """根据配置决定是否启用"""
    providers = {}

    # 只在启用时注册
    if settings.extras.get("enable_monitoring", False):
        providers["api_tracker"] = SingletonProvider(...)
        logger.info("✅ 监控扩展已启用")
    else:
        logger.info("⏸️  监控扩展已禁用")

    return providers
```

### 5. 文档和示例

为每个扩展编写清晰的文档：

```python
"""
Performance Monitoring Extension
=================================

功能:
  - API调用性能追踪
  - 数据库查询性能监控
  - 自动生成性能报告

配置:
  在Settings中添加:
  ```python
  class MySettings(FrameworkSettings):
      extras: dict = {
          "enable_monitoring": True,
          "slow_threshold_ms": 500,
      }
  ```

使用:
  ```python
  tracker = runtime.get("api_tracker")
  with tracker.track("登录API"):
      response = http.post("/login", ...)
  ```

输出:
  - 控制台: 实时性能日志
  - Allure: 性能统计图表
"""
```

### 6. 测试你的扩展

```python
# tests/test_extensions.py
import pytest

def test_monitoring_extension(runtime):
    """测试监控扩展是否正确加载"""
    tracker = runtime.get("api_tracker")
    assert tracker is not None

    with tracker.track("test_operation"):
        time.sleep(0.1)

    stats = tracker.get_stats()
    assert "test_operation" in stats
    assert stats["test_operation"]["count"] == 1

def test_data_factory_extension(runtime):
    """测试数据工厂扩展"""
    factory = runtime.get("data_factory")
    assert factory is not None

    user = factory.create_user(age=30)
    assert user["age"] == 30
    assert "email" in user
```

---

## ❓ 常见问题

### Q1: 扩展加载顺序如何控制？

**A**: pluggy按注册顺序调用Hook。如果需要特定顺序：

```python
Bootstrap()
    .with_plugin("my_project.extensions.config")      # 1. 先加载配置
    .with_plugin("my_project.extensions.monitoring")  # 2. 再加载监控
    .with_plugin("my_project.extensions.validators")  # 3. 最后验证
    .build()
```

### Q2: 扩展之间如何共享数据？

**A**: 通过RuntimeContext传递：

```python
# 扩展A: 设置数据
@hookimpl
def df_post_bootstrap(runtime):
    runtime.extras["shared_data"] = {"key": "value"}

# 扩展B: 读取数据
@hookimpl
def df_post_bootstrap(runtime):
    data = runtime.extras.get("shared_data")
    print(data)
```

### Q3: 如何调试扩展？

**A**: 使用日志和断点：

```python
@hookimpl
def df_providers(settings, logger):
    logger.debug("进入df_providers hook")
    logger.debug(f"Settings: {settings}")

    # 设置断点
    import pdb; pdb.set_trace()

    return {}
```

### Q4: 扩展抛出异常会怎样？

**A**: 会中断Bootstrap流程。建议：

```python
@hookimpl
def df_post_bootstrap(runtime):
    try:
        # 可能失败的操作
        risky_operation()
    except Exception as e:
        # 记录日志但不中断
        runtime.logger.warning(f"扩展执行失败: {e}")
        # 或者重新抛出异常中断流程
        # raise
```

### Q5: 如何在不同环境使用不同扩展？

**A**: 条件注册：

```python
@pytest.fixture(scope="session")
def runtime(request):
    builder = Bootstrap().with_settings(MySettings)

    # 生产环境加载额外验证
    if os.getenv("ENV") == "production":
        builder.with_plugin("my_project.extensions.prod_validator")

    # 开发环境加载Mock
    if os.getenv("ENV") == "development":
        builder.with_plugin("my_project.extensions.mocks")

    return builder.build().run()
```

### Q6: Provider的生命周期是什么？

**A**:
- `SingletonProvider`: 整个测试会话只创建一次
- 自定义Provider: 可以控制生命周期

```python
from df_test_framework.infrastructure.providers import Provider

class PerTestProvider(Provider):
    """每个测试创建新实例"""
    def get(self, context):
        return MyService()  # 每次调用都创建新实例
```

### Q7: 如何打包和分发扩展？

**A**: 作为独立包发布：

```python
# my_extensions/setup.py
setup(
    name="my-test-extensions",
    version="1.0.0",
    packages=["my_extensions"],
    install_requires=["df-test-framework>=2.0.0"],
    entry_points={
        "df_test_framework.plugins": [
            "monitoring = my_extensions.monitoring",
        ]
    }
)
```

安装后自动加载：

```bash
pip install my-test-extensions
# 扩展会自动通过entry_points加载
```

---

## 🔗 相关资源

- [API参考 - Extensions](../api-reference/extensions.md) - 详细API文档
- [架构设计 - 扩展点](../architecture/extension-points.md) - 扩展系统架构
- [pluggy官方文档](https://pluggy.readthedocs.io/) - pluggy使用指南

---

**返回**: [用户指南首页](README.md) | [文档中心](../README.md)
