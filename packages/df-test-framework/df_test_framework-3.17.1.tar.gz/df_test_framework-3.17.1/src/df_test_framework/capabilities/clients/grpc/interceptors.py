"""gRPC 拦截器

提供请求/响应拦截能力
"""

from __future__ import annotations

import time
from typing import Any

from loguru import logger


class BaseInterceptor:
    """拦截器基类"""

    def intercept_unary(
        self,
        method: str,
        request: Any,
        metadata: list[tuple[str, str]],
    ) -> tuple[Any, list[tuple[str, str]]]:
        """拦截一元调用

        Args:
            method: 方法名
            request: 请求对象
            metadata: 元数据

        Returns:
            (处理后的请求, 处理后的元数据)
        """
        return request, metadata

    def intercept_response(
        self,
        method: str,
        response: Any,
        metadata: dict[str, str],
    ) -> Any:
        """拦截响应

        Args:
            method: 方法名
            response: 响应对象
            metadata: 响应元数据

        Returns:
            处理后的响应
        """
        return response


class LoggingInterceptor(BaseInterceptor):
    """日志拦截器

    记录所有 gRPC 调用的日志
    """

    def __init__(self, log_request: bool = True, log_response: bool = True):
        self.log_request = log_request
        self.log_response = log_response

    def intercept_unary(
        self,
        method: str,
        request: Any,
        metadata: list[tuple[str, str]],
    ) -> tuple[Any, list[tuple[str, str]]]:
        if self.log_request:
            logger.info(f"gRPC Request: {method}")
            logger.debug(f"Request data: {request}")
            logger.debug(f"Metadata: {dict(metadata)}")

        return request, metadata

    def intercept_response(
        self,
        method: str,
        response: Any,
        metadata: dict[str, str],
    ) -> Any:
        if self.log_response:
            logger.info(f"gRPC Response: {method}")
            logger.debug(f"Response data: {response}")
            logger.debug(f"Trailing metadata: {metadata}")

        return response


class MetadataInterceptor(BaseInterceptor):
    """元数据拦截器

    自动添加通用元数据到所有请求
    """

    def __init__(self, metadata: dict[str, str] | None = None):
        self.metadata = metadata or {}

    def add_metadata(self, key: str, value: str) -> None:
        """添加元数据"""
        self.metadata[key] = value

    def remove_metadata(self, key: str) -> None:
        """移除元数据"""
        self.metadata.pop(key, None)

    def intercept_unary(
        self,
        method: str,
        request: Any,
        metadata: list[tuple[str, str]],
    ) -> tuple[Any, list[tuple[str, str]]]:
        # 合并元数据
        combined_metadata = list(metadata)
        for key, value in self.metadata.items():
            combined_metadata.append((key, value))

        return request, combined_metadata


class RetryInterceptor(BaseInterceptor):
    """重试拦截器

    在失败时自动重试
    """

    def __init__(
        self,
        max_retries: int = 3,
        retry_on_codes: list[int] | None = None,
        backoff_multiplier: float = 2.0,
        initial_backoff: float = 0.1,
    ):
        """初始化重试拦截器

        Args:
            max_retries: 最大重试次数
            retry_on_codes: 需要重试的状态码列表
            backoff_multiplier: 退避倍数
            initial_backoff: 初始退避时间（秒）
        """
        self.max_retries = max_retries
        self.retry_on_codes = retry_on_codes or [14]  # UNAVAILABLE
        self.backoff_multiplier = backoff_multiplier
        self.initial_backoff = initial_backoff

    def should_retry(self, error_code: int) -> bool:
        """判断是否应该重试"""
        return error_code in self.retry_on_codes

    def calculate_backoff(self, attempt: int) -> float:
        """计算退避时间"""
        return self.initial_backoff * (self.backoff_multiplier**attempt)


class TimingInterceptor(BaseInterceptor):
    """计时拦截器

    记录每个 RPC 调用的耗时
    """

    def __init__(self):
        self.timings: dict[str, list[float]] = {}

    def intercept_unary(
        self,
        method: str,
        request: Any,
        metadata: list[tuple[str, str]],
    ) -> tuple[Any, list[tuple[str, str]]]:
        # 记录开始时间到元数据中
        start_time = time.time()
        metadata.append(("x-start-time", str(start_time)))

        return request, metadata

    def intercept_response(
        self,
        method: str,
        response: Any,
        metadata: dict[str, str],
    ) -> Any:
        # 从元数据中获取开始时间
        start_time_str = metadata.get("x-start-time")
        if start_time_str:
            start_time = float(start_time_str)
            duration = time.time() - start_time

            # 记录耗时
            if method not in self.timings:
                self.timings[method] = []
            self.timings[method].append(duration)

            logger.info(f"{method} took {duration * 1000:.2f}ms")

        return response

    def get_average_timing(self, method: str) -> float | None:
        """获取方法的平均耗时"""
        if method not in self.timings:
            return None

        timings = self.timings[method]
        return sum(timings) / len(timings) if timings else None

    def get_all_timings(self) -> dict[str, dict[str, float]]:
        """获取所有方法的耗时统计"""
        result = {}
        for method, timings in self.timings.items():
            if not timings:
                continue

            result[method] = {
                "count": len(timings),
                "total": sum(timings),
                "average": sum(timings) / len(timings),
                "min": min(timings),
                "max": max(timings),
            }

        return result
