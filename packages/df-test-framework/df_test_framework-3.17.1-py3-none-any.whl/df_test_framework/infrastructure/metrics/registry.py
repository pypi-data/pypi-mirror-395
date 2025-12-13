"""指标注册表

管理所有已注册的指标

v3.10.0 新增 - P2.3 Prometheus监控
"""

from __future__ import annotations

import threading
from typing import Any

from .types import Counter, Gauge, Histogram, MetricWrapper, Summary


class MetricsRegistry:
    """指标注册表

    集中管理所有指标，提供注册、查询和导出功能

    使用示例:
        >>> registry = MetricsRegistry()
        >>> counter = registry.counter("requests_total", "Total requests")
        >>> gauge = registry.gauge("active_users", "Active users")
        >>>
        >>> # 获取已注册指标
        >>> counter = registry.get("requests_total")
        >>>
        >>> # 导出所有指标
        >>> metrics = registry.collect()
    """

    def __init__(self, use_prometheus: bool = False):
        """初始化注册表

        Args:
            use_prometheus: 是否使用prometheus_client库
        """
        self._metrics: dict[str, MetricWrapper] = {}
        self._lock = threading.Lock()
        self._use_prometheus = use_prometheus
        self._prometheus_registry = None

        if use_prometheus:
            try:
                from prometheus_client import CollectorRegistry

                self._prometheus_registry = CollectorRegistry()
            except ImportError:
                self._use_prometheus = False

    def counter(self, name: str, description: str, labels: list[str] | None = None) -> Counter:
        """创建或获取计数器

        Args:
            name: 指标名称
            description: 指标描述
            labels: 标签名列表

        Returns:
            Counter实例
        """
        labels = labels or []

        with self._lock:
            if name in self._metrics:
                return self._metrics[name]  # type: ignore

            if self._use_prometheus:
                from prometheus_client import Counter as PromCounter

                prom_counter = PromCounter(
                    name, description, labels, registry=self._prometheus_registry
                )
                counter = Counter(
                    name=name, description=description, label_names=labels, _metric=prom_counter
                )
            else:
                counter = Counter(name=name, description=description, label_names=labels)

            self._metrics[name] = counter
            return counter

    def gauge(self, name: str, description: str, labels: list[str] | None = None) -> Gauge:
        """创建或获取仪表盘

        Args:
            name: 指标名称
            description: 指标描述
            labels: 标签名列表

        Returns:
            Gauge实例
        """
        labels = labels or []

        with self._lock:
            if name in self._metrics:
                return self._metrics[name]  # type: ignore

            if self._use_prometheus:
                from prometheus_client import Gauge as PromGauge

                prom_gauge = PromGauge(
                    name, description, labels, registry=self._prometheus_registry
                )
                gauge = Gauge(
                    name=name, description=description, label_names=labels, _metric=prom_gauge
                )
            else:
                gauge = Gauge(name=name, description=description, label_names=labels)

            self._metrics[name] = gauge
            return gauge

    def histogram(
        self,
        name: str,
        description: str,
        labels: list[str] | None = None,
        buckets: tuple[float, ...] | None = None,
    ) -> Histogram:
        """创建或获取直方图

        Args:
            name: 指标名称
            description: 指标描述
            labels: 标签名列表
            buckets: 桶边界

        Returns:
            Histogram实例
        """
        labels = labels or []
        default_buckets = (
            0.005,
            0.01,
            0.025,
            0.05,
            0.075,
            0.1,
            0.25,
            0.5,
            0.75,
            1.0,
            2.5,
            5.0,
            7.5,
            10.0,
            float("inf"),
        )
        buckets = buckets or default_buckets

        with self._lock:
            if name in self._metrics:
                return self._metrics[name]  # type: ignore

            if self._use_prometheus:
                from prometheus_client import Histogram as PromHistogram

                prom_histogram = PromHistogram(
                    name, description, labels, buckets=buckets, registry=self._prometheus_registry
                )
                histogram = Histogram(
                    name=name,
                    description=description,
                    label_names=labels,
                    buckets=buckets,
                    _metric=prom_histogram,
                )
            else:
                histogram = Histogram(
                    name=name, description=description, label_names=labels, buckets=buckets
                )

            self._metrics[name] = histogram
            return histogram

    def summary(self, name: str, description: str, labels: list[str] | None = None) -> Summary:
        """创建或获取摘要

        Args:
            name: 指标名称
            description: 指标描述
            labels: 标签名列表

        Returns:
            Summary实例
        """
        labels = labels or []

        with self._lock:
            if name in self._metrics:
                return self._metrics[name]  # type: ignore

            if self._use_prometheus:
                from prometheus_client import Summary as PromSummary

                prom_summary = PromSummary(
                    name, description, labels, registry=self._prometheus_registry
                )
                summary = Summary(
                    name=name, description=description, label_names=labels, _metric=prom_summary
                )
            else:
                summary = Summary(name=name, description=description, label_names=labels)

            self._metrics[name] = summary
            return summary

    def get(self, name: str) -> MetricWrapper | None:
        """获取已注册的指标

        Args:
            name: 指标名称

        Returns:
            指标实例，不存在则返回None
        """
        with self._lock:
            return self._metrics.get(name)

    def unregister(self, name: str) -> bool:
        """取消注册指标

        Args:
            name: 指标名称

        Returns:
            是否成功取消注册
        """
        with self._lock:
            if name in self._metrics:
                metric = self._metrics.pop(name)

                # 从prometheus注册表中移除
                if self._use_prometheus and metric._metric is not None:
                    try:
                        self._prometheus_registry.unregister(metric._metric)
                    except Exception:
                        pass

                return True
            return False

    def clear(self) -> None:
        """清除所有指标"""
        with self._lock:
            self._metrics.clear()

            if self._use_prometheus and self._prometheus_registry:
                # 重新创建注册表
                from prometheus_client import CollectorRegistry

                self._prometheus_registry = CollectorRegistry()

    def collect(self) -> dict[str, Any]:
        """收集所有指标

        Returns:
            指标名称到值的映射
        """
        result = {}

        with self._lock:
            for name, metric in self._metrics.items():
                if isinstance(metric, Counter):
                    result[name] = {
                        "type": "counter",
                        "description": metric.description,
                        "value": metric.get() if not metric.label_names else "labeled",
                    }
                elif isinstance(metric, Gauge):
                    result[name] = {
                        "type": "gauge",
                        "description": metric.description,
                        "value": metric.get() if not metric.label_names else "labeled",
                    }
                elif isinstance(metric, Histogram):
                    result[name] = {
                        "type": "histogram",
                        "description": metric.description,
                        "count": metric.get_sample_count() if not metric.label_names else "labeled",
                        "sum": metric.get_sample_sum() if not metric.label_names else "labeled",
                    }
                elif isinstance(metric, Summary):
                    result[name] = {
                        "type": "summary",
                        "description": metric.description,
                        "count": metric.get_sample_count() if not metric.label_names else "labeled",
                    }

        return result

    def list_metrics(self) -> list[str]:
        """列出所有指标名称

        Returns:
            指标名称列表
        """
        with self._lock:
            return list(self._metrics.keys())

    @property
    def prometheus_registry(self):
        """获取prometheus注册表"""
        return self._prometheus_registry


__all__ = ["MetricsRegistry"]
