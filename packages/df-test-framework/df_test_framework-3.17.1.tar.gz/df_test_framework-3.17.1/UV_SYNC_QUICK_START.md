# uv sync 快速开始指南

> **TL;DR**: 使用 `uv sync` 进行现代化依赖管理，所有命令使用 `uv run` 前缀

---

## 🚀 快速开始

### 1. 首次设置

```bash
# 克隆项目
git clone https://github.com/yourorg/df-test-framework.git
cd df-test-framework

# 同步依赖（自动创建虚拟环境）
uv sync --all-extras
```

### 2. 运行命令

所有命令都使用 `uv run` 前缀：

```bash
# 运行测试
uv run pytest -v

# 运行覆盖率测试
uv run pytest --cov=src/df_test_framework --cov-report=html

# 代码检查
uv run ruff check src/ tests/
uv run ruff format src/ tests/

# CLI 工具
uv run df-test --help
uv run df-test init my-project
```

---

## 📝 常用命令速查

### 开发命令

| 任务 | 命令 |
|------|------|
| **同步依赖** | `uv sync --all-extras` |
| **运行测试** | `uv run pytest -v` |
| **测试覆盖率** | `uv run pytest --cov=src/df_test_framework --cov-report=html` |
| **代码检查** | `uv run ruff check src/ tests/` |
| **代码格式化** | `uv run ruff format src/ tests/` |
| **类型检查** | `uv run mypy src/` |
| **CLI 工具** | `uv run df-test --help` |

### 依赖管理

| 任务 | 命令 |
|------|------|
| **安装所有依赖** | `uv sync --all-extras` |
| **只安装基础依赖** | `uv sync` |
| **安装 dev 依赖** | `uv sync --extra dev` |
| **更新依赖** | `uv lock --upgrade && uv sync --all-extras` |
| **重建环境** | `rm -rf .venv && uv sync --all-extras` |

### 测试命令

| 任务 | 命令 |
|------|------|
| **运行所有测试** | `uv run pytest -v` |
| **运行特定文件** | `uv run pytest tests/utils/test_common.py -v` |
| **运行冒烟测试** | `uv run pytest -m smoke -v` |
| **排除慢速测试** | `uv run pytest -m "not slow" -v` |
| **并行运行** | `uv run pytest -n auto -v` |

---

## 🆚 新旧对比

### 旧方式 (不推荐)

```bash
# 安装依赖
uv pip install -e ".[dev]"

# 运行命令（直接运行）
pytest -v
df-test --help
ruff check src/
```

### 新方式 (推荐) ✅

```bash
# 同步依赖
uv sync --all-extras

# 运行命令（使用 uv run）
uv run pytest -v
uv run df-test --help
uv run ruff check src/
```

---

## 📁 关键文件

| 文件 | 说明 | 是否提交到 Git |
|------|------|----------------|
| `pyproject.toml` | 项目配置和依赖声明 | ✅ 是 |
| `uv.lock` | 依赖锁定文件 | ✅ **是（重要！）** |
| `.python-version` | Python 版本指定 | ✅ 是 |
| `.venv/` | 虚拟环境目录 | ❌ 否 |

---

## 💡 提示

1. ✅ **永远使用 `uv run`**: 确保在正确的虚拟环境中运行命令
2. ✅ **提交 `uv.lock`**: 确保团队成员使用相同的依赖版本
3. ✅ **不要提交 `.venv/`**: 虚拟环境是自动生成的
4. ✅ **定期更新依赖**: `uv lock --upgrade && uv sync --all-extras`

---

## 🆘 遇到问题？

### 依赖安装失败

```bash
# 清理并重新安装
rm -rf .venv
uv sync --all-extras
```

### 命令找不到

```bash
# 确保使用 uv run 前缀
uv run pytest --version
uv run df-test --help
```

### 版本不一致

```bash
# 更新 uv.lock
uv lock --upgrade
uv sync --all-extras
```

---

## 📚 更多文档

- [完整迁移指南](docs/UV_SYNC_MIGRATION.md)
- [贡献指南](CONTRIBUTING.md)
- [项目 README](README.md)

---

**记住**: 使用 `uv sync` + `uv run` 就对了！🎉
