# 扩展点详解

本文档深入解析DF Test Framework的扩展系统，包括Hook机制、插件开发和最佳实践。

## 📋 目录

- [扩展系统概述](#扩展系统概述)
- [Hook规范详解](#hook规范详解)
- [插件开发指南](#插件开发指南)
- [内置扩展分析](#内置扩展分析)
- [高级扩展模式](#高级扩展模式)
- [调试与测试](#调试与测试)
- [性能考量](#性能考量)

## 🎯 扩展系统概述

### 设计理念

DF Test Framework的扩展系统基于**pluggy**实现，遵循以下原则：

1. **非侵入式**: 扩展不修改框架核心代码
2. **声明式**: 通过装饰器声明Hook实现
3. **可组合**: 多个扩展可以同时工作
4. **惰性加载**: 扩展在需要时才被调用

### 架构概览

```
┌─────────────────────────────────────────┐
│         Bootstrap                        │
│  - 收集扩展                               │
│  - 注册到ExtensionManager                │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│    ExtensionManager (pluggy)            │
│  - PluginManager                         │
│  - HookSpecs注册                         │
│  - Plugin注册                            │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│    Hook执行时机                          │
│  1. df_config_sources (配置阶段)         │
│  2. df_providers (Provider注册阶段)      │
│  3. df_post_bootstrap (启动后)           │
└─────────────────────────────────────────┘
```

### 扩展生命周期

```python
# 1. 定义扩展
class MyExtension:
    @hookimpl
    def df_config_sources(self, settings_cls):
        return [CustomConfigSource()]

    @hookimpl
    def df_providers(self, settings, logger):
        return {"my_service": SingletonProvider(...)}

    @hookimpl
    def df_post_bootstrap(self, runtime):
        print("扩展已初始化")

# 2. 注册扩展
runtime = (
    Bootstrap()
    .with_settings(MySettings)
    .with_plugin(MyExtension())  # 注册
    .build()
    .run()
)

# 3. 自动执行
# - df_config_sources在configure_settings前被调用
# - df_providers在创建ProviderRegistry时被调用
# - df_post_bootstrap在RuntimeContext创建后被调用
```

## 🎣 Hook规范详解

### Hook 1: df_config_sources

**调用时机**: 在`configure_settings()`之前

**用途**: 提供额外的配置源

**签名**:

```python
@hookspec
def df_config_sources(
    self,
    settings_cls: type[FrameworkSettings]
) -> Iterable[ConfigSource]:
    """
    返回额外的ConfigSource对象列表

    参数:
        settings_cls: 当前使用的FrameworkSettings子类

    返回:
        ConfigSource列表（可以为空列表或None）
    """
```

**使用场景**:

1. **从远程配置中心加载配置**
2. **从数据库加载配置**
3. **从文件系统特定位置加载配置**
4. **动态生成配置**

**示例1: 远程配置中心**

```python
from df_test_framework.extensions import hookimpl
from df_test_framework import ConfigSource
import requests

class RemoteConfigSource(ConfigSource):
    """从远程配置中心加载配置"""

    def __init__(self, config_url: str):
        self.config_url = config_url

    def load(self) -> dict:
        response = requests.get(self.config_url)
        response.raise_for_status()
        return response.json()

class RemoteConfigExtension:
    @hookimpl
    def df_config_sources(self, settings_cls):
        # 根据settings类型返回不同的配置URL
        env = os.getenv("ENVIRONMENT", "test")
        config_url = f"http://config-center/api/config/{settings_cls.__name__}/{env}"

        return [RemoteConfigSource(config_url)]

# 使用
runtime = (
    Bootstrap()
    .with_settings(MySettings)
    .with_plugin(RemoteConfigExtension())
    .build()
    .run()
)
# settings会自动合并远程配置
```

**示例2: 数据库配置**

```python
class DatabaseConfigSource(ConfigSource):
    """从数据库加载配置"""

    def __init__(self, db_url: str, table: str = "app_config"):
        self.db_url = db_url
        self.table = table

    def load(self) -> dict:
        from sqlalchemy import create_engine, text

        engine = create_engine(self.db_url)
        with engine.connect() as conn:
            result = conn.execute(
                text(f"SELECT key, value FROM {self.table}")
            )
            return {row.key: row.value for row in result}

class DatabaseConfigExtension:
    @hookimpl
    def df_config_sources(self, settings_cls):
        db_url = os.getenv("CONFIG_DB_URL")
        if db_url:
            return [DatabaseConfigSource(db_url)]
        return []
```

**配置优先级**:

```python
# 最终配置 = 默认值 <- .env文件 <- 环境变量 <- df_config_sources <- 命令行参数
#                                                     ▲
#                                               这里插入扩展配置
```

### Hook 2: df_providers

**调用时机**: 在`RuntimeBuilder.build()`时，`default_providers()`之后

**用途**: 注册自定义资源Provider

**签名**:

```python
@hookspec
def df_providers(
    self,
    settings: FrameworkSettings,
    logger
) -> Dict[str, Provider]:
    """
    返回额外的Provider字典

    参数:
        settings: 已配置的FrameworkSettings实例
        logger: 已配置的Logger实例

    返回:
        Dict[str, Provider] - 键为Provider名称，值为Provider实例
    """
```

**使用场景**:

1. **注册自定义服务客户端**（如消息队列、对象存储）
2. **注册业务特定的工具类**
3. **替换默认Provider实现**

**示例1: 消息队列客户端**

```python
from df_test_framework import SingletonProvider
from df_test_framework.extensions import hookimpl
import pika

class RabbitMQClient:
    """RabbitMQ客户端"""

    def __init__(self, host: str, port: int, logger):
        self.logger = logger
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port)
        )
        self.channel = self.connection.channel()
        self.logger.info(f"RabbitMQ连接已建立: {host}:{port}")

    def publish(self, queue: str, message: str):
        self.channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=message
        )
        self.logger.debug(f"消息已发送到队列 {queue}: {message}")

    def close(self):
        self.connection.close()

class RabbitMQExtension:
    @hookimpl
    def df_providers(self, settings, logger):
        return {
            "rabbitmq": SingletonProvider(
                lambda rt: RabbitMQClient(
                    host=rt.settings.rabbitmq.host,
                    port=rt.settings.rabbitmq.port,
                    logger=rt.logger
                )
            )
        }

# 使用
runtime = Bootstrap().with_plugin(RabbitMQExtension()).build().run()
mq = runtime.get("rabbitmq")
mq.publish("test_queue", "Hello")
```

**示例2: 对象存储客户端**

```python
from minio import Minio

class MinIOClient:
    """MinIO对象存储客户端"""

    def __init__(self, endpoint: str, access_key: str, secret_key: str, logger):
        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=False
        )
        self.logger = logger

    def upload_file(self, bucket: str, object_name: str, file_path: str):
        self.client.fput_object(bucket, object_name, file_path)
        self.logger.info(f"文件已上传: {bucket}/{object_name}")

class MinIOExtension:
    @hookimpl
    def df_providers(self, settings, logger):
        return {
            "minio": SingletonProvider(
                lambda rt: MinIOClient(
                    endpoint=rt.settings.minio.endpoint,
                    access_key=rt.settings.minio.access_key,
                    secret_key=rt.settings.minio.secret_key,
                    logger=rt.logger
                )
            )
        }
```

**示例3: 替换默认Provider**

```python
class CustomHttpClient(HttpClient):
    """自定义HttpClient - 添加额外功能"""

    def request(self, method: str, url: str, **kwargs):
        # 自动添加认证头
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        kwargs["headers"]["X-Custom-Auth"] = self._get_auth_token()

        return super().request(method, url, **kwargs)

class CustomHttpExtension:
    @hookimpl
    def df_providers(self, settings, logger):
        # 替换默认的http_client
        return {
            "http_client": SingletonProvider(
                lambda rt: CustomHttpClient(
                    base_url=rt.settings.http.base_url,
                    logger=rt.logger
                )
            )
        }

# 现在runtime.http_client()返回CustomHttpClient实例
```

### Hook 3: df_post_bootstrap

**调用时机**: 在`RuntimeContext`创建之后，`run()`返回之前

**用途**: 执行初始化逻辑、验证、预热

**签名**:

```python
@hookspec
def df_post_bootstrap(
    self,
    runtime: RuntimeContext
) -> None:
    """
    在RuntimeContext创建后执行

    参数:
        runtime: 完整的RuntimeContext实例
    """
```

**使用场景**:

1. **初始化数据库schema**
2. **预热缓存**
3. **验证配置连通性**
4. **启动后台任务**

**示例1: 数据库Schema初始化**

```python
class DatabaseSchemaExtension:
    @hookimpl
    def df_post_bootstrap(self, runtime):
        db = runtime.database()
        logger = runtime.logger

        # 检查表是否存在
        result = db.execute(
            "SELECT COUNT(*) FROM information_schema.tables "
            "WHERE table_name = 'users'"
        ).scalar()

        if result == 0:
            logger.warning("users表不存在，正在创建...")
            db.execute("""
                CREATE TABLE users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            logger.info("users表创建成功")
```

**示例2: 缓存预热**

```python
class CacheWarmupExtension:
    @hookimpl
    def df_post_bootstrap(self, runtime):
        redis = runtime.redis()
        logger = runtime.logger

        logger.info("开始预热缓存...")

        # 预加载常用配置
        common_configs = {
            "app:version": "2.0.0",
            "app:features": ["feature_a", "feature_b"],
            "app:limits": {"max_users": 1000}
        }

        for key, value in common_configs.items():
            redis.set(key, value, ex=3600)

        logger.info(f"缓存预热完成，加载了{len(common_configs)}个配置项")
```

**示例3: 连通性验证**

```python
class ConnectivityCheckExtension:
    @hookimpl
    def df_post_bootstrap(self, runtime):
        logger = runtime.logger
        settings = runtime.settings

        # 检查HTTP服务连通性
        try:
            http = runtime.http_client()
            response = http.get("/health")
            if response.status_code == 200:
                logger.info("✅ HTTP服务连通性检查通过")
            else:
                logger.error(f"❌ HTTP服务返回状态码: {response.status_code}")
        except Exception as e:
            logger.error(f"❌ HTTP服务连通性检查失败: {e}")

        # 检查数据库连通性
        try:
            db = runtime.database()
            db.execute("SELECT 1")
            logger.info("✅ 数据库连通性检查通过")
        except Exception as e:
            logger.error(f"❌ 数据库连通性检查失败: {e}")

        # 检查Redis连通性
        try:
            redis = runtime.redis()
            redis.ping()
            logger.info("✅ Redis连通性检查通过")
        except Exception as e:
            logger.error(f"❌ Redis连通性检查失败: {e}")
```

## 🛠️ 插件开发指南

### 插件结构模板

**完整插件示例**:

```python
# my_plugin.py
from df_test_framework.extensions import hookimpl
from df_test_framework import SingletonProvider, ConfigSource
from typing import Dict, Iterable, Optional
import logging

class MyPluginConfig:
    """插件配置"""
    def __init__(self, enabled: bool = True, level: str = "INFO"):
        self.enabled = enabled
        self.level = level

class MyPlugin:
    """
    我的自定义插件

    功能:
    - 提供额外配置源
    - 注册自定义Provider
    - 执行初始化逻辑

    使用:
        runtime = Bootstrap().with_plugin(MyPlugin()).build().run()
    """

    def __init__(self, config: Optional[MyPluginConfig] = None):
        self.config = config or MyPluginConfig()

    @hookimpl
    def df_config_sources(self, settings_cls) -> Iterable[ConfigSource]:
        """提供额外配置"""
        if not self.config.enabled:
            return []

        # 返回自定义配置源
        return [MyConfigSource()]

    @hookimpl
    def df_providers(self, settings, logger) -> Dict[str, Provider]:
        """注册自定义Provider"""
        if not self.config.enabled:
            return {}

        return {
            "my_service": SingletonProvider(
                lambda rt: MyService(rt.settings, rt.logger)
            )
        }

    @hookimpl
    def df_post_bootstrap(self, runtime) -> None:
        """初始化逻辑"""
        if not self.config.enabled:
            return

        runtime.logger.info(f"MyPlugin已启动，级别: {self.config.level}")

        # 执行初始化
        my_service = runtime.get("my_service")
        my_service.initialize()
```

### 插件命名规范

```python
# ✅ 好的命名
class AuthenticationPlugin: ...
class MonitoringExtension: ...
class CacheWarmupPlugin: ...

# ❌ 避免的命名
class Plugin1: ...  # 不清晰
class Ext: ...      # 缩写
class MyStuff: ...  # 不专业
```

### 插件打包发布

**项目结构**:

```
my-plugin/
├── src/
│   └── df_test_framework_my_plugin/
│       ├── __init__.py
│       ├── plugin.py
│       └── services.py
├── tests/
│   └── test_plugin.py
├── README.md
├── LICENSE
└── pyproject.toml
```

**pyproject.toml**:

```toml
[project]
name = "df-test-framework-my-plugin"
version = "1.0.0"
description = "我的DF Test Framework插件"
dependencies = [
    "df-test-framework>=2.0.0,<3.0.0",
]

[project.entry-points."df_test_framework.plugins"]
my_plugin = "df_test_framework_my_plugin:MyPlugin"
```

**自动发现插件**:

```python
# 用户无需手动注册，框架自动发现
runtime = Bootstrap().with_settings(MySettings).build().run()
# MyPlugin自动加载（如果已安装）
```

## 🏆 内置扩展分析

### APIPerformanceTracker

**位置**: `src/df_test_framework/extensions/builtin/monitoring/api_tracker.py`

**功能**: 追踪API请求性能

**实现**:

```python
class APIPerformanceTracker:
    def __init__(self):
        self.metrics = {}

    @hookimpl
    def df_post_bootstrap(self, runtime):
        # Hook到HttpClient的请求方法
        original_request = runtime.http_client().request

        def tracked_request(method, url, **kwargs):
            start_time = time.time()
            try:
                response = original_request(method, url, **kwargs)
                duration = time.time() - start_time

                # 记录指标
                key = f"{method} {url}"
                if key not in self.metrics:
                    self.metrics[key] = []
                self.metrics[key].append(duration)

                runtime.logger.debug(
                    f"API请求: {method} {url} - {duration:.3f}s"
                )

                return response
            except Exception as e:
                duration = time.time() - start_time
                runtime.logger.error(
                    f"API请求失败: {method} {url} - {duration:.3f}s - {e}"
                )
                raise

        # 替换方法
        runtime.http_client().request = tracked_request

    def get_stats(self):
        """获取性能统计"""
        stats = {}
        for endpoint, durations in self.metrics.items():
            stats[endpoint] = {
                "count": len(durations),
                "avg": sum(durations) / len(durations),
                "min": min(durations),
                "max": max(durations),
            }
        return stats
```

### SlowQueryMonitor

**位置**: `src/df_test_framework/extensions/builtin/monitoring/db_monitor.py`

**功能**: 监控慢SQL查询

**实现**:

```python
class SlowQueryMonitor:
    def __init__(self, threshold: float = 1.0):
        self.threshold = threshold  # 慢查询阈值（秒）
        self.slow_queries = []

    @hookimpl
    def df_post_bootstrap(self, runtime):
        db = runtime.database()
        original_execute = db.execute

        def monitored_execute(query, params=None):
            start_time = time.time()
            result = original_execute(query, params)
            duration = time.time() - start_time

            if duration > self.threshold:
                self.slow_queries.append({
                    "query": query,
                    "params": params,
                    "duration": duration,
                    "timestamp": datetime.now()
                })
                runtime.logger.warning(
                    f"慢查询检测: {duration:.3f}s - {query[:100]}"
                )

            return result

        db.execute = monitored_execute
```

## 🚀 高级扩展模式

### 模式1: 条件扩展

```python
class ConditionalExtension:
    """根据环境决定是否启用"""

    @hookimpl
    def df_post_bootstrap(self, runtime):
        env = runtime.settings.environment

        if env == "prod":
            # 生产环境：启用严格模式
            self._enable_strict_mode(runtime)
        elif env == "dev":
            # 开发环境：启用调试模式
            self._enable_debug_mode(runtime)

    def _enable_strict_mode(self, runtime):
        runtime.logger.info("严格模式已启用")
        # 禁用某些危险操作

    def _enable_debug_mode(self, runtime):
        runtime.logger.info("调试模式已启用")
        # 启用详细日志
```

### 模式2: 扩展组合

```python
class CompositeExtension:
    """组合多个扩展"""

    def __init__(self, *extensions):
        self.extensions = extensions

    @hookimpl
    def df_config_sources(self, settings_cls):
        sources = []
        for ext in self.extensions:
            if hasattr(ext, 'df_config_sources'):
                result = ext.df_config_sources(settings_cls)
                if result:
                    sources.extend(result)
        return sources

    @hookimpl
    def df_providers(self, settings, logger):
        providers = {}
        for ext in self.extensions:
            if hasattr(ext, 'df_providers'):
                result = ext.df_providers(settings, logger)
                if result:
                    providers.update(result)
        return providers

    @hookimpl
    def df_post_bootstrap(self, runtime):
        for ext in self.extensions:
            if hasattr(ext, 'df_post_bootstrap'):
                ext.df_post_bootstrap(runtime)

# 使用
combined = CompositeExtension(
    AuthExtension(),
    MonitoringExtension(),
    CacheExtension()
)
runtime = Bootstrap().with_plugin(combined).build().run()
```

### 模式3: 动态扩展加载

```python
class DynamicExtensionLoader:
    """从配置文件动态加载扩展"""

    @hookimpl
    def df_config_sources(self, settings_cls):
        # 从配置文件读取扩展列表
        config_file = os.getenv("EXTENSIONS_CONFIG", "extensions.yaml")
        if os.path.exists(config_file):
            with open(config_file) as f:
                config = yaml.safe_load(f)

            extensions = config.get("extensions", [])
            for ext_config in extensions:
                # 动态导入扩展
                module_path = ext_config["module"]
                class_name = ext_config["class"]
                module = importlib.import_module(module_path)
                ext_class = getattr(module, class_name)

                # 实例化并注册
                ext_instance = ext_class(**ext_config.get("params", {}))
                # ... 注册逻辑
```

## 🐛 调试与测试

### 调试扩展

**启用调试日志**:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

runtime = Bootstrap().with_plugin(MyPlugin()).build().run()
# 查看详细的Hook调用日志
```

**手动测试Hook**:

```python
def test_my_plugin_config_sources():
    """测试df_config_sources"""
    plugin = MyPlugin()
    sources = plugin.df_config_sources(MySettings)

    assert sources is not None
    assert len(sources) > 0
    assert isinstance(sources[0], ConfigSource)

def test_my_plugin_providers():
    """测试df_providers"""
    plugin = MyPlugin()
    settings = MySettings()
    logger = logging.getLogger()

    providers = plugin.df_providers(settings, logger)

    assert "my_service" in providers
    assert isinstance(providers["my_service"], SingletonProvider)
```

### 集成测试

```python
def test_plugin_integration():
    """完整集成测试"""
    runtime = (
        Bootstrap()
        .with_settings(MySettings)
        .with_plugin(MyPlugin())
        .build()
        .run()
    )

    # 验证Provider已注册
    my_service = runtime.get("my_service")
    assert my_service is not None

    # 验证初始化逻辑执行
    assert my_service.initialized is True

    runtime.close()
```

## ⚡ 性能考量

### 1. 避免阻塞操作

```python
# ❌ 避免：阻塞操作
class BadExtension:
    @hookimpl
    def df_post_bootstrap(self, runtime):
        time.sleep(10)  # 阻塞启动流程

# ✅ 好：异步或后台执行
class GoodExtension:
    @hookimpl
    def df_post_bootstrap(self, runtime):
        # 启动后台线程
        thread = threading.Thread(target=self._background_task)
        thread.daemon = True
        thread.start()
```

### 2. 延迟初始化

```python
class LazyExtension:
    def __init__(self):
        self._service = None

    @hookimpl
    def df_providers(self, settings, logger):
        # 返回延迟初始化的Provider
        return {
            "lazy_service": SingletonProvider(
                lambda rt: self._create_service(rt)  # 只在首次访问时创建
            )
        }

    def _create_service(self, runtime):
        if self._service is None:
            self._service = ExpensiveService(runtime)
        return self._service
```

### 3. 缓存结果

```python
class CachedExtension:
    def __init__(self):
        self._config_cache = None

    @hookimpl
    def df_config_sources(self, settings_cls):
        if self._config_cache is None:
            # 只加载一次
            self._config_cache = self._load_config()
        return [self._config_cache]
```

## 🔗 相关文档

- [扩展系统用户指南](../user-guide/extensions.md)
- [API参考 - Extensions](../api-reference/extensions.md)
- [v2.0架构详解](v2-architecture.md)

---

**返回**: [架构文档](README.md) | [文档首页](../README.md)
