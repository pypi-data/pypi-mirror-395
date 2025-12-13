"""性能监控工具"""

import time
from collections.abc import Callable
from functools import wraps

from loguru import logger

try:
    import allure

    ALLURE_AVAILABLE = True
except ImportError:
    ALLURE_AVAILABLE = False


def track_performance(threshold_ms: float = 1000, log_result: bool = True):
    """
    性能跟踪装饰器

    自动记录函数执行时间,并在超过阈值时发出警告

    Args:
        threshold_ms: 性能阈值(毫秒),超过此值将记录警告
        log_result: 是否记录执行结果

    Returns:
        装饰器函数

    Example:
        @track_performance(threshold_ms=500)
        def test_api_response():
            response = api.get("/users")
            assert response.status_code == 200
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            start_time = time.time()

            try:
                # 执行函数
                result = func(*args, **kwargs)

                # 计算执行时间
                duration_ms = (time.time() - start_time) * 1000

                # 记录性能日志
                if log_result:
                    logger.info(f"[性能] {func_name} 执行时间: {duration_ms:.2f}ms")

                # Allure报告附件
                if ALLURE_AVAILABLE:
                    allure.attach(
                        f"{duration_ms:.2f}ms",
                        name=f"{func_name}_执行时间",
                        attachment_type=allure.attachment_type.TEXT,
                    )

                # 性能警告
                if duration_ms > threshold_ms:
                    logger.warning(
                        f"[性能警告] {func_name} 执行时间 {duration_ms:.2f}ms "
                        f"超过阈值 {threshold_ms}ms"
                    )

                    if ALLURE_AVAILABLE:
                        allure.attach(
                            f"执行时间 {duration_ms:.2f}ms 超过阈值 {threshold_ms}ms",
                            name="性能警告",
                            attachment_type=allure.attachment_type.TEXT,
                        )

                return result

            except Exception as e:
                # 即使出错也记录执行时间
                duration_ms = (time.time() - start_time) * 1000
                logger.error(f"[性能] {func_name} 执行失败 (耗时 {duration_ms:.2f}ms): {str(e)}")
                raise

        return wrapper

    return decorator


class PerformanceTimer:
    """
    性能计时器上下文管理器

    用于测量代码块的执行时间

    Example:
        with PerformanceTimer("数据库查询") as timer:
            result = db.query_all("SELECT * FROM users")

        print(f"查询耗时: {timer.duration_ms}ms")
    """

    def __init__(
        self,
        name: str,
        threshold_ms: float | None = None,
        log_result: bool = True,
    ):
        """
        初始化性能计时器

        Args:
            name: 计时器名称
            threshold_ms: 性能阈值(毫秒),如果设置则超过阈值时记录警告
            log_result: 是否记录结果
        """
        self.name = name
        self.threshold_ms = threshold_ms
        self.log_result = log_result
        self.start_time: float | None = None
        self.end_time: float | None = None
        self.duration_ms: float | None = None

    def __enter__(self):
        """进入上下文"""
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文"""
        self.end_time = time.time()
        self.duration_ms = (self.end_time - self.start_time) * 1000

        if self.log_result:
            logger.info(f"[性能] {self.name} 执行时间: {self.duration_ms:.2f}ms")

        # 性能警告
        if self.threshold_ms and self.duration_ms > self.threshold_ms:
            logger.warning(
                f"[性能警告] {self.name} 执行时间 {self.duration_ms:.2f}ms "
                f"超过阈值 {self.threshold_ms}ms"
            )


class PerformanceCollector:
    """
    性能数据收集器

    用于收集和统计多次操作的性能数据

    Example:
        collector = PerformanceCollector("API请求")

        for i in range(100):
            with collector.measure():
                api.get("/users")

        print(collector.summary())
    """

    def __init__(self, name: str):
        """
        初始化性能收集器

        Args:
            name: 收集器名称
        """
        self.name = name
        self.durations: list[float] = []
        self._current_start: float | None = None

    def measure(self):
        """返回计时上下文管理器"""

        class MeasureContext:
            def __init__(self, collector: "PerformanceCollector"):
                self.collector = collector

            def __enter__(self):
                self.collector._current_start = time.time()
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                if self.collector._current_start:
                    duration = (time.time() - self.collector._current_start) * 1000
                    self.collector.durations.append(duration)
                    self.collector._current_start = None

        return MeasureContext(self)

    def summary(self) -> dict:
        """
        获取性能统计摘要

        Returns:
            包含统计数据的字典
        """
        if not self.durations:
            return {
                "name": self.name,
                "count": 0,
                "total_ms": 0,
                "avg_ms": 0,
                "min_ms": 0,
                "max_ms": 0,
            }

        total = sum(self.durations)
        count = len(self.durations)

        return {
            "name": self.name,
            "count": count,
            "total_ms": round(total, 2),
            "avg_ms": round(total / count, 2),
            "min_ms": round(min(self.durations), 2),
            "max_ms": round(max(self.durations), 2),
        }

    def log_summary(self):
        """记录性能统计摘要到日志"""
        summary = self.summary()
        logger.info(
            f"[性能统计] {summary['name']} - "
            f"次数: {summary['count']}, "
            f"总耗时: {summary['total_ms']}ms, "
            f"平均: {summary['avg_ms']}ms, "
            f"最小: {summary['min_ms']}ms, "
            f"最大: {summary['max_ms']}ms"
        )

    def reset(self):
        """重置收集器"""
        self.durations.clear()


__all__ = ["track_performance", "PerformanceTimer", "PerformanceCollector"]
