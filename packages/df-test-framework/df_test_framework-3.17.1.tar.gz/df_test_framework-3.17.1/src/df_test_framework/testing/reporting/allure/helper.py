"""Allure报告辅助工具

提供Allure报告增强功能:
- 自动添加环境信息
- 附加日志文件
- 截图管理
- 自定义标签
"""

import json
import os
from decimal import Decimal
from pathlib import Path
from typing import Any

import allure
from allure_commons.types import AttachmentType
from loguru import logger


class DecimalEncoder(json.JSONEncoder):
    """自定义JSON编码器，支持Decimal和datetime类型"""

    def default(self, obj):
        from datetime import date, datetime

        if isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)


class AllureHelper:
    """Allure报告辅助类"""

    @staticmethod
    def attach_log_file(log_file: str, name: str = "测试日志") -> None:
        """
        附加日志文件到Allure报告

        Args:
            log_file: 日志文件路径
            name: 附件名称
        """
        try:
            if not Path(log_file).exists():
                logger.warning(f"日志文件不存在: {log_file}")
                return

            with open(log_file, encoding="utf-8") as f:
                content = f.read()

            allure.attach(
                content,
                name=name,
                attachment_type=AttachmentType.TEXT,
            )
        except Exception as e:
            logger.error(f"附加日志文件失败: {e}")

    @staticmethod
    def attach_json(data: dict[str, Any], name: str = "JSON数据") -> None:
        """
        附加JSON数据到Allure报告

        Args:
            data: JSON数据
            name: 附件名称

        Note:
            自动处理特殊类型:
            - Decimal → float
            - datetime/date → ISO格式字符串
        """
        try:
            json_str = json.dumps(data, ensure_ascii=False, indent=2, cls=DecimalEncoder)
            allure.attach(
                json_str,
                name=name,
                attachment_type=AttachmentType.JSON,
            )
        except Exception as e:
            logger.error(f"附加JSON数据失败: {e}")

    @staticmethod
    def attach_screenshot(
        screenshot: bytes | str, name: str = "截图", screenshot_type: str = "png"
    ) -> None:
        """
        附加截图到Allure报告

        Args:
            screenshot: 截图数据(字节或文件路径)
            name: 附件名称
            screenshot_type: 截图类型(png/jpg)
        """
        try:
            if isinstance(screenshot, str):
                # 从文件路径读取
                if not Path(screenshot).exists():
                    logger.warning(f"截图文件不存在: {screenshot}")
                    return
                with open(screenshot, "rb") as f:
                    screenshot_data = f.read()
            else:
                screenshot_data = screenshot

            attachment_type = AttachmentType.PNG if screenshot_type == "png" else AttachmentType.JPG

            allure.attach(
                screenshot_data,
                name=name,
                attachment_type=attachment_type,
            )
        except Exception as e:
            logger.error(f"附加截图失败: {e}")

    @staticmethod
    def add_environment_info(env_info: dict[str, str]) -> None:
        """
        添加环境信息到Allure报告

        Args:
            env_info: 环境信息字典

        Example:
            AllureHelper.add_environment_info({
                "环境": "test",
                "Python版本": "3.11",
                "操作系统": "Windows"
            })
        """
        try:
            # 获取Allure结果目录
            allure_results_dir = os.getenv("ALLURE_RESULTS_DIR", "reports/allure-results")
            results_path = Path(allure_results_dir)
            results_path.mkdir(parents=True, exist_ok=True)

            # 写入environment.properties文件
            # 使用 ISO-8859-1 编码（Java Properties 标准），并对中文进行 Unicode 转义
            env_file = results_path / "environment.properties"
            with open(env_file, "w", encoding="utf-8") as f:
                for key, value in env_info.items():
                    # 对中文字符进行 Unicode 转义，确保 Allure 正确显示
                    # 将中文转换为 \uXXXX 格式
                    key_escaped = key.encode("unicode-escape").decode("ascii")
                    value_escaped = value.encode("unicode-escape").decode("ascii")
                    f.write(f"{key_escaped}={value_escaped}\n")

            logger.info(f"环境信息已添加到Allure报告: {env_file}")
        except Exception as e:
            logger.error(f"添加环境信息失败: {e}")

    @staticmethod
    def add_categories(categories: list[dict[str, Any]]) -> None:
        """
        添加自定义分类到Allure报告

        Args:
            categories: 分类配置列表

        Example:
            AllureHelper.add_categories([
                {
                    "name": "API错误",
                    "matchedStatuses": ["failed"],
                    "messageRegex": ".*API.*"
                },
                {
                    "name": "超时错误",
                    "matchedStatuses": ["broken"],
                    "messageRegex": ".*timeout.*"
                }
            ])
        """
        try:
            # 获取Allure结果目录
            allure_results_dir = os.getenv("ALLURE_RESULTS_DIR", "reports/allure-results")
            results_path = Path(allure_results_dir)
            results_path.mkdir(parents=True, exist_ok=True)

            # 写入categories.json文件
            categories_file = results_path / "categories.json"
            with open(categories_file, "w", encoding="utf-8") as f:
                json.dump(categories, f, ensure_ascii=False, indent=2)

            logger.info(f"自定义分类已添加到Allure报告: {categories_file}")
        except Exception as e:
            logger.error(f"添加自定义分类失败: {e}")

    @staticmethod
    def add_step(title: str, description: str | None = None):
        """
        添加测试步骤(装饰器或上下文管理器)

        Args:
            title: 步骤标题
            description: 步骤描述

        Example:
            # 作为装饰器使用
            @AllureHelper.add_step("执行登录操作")
            def login(username, password):
                pass

            # 作为上下文管理器使用
            with AllureHelper.add_step("验证响应"):
                assert response.status_code == 200
        """
        return allure.step(title)

    @staticmethod
    def add_link(url: str, link_type: str = "link", name: str | None = None) -> None:
        """
        添加链接到Allure报告

        Args:
            url: 链接URL
            link_type: 链接类型(link/issue/test_case)
            name: 链接名称
        """
        if link_type == "issue":
            allure.dynamic.link(url, link_type="issue", name=name or url)
        elif link_type == "test_case":
            allure.dynamic.link(url, link_type="test_case", name=name or url)
        else:
            allure.dynamic.link(url, name=name or url)

    @staticmethod
    def add_label(label_type: str, *values: str) -> None:
        """
        添加标签到Allure报告

        Args:
            label_type: 标签类型(feature/story/severity/tag等)
            values: 标签值
        """
        for value in values:
            allure.dynamic.label(label_type, value)

    @staticmethod
    def set_description(description: str, description_type: str = "text") -> None:
        """
        设置测试描述

        Args:
            description: 描述内容
            description_type: 描述类型(text/html/markdown)
        """
        if description_type == "html":
            allure.dynamic.description_html(description)
        else:
            allure.dynamic.description(description)


# 便捷函数
def attach_log(log_file: str, name: str = "测试日志") -> None:
    """附加日志文件"""
    AllureHelper.attach_log_file(log_file, name)


def attach_json(data: dict[str, Any], name: str = "JSON数据") -> None:
    """附加JSON数据"""
    AllureHelper.attach_json(data, name)


def attach_screenshot(screenshot: bytes | str, name: str = "截图") -> None:
    """附加截图"""
    AllureHelper.attach_screenshot(screenshot, name)


def step(title: str):
    """添加测试步骤"""
    return AllureHelper.add_step(title)


__all__ = [
    "AllureHelper",
    "attach_log",
    "attach_json",
    "attach_screenshot",
    "step",
]
