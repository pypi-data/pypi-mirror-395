# 测试环境Docker镜像
# 基于Python 3.12的轻量级Alpine镜像

FROM python:3.12-slim

LABEL maintainer="DF QA Team"
LABEL description="DF Test Framework测试环境"
LABEL version="2.0.0"

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    # 基础工具
    curl \
    git \
    # Playwright依赖
    wget \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxcb1 \
    libxkbcommon0 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libatspi2.0-0 \
    # 清理
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 安装uv（更快的包管理器）
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    mv /root/.cargo/bin/uv /usr/local/bin/

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN uv pip install --system -r requirements.txt && \
    uv pip install --system \
    pytest \
    pytest-cov \
    pytest-html \
    pytest-xdist \
    allure-pytest \
    playwright && \
    # 安装Playwright浏览器
    playwright install chromium firefox webkit

# 创建必要的目录
RUN mkdir -p /app/tests /app/reports /app/logs

# 设置健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# 默认命令
CMD ["pytest", "--version"]
