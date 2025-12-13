"""示例03: 运行时配置覆盖

v3.5.0核心特性：测试隔离和临时配置修改

演示内容:
1. 使用with_overrides()创建临时配置上下文
2. 修改HTTP超时、重试次数等参数
3. 原始配置保持不变（不可变设计）
4. 测试间完全隔离
5. 嵌套覆盖支持
6. 实战场景演示

运行方式:
    python examples/07-v35-features/03_runtime_overrides.py
"""

from typing import Self

from pydantic import model_validator

from df_test_framework import Bootstrap, FrameworkSettings, HTTPConfig
from df_test_framework.infrastructure.config import SignatureInterceptorConfig

# ============================================================
# 准备工作：创建基础Settings
# ============================================================

def _create_http_config() -> HTTPConfig:
    """创建HTTP配置"""
    return HTTPConfig(
        base_url="https://jsonplaceholder.typicode.com",
        timeout=30,  # 默认30秒超时
        max_retries=3,  # 默认重试3次
        interceptors=[
            SignatureInterceptorConfig(
                type="signature",
                enabled=True,
                priority=10,
                algorithm="md5",
                secret="default_secret",
                header_name="X-Sign",
                include_paths=["/**"],
            ),
        ]
    )


class DemoSettings(FrameworkSettings):
    """演示用Settings"""

    @model_validator(mode='after')
    def _setup_interceptors(self) -> Self:
        """设置HTTP拦截器"""
        self.http = _create_http_config()
        return self


# ============================================================
# 示例1: 基础运行时覆盖
# ============================================================

def demo_basic_override():
    """演示基础的运行时配置覆盖"""
    print("\n" + "="*60)
    print("示例1: 基础运行时覆盖")
    print("="*60)

    # 创建原始运行时上下文
    runtime_ctx = (
        Bootstrap()
        .with_settings(DemoSettings)
        .build()
        .run()
    )

    print("\n原始配置:")
    print(f"  HTTP超时: {runtime_ctx.settings.http.timeout}s")
    print(f"  HTTP重试: {runtime_ctx.settings.http.max_retries}次")

    # 创建临时配置上下文（修改超时时间）
    print("\n创建临时配置上下文（超时5秒）...")
    test_ctx = runtime_ctx.with_overrides({
        "http.timeout": 5,
        "http.max_retries": 1,
    })

    print("临时配置:")
    print(f"  HTTP超时: {test_ctx.settings.http.timeout}s")
    print(f"  HTTP重试: {test_ctx.settings.http.max_retries}次")

    # 验证原始配置未改变
    print("\n验证原始配置未改变:")
    print(f"  HTTP超时: {runtime_ctx.settings.http.timeout}s (仍然是30秒)")
    print(f"  HTTP重试: {runtime_ctx.settings.http.max_retries}次 (仍然是3次)")

    print("\n✅ 不可变设计：with_overrides()创建新上下文，不修改原始配置")


# ============================================================
# 示例2: 测试隔离演示
# ============================================================

def demo_test_isolation():
    """演示测试隔离场景"""
    print("\n" + "="*60)
    print("示例2: 测试隔离")
    print("="*60)

    # 创建全局运行时
    runtime_ctx = (
        Bootstrap()
        .with_settings(DemoSettings)
        .build()
        .run()
    )

    print("\n场景: 两个测试需要不同的超时配置\n")

    # 测试1: 快速接口测试（短超时）
    print("测试1: 快速接口测试")
    test1_ctx = runtime_ctx.with_overrides({"http.timeout": 5})
    client1 = test1_ctx.http_client()
    print(f"  超时配置: {test1_ctx.settings.http.timeout}s")

    try:
        response = client1.get("/posts/1", timeout=5)  # 设置短超时
        print(f"  结果: ✅ 成功 (状态码: {response.status_code})")
    except Exception:
        print("  结果: ❌ 超时")

    # 测试2: 慢速接口测试（长超时）
    print("\n测试2: 慢速接口测试")
    test2_ctx = runtime_ctx.with_overrides({"http.timeout": 60})
    client2 = test2_ctx.http_client()
    print(f"  超时配置: {test2_ctx.settings.http.timeout}s")

    try:
        response = client2.get("/posts/1")
        print(f"  结果: ✅ 成功 (状态码: {response.status_code})")
    except Exception:
        print("  结果: ❌ 失败")

    # 验证测试间隔离
    print("\n验证测试间隔离:")
    print(f"  test1超时: {test1_ctx.settings.http.timeout}s")
    print(f"  test2超时: {test2_ctx.settings.http.timeout}s")
    print(f"  原始超时: {runtime_ctx.settings.http.timeout}s")
    print("  ✅ 每个测试都有独立的配置")


# ============================================================
# 示例3: 嵌套覆盖
# ============================================================

def demo_nested_overrides():
    """演示嵌套配置覆盖"""
    print("\n" + "="*60)
    print("示例3: 嵌套覆盖")
    print("="*60)

    # 原始配置
    runtime_ctx = (
        Bootstrap()
        .with_settings(DemoSettings)
        .build()
        .run()
    )

    print("\n原始配置:")
    print(f"  超时: {runtime_ctx.settings.http.timeout}s")
    print(f"  重试: {runtime_ctx.settings.http.max_retries}次")

    # 第一层覆盖
    ctx_level1 = runtime_ctx.with_overrides({"http.timeout": 20})
    print("\n第一层覆盖 (超时20s):")
    print(f"  超时: {ctx_level1.settings.http.timeout}s")
    print(f"  重试: {ctx_level1.settings.http.max_retries}次")

    # 第二层覆盖（基于第一层）
    ctx_level2 = ctx_level1.with_overrides({
        "http.timeout": 10,
        "http.max_retries": 1,
    })
    print("\n第二层覆盖 (基于第一层，超时10s，重试1次):")
    print(f"  超时: {ctx_level2.settings.http.timeout}s")
    print(f"  重试: {ctx_level2.settings.http.max_retries}次")

    # 验证各层独立
    print("\n验证各层配置独立:")
    print(f"  原始:   超时{runtime_ctx.settings.http.timeout}s, 重试{runtime_ctx.settings.http.max_retries}次")
    print(f"  第一层: 超时{ctx_level1.settings.http.timeout}s, 重试{ctx_level1.settings.http.max_retries}次")
    print(f"  第二层: 超时{ctx_level2.settings.http.timeout}s, 重试{ctx_level2.settings.http.max_retries}次")


# ============================================================
# 示例4: 覆盖多个配置项
# ============================================================

def demo_multiple_overrides():
    """演示覆盖多个配置项"""
    print("\n" + "="*60)
    print("示例4: 覆盖多个配置项")
    print("="*60)

    runtime_ctx = (
        Bootstrap()
        .with_settings(DemoSettings)
        .build()
        .run()
    )

    print("\n原始配置:")
    print(f"  HTTP超时: {runtime_ctx.settings.http.timeout}s")
    print(f"  HTTP重试: {runtime_ctx.settings.http.max_retries}次")
    print(f"  HTTP Base URL: {runtime_ctx.settings.http.base_url}")
    print(f"  日志级别: {runtime_ctx.settings.logging.level}")

    # 同时覆盖多个配置项
    test_ctx = runtime_ctx.with_overrides({
        "http.timeout": 10,
        "http.max_retries": 1,
        "http.base_url": "http://localhost:3000",
        "logging.level": "DEBUG",
    })

    print("\n覆盖后配置:")
    print(f"  HTTP超时: {test_ctx.settings.http.timeout}s")
    print(f"  HTTP重试: {test_ctx.settings.http.max_retries}次")
    print(f"  HTTP Base URL: {test_ctx.settings.http.base_url}")
    print(f"  日志级别: {test_ctx.settings.logging.level}")

    print("\n✅ 可以同时覆盖任意多个配置项")


# ============================================================
# 示例5: 实战场景 - 测试不同超时场景
# ============================================================

def demo_timeout_scenarios():
    """实战场景：测试不同超时场景"""
    print("\n" + "="*60)
    print("示例5: 实战场景 - 测试不同超时场景")
    print("="*60)

    runtime_ctx = (
        Bootstrap()
        .with_settings(DemoSettings)
        .build()
        .run()
    )

    # 定义测试场景
    scenarios = [
        {
            "name": "快速API（健康检查）",
            "timeout": 2,
            "endpoint": "/posts/1",
            "description": "健康检查接口，应该在2秒内响应"
        },
        {
            "name": "正常API（业务接口）",
            "timeout": 10,
            "endpoint": "/posts",
            "description": "普通业务接口，10秒超时"
        },
        {
            "name": "慢速API（报表导出）",
            "timeout": 60,
            "endpoint": "/posts?_limit=100",
            "description": "报表导出，允许60秒超时"
        },
    ]

    # 执行各场景测试
    for scenario in scenarios:
        print(f"\n{'='*40}")
        print(f"场景: {scenario['name']}")
        print(f"{'='*40}")
        print(f"说明: {scenario['description']}")
        print(f"超时: {scenario['timeout']}s")
        print(f"接口: {scenario['endpoint']}")

        # 创建场景专用上下文
        scenario_ctx = runtime_ctx.with_overrides({
            "http.timeout": scenario["timeout"]
        })
        client = scenario_ctx.http_client()

        # 发送请求
        try:
            response = client.get(scenario["endpoint"])
            print(f"结果: ✅ 成功 (状态码: {response.status_code})")
        except Exception:
            print("结果: ❌ 超时或失败")

    print("\n✅ 不同场景使用不同的超时配置，互不影响")


# ============================================================
# 示例6: 实战场景 - Mock环境测试
# ============================================================

def demo_mock_environment():
    """实战场景：Mock环境测试"""
    print("\n" + "="*60)
    print("示例6: 实战场景 - Mock环境测试")
    print("="*60)

    # 创建生产环境配置
    runtime_ctx = (
        Bootstrap()
        .with_settings(DemoSettings)
        .build()
        .run()
    )

    print("\n生产环境配置:")
    print(f"  API地址: {runtime_ctx.settings.http.base_url}")

    # 创建Mock环境配置（用于测试）
    print("\n创建Mock环境配置...")
    mock_ctx = runtime_ctx.with_overrides({
        "http.base_url": "http://localhost:3000",
        "http.timeout": 5,  # Mock服务器响应快，短超时即可
        "logging.level": "DEBUG",  # 详细日志便于调试
    })

    print("Mock环境配置:")
    print(f"  API地址: {mock_ctx.settings.http.base_url}")
    print(f"  超时时间: {mock_ctx.settings.http.timeout}s")
    print(f"  日志级别: {mock_ctx.settings.logging.level}")

    print("\n使用场景:")
    print("  1. 本地开发时使用Mock服务器")
    print("  2. CI环境使用Mock服务器加速测试")
    print("  3. 集成测试时隔离外部依赖")

    print("\n✅ 通过with_overrides()轻松切换Mock环境")


# ============================================================
# 示例7: 实战场景 - 并发测试
# ============================================================

def demo_concurrent_tests():
    """实战场景：并发测试配置隔离"""
    print("\n" + "="*60)
    print("示例7: 实战场景 - 并发测试配置隔离")
    print("="*60)

    runtime_ctx = (
        Bootstrap()
        .with_settings(DemoSettings)
        .build()
        .run()
    )

    print("\n场景: pytest -n 4 并发执行测试")
    print("\n并发测试配置需求:")
    print("  - 测试1: 需要5秒超时")
    print("  - 测试2: 需要10秒超时")
    print("  - 测试3: 需要Mock服务器")
    print("  - 测试4: 需要Debug日志")

    # 模拟4个并发测试
    configs = [
        {"http.timeout": 5},
        {"http.timeout": 10},
        {"http.base_url": "http://localhost:3000"},
        {"logging.level": "DEBUG"},
    ]

    print("\n创建4个独立的测试上下文:")
    test_contexts = []
    for i, config in enumerate(configs, 1):
        ctx = runtime_ctx.with_overrides(config)
        test_contexts.append(ctx)
        print(f"  测试{i}上下文: {config}")

    # 验证配置隔离
    print("\n验证配置隔离:")
    for i, ctx in enumerate(test_contexts, 1):
        print(f"  测试{i}: 超时={ctx.settings.http.timeout}s, " +
              f"URL={ctx.settings.http.base_url}, " +
              f"日志={ctx.settings.logging.level}")

    print("\n✅ with_overrides()天然支持并发测试配置隔离")


# ============================================================
# 主函数
# ============================================================

def main():
    """运行所有示例"""
    print("\n" + "🚀 v3.5运行时配置覆盖示例".center(60, "="))

    try:
        # 示例1: 基础运行时覆盖
        demo_basic_override()

        # 示例2: 测试隔离
        demo_test_isolation()

        # 示例3: 嵌套覆盖
        demo_nested_overrides()

        # 示例4: 覆盖多个配置项
        demo_multiple_overrides()

        # 示例5: 实战场景 - 测试不同超时场景
        demo_timeout_scenarios()

        # 示例6: 实战场景 - Mock环境测试
        demo_mock_environment()

        # 示例7: 实战场景 - 并发测试
        demo_concurrent_tests()

        print("\n" + "✅ 所有示例运行完成！".center(60, "="))

        print("\n💡 关键要点:")
        print("  1. with_overrides()创建新上下文，不修改原始配置（不可变设计）")
        print("  2. 支持嵌套覆盖：ctx.with_overrides().with_overrides()")
        print("  3. 可同时覆盖任意多个配置项")
        print("  4. 天然支持并发测试配置隔离")
        print("  5. 覆盖路径使用点号分隔: 'http.timeout'")

        print("\n🎯 适用场景:")
        print("  ✅ 测试不同超时场景")
        print("  ✅ 本地开发使用Mock服务器")
        print("  ✅ 并发测试配置隔离")
        print("  ✅ 临时修改日志级别调试")
        print("  ✅ 集成测试时覆盖配置")

        print("\n⚠️ 使用注意:")
        print("  - 仅在测试中使用，避免在业务代码中滥用")
        print("  - 覆盖值类型要匹配（int不能传str）")
        print("  - 覆盖路径必须存在（不会创建新字段）")
        print("  - 使用返回的新context，不是原始runtime_ctx")

        print("\n📚 下一步:")
        print("  - 查看 04_observability.py 学习可观测性集成")
        print("  - 查看 docs/user-guide/PHASE3_FEATURES.md 了解with_overrides详细用法")
        print("  - 查看 gift-card-test项目的实际使用案例")

    except Exception as e:
        print(f"\n❌ 示例运行失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
