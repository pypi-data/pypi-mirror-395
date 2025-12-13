""".gitignore 文件模板"""

GITIGNORE_TEMPLATE = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# 虚拟环境
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# 测试
.pytest_cache/
.coverage
htmlcov/
reports/

# 环境配置
.env
.env.local

# 日志
*.log
logs/

# OS
.DS_Store
Thumbs.db
"""

__all__ = ["GITIGNORE_TEMPLATE"]
