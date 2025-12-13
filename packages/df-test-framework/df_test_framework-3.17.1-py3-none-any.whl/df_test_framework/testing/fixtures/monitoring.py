"""性能监控相关的pytest fixtures

v1.3.0 新增
提供API性能追踪和慢查询监控的fixtures
"""

import json
from collections.abc import Generator

import pytest

try:
    import allure

    ALLURE_AVAILABLE = True
except ImportError:
    ALLURE_AVAILABLE = False

from loguru import logger

from ...extensions.builtin.monitoring import APIPerformanceTracker, SlowQueryMonitor


@pytest.fixture(scope="session")
def api_performance_tracker() -> Generator[APIPerformanceTracker, None, None]:
    """API性能追踪器 (session级别)

    整个测试会话共享,用于统计所有测试的API性能

    使用示例:
        def test_api_performance(master_card_api, api_performance_tracker):
            import time
            start = time.time()

            response = master_card_api.create_cards(request)

            duration_ms = (time.time() - start) * 1000
            api_performance_tracker.record("create_card", duration_ms, success=True)

    Yields:
        APIPerformanceTracker实例

    v1.3.0 新增
    """
    tracker = APIPerformanceTracker(slow_threshold_ms=200)
    logger.info("API性能追踪已启用")

    yield tracker

    # 测试结束后输出统计报告
    logger.info("\n" + tracker.get_report())

    # 如果有Allure,附加到报告
    if ALLURE_AVAILABLE:
        try:
            summary = tracker.get_summary()
            allure.attach(
                json.dumps(summary, indent=2, ensure_ascii=False),
                name="API性能统计",
                attachment_type=allure.attachment_type.JSON,
            )

            slow_calls = tracker.get_slow_calls()
            if slow_calls:
                allure.attach(
                    json.dumps(slow_calls, indent=2, ensure_ascii=False),
                    name="慢调用Top 10",
                    attachment_type=allure.attachment_type.JSON,
                )
        except Exception as e:
            logger.warning(f"附加性能报告到Allure失败: {e}")


@pytest.fixture(scope="function")
def api_tracker() -> Generator[APIPerformanceTracker, None, None]:
    """API性能追踪器 (function级别)

    每个测试独立的追踪器,用于单个测试的性能分析

    使用示例:
        def test_single_api_performance(api_tracker):
            # 测试中记录API调用
            api_tracker.record("api_name", duration_ms=100, success=True)

            # 在测试中获取统计
            summary = api_tracker.get_summary()
            assert summary["api_name"]["平均响应时间(ms)"] < 200

    Yields:
        APIPerformanceTracker实例

    v1.3.0 新增
    """
    tracker = APIPerformanceTracker(slow_threshold_ms=200)

    yield tracker

    # 测试结束后附加到Allure(如果可用)
    if ALLURE_AVAILABLE:
        try:
            summary = tracker.get_summary()
            if summary:
                allure.attach(
                    json.dumps(summary, indent=2, ensure_ascii=False),
                    name="测试性能统计",
                    attachment_type=allure.attachment_type.JSON,
                )
        except Exception as e:
            logger.debug(f"附加性能统计失败: {e}")


@pytest.fixture(scope="session")
def slow_query_monitor() -> Generator[SlowQueryMonitor, None, None]:
    """慢查询监控器 (session级别)

    整个测试会话共享,统计所有慢查询

    注意: 需要配合 db_with_monitoring fixture 使用

    使用示例:
        def test_query_performance(db_with_monitoring, slow_query_monitor):
            # 执行数据库操作
            result = db.query_all("SELECT * FROM table")

            # 检查慢查询
            stats = slow_query_monitor.get_statistics()
            assert stats["慢查询比例(%)"] < 10

    Yields:
        SlowQueryMonitor实例

    v1.3.0 新增
    """
    monitor = SlowQueryMonitor(threshold_ms=100, max_records=1000)
    logger.info("慢查询监控已启用")

    yield monitor

    # 测试结束后输出统计
    stats = monitor.get_statistics()
    logger.info(f"\n慢查询统计: {json.dumps(stats, indent=2, ensure_ascii=False)}")

    slow_queries = monitor.get_slow_queries(limit=20)
    if slow_queries:
        logger.warning(f"\n慢查询Top 20:\n{json.dumps(slow_queries, indent=2, ensure_ascii=False)}")

        # 附加到Allure
        if ALLURE_AVAILABLE:
            try:
                allure.attach(
                    json.dumps(
                        {"统计": stats, "慢查询Top 20": slow_queries},
                        indent=2,
                        ensure_ascii=False,
                    ),
                    name="慢查询报告",
                    attachment_type=allure.attachment_type.JSON,
                )
            except Exception as e:
                logger.warning(f"附加慢查询报告失败: {e}")


# ==================== 数据库监控fixture示例 ====================
#
# 注意: db_with_monitoring 不是一个可用的fixture,而是示例代码
# 原因: 框架不应该包含具体的数据库连接配置
#
# 在测试项目中,你应该这样创建自己的db fixture并启用监控:
#
# @pytest.fixture(scope="session")
# def db(slow_query_monitor):
#     from df_test_framework.core.database import Database
#     from df_test_framework.monitoring import setup_slow_query_logging
#     from config import settings  # 你的项目配置
#
#     database = Database(
#         settings.db_connection_string,  # 你的连接字符串
#         pool_size=settings.db_pool_size,
#         max_overflow=settings.db_max_overflow,
#     )
#
#     # 启用慢查询监控
#     setup_slow_query_logging(database.engine, monitor=slow_query_monitor)
#
#     yield database
#     database.close()
#
# v1.3.0 新增
#
# 更多示例请参考:
# - src/df_test_framework/fixtures/monitoring_examples.py
#
# =============================================================


# ==================== 自动附加性能报告到每个测试 ====================


@pytest.fixture(scope="function", autouse=False)
def auto_attach_performance(request, api_tracker):
    """自动附加性能统计到每个测试的Allure报告

    使用方式1 - 在conftest.py中全局启用:
        pytest_plugins = ["df_test_framework.fixtures.monitoring"]

    使用方式2 - 在单个测试中使用:
        def test_api(auto_attach_performance, api_tracker):
            api_tracker.record("test_api", 100, True)

    v1.3.0 新增
    """
    yield

    # 测试结束后附加性能统计
    if ALLURE_AVAILABLE:
        try:
            summary = api_tracker.get_summary()
            if summary:
                allure.attach(
                    json.dumps(summary, indent=2, ensure_ascii=False),
                    name=f"性能统计 - {request.node.name}",
                    attachment_type=allure.attachment_type.JSON,
                )
        except Exception as e:
            logger.debug(f"自动附加性能统计失败: {e}")
