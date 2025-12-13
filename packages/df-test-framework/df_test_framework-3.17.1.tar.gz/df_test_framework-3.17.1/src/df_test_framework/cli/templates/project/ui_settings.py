"""UI项目配置模板"""

UI_SETTINGS_TEMPLATE = """\"\"\"项目配置 - UI测试项目

基于df-test-framework的UI测试配置。
\"\"\"

from pydantic import Field
from df_test_framework import FrameworkSettings


class {ProjectName}Settings(FrameworkSettings):
    \"\"\"UI测试项目配置

    针对UI测试的配置，包含浏览器设置等。
    \"\"\"

    # UI测试基础URL
    base_url: str = Field(default="https://example.com", description="测试网站基础URL")

    # 浏览器配置
    browser_type: str = Field(default="chromium", description="浏览器类型: chromium/firefox/webkit")
    headless: bool = Field(default=True, description="浏览器无头模式")
    browser_timeout: int = Field(default=30000, description="浏览器超时时间（毫秒）")
    viewport_width: int = Field(default=1280, description="视口宽度")
    viewport_height: int = Field(default=720, description="视口高度")

    # 测试配置
    screenshot_on_failure: bool = Field(default=True, description="失败时自动截图")
    slow_mo: int = Field(default=0, description="操作延迟（毫秒），用于调试")

    # 添加项目特定配置
    # 例如：
    # test_username: str = Field(default="test_user")
    # test_password: str = Field(default="test_pass")


__all__ = ["{ProjectName}Settings"]
"""

__all__ = ["UI_SETTINGS_TEMPLATE"]
