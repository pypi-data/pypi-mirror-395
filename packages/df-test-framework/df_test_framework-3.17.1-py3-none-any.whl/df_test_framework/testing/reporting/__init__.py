"""测试报告模块

提供测试报告生成和可视化功能：
- Allure 测试报告集成
- 未来可扩展其他报告格式（HTML、JUnit 等）
"""

from . import allure

__all__ = ["allure"]
