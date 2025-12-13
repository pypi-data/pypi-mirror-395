"""指标类型定义

定义Prometheus兼容的指标类型

v3.10.0 新增 - P2.3 Prometheus监控
"""

from __future__ import annotations

import threading
import time
from abc import ABC, abstractmethod
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any


@dataclass
class MetricWrapper(ABC):
    """指标包装器基类

    提供统一的指标接口，支持有无prometheus_client的情况
    """

    name: str
    description: str
    label_names: list[str] = field(default_factory=list)
    _metric: Any = field(default=None, repr=False)

    @abstractmethod
    def labels(self, **kwargs) -> MetricWrapper:
        """获取带标签的指标实例"""
        pass


@dataclass
class Counter(MetricWrapper):
    """计数器

    只能递增的指标，用于统计事件发生次数

    使用示例:
        >>> counter = Counter("requests_total", "Total requests", ["method"])
        >>> counter.labels(method="GET").inc()
        >>> counter.labels(method="POST").inc(5)
    """

    _values: dict[tuple, float] = field(default_factory=dict, repr=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)
    _current_labels: tuple = field(default=(), repr=False)
    _local_value: float = field(default=0.0, repr=False)  # 本地值副本，用于 Prometheus 指标

    def labels(self, **kwargs: str) -> Counter:
        """获取带标签的计数器实例"""
        if self._metric is not None:
            # 使用真实的prometheus_client
            labeled = Counter(
                name=self.name,
                description=self.description,
                label_names=self.label_names,
                _metric=self._metric.labels(**kwargs),
            )
            return labeled

        # 使用内存存储
        label_values = tuple(kwargs.get(k, "") for k in self.label_names)
        new_counter = Counter(
            name=self.name,
            description=self.description,
            label_names=self.label_names,
            _values=self._values,
            _lock=self._lock,
            _current_labels=label_values,
        )
        return new_counter

    def inc(self, amount: float = 1) -> None:
        """增加计数

        Args:
            amount: 增加量（必须为正数）
        """
        if amount < 0:
            raise ValueError("Counter只能增加，不能减少")

        if self._metric is not None:
            self._metric.inc(amount)
            self._local_value += amount  # 维护本地值副本
            return

        with self._lock:
            current = self._values.get(self._current_labels, 0)
            self._values[self._current_labels] = current + amount

    def get(self) -> float:
        """获取当前值

        注意: 当使用 Prometheus 指标时，返回本地维护的值副本，
        避免依赖 prometheus_client 的私有 API。
        """
        if self._metric is not None:
            return self._local_value

        with self._lock:
            return self._values.get(self._current_labels, 0)


@dataclass
class Gauge(MetricWrapper):
    """仪表盘

    可增可减的指标，用于表示当前状态

    使用示例:
        >>> gauge = Gauge("active_connections", "Active connections")
        >>> gauge.inc()
        >>> gauge.dec()
        >>> gauge.set(10)
    """

    _values: dict[tuple, float] = field(default_factory=dict, repr=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)
    _current_labels: tuple = field(default=(), repr=False)
    _local_value: float = field(default=0.0, repr=False)  # 本地值副本，用于 Prometheus 指标

    def labels(self, **kwargs: str) -> Gauge:
        """获取带标签的仪表盘实例"""
        if self._metric is not None:
            labeled = Gauge(
                name=self.name,
                description=self.description,
                label_names=self.label_names,
                _metric=self._metric.labels(**kwargs),
            )
            return labeled

        label_values = tuple(kwargs.get(k, "") for k in self.label_names)
        new_gauge = Gauge(
            name=self.name,
            description=self.description,
            label_names=self.label_names,
            _values=self._values,
            _lock=self._lock,
            _current_labels=label_values,
        )
        return new_gauge

    def inc(self, amount: float = 1) -> None:
        """增加值"""
        if self._metric is not None:
            self._metric.inc(amount)
            self._local_value += amount  # 维护本地值副本
            return

        with self._lock:
            current = self._values.get(self._current_labels, 0)
            self._values[self._current_labels] = current + amount

    def dec(self, amount: float = 1) -> None:
        """减少值"""
        if self._metric is not None:
            self._metric.dec(amount)
            self._local_value -= amount  # 维护本地值副本
            return

        with self._lock:
            current = self._values.get(self._current_labels, 0)
            self._values[self._current_labels] = current - amount

    def set(self, value: float) -> None:
        """设置值"""
        if self._metric is not None:
            self._metric.set(value)
            self._local_value = value  # 维护本地值副本
            return

        with self._lock:
            self._values[self._current_labels] = value

    def get(self) -> float:
        """获取当前值

        注意: 当使用 Prometheus 指标时，返回本地维护的值副本，
        避免依赖 prometheus_client 的私有 API。
        """
        if self._metric is not None:
            return self._local_value

        with self._lock:
            return self._values.get(self._current_labels, 0)

    @contextmanager
    def track_inprogress(self):
        """追踪进行中的操作

        使用示例:
            >>> with gauge.track_inprogress():
            ...     do_work()
        """
        self.inc()
        try:
            yield
        finally:
            self.dec()


@dataclass
class Histogram(MetricWrapper):
    """直方图

    统计值的分布，自动计算bucket

    使用示例:
        >>> histogram = Histogram("request_duration", "Request duration")
        >>> histogram.observe(0.5)
        >>> with histogram.time():
        ...     do_work()
    """

    buckets: tuple[float, ...] = field(
        default=(
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
    )
    _observations: dict[tuple, list[float]] = field(default_factory=dict, repr=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)
    _current_labels: tuple = field(default=(), repr=False)

    def labels(self, **kwargs) -> Histogram:
        """获取带标签的直方图实例"""
        if self._metric is not None:
            labeled = Histogram(
                name=self.name,
                description=self.description,
                label_names=self.label_names,
                buckets=self.buckets,
                _metric=self._metric.labels(**kwargs),
            )
            return labeled

        label_values = tuple(kwargs.get(k, "") for k in self.label_names)
        new_histogram = Histogram(
            name=self.name,
            description=self.description,
            label_names=self.label_names,
            buckets=self.buckets,
            _observations=self._observations,
            _lock=self._lock,
            _current_labels=label_values,
        )
        return new_histogram

    def observe(self, value: float) -> None:
        """记录观测值

        Args:
            value: 观测值
        """
        if self._metric is not None:
            self._metric.observe(value)
            return

        with self._lock:
            if self._current_labels not in self._observations:
                self._observations[self._current_labels] = []
            self._observations[self._current_labels].append(value)

    @contextmanager
    def time(self):
        """计时上下文管理器

        使用示例:
            >>> with histogram.time():
            ...     do_work()
        """
        start = time.perf_counter()
        try:
            yield
        finally:
            duration = time.perf_counter() - start
            self.observe(duration)

    def get_sample_count(self) -> int:
        """获取样本数量"""
        with self._lock:
            obs = self._observations.get(self._current_labels, [])
            return len(obs)

    def get_sample_sum(self) -> float:
        """获取样本总和"""
        with self._lock:
            obs = self._observations.get(self._current_labels, [])
            return sum(obs)


@dataclass
class Summary(MetricWrapper):
    """摘要

    统计百分位数

    使用示例:
        >>> summary = Summary("request_size", "Request size")
        >>> summary.observe(100)
    """

    _observations: dict[tuple, list[float]] = field(default_factory=dict, repr=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)
    _current_labels: tuple = field(default=(), repr=False)

    def labels(self, **kwargs) -> Summary:
        """获取带标签的摘要实例"""
        if self._metric is not None:
            labeled = Summary(
                name=self.name,
                description=self.description,
                label_names=self.label_names,
                _metric=self._metric.labels(**kwargs),
            )
            return labeled

        label_values = tuple(kwargs.get(k, "") for k in self.label_names)
        new_summary = Summary(
            name=self.name,
            description=self.description,
            label_names=self.label_names,
            _observations=self._observations,
            _lock=self._lock,
            _current_labels=label_values,
        )
        return new_summary

    def observe(self, value: float) -> None:
        """记录观测值"""
        if self._metric is not None:
            self._metric.observe(value)
            return

        with self._lock:
            if self._current_labels not in self._observations:
                self._observations[self._current_labels] = []
            self._observations[self._current_labels].append(value)

    @contextmanager
    def time(self):
        """计时上下文管理器"""
        start = time.perf_counter()
        try:
            yield
        finally:
            duration = time.perf_counter() - start
            self.observe(duration)

    def get_sample_count(self) -> int:
        """获取样本数量"""
        with self._lock:
            obs = self._observations.get(self._current_labels, [])
            return len(obs)


__all__ = [
    "MetricWrapper",
    "Counter",
    "Gauge",
    "Histogram",
    "Summary",
]
