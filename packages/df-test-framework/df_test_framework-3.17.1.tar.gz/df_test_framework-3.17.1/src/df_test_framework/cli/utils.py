"""CLI工具函数

提供命令行工具的通用工具函数，包括字符串转换、文件操作等。
"""

from __future__ import annotations

from pathlib import Path


def to_snake_case(name: str) -> str:
    """将项目名转换为snake_case

    支持多种输入格式：
    - 横杠分隔: my-test-project -> my_test_project
    - 空格分隔: my test project -> my_test_project
    - 驼峰命名: MyTestProject -> my_test_project
    - 已经是蛇形: my_test_project -> my_test_project

    Args:
        name: 项目名

    Returns:
        snake_case名称

    Example:
        >>> to_snake_case("my-test-project")
        'my_test_project'
        >>> to_snake_case("MyTestProject")
        'my_test_project'
        >>> to_snake_case("UserLogin")
        'user_login'
    """
    import re

    # 首先处理横杠和空格
    name = name.replace("-", "_").replace(" ", "_")

    # 处理驼峰命名：在大写字母前插入下划线
    # UserLogin -> User_Login -> user_login
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)

    # 处理连续大写字母的情况
    # HTTPClient -> HTTP_Client -> http_client
    name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)

    # 转小写并去除多余的下划线
    return re.sub(r"_+", "_", name).lower().strip("_")


def to_pascal_case(name: str) -> str:
    """将项目名转换为PascalCase

    支持多种输入格式：
    - 横杠分隔: my-test-project -> MyTestProject
    - 下划线分隔: my_test_project -> MyTestProject
    - 驼峰命名: UserLogin -> UserLogin (保持不变)
    - 空格分隔: my test project -> MyTestProject

    Args:
        name: 项目名

    Returns:
        PascalCase名称

    Example:
        >>> to_pascal_case("my-test-project")
        'MyTestProject'
        >>> to_pascal_case("gift_card_test")
        'GiftCardTest'
        >>> to_pascal_case("UserLogin")
        'UserLogin'
    """
    # 先转为蛇形，然后再转为Pascal（确保一致性）
    snake = to_snake_case(name)
    return "".join(word.capitalize() for word in snake.split("_") if word)


def create_file(file_path: Path, content: str, *, force: bool = False) -> None:
    """创建文件

    Args:
        file_path: 文件路径
        content: 文件内容
        force: 是否强制覆盖

    Raises:
        FileExistsError: 文件已存在且force=False
    """
    if file_path.exists() and not force:
        raise FileExistsError(f"{file_path} already exists. Use --force to overwrite.")

    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")


def replace_template_vars(template: str, replacements: dict[str, str]) -> str:
    """替换模板中的变量

    Args:
        template: 模板字符串
        replacements: 变量替换字典

    Returns:
        替换后的字符串

    Example:
        >>> replace_template_vars("Hello {name}!", {"name": "World"})
        'Hello World!'
    """
    result = template
    for key, value in replacements.items():
        result = result.replace(key, value)
    return result


def detect_project_name() -> str:
    """检测当前项目名称

    从当前工作目录的pyproject.toml或setup.py中检测项目名称。
    如果无法检测，返回当前目录名。

    Returns:
        项目名称
    """
    cwd = Path.cwd()

    # 尝试从pyproject.toml读取
    pyproject_file = cwd / "pyproject.toml"
    if pyproject_file.exists():
        content = pyproject_file.read_text(encoding="utf-8")
        for line in content.splitlines():
            if line.strip().startswith("name"):
                # name = "project-name"
                parts = line.split("=", 1)
                if len(parts) == 2:
                    name = parts[1].strip().strip('"').strip("'")
                    return name

    # 回退到目录名
    return cwd.name


__all__ = [
    "to_pascal_case",
    "to_snake_case",
    "create_file",
    "replace_template_vars",
    "detect_project_name",
]
