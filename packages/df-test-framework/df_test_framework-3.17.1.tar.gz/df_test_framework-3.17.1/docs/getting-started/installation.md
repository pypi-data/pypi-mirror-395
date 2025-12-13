# 安装指南

本文档将指导您安装和配置 DF Test Framework v3.0.0-alpha。

## 📋 系统要求

- **Python**：3.10+（推荐 3.11+）
- **操作系统**：Windows / Linux / macOS
- **包管理器**：`uv`（推荐）或 `pip`
- **可选组件**：Allure、Playwright、数据库客户端等

## 🔧 安装步骤

### 方式 1：使用 uv（推荐）

```bash
# 安装 uv（如果尚未安装）
pip install uv

# 安装框架核心
uv pip install df-test-framework
```

### 方式 2：使用 pip

```bash
pip install df-test-framework
```

### 开发模式安装

若需调试或贡献代码：

```bash
git clone https://github.com/your-org/test-framework.git
cd test-framework

# 安装开发依赖与可编辑模式
uv pip install -e ".[dev]"
```

## ✅ 验证安装

```python
import df_test_framework as df
print(df.__version__)
# 期望输出: 3.0.0-alpha
```

或使用命令行：

```bash
python -c "import df_test_framework; print(df_test_framework.__version__)"
```

验证 CLI 是否可用：

```bash
df-test --help
```

## 📦 依赖说明

核心依赖：
- `httpx` — 现代 HTTP 客户端
- `pydantic` / `pydantic-settings` — 类型安全配置体系
- `sqlalchemy` — 数据库访问与连接池
- `redis` — Redis 客户端
- `loguru` — 结构化日志
- `pluggy` — 扩展与 Hook 系统
- `pytest` — 测试运行器

可选依赖（按需安装）：

```bash
# Allure 报告支持
uv pip install df-test-framework[allure]

# UI 测试（Playwright）支持
uv pip install df-test-framework[ui]

# 一次性安装全部扩展
uv pip install df-test-framework[all]
```

Playwright 首次安装后需要下载浏览器内核：

```bash
playwright install
```

## 🐛 常见问题

### ImportError

检查：
1. Python 版本 ≥ 3.10。  
2. 虚拟环境已激活。  
3. `pip list` 或 `uv pip list` 中存在 `df-test-framework` 及依赖。  
4. 若使用 VS Code / PyCharm，确保解释器指向正确的虚拟环境。

### 依赖冲突

建议始终使用虚拟环境：

```bash
# 使用 venv
python -m venv .venv
source .venv/bin/activate    # Linux/macOS
.venv\Scripts\activate       # Windows

# 或使用 uv
uv venv
source .venv/bin/activate
```

## 🎯 下一步

- [快速入门](quickstart.md) — 使用 `df-test init` 生成项目骨架  
- [30 分钟教程](tutorial.md) — 编写第一个 API 测试  
- [快速参考](../user-guide/QUICK_REFERENCE.md) — Fixtures、调试、常用命令

---

返回：[快速开始目录](README.md) | [文档首页](../README.md)
