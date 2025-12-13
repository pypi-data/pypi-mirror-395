"""scripts/run_tests.sh 脚本模板"""

SCRIPT_RUN_TESTS_TEMPLATE = """#!/bin/bash
# 测试运行脚本

set -e  # 遇到错误立即退出

echo "🚀 开始运行测试..."

# 解析参数
TEST_TYPE="${1:-all}"  # 默认运行所有测试
MARKER="${2:-}"

case "$TEST_TYPE" in
    api)
        echo "📋 运行API测试..."
        if [ -n "$MARKER" ]; then
            pytest tests/api/ -m "$MARKER" -v
        else
            pytest tests/api/ -v
        fi
        ;;
    ui)
        echo "📋 运行UI测试..."
        if [ -n "$MARKER" ]; then
            pytest tests/ui/ -m "$MARKER" -v
        else
            pytest tests/ui/ -v
        fi
        ;;
    smoke)
        echo "📋 运行冒烟测试..."
        pytest -m smoke -v
        ;;
    all)
        echo "📋 运行所有测试..."
        pytest -v
        ;;
    *)
        echo "❌ 未知的测试类型: $TEST_TYPE"
        echo "用法: ./scripts/run_tests.sh [api|ui|smoke|all] [marker]"
        exit 1
        ;;
esac

echo "✅ 测试完成！"
"""

__all__ = ["SCRIPT_RUN_TESTS_TEMPLATE"]
