# Extensions API 参考

扩展系统的完整API参考，包含Hook机制、ExtensionManager和自定义扩展开发。

---

## 📦 模块导入

```python
# ExtensionManager
from df_test_framework import ExtensionManager, create_extension_manager

# Hook装饰器
from df_test_framework import hookimpl

# 或者从具体模块导入
from df_test_framework.extensions import (
    ExtensionManager,
    create_extension_manager,
    hookimpl,
)
```

---

## 🎯 扩展系统概述

DF Test Framework的扩展系统基于[pluggy](https://pluggy.readthedocs.io/)实现，提供了强大的Hook机制，允许在框架的关键节点注入自定义逻辑。

### 核心概念

1. **Hook Specification（规范）**: 框架定义的扩展点
2. **Hook Implementation（实现）**: 插件对Hook的具体实现
3. **ExtensionManager（管理器）**: 管理插件注册和Hook调用
4. **Plugin（插件）**: 包含Hook实现的类或模块

### 工作流程

```
定义扩展类 → 使用@hookimpl装饰方法 → 注册到ExtensionManager → 框架在适当时机调用Hook
```

---

## 🔌 可用的Hook点

框架提供了3个内置Hook点，覆盖配置加载、资源注册和Bootstrap后处理。

### df_config_sources

**时机**: 配置加载阶段

**功能**: 提供额外的配置源（ConfigSource）

**签名**:
```python
@hookimpl
def df_config_sources(
    self,
    settings_cls: Type[FrameworkSettings]
) -> Iterable[ConfigSource]:
    """返回要添加到配置管道的ConfigSource对象列表"""
```

**参数**:
- `settings_cls`: Settings类

**返回**: `Iterable[ConfigSource]`

**使用场景**:
- 从远程配置中心加载配置
- 从数据库加载配置
- 添加自定义配置源

**示例**:
```python
from df_test_framework import hookimpl
from df_test_framework.infrastructure.config.sources import ConfigSource

class RemoteConfigExtension:
    """从远程配置中心加载配置"""

    @hookimpl
    def df_config_sources(self, settings_cls):
        """添加远程配置源"""
        return [RemoteConfigSource(url="https://config.example.com")]

class RemoteConfigSource(ConfigSource):
    def __init__(self, url: str):
        self.url = url

    def load(self, settings_cls):
        # 从远程加载配置
        response = requests.get(self.url)
        return response.json()
```

---

### df_providers

**时机**: Provider注册阶段

**功能**: 注册自定义Provider到Registry

**签名**:
```python
@hookimpl
def df_providers(
    self,
    settings: FrameworkSettings,
    logger
) -> Dict[str, Provider]:
    """返回provider_name -> Provider的映射"""
```

**参数**:
- `settings`: 配置对象
- `logger`: 日志对象

**返回**: `Dict[str, Provider]`

**使用场景**:
- 注册自定义资源Provider
- 注册第三方服务客户端
- 注册业务特定的工具类

**示例**:
```python
from df_test_framework import hookimpl

class CustomProviderExtension:
    """注册自定义Provider"""

    @hookimpl
    def df_providers(self, settings, logger):
        """注册Kafka客户端Provider"""
        return {
            "kafka_client": KafkaProvider(settings, logger),
            "minio_client": MinioProvider(settings, logger),
        }

class KafkaProvider:
    def __init__(self, settings, logger):
        self.settings = settings
        self.logger = logger
        self._client = None

    def get(self, runtime):
        if self._client is None:
            # 延迟初始化
            self._client = KafkaClient(
                bootstrap_servers=self.settings.kafka_servers
            )
        return self._client

    def shutdown(self):
        if self._client:
            self._client.close()
```

---

### df_post_bootstrap

**时机**: Bootstrap完成后

**功能**: 执行Bootstrap后的自定义逻辑

**签名**:
```python
@hookimpl
def df_post_bootstrap(
    self,
    runtime: RuntimeContext
) -> None:
    """在RuntimeContext创建后执行任意逻辑"""
```

**参数**:
- `runtime`: 运行时上下文

**返回**: `None`

**使用场景**:
- 初始化全局状态
- 预热缓存
- 记录启动日志
- 发送启动通知

**示例**:
```python
from df_test_framework import hookimpl

class StartupNotificationExtension:
    """启动通知扩展"""

    @hookimpl
    def df_post_bootstrap(self, runtime):
        """Bootstrap完成后发送通知"""
        logger = runtime.logger
        settings = runtime.settings

        logger.info(f"框架已启动: env={settings.env}")

        # 发送启动通知到Slack
        send_slack_notification(
            f"测试环境启动: {settings.env}"
        )

        # 预热缓存
        self._warm_up_cache(runtime)

    def _warm_up_cache(self, runtime):
        """预热缓存"""
        redis = runtime.redis()
        redis.set("warmup", "completed")
```

---

## 🔧 ExtensionManager - 扩展管理器

**说明**: 管理插件注册和Hook调用的核心类。

### 创建ExtensionManager

```python
from df_test_framework import create_extension_manager

# 创建管理器
manager = create_extension_manager()
```

---

### 核心方法

#### register()

**功能**: 注册单个插件

**签名**:
```python
def register(plugin: Union[str, object]) -> None
```

**参数**:
- `plugin`: 插件对象或模块路径字符串

**示例**:
```python
# 方式1: 注册插件对象
manager.register(MyExtension())

# 方式2: 注册模块路径
manager.register("my_project.extensions.monitoring")
```

---

#### register_many()

**功能**: 批量注册插件

**签名**:
```python
def register_many(plugins: Iterable[Union[str, object]]) -> None
```

**示例**:
```python
manager.register_many([
    MyExtension(),
    AnotherExtension(),
    "my_project.extensions.metrics",
])
```

---

### 与Bootstrap集成

Bootstrap提供了`with_plugin()`方法来注册插件：

```python
from df_test_framework import Bootstrap

runtime = (
    Bootstrap()
    .with_settings(MySettings)
    .with_plugin(MonitoringExtension())
    .with_plugin(LoggingExtension())
    .build()
    .run()
)
```

---

## 📝 开发自定义扩展

### 基本步骤

1. **创建扩展类**
2. **实现Hook方法（使用@hookimpl装饰）**
3. **注册扩展到Bootstrap**

---

### 示例1: 请求监控扩展

```python
from df_test_framework import hookimpl
from typing import Dict
import time

class APIMonitoringExtension:
    """API请求监控扩展"""

    def __init__(self):
        self.request_count = 0
        self.total_duration = 0

    @hookimpl
    def df_post_bootstrap(self, runtime):
        """初始化监控"""
        logger = runtime.logger
        logger.info("API监控扩展已启动")

        # 可以在这里注册HTTP拦截器
        http = runtime.http_client()
        self._wrap_http_client(http, logger)

    def _wrap_http_client(self, http, logger):
        """包装HTTP客户端，记录请求统计"""
        original_request = http.request

        def monitored_request(method, url, **kwargs):
            start = time.time()
            try:
                response = original_request(method, url, **kwargs)
                duration = time.time() - start

                # 记录统计
                self.request_count += 1
                self.total_duration += duration

                logger.info(
                    f"API请求: {method} {url}, "
                    f"耗时: {duration:.3f}s, "
                    f"总请求数: {self.request_count}"
                )

                return response
            except Exception as e:
                duration = time.time() - start
                logger.error(
                    f"API请求失败: {method} {url}, "
                    f"耗时: {duration:.3f}s, "
                    f"错误: {str(e)}"
                )
                raise

        http.request = monitored_request

# 使用
runtime = (
    Bootstrap()
    .with_settings(MySettings)
    .with_plugin(APIMonitoringExtension())
    .build()
    .run()
)
```

---

### 示例2: 数据库连接池监控

```python
from df_test_framework import hookimpl

class DatabaseMonitoringExtension:
    """数据库连接池监控扩展"""

    @hookimpl
    def df_post_bootstrap(self, runtime):
        """监控数据库连接池"""
        logger = runtime.logger
        db = runtime.database()

        # 获取连接池信息
        pool = db.engine.pool

        logger.info(
            f"数据库连接池状态: "
            f"size={pool.size()}, "
            f"checked_out={pool.checked_out_connections()}, "
            f"overflow={pool.overflow()}"
        )

        # 定期报告连接池状态
        import threading

        def report_pool_status():
            while True:
                time.sleep(60)  # 每分钟报告一次
                logger.info(
                    f"连接池状态: "
                    f"size={pool.size()}, "
                    f"checked_out={pool.checked_out_connections()}"
                )

        thread = threading.Thread(target=report_pool_status, daemon=True)
        thread.start()
```

---

### 示例3: 环境验证扩展

```python
from df_test_framework import hookimpl

class EnvironmentValidationExtension:
    """环境验证扩展"""

    @hookimpl
    def df_post_bootstrap(self, runtime):
        """验证运行环境"""
        logger = runtime.logger
        settings = runtime.settings

        # 验证必需的配置
        if not settings.http.base_url:
            raise ValueError("HTTP base_url未配置")

        # 验证数据库连接
        try:
            db = runtime.database()
            db.query_one("SELECT 1")
            logger.info("✅ 数据库连接正常")
        except Exception as e:
            logger.error(f"❌ 数据库连接失败: {str(e)}")
            raise

        # 验证Redis连接
        try:
            redis = runtime.redis()
            redis.ping()
            logger.info("✅ Redis连接正常")
        except Exception as e:
            logger.warning(f"⚠️ Redis连接失败: {str(e)}")

        # 验证API可达性
        try:
            http = runtime.http_client()
            response = http.get("/health")
            logger.info(f"✅ API健康检查通过: {response.status_code}")
        except Exception as e:
            logger.error(f"❌ API健康检查失败: {str(e)}")
            raise
```

---

### 示例4: 自定义Provider扩展

```python
from df_test_framework import hookimpl
import boto3

class AWSServicesExtension:
    """AWS服务Provider扩展"""

    @hookimpl
    def df_providers(self, settings, logger):
        """注册AWS服务Providers"""
        return {
            "s3_client": S3Provider(settings, logger),
            "sqs_client": SQSProvider(settings, logger),
        }

class S3Provider:
    """S3客户端Provider"""

    def __init__(self, settings, logger):
        self.settings = settings
        self.logger = logger
        self._client = None

    def get(self, runtime):
        if self._client is None:
            self._client = boto3.client(
                "s3",
                aws_access_key_id=self.settings.aws_access_key,
                aws_secret_access_key=self.settings.aws_secret_key,
                region_name=self.settings.aws_region,
            )
            self.logger.info("S3客户端已初始化")
        return self._client

    def shutdown(self):
        # S3客户端无需显式关闭
        pass

class SQSProvider:
    """SQS客户端Provider"""

    def __init__(self, settings, logger):
        self.settings = settings
        self.logger = logger
        self._client = None

    def get(self, runtime):
        if self._client is None:
            self._client = boto3.client(
                "sqs",
                aws_access_key_id=self.settings.aws_access_key,
                aws_secret_access_key=self.settings.aws_secret_key,
                region_name=self.settings.aws_region,
            )
            self.logger.info("SQS客户端已初始化")
        return self._client

    def shutdown(self):
        pass

# 使用
runtime = (
    Bootstrap()
    .with_settings(MySettings)
    .with_plugin(AWSServicesExtension())
    .build()
    .run()
)

# 在测试中使用
s3 = runtime.get("s3_client")
s3.upload_file("local_file.txt", "my-bucket", "remote_file.txt")

sqs = runtime.get("sqs_client")
sqs.send_message(QueueUrl="https://sqs...", MessageBody="Hello")
```

---

## 🎨 扩展开发最佳实践

### 1. 命名约定

```python
# ✅ 好的命名
class MetricsCollectionExtension:
    pass

class DatabaseOptimizationExtension:
    pass

# ❌ 避免的命名
class Extension1:  # 不清晰
    pass

class Plugin:  # 太通用
    pass
```

---

### 2. 单一职责

每个扩展应该只关注一个特定功能：

```python
# ✅ 好的设计：每个扩展专注于一个功能
class MetricsExtension:
    """只负责收集指标"""
    pass

class LoggingExtension:
    """只负责日志增强"""
    pass

# ❌ 避免的设计：一个扩展做太多事情
class EverythingExtension:
    """监控、日志、验证、通知...全部功能"""
    pass
```

---

### 3. 错误处理

```python
class RobustExtension:
    @hookimpl
    def df_post_bootstrap(self, runtime):
        logger = runtime.logger

        try:
            # 执行扩展逻辑
            self._initialize(runtime)
        except Exception as e:
            # 记录错误但不影响框架启动
            logger.error(f"扩展初始化失败: {str(e)}")
            # 可选：根据严重性决定是否抛出异常
            if self.is_critical:
                raise
```

---

### 4. 资源清理

```python
class CleanupAwareExtension:
    def __init__(self):
        self.resources = []

    @hookimpl
    def df_post_bootstrap(self, runtime):
        # 创建资源
        resource = SomeResource()
        self.resources.append(resource)

        # 注册清理函数
        import atexit
        atexit.register(self.cleanup)

    def cleanup(self):
        """清理资源"""
        for resource in self.resources:
            try:
                resource.close()
            except Exception:
                pass
```

---

### 5. 配置支持

```python
from pydantic import BaseModel, Field

class MyExtensionConfig(BaseModel):
    enabled: bool = Field(default=True)
    interval: int = Field(default=60)
    threshold: float = Field(default=0.8)

class ConfigurableExtension:
    def __init__(self, config: MyExtensionConfig = None):
        self.config = config or MyExtensionConfig()

    @hookimpl
    def df_post_bootstrap(self, runtime):
        if not self.config.enabled:
            return  # 扩展被禁用

        # 使用配置
        logger = runtime.logger
        logger.info(f"扩展启动: interval={self.config.interval}s")

# 使用
config = MyExtensionConfig(enabled=True, interval=30)
runtime = (
    Bootstrap()
    .with_settings(MySettings)
    .with_plugin(ConfigurableExtension(config))
    .build()
    .run()
)
```

---

## 📚 完整扩展示例

### Allure报告增强扩展

```python
from df_test_framework import hookimpl
import allure

class AllureEnhancementExtension:
    """Allure报告增强扩展"""

    @hookimpl
    def df_post_bootstrap(self, runtime):
        """添加环境信息到Allure报告"""
        settings = runtime.settings

        # 添加环境信息
        allure.environment(
            env=settings.env,
            api_base_url=settings.http.base_url,
            database=self._mask_connection_string(settings.db.connection_string),
            redis_host=settings.redis.host,
        )

        # 添加框架版本
        import df_test_framework
        allure.environment(
            framework_version=df_test_framework.__version__
        )

    def _mask_connection_string(self, conn_str):
        """脱敏连接字符串"""
        if not conn_str:
            return "N/A"
        if "@" in conn_str:
            parts = conn_str.split("@")
            return f"***@{parts[1]}"
        return conn_str
```

---

### 性能分析扩展

```python
from df_test_framework import hookimpl
import time
from collections import defaultdict

class PerformanceProfilingExtension:
    """性能分析扩展"""

    def __init__(self):
        self.api_stats = defaultdict(lambda: {"count": 0, "total_time": 0})
        self.db_stats = defaultdict(lambda: {"count": 0, "total_time": 0})

    @hookimpl
    def df_post_bootstrap(self, runtime):
        """初始化性能分析"""
        self._wrap_http_client(runtime)
        self._wrap_database(runtime)

        # 注册清理函数，打印统计
        import atexit
        atexit.register(self.print_stats)

    def _wrap_http_client(self, runtime):
        """包装HTTP客户端"""
        http = runtime.http_client()
        original_request = http.request

        def profiled_request(method, url, **kwargs):
            start = time.time()
            try:
                return original_request(method, url, **kwargs)
            finally:
                duration = time.time() - start
                key = f"{method} {url}"
                self.api_stats[key]["count"] += 1
                self.api_stats[key]["total_time"] += duration

        http.request = profiled_request

    def _wrap_database(self, runtime):
        """包装数据库"""
        db = runtime.database()
        original_execute = db.execute

        def profiled_execute(sql, params=None):
            start = time.time()
            try:
                return original_execute(sql, params)
            finally:
                duration = time.time() - start
                # 简化SQL（只取前50个字符）
                sql_key = sql[:50]
                self.db_stats[sql_key]["count"] += 1
                self.db_stats[sql_key]["total_time"] += duration

        db.execute = profiled_execute

    def print_stats(self):
        """打印性能统计"""
        print("\n" + "=" * 80)
        print("性能分析报告")
        print("=" * 80)

        print("\nAPI请求统计:")
        for endpoint, stats in sorted(
            self.api_stats.items(),
            key=lambda x: x[1]["total_time"],
            reverse=True
        ):
            avg_time = stats["total_time"] / stats["count"]
            print(
                f"  {endpoint}: "
                f"{stats['count']}次, "
                f"总耗时{stats['total_time']:.2f}s, "
                f"平均{avg_time:.3f}s"
            )

        print("\n数据库查询统计:")
        for sql, stats in sorted(
            self.db_stats.items(),
            key=lambda x: x[1]["total_time"],
            reverse=True
        )[:10]:  # 只显示top 10
            avg_time = stats["total_time"] / stats["count"]
            print(
                f"  {sql}...: "
                f"{stats['count']}次, "
                f"总耗时{stats['total_time']:.2f}s, "
                f"平均{avg_time:.3f}s"
            )
```

---

## 🔗 相关文档

### v3架构文档
- [Clients API](clients.md) - HTTP客户端
- [Databases API](databases.md) - 数据访问
- [Drivers API](drivers.md) - Web自动化
- [Infrastructure API](infrastructure.md) - Bootstrap和Runtime
- [Testing API](testing.md) - Pytest Fixtures和测试辅助工具

### v2兼容文档
- [Core API](core.md) - v2版核心功能
- [Patterns API](patterns.md) - v2版设计模式

### 其他资源
- [扩展系统指南](../user-guide/extensions.md) - 扩展开发详解
- [快速入门](../getting-started/quickstart.md) - 5分钟上手指南
- [v3架构设计](../architecture/V3_ARCHITECTURE.md) - 架构概述

---

**返回**: [API参考首页](README.md) | [文档首页](../README.md)
