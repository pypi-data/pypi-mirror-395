"""增强的 .gitignore 模板"""

ENHANCED_GITIGNORE_TEMPLATE = """# Python
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
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
Thumbs.db

# 测试
.pytest_cache/
.coverage
htmlcov/
.tox/
.hypothesis/

# 测试报告和产出
reports/**
!reports/.gitkeep
reports/screenshots/
reports/videos/
reports/logs/
reports/allure-results/
allure-report/

# Playwright特有
.playwright/
playwright-report/
test-results/

# 数据库
*.db
*.sqlite
*.sqlite3

# 环境配置
.env
.env.local
.env.*.local

# 日志
*.log
logs/

# 临时文件
*.tmp
*.temp
.cache/

# macOS
.DS_Store
.AppleDouble
.LSOverride

# Windows
Thumbs.db
ehthumbs.db
Desktop.ini
"""

__all__ = ["ENHANCED_GITIGNORE_TEMPLATE"]
