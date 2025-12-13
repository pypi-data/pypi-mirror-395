"""弹性工具模块 - 熔断器实现

本模块提供熔断器(Circuit Breaker)模式实现，用于防止级联失败和系统雪崩。

熔断器状态机:
    CLOSED (关闭) -> OPEN (打开) -> HALF_OPEN (半开) -> CLOSED

    - CLOSED: 正常状态，所有请求正常执行
    - OPEN: 熔断状态，所有请求直接失败，不执行
    - HALF_OPEN: 尝试恢复状态，允许少量请求尝试

典型使用场景:
    1. HTTP API调用 - 防止外部服务故障导致雪崩
    2. 数据库查询 - 数据库超时时快速失败
    3. 第三方服务调用 - 限制失败重试

示例:
    基础使用::

        from df_test_framework.utils.resilience import CircuitBreaker

        breaker = CircuitBreaker(failure_threshold=3, timeout=60)

        try:
            result = breaker.call(external_api_call)
        except CircuitOpenError:
            # 熔断器已打开，使用降级方案
            result = get_cached_data()

    装饰器使用::

        from df_test_framework.utils.resilience import circuit_breaker

        @circuit_breaker(failure_threshold=5, timeout=30)
        def call_payment_api():
            response = requests.post("/payment", json=data)
            response.raise_for_status()
            return response.json()

版本: v3.7.0
作者: DF Framework Team
"""

import functools
import threading
from collections.abc import Callable
from datetime import datetime, timedelta
from enum import Enum
from typing import Any


class CircuitState(Enum):
    """熔断器状态枚举

    Attributes:
        CLOSED: 关闭状态(正常运行)
        OPEN: 打开状态(熔断中，拒绝所有请求)
        HALF_OPEN: 半开状态(尝试恢复，允许少量测试请求)
    """

    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitOpenError(Exception):
    """熔断器打开异常

    当熔断器处于OPEN状态时，调用被保护的函数会抛出此异常。

    使用示例::

        try:
            breaker.call(risky_function)
        except CircuitOpenError as e:
            logger.warning(f"服务熔断: {e}")
            return fallback_response()
    """

    pass


class CircuitBreaker:
    """熔断器: 防止级联失败，提升系统韧性

    熔断器会监控被保护函数的执行情况:
    - 连续失败达到阈值 -> 打开熔断器 (OPEN)
    - 熔断超时后 -> 尝试半开状态 (HALF_OPEN)
    - 半开状态成功 -> 恢复正常 (CLOSED)

    Attributes:
        failure_threshold: 失败阈值，连续失败N次后触发熔断
        success_threshold: 成功阈值，半开状态连续成功N次后恢复
        timeout: 熔断超时时间(秒)，超时后尝试半开
        exception_whitelist: 白名单异常元组，这些异常不计入失败

    状态变量:
        state: 当前状态 (CLOSED/OPEN/HALF_OPEN)
        failure_count: 连续失败计数
        success_count: 半开状态下的成功计数
        last_failure_time: 最后一次失败时间

    线程安全:
        使用 threading.Lock 保证线程安全

    示例::

        # 创建熔断器: 失败3次触发，60秒后尝试恢复
        breaker = CircuitBreaker(
            failure_threshold=3,
            success_threshold=2,
            timeout=60,
            exception_whitelist=(ValueError, KeyError)
        )

        # 保护API调用
        try:
            response = breaker.call(requests.get, "https://api.example.com/data")
            return response.json()
        except CircuitOpenError:
            # 熔断器打开，使用缓存数据
            return get_cached_data()
        except Exception as e:
            # 其他异常正常处理
            logger.error(f"API调用失败: {e}")
            raise
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        success_threshold: int = 2,
        timeout: int = 60,
        exception_whitelist: tuple[type[Exception], ...] | None = None,
    ):
        """初始化熔断器

        Args:
            failure_threshold: 失败阈值，默认5次
            success_threshold: 成功阈值(半开->关闭)，默认2次
            timeout: 熔断超时时间(秒)，默认60秒
            exception_whitelist: 白名单异常元组，这些异常不计入失败

        Raises:
            ValueError: 如果阈值参数无效

        示例::

            # 严格模式: 失败2次就熔断，10秒后恢复
            strict_breaker = CircuitBreaker(
                failure_threshold=2,
                timeout=10
            )

            # 宽松模式: 失败10次才熔断，120秒后恢复
            lenient_breaker = CircuitBreaker(
                failure_threshold=10,
                timeout=120
            )

            # 忽略特定异常
            breaker = CircuitBreaker(
                exception_whitelist=(ValueError, TypeError)
            )
        """
        if failure_threshold <= 0:
            raise ValueError(f"failure_threshold必须大于0, 当前值: {failure_threshold}")
        if success_threshold <= 0:
            raise ValueError(f"success_threshold必须大于0, 当前值: {success_threshold}")
        if timeout <= 0:
            raise ValueError(f"timeout必须大于0, 当前值: {timeout}")

        self.failure_threshold = failure_threshold
        self.success_threshold = success_threshold
        self.timeout = timeout
        self.exception_whitelist = exception_whitelist or ()

        # 状态变量
        self.failure_count = 0
        self.success_count = 0
        self.state = CircuitState.CLOSED
        self.last_failure_time: datetime | None = None

        # 线程锁
        self._lock = threading.Lock()

    def call(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """调用被保护的函数

        根据熔断器状态决定是否执行函数:
        - CLOSED: 正常执行
        - OPEN: 检查超时，如果超时则转为HALF_OPEN，否则抛出CircuitOpenError
        - HALF_OPEN: 执行测试请求

        Args:
            func: 被保护的函数
            *args: 函数位置参数
            **kwargs: 函数关键字参数

        Returns:
            函数执行结果

        Raises:
            CircuitOpenError: 熔断器处于OPEN状态且未超时
            Exception: 被保护函数抛出的异常

        示例::

            # 方式1: 直接调用
            result = breaker.call(requests.get, "https://api.example.com")

            # 方式2: 使用lambda
            result = breaker.call(lambda: complex_operation(a, b, c))

            # 方式3: 带参数调用
            result = breaker.call(
                requests.post,
                "https://api.example.com",
                json={"key": "value"},
                timeout=10
            )
        """
        with self._lock:
            # 检查是否应该从OPEN转为HALF_OPEN
            if self.state == CircuitState.OPEN:
                if self._should_attempt_reset():
                    self.state = CircuitState.HALF_OPEN
                    self.success_count = 0
                else:
                    raise CircuitOpenError(
                        f"熔断器已打开，将在 {self._get_reset_time()} 后尝试恢复"
                    )

        # 执行被保护的函数
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result

        except Exception as e:
            # 白名单异常不计入失败
            if isinstance(e, self.exception_whitelist):
                raise

            self._on_failure()
            raise

    def _on_success(self) -> None:
        """成功回调: 处理函数执行成功的情况

        行为:
        - 清零失败计数
        - HALF_OPEN状态: 增加成功计数，达到阈值后转为CLOSED
        - CLOSED状态: 保持不变
        """
        with self._lock:
            self.failure_count = 0

            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1

                # 连续成功达到阈值，恢复为CLOSED
                if self.success_count >= self.success_threshold:
                    self.state = CircuitState.CLOSED
                    self.success_count = 0

    def _on_failure(self) -> None:
        """失败回调: 处理函数执行失败的情况

        行为:
        - 增加失败计数
        - 记录失败时间
        - HALF_OPEN状态失败 -> 立即重新打开熔断器
        - CLOSED状态失败次数达到阈值 -> 转为OPEN状态
        """
        with self._lock:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            # HALF_OPEN状态下失败，立即重新打开熔断器
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.OPEN
                self.success_count = 0
            # CLOSED状态下失败次数达到阈值，打开熔断器
            elif self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN

    def _should_attempt_reset(self) -> bool:
        """判断是否应该尝试恢复(OPEN -> HALF_OPEN)

        Returns:
            bool: 如果距离最后失败时间超过timeout秒，返回True
        """
        if self.last_failure_time is None:
            return True

        elapsed = datetime.now() - self.last_failure_time
        return elapsed >= timedelta(seconds=self.timeout)

    def _get_reset_time(self) -> str:
        """获取恢复时间描述

        Returns:
            str: 剩余时间描述，如 "30秒"
        """
        if self.last_failure_time is None:
            return "未知"

        reset_time = self.last_failure_time + timedelta(seconds=self.timeout)
        remaining = (reset_time - datetime.now()).total_seconds()

        if remaining <= 0:
            return "即将恢复"

        return f"{int(remaining)}秒"

    def reset(self) -> None:
        """手动重置熔断器到初始状态

        将所有计数器清零，状态恢复为CLOSED。
        用于测试或手动干预场景。

        示例::

            # 手动恢复服务
            if admin_confirms_service_recovered():
                breaker.reset()
                logger.info("熔断器已手动重置")
        """
        with self._lock:
            self.failure_count = 0
            self.success_count = 0
            self.state = CircuitState.CLOSED
            self.last_failure_time = None

    @property
    def is_open(self) -> bool:
        """熔断器是否打开

        Returns:
            bool: True表示熔断器处于OPEN状态
        """
        return self.state == CircuitState.OPEN

    @property
    def is_closed(self) -> bool:
        """熔断器是否关闭(正常状态)

        Returns:
            bool: True表示熔断器处于CLOSED状态
        """
        return self.state == CircuitState.CLOSED

    @property
    def is_half_open(self) -> bool:
        """熔断器是否半开(恢复测试状态)

        Returns:
            bool: True表示熔断器处于HALF_OPEN状态
        """
        return self.state == CircuitState.HALF_OPEN


def circuit_breaker(
    failure_threshold: int = 5,
    success_threshold: int = 2,
    timeout: int = 60,
    exception_whitelist: tuple[type[Exception], ...] | None = None,
) -> Callable:
    """熔断器装饰器

    使用装饰器模式为函数添加熔断保护，使用更简洁。

    注意: 装饰器会为每个被装饰的函数创建独立的熔断器实例。

    Args:
        failure_threshold: 失败阈值，默认5次
        success_threshold: 成功阈值，默认2次
        timeout: 熔断超时时间(秒)，默认60秒
        exception_whitelist: 白名单异常元组

    Returns:
        装饰器函数

    示例::

        # 装饰普通函数
        @circuit_breaker(failure_threshold=3, timeout=30)
        def call_external_api():
            response = requests.get("https://api.example.com/data")
            response.raise_for_status()
            return response.json()

        # 装饰类方法
        class PaymentService:
            @circuit_breaker(failure_threshold=5, timeout=60)
            def charge(self, amount: float):
                return self.payment_gateway.charge(amount)

        # 忽略特定异常
        @circuit_breaker(
            failure_threshold=3,
            exception_whitelist=(ValueError, TypeError)
        )
        def validate_and_process(data):
            if not data:
                raise ValueError("数据为空")  # 不计入失败
            return process(data)

        # 使用
        try:
            result = call_external_api()
        except CircuitOpenError:
            result = get_fallback_data()
    """
    breaker = CircuitBreaker(
        failure_threshold=failure_threshold,
        success_threshold=success_threshold,
        timeout=timeout,
        exception_whitelist=exception_whitelist,
    )

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return breaker.call(func, *args, **kwargs)

        # 将熔断器实例附加到函数上，方便访问状态
        wrapper.breaker = breaker  # type: ignore
        return wrapper

    return decorator


__all__ = [
    "CircuitState",
    "CircuitBreaker",
    "CircuitOpenError",
    "circuit_breaker",
]
