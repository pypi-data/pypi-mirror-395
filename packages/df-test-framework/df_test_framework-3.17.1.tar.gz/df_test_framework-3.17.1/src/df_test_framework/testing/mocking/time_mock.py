"""时间Mock支持

基于freezegun的时间Mock功能，用于测试时间敏感逻辑

核心特性:
- 冻结时间：固定在某个时刻
- 时间旅行：前进/后退
- 自定义时间流速
- 支持datetime、time等时间模块

使用场景:
- 测试定时任务
- 测试过期逻辑
- 测试时间戳生成
- 测试时间计算
"""

from __future__ import annotations

import contextlib
from datetime import datetime, timedelta

try:
    from freezegun import freeze_time

    FREEZEGUN_AVAILABLE = True
except ImportError:
    freeze_time = None
    FREEZEGUN_AVAILABLE = False


class TimeMocker:
    """时间Mock工具类

    提供便捷的时间Mock API，基于freezegun

    Features:
    - 冻结时间到指定时刻
    - 时间前进/后退
    - 自动管理freeze_time上下文

    Example:
        >>> @pytest.fixture
        ... def time_mock():
        ...     mocker = TimeMocker()
        ...     yield mocker
        ...     mocker.stop()

        >>> def test_expiration(time_mock):
        ...     # 冻结时间到2024-01-01 12:00:00
        ...     time_mock.freeze("2024-01-01 12:00:00")
        ...
        ...     # 测试代码...
        ...     now = datetime.now()
        ...     assert now.year == 2024
        ...     assert now.month == 1
        ...
        ...     # 时间前进1小时
        ...     time_mock.move_to("2024-01-01 13:00:00")
        ...     now = datetime.now()
        ...     assert now.hour == 13
    """

    def __init__(self):
        """初始化TimeMocker"""
        self._current_freeze = None
        self._ensure_freezegun_available()

    def _ensure_freezegun_available(self):
        """确保freezegun可用

        Raises:
            ImportError: freezegun未安装
        """
        if not FREEZEGUN_AVAILABLE:
            raise ImportError(
                "freezegun is not installed. Please install it: pip install freezegun"
            )

    def freeze(self, time_to_freeze: str | datetime) -> TimeMocker:
        """冻结时间到指定时刻

        Args:
            time_to_freeze: 要冻结到的时间
                - 字符串: "2024-01-01", "2024-01-01 12:00:00"
                - datetime对象

        Returns:
            self，支持链式调用

        Example:
            >>> time_mock.freeze("2024-01-01 12:00:00")
            >>> now = datetime.now()
            >>> assert now.year == 2024
        """
        # 停止之前的freeze
        if self._current_freeze:
            self._current_freeze.stop()

        # 启动新的freeze
        self._current_freeze = freeze_time(time_to_freeze)
        self._current_freeze.start()

        return self

    def move_to(self, time_to_move: str | datetime) -> TimeMocker:
        """移动时间到指定时刻（时间旅行）

        Args:
            time_to_move: 要移动到的时间

        Returns:
            self，支持链式调用

        Example:
            >>> time_mock.freeze("2024-01-01 12:00:00")
            >>> time_mock.move_to("2024-01-02 15:30:00")
        """
        return self.freeze(time_to_move)

    def tick(self, delta: timedelta | None = None, seconds: float | None = None) -> TimeMocker:
        """时间前进（增量）

        Args:
            delta: 时间增量（timedelta对象）
            seconds: 秒数（快捷方式）

        Returns:
            self，支持链式调用

        Example:
            >>> time_mock.freeze("2024-01-01 12:00:00")
            >>> time_mock.tick(seconds=3600)  # 前进1小时
            >>> now = datetime.now()
            >>> assert now.hour == 13

            >>> time_mock.tick(delta=timedelta(days=1))  # 前进1天
        """
        if delta is None and seconds is None:
            raise ValueError("Either delta or seconds must be provided")

        if delta is None:
            delta = timedelta(seconds=seconds)

        if self._current_freeze is None:
            raise RuntimeError("No time is frozen. Call freeze() first.")

        # freezegun的freeze_time对象有tick()方法
        self._current_freeze.tick(delta=delta)
        return self

    def stop(self) -> None:
        """停止时间Mock，恢复真实时间"""
        if self._current_freeze:
            self._current_freeze.stop()
            self._current_freeze = None

    @contextlib.contextmanager
    def freeze_context(self, time_to_freeze: str | datetime):
        """上下文管理器方式冻结时间

        Args:
            time_to_freeze: 要冻结到的时间

        Yields:
            None

        Example:
            >>> with time_mock.freeze_context("2024-01-01"):
            ...     now = datetime.now()
            ...     assert now.year == 2024
            # 退出上下文后自动恢复
        """
        self.freeze(time_to_freeze)
        try:
            yield
        finally:
            self.stop()

    def __enter__(self):
        """上下文管理器入口"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.stop()


# 提供全局函数作为快捷方式


def freeze_time_at(time_to_freeze: str | datetime):
    """快捷函数：冻结时间到指定时刻

    Args:
        time_to_freeze: 要冻结到的时间

    Returns:
        freeze_time上下文管理器

    Example:
        >>> # 装饰器方式
        >>> @freeze_time_at("2024-01-01 12:00:00")
        ... def test_something():
        ...     now = datetime.now()
        ...     assert now.year == 2024

        >>> # 上下文管理器方式
        >>> with freeze_time_at("2024-01-01"):
        ...     now = datetime.now()
        ...     assert now.year == 2024
    """
    if not FREEZEGUN_AVAILABLE:
        raise ImportError("freezegun is not installed. Please install it: pip install freezegun")
    return freeze_time(time_to_freeze)


__all__ = [
    "TimeMocker",
    "freeze_time_at",
    "FREEZEGUN_AVAILABLE",
]
