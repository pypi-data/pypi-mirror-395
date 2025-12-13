"""pytest调试辅助插件

提供测试失败时的自动诊断和环境信息收集。
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest


class DebugPlugin:
    """pytest调试插件

    自动收集测试失败时的环境信息，帮助快速定位问题。

    Features:
        - 测试失败时自动保存环境信息
        - 配置验证
        - 环境变量检查
        - 测试运行前的预检
    """

    def __init__(self):
        self.failures: list = []
        self.debug_dir = Path("reports/debug")
        self.debug_dir.mkdir(parents=True, exist_ok=True)

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        """测试执行后的钩子"""
        outcome = yield
        report = outcome.get_result()

        # 只处理测试执行阶段的失败
        if report.when == "call" and report.failed:
            self._handle_test_failure(item, report, call)

    def _handle_test_failure(self, item, report, call):
        """处理测试失败"""
        failure_info = {
            "test_name": item.nodeid,
            "timestamp": datetime.now().isoformat(),
            "failure_message": str(report.longrepr),
            "environment": self._collect_environment_info(),
            "test_metadata": self._collect_test_metadata(item),
        }

        self.failures.append(failure_info)

        # 保存失败信息到文件
        self._save_failure_info(item.nodeid, failure_info)

        # 打印调试信息
        self._print_debug_info(failure_info)

    def _collect_environment_info(self) -> dict[str, Any]:
        """收集环境信息"""
        return {
            "python_version": sys.version,
            "platform": sys.platform,
            "cwd": os.getcwd(),
            "env_vars": {
                k: v
                for k, v in os.environ.items()
                if k.startswith(("DF_", "PYTEST_", "HTTP_", "DB_", "REDIS_"))
            },
        }

    def _collect_test_metadata(self, item) -> dict[str, Any]:
        """收集测试元数据"""
        return {
            "file": item.location[0],
            "line": item.location[1],
            "function": item.location[2],
            "markers": [m.name for m in item.iter_markers()],
            "fixtures": list(item.fixturenames),
        }

    def _save_failure_info(self, test_name: str, info: dict[str, Any]):
        """保存失败信息到文件"""
        # 生成安全的文件名
        safe_name = test_name.replace("::", "_").replace("/", "_").replace("\\", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"failure_{safe_name}_{timestamp}.json"

        filepath = self.debug_dir / filename

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(info, f, indent=2, ensure_ascii=False)
            print(f"\n💾 调试信息已保存: {filepath}")
        except Exception as e:
            print(f"\n⚠️  保存调试信息失败: {e}")

    def _print_debug_info(self, info: dict[str, Any]):
        """打印调试信息"""
        print("\n" + "=" * 80)
        print("🐛 测试失败调试信息")
        print("=" * 80)
        print(f"测试: {info['test_name']}")
        print(f"时间: {info['timestamp']}")
        print("\n环境:")
        print(f"  Python: {info['environment']['python_version'].split()[0]}")
        print(f"  平台: {info['environment']['platform']}")
        print(f"  工作目录: {info['environment']['cwd']}")

        if info["environment"]["env_vars"]:
            print("\n相关环境变量:")
            for key, value in info["environment"]["env_vars"].items():
                # 脱敏显示
                display_value = value
                if any(
                    sensitive in key.lower() for sensitive in ["password", "secret", "token", "key"]
                ):
                    display_value = "***"
                print(f"  {key}: {display_value}")

        print("=" * 80)

    @pytest.hookimpl(tryfirst=True)
    def pytest_sessionstart(self, session):
        """测试会话开始时的钩子"""
        print("\n🔍 调试插件已启用")
        print(f"   调试信息目录: {self.debug_dir.absolute()}")

    @pytest.hookimpl(trylast=True)
    def pytest_sessionfinish(self, session, exitstatus):
        """测试会话结束时的钩子"""
        if self.failures:
            print("\n" + "=" * 80)
            print(f"📊 测试失败总结: {len(self.failures)} 个失败")
            print("=" * 80)
            for i, failure in enumerate(self.failures, 1):
                print(f"{i}. {failure['test_name']}")
            print("=" * 80)


# pytest插件注册
@pytest.fixture(scope="session")
def debug_plugin():
    """调试插件fixture"""
    return DebugPlugin()


def pytest_configure(config):
    """pytest配置钩子"""
    # 检查是否启用调试模式
    if config.getoption("verbose", 0) >= 2 or os.getenv("DF_DEBUG") == "1":
        config.pluginmanager.register(DebugPlugin(), "df_debug_plugin")


# 添加命令行选项
def pytest_addoption(parser):
    """添加pytest命令行选项"""
    group = parser.getgroup("df-test-framework")
    group.addoption(
        "--df-debug",
        action="store_true",
        default=False,
        help="启用DF测试框架调试模式",
    )
    group.addoption(
        "--df-debug-dir",
        action="store",
        default="reports/debug",
        help="调试信息保存目录",
    )


__all__ = ["DebugPlugin", "debug_plugin"]
