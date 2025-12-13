"""指标管理器

MetricsManager 是监控指标的核心管理类

核心功能:
- 初始化 Prometheus 指标收集器
- 管理指标注册表
- 提供便捷的指标创建接口
- 支持指标服务器和推送网关

v3.10.0 新增 - P2.3 Prometheus监控
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Any

from .registry import MetricsRegistry
from .types import Counter, Gauge, Histogram, Summary

# 检查 prometheus_client 是否可用
try:
    import prometheus_client
    from prometheus_client import REGISTRY, push_to_gateway, start_http_server

    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False
    prometheus_client = None  # type: ignore


@dataclass
class MetricsConfig:
    """指标配置

    Attributes:
        service_name: 服务名称
        enabled: 是否启用指标收集
        use_prometheus: 是否使用prometheus_client库
        default_labels: 默认标签（添加到所有指标）
        server_port: 指标服务器端口
        pushgateway_url: 推送网关URL
        push_interval: 推送间隔（秒）
    """

    service_name: str = "df-test-framework"
    enabled: bool = True
    use_prometheus: bool = True
    default_labels: dict[str, str] = field(default_factory=dict)
    server_port: int = 8000
    pushgateway_url: str | None = None
    push_interval: float = 10.0


class MetricsManager:
    """指标管理器

    管理 Prometheus 指标的生命周期和配置

    使用示例:
        >>> # 基础用法
        >>> metrics = MetricsManager(service_name="my-service")
        >>> metrics.init()
        >>>
        >>> # 创建指标
        >>> counter = metrics.counter("requests_total", "Total requests", ["method"])
        >>> histogram = metrics.histogram("request_duration", "Request duration")
        >>>
        >>> # 记录指标
        >>> counter.labels(method="GET").inc()
        >>> histogram.observe(0.5)
        >>>
        >>> # 启动指标服务器
        >>> metrics.start_server(port=8000)
        >>>
        >>> # 使用配置
        >>> config = MetricsConfig(
        ...     service_name="my-service",
        ...     use_prometheus=True,
        ...     server_port=9090
        ... )
        >>> metrics = MetricsManager(config=config)
        >>> metrics.init()
    """

    def __init__(self, service_name: str | None = None, config: MetricsConfig | None = None):
        """初始化指标管理器

        Args:
            service_name: 服务名称（简化配置）
            config: 完整配置对象（优先级高于service_name）
        """
        if config:
            self.config = config
        else:
            self.config = MetricsConfig(service_name=service_name or "df-test-framework")

        self._registry: MetricsRegistry | None = None
        self._initialized = False
        self._server_started = False
        self._push_thread: threading.Thread | None = None
        self._stop_push = threading.Event()

    def init(self) -> MetricsManager:
        """初始化指标收集器

        Returns:
            self，支持链式调用
        """
        if self._initialized:
            return self

        if not self.config.enabled:
            self._initialized = True
            return self

        # 确定是否使用prometheus
        use_prom = self.config.use_prometheus and PROMETHEUS_AVAILABLE

        # 创建注册表
        self._registry = MetricsRegistry(use_prometheus=use_prom)

        # 创建服务信息指标
        info = self._registry.gauge(
            f"{self._safe_name(self.config.service_name)}_info",
            "Service information",
            labels=["version", "service"],
        )
        info.labels(version="3.10.0", service=self.config.service_name).set(1)

        self._initialized = True
        return self

    def shutdown(self) -> None:
        """关闭指标收集器"""
        # 停止推送线程
        if self._push_thread and self._push_thread.is_alive():
            self._stop_push.set()
            self._push_thread.join(timeout=5)

        self._initialized = False
        self._server_started = False

    @property
    def registry(self) -> MetricsRegistry:
        """获取指标注册表"""
        if not self._initialized:
            self.init()

        if self._registry is None:
            raise RuntimeError("MetricsManager未初始化")

        return self._registry

    def counter(self, name: str, description: str, labels: list[str] | None = None) -> Counter:
        """创建计数器

        Args:
            name: 指标名称
            description: 指标描述
            labels: 标签名列表

        Returns:
            Counter实例
        """
        return self.registry.counter(name, description, labels)

    def gauge(self, name: str, description: str, labels: list[str] | None = None) -> Gauge:
        """创建仪表盘

        Args:
            name: 指标名称
            description: 指标描述
            labels: 标签名列表

        Returns:
            Gauge实例
        """
        return self.registry.gauge(name, description, labels)

    def histogram(
        self,
        name: str,
        description: str,
        labels: list[str] | None = None,
        buckets: tuple[float, ...] | None = None,
    ) -> Histogram:
        """创建直方图

        Args:
            name: 指标名称
            description: 指标描述
            labels: 标签名列表
            buckets: 桶边界

        Returns:
            Histogram实例
        """
        return self.registry.histogram(name, description, labels, buckets)

    def summary(self, name: str, description: str, labels: list[str] | None = None) -> Summary:
        """创建摘要

        Args:
            name: 指标名称
            description: 指标描述
            labels: 标签名列表

        Returns:
            Summary实例
        """
        return self.registry.summary(name, description, labels)

    def start_server(self, port: int | None = None) -> None:
        """启动指标服务器

        Args:
            port: 服务端口（默认使用配置中的端口）

        Raises:
            ImportError: prometheus_client未安装
            RuntimeError: 服务器已启动
        """
        if not PROMETHEUS_AVAILABLE:
            raise ImportError("指标服务器需要安装: pip install prometheus-client")

        if self._server_started:
            return

        port = port or self.config.server_port
        start_http_server(port, registry=self.registry.prometheus_registry or REGISTRY)
        self._server_started = True

    def push_to_gateway(self, gateway_url: str | None = None, job: str | None = None) -> None:
        """推送指标到Pushgateway

        Args:
            gateway_url: 推送网关URL
            job: 作业名称

        Raises:
            ImportError: prometheus_client未安装
        """
        if not PROMETHEUS_AVAILABLE:
            raise ImportError("推送网关需要安装: pip install prometheus-client")

        url = gateway_url or self.config.pushgateway_url
        if not url:
            raise ValueError("pushgateway_url未配置")

        job_name = job or self.config.service_name

        push_to_gateway(url, job=job_name, registry=self.registry.prometheus_registry or REGISTRY)

    def start_push_loop(
        self, gateway_url: str | None = None, interval: float | None = None
    ) -> None:
        """启动定期推送循环

        Args:
            gateway_url: 推送网关URL
            interval: 推送间隔（秒）
        """
        url = gateway_url or self.config.pushgateway_url
        push_interval = interval or self.config.push_interval

        if not url:
            raise ValueError("pushgateway_url未配置")

        def push_loop():
            while not self._stop_push.wait(push_interval):
                try:
                    self.push_to_gateway(url)
                except Exception:
                    pass  # 静默失败

        self._stop_push.clear()
        self._push_thread = threading.Thread(target=push_loop, daemon=True)
        self._push_thread.start()

    def collect(self) -> dict[str, Any]:
        """收集所有指标

        Returns:
            指标数据字典
        """
        return self.registry.collect()

    @property
    def is_enabled(self) -> bool:
        """指标收集是否启用"""
        return self.config.enabled and self._initialized

    @property
    def is_initialized(self) -> bool:
        """是否已初始化"""
        return self._initialized

    def _safe_name(self, name: str) -> str:
        """转换为安全的指标名称

        Args:
            name: 原始名称

        Returns:
            符合Prometheus命名规范的名称
        """
        # 替换不允许的字符
        safe = name.replace("-", "_").replace(".", "_").replace(" ", "_")
        # 确保以字母开头
        if safe and not safe[0].isalpha():
            safe = "m_" + safe
        return safe


# 全局默认指标管理器（线程安全）
_default_manager: MetricsManager | None = None
_manager_lock = threading.Lock()


def get_metrics_manager() -> MetricsManager:
    """获取全局指标管理器（线程安全）

    使用双重检查锁定模式确保线程安全的单例创建。

    Returns:
        MetricsManager实例
    """
    global _default_manager
    if _default_manager is None:
        with _manager_lock:
            # 双重检查：获取锁后再次检查
            if _default_manager is None:
                _default_manager = MetricsManager()
    return _default_manager


def set_metrics_manager(manager: MetricsManager) -> None:
    """设置全局指标管理器（线程安全）

    Args:
        manager: MetricsManager实例
    """
    global _default_manager
    with _manager_lock:
        _default_manager = manager


__all__ = [
    "MetricsManager",
    "MetricsConfig",
    "get_metrics_manager",
    "set_metrics_manager",
    "PROMETHEUS_AVAILABLE",
]
