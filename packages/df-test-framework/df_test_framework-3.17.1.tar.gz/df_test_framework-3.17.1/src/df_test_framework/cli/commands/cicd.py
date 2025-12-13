"""CI/CD集成辅助模块

提供CI/CD模板文件的复制和生成功能。
"""

from __future__ import annotations

import shutil
from pathlib import Path

# CI/CD模板根目录
CICD_TEMPLATES_DIR = Path(__file__).parent.parent / "templates" / "cicd"


def generate_cicd_files(project_path: Path, ci_platform: str) -> list[Path]:
    """生成CI/CD配置文件

    Args:
        project_path: 项目根目录
        ci_platform: CI平台类型 (github-actions, gitlab-ci, jenkins, all, none)

    Returns:
        生成的文件路径列表

    Raises:
        ValueError: 不支持的CI平台
    """
    generated_files: list[Path] = []

    if ci_platform == "none":
        return generated_files

    # GitHub Actions
    if ci_platform in ("github-actions", "all"):
        github_dir = project_path / ".github" / "workflows"
        github_dir.mkdir(parents=True, exist_ok=True)

        workflows_src = CICD_TEMPLATES_DIR / ".github" / "workflows"
        for workflow_file in workflows_src.glob("*.yml"):
            dest_file = github_dir / workflow_file.name
            shutil.copy2(workflow_file, dest_file)
            generated_files.append(dest_file)

    # GitLab CI
    if ci_platform in ("gitlab-ci", "all"):
        gitlab_ci_src = CICD_TEMPLATES_DIR / ".gitlab-ci.yml"
        gitlab_ci_dest = project_path / ".gitlab-ci.yml"
        shutil.copy2(gitlab_ci_src, gitlab_ci_dest)
        generated_files.append(gitlab_ci_dest)

    # Jenkins
    if ci_platform in ("jenkins", "all"):
        jenkinsfile_src = CICD_TEMPLATES_DIR / "Jenkinsfile"
        jenkinsfile_dest = project_path / "Jenkinsfile"
        shutil.copy2(jenkinsfile_src, jenkinsfile_dest)
        generated_files.append(jenkinsfile_dest)

    # Docker支持（所有非none平台都生成）
    if ci_platform != "none":
        docker_dir = project_path / "docker"
        docker_dir.mkdir(parents=True, exist_ok=True)

        docker_src = CICD_TEMPLATES_DIR / "docker"
        for docker_file in docker_src.iterdir():
            if docker_file.is_file():
                dest_file = docker_dir / docker_file.name
                shutil.copy2(docker_file, dest_file)
                generated_files.append(dest_file)

    return generated_files


def get_supported_platforms() -> list[str]:
    """获取支持的CI平台列表

    Returns:
        支持的平台名称列表
    """
    return ["github-actions", "gitlab-ci", "jenkins", "all", "none"]


def validate_platform(platform: str) -> bool:
    """验证CI平台是否支持

    Args:
        platform: CI平台名称

    Returns:
        是否支持
    """
    return platform in get_supported_platforms()
