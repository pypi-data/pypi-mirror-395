"""
监控扩展示例

演示如何创建API性能监控和数据库慢查询监控扩展。
与docs/user-guide/extensions.md中的内置监控扩展对应。
"""

import time
from datetime import datetime

from pydantic import Field

from df_test_framework import Bootstrap, FrameworkSettings, hookimpl
from df_test_framework.infrastructure.providers import SingletonProvider


class APIPerformanceTracker:
    """API性能追踪器"""

    def __init__(self, slow_threshold_ms: int = 500):
        """
        初始化性能追踪器

        Args:
            slow_threshold_ms: 慢请求阈值（毫秒）
        """
        self.slow_threshold_ms = slow_threshold_ms
        self.stats: dict[str, list[float]] = {}
        self.current_request = {}

    def start_tracking(self, name: str):
        """开始追踪"""
        self.current_request[name] = time.time()
        print(f"⏱️  [监控] 开始追踪: {name}")

    def end_tracking(self, name: str) -> float:
        """结束追踪并返回耗时"""
        if name not in self.current_request:
            return 0

        start_time = self.current_request.pop(name)
        elapsed_ms = (time.time() - start_time) * 1000

        # 记录统计
        if name not in self.stats:
            self.stats[name] = []
        self.stats[name].append(elapsed_ms)

        # 判断是否为慢请求
        if elapsed_ms > self.slow_threshold_ms:
            print(f"⚠️  [监控] {name} 耗时: {elapsed_ms:.2f}ms ⚠️ (超过阈值{self.slow_threshold_ms}ms)")
        else:
            print(f"✅ [监控] {name} 耗时: {elapsed_ms:.2f}ms")

        return elapsed_ms

    def get_stats(self) -> dict[str, dict[str, float]]:
        """获取统计信息"""
        result = {}
        for name, times in self.stats.items():
            result[name] = {
                "count": len(times),
                "total_ms": sum(times),
                "avg_ms": sum(times) / len(times),
                "min_ms": min(times),
                "max_ms": max(times),
            }
        return result

    def print_stats(self):
        """打印统计报告"""
        print("\n" + "=" * 70)
        print("📊 性能统计报告")
        print("=" * 70)

        stats = self.get_stats()
        if not stats:
            print("暂无统计数据")
            return

        for name, stat in stats.items():
            print(f"\n📌 {name}")
            print(f"   调用次数: {stat['count']}")
            print(f"   平均耗时: {stat['avg_ms']:.2f}ms")
            print(f"   最小耗时: {stat['min_ms']:.2f}ms")
            print(f"   最大耗时: {stat['max_ms']:.2f}ms")
            print(f"   总耗时:   {stat['total_ms']:.2f}ms")

        print("=" * 70)


class DatabaseMonitor:
    """数据库慢查询监控"""

    def __init__(self, slow_query_threshold_ms: int = 100):
        """
        初始化数据库监控

        Args:
            slow_query_threshold_ms: 慢查询阈值（毫秒）
        """
        self.slow_query_threshold_ms = slow_query_threshold_ms
        self.query_start_time = None
        self.slow_queries: list[dict] = []

    def before_query(self, sql: str):
        """查询前记录时间"""
        self.query_start_time = time.time()
        print(f"🔍 [DB监控] 执行查询: {sql[:50]}...")

    def after_query(self, sql: str, result_count: int = 0):
        """查询后检查耗时"""
        if not self.query_start_time:
            return

        elapsed_ms = (time.time() - self.query_start_time) * 1000
        self.query_start_time = None

        if elapsed_ms > self.slow_query_threshold_ms:
            slow_query = {
                "sql": sql,
                "elapsed_ms": elapsed_ms,
                "result_count": result_count,
                "timestamp": datetime.now().isoformat(),
            }
            self.slow_queries.append(slow_query)
            print(f"⚠️  [DB监控] 慢查询检测: {elapsed_ms:.2f}ms (阈值{self.slow_query_threshold_ms}ms)")
            print(f"   SQL: {sql[:100]}...")
        else:
            print(f"✅ [DB监控] 查询完成: {elapsed_ms:.2f}ms, 结果数: {result_count}")

    def print_slow_queries(self):
        """打印慢查询报告"""
        if not self.slow_queries:
            print("\n✅ 未检测到慢查询")
            return

        print("\n" + "=" * 70)
        print(f"⚠️  慢查询报告 (阈值: {self.slow_query_threshold_ms}ms)")
        print("=" * 70)

        for i, query in enumerate(self.slow_queries, 1):
            print(f"\n{i}. 耗时: {query['elapsed_ms']:.2f}ms")
            print(f"   时间: {query['timestamp']}")
            print(f"   SQL: {query['sql'][:100]}...")
            print(f"   结果数: {query['result_count']}")

        print("=" * 70)


# 监控扩展类
class MonitoringExtension:
    """监控扩展 - 集成API性能追踪和数据库监控"""

    def __init__(self, slow_api_threshold_ms: int = 500, slow_query_threshold_ms: int = 100):
        self.api_tracker = APIPerformanceTracker(slow_api_threshold_ms)
        self.db_monitor = DatabaseMonitor(slow_query_threshold_ms)

    @hookimpl
    def df_providers(self, settings, logger):
        """注册监控Provider"""
        return {
            "api_performance_tracker": SingletonProvider(lambda ctx: self.api_tracker),
            "db_monitor": SingletonProvider(lambda ctx: self.db_monitor),
        }

    @hookimpl
    def df_post_bootstrap(self, runtime):
        """Bootstrap完成后打印信息"""
        runtime.logger.info("✅ 监控扩展已加载")
        runtime.logger.info(f"   API慢请求阈值: {self.api_tracker.slow_threshold_ms}ms")
        runtime.logger.info(f"   数据库慢查询阈值: {self.db_monitor.slow_query_threshold_ms}ms")


# 配置类
class Settings(FrameworkSettings):
    """示例配置"""
    api_base_url: str = Field(default="https://jsonplaceholder.typicode.com")


# ================== 示例代码 ==================

def example_api_performance_tracking():
    """示例1: API性能追踪"""
    print("\n" + "=" * 70)
    print("示例1: API性能追踪")
    print("=" * 70)

    # 创建监控扩展
    monitoring = MonitoringExtension(slow_api_threshold_ms=200)

    # 启动应用
    app = Bootstrap().with_settings(Settings).with_extensions([monitoring]).build()
    runtime = app.run()

    # 获取追踪器
    tracker = runtime.get("api_performance_tracker")
    http = runtime.http_client()

    # 执行多个API调用
    print("\n📡 执行API调用...")

    # 第一个请求
    tracker.start_tracking("获取用户信息")
    try:
        response = http.get("/users/1")
        print(f"   用户: {response.json().get('name')}")
    except Exception as e:
        print(f"   错误: {e}")
    finally:
        tracker.end_tracking("获取用户信息")

    # 第二个请求
    tracker.start_tracking("获取用户列表")
    try:
        response = http.get("/users")
        print(f"   用户数: {len(response.json())}")
    except Exception as e:
        print(f"   错误: {e}")
    finally:
        tracker.end_tracking("获取用户列表")

    # 第三个请求
    tracker.start_tracking("获取帖子")
    try:
        response = http.get("/posts/1")
        print(f"   标题: {response.json().get('title')[:30]}...")
    except Exception as e:
        print(f"   错误: {e}")
    finally:
        tracker.end_tracking("获取帖子")

    # 打印统计报告
    tracker.print_stats()


def example_database_monitoring():
    """示例2: 数据库慢查询监控"""
    print("\n" + "=" * 70)
    print("示例2: 数据库慢查询监控（模拟）")
    print("=" * 70)

    monitoring = MonitoringExtension(slow_query_threshold_ms=50)
    app = Bootstrap().with_settings(Settings).with_extensions([monitoring]).build()
    runtime = app.run()

    db_monitor = runtime.get("db_monitor")

    # 模拟数据库查询
    print("\n🔍 模拟数据库查询...")

    # 快速查询
    sql1 = "SELECT * FROM users WHERE id = 1"
    db_monitor.before_query(sql1)
    time.sleep(0.02)  # 模拟20ms查询
    db_monitor.after_query(sql1, result_count=1)

    # 慢查询1
    sql2 = "SELECT * FROM orders WHERE created_at > '2024-01-01' ORDER BY id DESC"
    db_monitor.before_query(sql2)
    time.sleep(0.08)  # 模拟80ms查询
    db_monitor.after_query(sql2, result_count=1000)

    # 慢查询2
    sql3 = "SELECT o.*, u.name FROM orders o JOIN users u ON o.user_id = u.id"
    db_monitor.before_query(sql3)
    time.sleep(0.12)  # 模拟120ms查询
    db_monitor.after_query(sql3, result_count=500)

    # 打印慢查询报告
    db_monitor.print_slow_queries()


def example_combined_monitoring():
    """示例3: 综合监控"""
    print("\n" + "=" * 70)
    print("示例3: API + 数据库综合监控")
    print("=" * 70)

    monitoring = MonitoringExtension(
        slow_api_threshold_ms=300,
        slow_query_threshold_ms=50
    )

    app = Bootstrap().with_settings(Settings).with_extensions([monitoring]).build()
    runtime = app.run()

    api_tracker = runtime.get("api_performance_tracker")
    db_monitor = runtime.get("db_monitor")
    http = runtime.http_client()

    print("\n🚀 执行业务流程...")

    # 业务流程：获取用户 + 查询数据库
    with api_tracker:
        api_tracker.start_tracking("业务流程:用户订单查询")

        # 1. 调用API获取用户
        print("\n📡 步骤1: 获取用户信息")
        try:
            response = http.get("/users/1")
            user_name = response.json().get('name')
            print(f"   ✓ 用户: {user_name}")
        except Exception as e:
            print(f"   ✗ 错误: {e}")

        # 2. 模拟查询数据库
        print("\n🔍 步骤2: 查询用户订单")
        sql = "SELECT * FROM orders WHERE user_id = 1"
        db_monitor.before_query(sql)
        time.sleep(0.06)  # 模拟60ms查询
        db_monitor.after_query(sql, result_count=5)
        print("   ✓ 订单数: 5")

        api_tracker.end_tracking("业务流程:用户订单查询")

    # 打印综合报告
    print("\n" + "=" * 70)
    print("📊 综合监控报告")
    print("=" * 70)
    api_tracker.print_stats()
    db_monitor.print_slow_queries()


if __name__ == "__main__":
    print("\n🔍 监控扩展示例")
    print("=" * 70)
    print("演示如何使用监控扩展进行性能追踪和慢查询检测")
    print("=" * 70)

    # 运行示例
    example_api_performance_tracking()
    example_database_monitoring()
    example_combined_monitoring()

    print("\n" + "=" * 70)
    print("✅ 所有示例执行完成!")
    print("=" * 70)
    print("\n💡 使用建议:")
    print("  1. 根据项目调整慢请求/慢查询阈值")
    print("  2. 在测试结束后查看性能统计报告")
    print("  3. 结合Allure报告查看性能趋势")
    print("  4. 对慢请求/慢查询进行优化")
