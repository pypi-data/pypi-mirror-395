# 框架依赖管理策略

## 📋 文档概述

本文档记录了 DF Test Framework 在 CI 环境中进行自身项目安装和测试时遇到的**循环依赖问题**，以及相应的分析、解决方案和未来规划。

**创建时间**: 2025-11-26
**适用版本**: v3.10.0+
**维护者**: 框架核心团队

---

## 🔍 问题背景

### 问题描述

在 GitHub Actions 定时健康检查工作流中，执行 `df-test init` 命令创建测试项目时失败：

```bash
$ uv run df-test init health-check-api --type api
$ cd health-check-api && uv sync

× No solution found when resolving dependencies:
╰─▶ Because df-test-framework was not found in the package registry
    and your project depends on df-test-framework>=3.5.0,
    we can conclude that your project's requirements are unsatisfiable.
```

**失败原因**: 生成的项目依赖 `df-test-framework>=3.5.0`，但框架尚未发布到 PyPI，导致依赖解析失败。

### 问题场景

```
┌─────────────────────────────────────────────────┐
│  df-test-framework (框架源码)                  │
│  ├── CLI工具 (df-test)                          │
│  │   └── init 命令：生成测试项目                │
│  └── 运行时库 (clients, databases, testing等)   │
└─────────────────────────────────────────────────┘
         │
         │ df-test init 生成项目
         ↓
┌─────────────────────────────────────────────────┐
│  test-project (CLI生成的测试项目)               │
│  ├── pyproject.toml                             │
│  │   └── dependencies:                          │
│  │       "df-test-framework>=3.5.0"  ❌ PyPI没有│
│  └── tests/                                     │
└─────────────────────────────────────────────────┘
         │
         │ uv sync (CI环境)
         ↓
      ❌ 失败：PyPI 找不到包
```

### 触发条件

1. **CI 环境**：在 GitHub Actions 中运行健康检查
2. **框架未发布**：`df-test-framework` 尚未发布到 PyPI
3. **CLI 生成项目**：使用 `df-test init` 创建新项目
4. **依赖安装**：执行 `uv sync` 安装依赖时失败

---

## 🎯 根本原因分析

### 架构问题：CLI 与框架耦合

```
问题本质：CLI 工具和运行时库在同一个包中
┌──────────────────────────────────────────────┐
│  df-test-framework (单一包)                  │
│  ├── CLI (脚手架工具)                         │
│  │   └── 生成依赖框架的项目                   │
│  └── Runtime Library (运行时库)              │
│      └── 被生成的项目依赖                     │
└──────────────────────────────────────────────┘
         ↓
      循环依赖
         ↓
┌──────────────────────────────────────────────┐
│  CLI init → 生成项目 → 依赖 Runtime Library  │
│  Runtime Library → 尚未发布 → 依赖解析失败   │
└──────────────────────────────────────────────┘
```

### 问题分类

| 问题类型 | 描述 | 影响范围 |
|---------|------|---------|
| **循环依赖** | CLI 生成的项目依赖框架本身 | CI 健康检查失败 |
| **发布耦合** | CLI 和 Runtime 必须同时发布 | 版本管理复杂 |
| **环境差异** | 本地开发 vs CI 环境行为不一致 | 开发体验差 |

---

## 🏭 业界最佳实践

### 方案 A：完全分离（推荐指数：⭐⭐⭐⭐⭐）

**代表项目**: Vue CLI, Create React App, Vite

```
vue-cli (脚手架工具包)
    ├── 发布到 npm: @vue/cli
    └── 生成的项目依赖: vue (独立包)

create-react-app (脚手架工具包)
    ├── 发布到 npm: create-react-app
    └── 生成的项目依赖: react-scripts (独立包)

vite (脚手架工具包)
    ├── 发布到 npm: create-vite
    └── 生成的项目依赖: vite (独立包)
```

**优势**:
- ✅ **完全解耦**：CLI 和 Runtime 独立发布、独立迭代
- ✅ **版本灵活**：用户可以升级 Runtime 而不升级 CLI
- ✅ **职责清晰**：CLI 专注脚手架，Runtime 专注功能
- ✅ **无循环依赖**：天然避免依赖问题

**劣势**:
- ❌ **维护成本**：需要管理两个独立的包
- ❌ **发布复杂**：需要协调两个包的发布流程
- ❌ **文档分散**：需要维护两套文档

**适用场景**: 成熟的大型框架，有专门的团队维护

---

### 方案 B：Cookiecutter 模式（推荐指数：⭐⭐⭐⭐）

**代表项目**: Django, FastAPI

```
django-admin startproject
    ├── 使用内置模板
    └── 生成的项目依赖: django (同一个包)

cookiecutter (独立脚手架工具)
    ├── 从 GitHub 读取模板
    └── 生成的项目依赖: 任意包
```

**优势**:
- ✅ **模板灵活**：模板可以独立于框架版本迭代
- ✅ **无需发布**：模板可以从 Git 仓库直接拉取
- ✅ **社区友好**：用户可以贡献自定义模板

**劣势**:
- ❌ **模板管理**：需要维护独立的模板仓库
- ❌ **版本同步**：模板和框架版本可能不匹配
- ❌ **网络依赖**：需要联网下载模板

**适用场景**: 中型框架，需要灵活的模板系统

---

### 方案 C：环境变量智能切换（推荐指数：⭐⭐⭐）

**代表项目**: 无典型案例（自创方案）

```python
# 根据环境自动选择依赖方式
def _get_framework_dependency() -> str:
    # CI 环境：使用本地路径依赖
    if os.getenv("CI") == "true":
        return '"df-test-framework @ file://.."'

    # 本地开发标志：使用本地路径依赖
    if os.getenv("DF_TEST_LOCAL_DEV") == "1":
        return '"df-test-framework @ file://.."'

    # 生产环境：从 PyPI 安装
    return '"df-test-framework>=3.5.0"'
```

**优势**:
- ✅ **零改动**：CLI 和 Runtime 保持在同一个包
- ✅ **自动检测**：CI 环境自动使用本地路径
- ✅ **简单实用**：实现成本低，维护简单
- ✅ **向后兼容**：不破坏现有架构

**劣势**:
- ❌ **非标准方案**：不是业界通用做法
- ❌ **魔法行为**：环境变量控制行为不够显式
- ❌ **仍有耦合**：CLI 和 Runtime 仍在同一个包

**适用场景**: 小型框架，快速迭代，临时解决方案

---

## ✅ 当前实现方案

### 技术选型：方案 C（环境变量智能切换）

**选择理由**:
1. **快速迭代**：框架处于快速开发阶段，暂不拆分
2. **实现成本低**：只需修改模板和 CLI 命令
3. **向后兼容**：不影响现有用户
4. **符合 12-Factor App 原则**：环境变量配置

### 实现细节

#### 1. 智能依赖选择函数

**文件**: `src/df_test_framework/cli/commands/init_cmd.py`

```python
def _get_framework_dependency() -> str:
    """智能选择框架依赖

    根据环境自动选择合适的依赖方式：
    1. CI 环境（自动检测） → 本地路径依赖
    2. DF_TEST_LOCAL_DEV=1 → 本地路径依赖
    3. 默认 → PyPI 版本依赖

    Returns:
        框架依赖字符串

    Example:
        >>> os.environ["CI"] = "true"
        >>> _get_framework_dependency()
        '"df-test-framework @ file://.."'

        >>> os.environ.pop("CI")
        >>> _get_framework_dependency()
        '"df-test-framework>=3.5.0"'
    """
    # 检测 CI 环境（GitHub Actions, GitLab CI, Jenkins 等都会设置 CI=true）
    if os.getenv("CI") == "true":
        return '"df-test-framework @ file://.."'

    # 检测本地开发标志
    if os.getenv("DF_TEST_LOCAL_DEV") == "1":
        return '"df-test-framework @ file://.."'

    # 生产环境：从 PyPI 安装
    return '"df-test-framework>=3.5.0"'
```

#### 2. 模板变量替换

**文件**: `src/df_test_framework/cli/templates/project/pyproject_toml.py`

```toml
[project]
name = "{project_name}"
version = "1.0.0"
dependencies = [
    {framework_dependency},  # ✅ 动态替换
    "pytest>=8.0.0",
    # ...
]
```

#### 3. CI 工作流验证

**文件**: `.github/workflows/scheduled.yml`

```yaml
- name: CLI命令健康检查
  run: |
    echo "::group::Init命令"
    # CI环境自动检测：框架会使用本地路径依赖（CI=true）
    uv run df-test init health-check-api --type api
    test -f health-check-api/pytest.ini || exit 1
    echo "::endgroup::"

    echo "::group::验证依赖配置"
    # 验证生成的项目使用了本地路径依赖
    grep 'df-test-framework @ file://..' health-check-api/pyproject.toml || exit 1
    echo "✅ 已正确使用本地路径依赖"
    echo "::endgroup::"
```

### 环境检测逻辑

| 环境 | `CI` 变量 | `DF_TEST_LOCAL_DEV` | 依赖方式 | 使用场景 |
|------|----------|---------------------|---------|---------|
| **GitHub Actions** | `true` | - | `file://..` | CI 健康检查 |
| **GitLab CI** | `true` | - | `file://..` | CI 健康检查 |
| **Jenkins** | `true` | - | `file://..` | CI 健康检查 |
| **本地开发** | - | `1` | `file://..` | 框架开发测试 |
| **生产环境** | - | - | `>=3.5.0` | 用户使用 |

### 测试覆盖

**文件**: `tests/cli/test_init_cmd.py`

```python
class TestFrameworkDependency:
    """测试智能依赖选择功能（v3.10.0+）"""

    def test_get_framework_dependency_in_ci(self, monkeypatch):
        """测试 CI 环境自动使用本地路径"""
        monkeypatch.setenv("CI", "true")
        result = _get_framework_dependency()
        assert result == '"df-test-framework @ file://.."'

    def test_get_framework_dependency_with_local_dev_flag(self, monkeypatch):
        """测试 DF_TEST_LOCAL_DEV=1 使用本地路径"""
        monkeypatch.delenv("CI", raising=False)
        monkeypatch.setenv("DF_TEST_LOCAL_DEV", "1")
        result = _get_framework_dependency()
        assert result == '"df-test-framework @ file://.."'

    def test_get_framework_dependency_default(self, monkeypatch):
        """测试默认使用 PyPI 版本"""
        monkeypatch.delenv("CI", raising=False)
        monkeypatch.delenv("DF_TEST_LOCAL_DEV", raising=False)
        result = _get_framework_dependency()
        assert result == '"df-test-framework>=3.5.0"'

    def test_init_project_uses_correct_dependency_in_ci(self, tmp_path, monkeypatch):
        """测试 CI 环境生成的项目使用本地路径依赖"""
        monkeypatch.setenv("CI", "true")
        project_dir = tmp_path / "ci_test_project"
        init_project(project_dir, project_type="api", force=True)
        pyproject = (project_dir / "pyproject.toml").read_text(encoding="utf-8")
        assert "df-test-framework @ file://.." in pyproject

    def test_init_project_uses_correct_dependency_default(self, tmp_path, monkeypatch):
        """测试默认环境生成的项目使用 PyPI 版本"""
        monkeypatch.delenv("CI", raising=False)
        monkeypatch.delenv("DF_TEST_LOCAL_DEV", raising=False)
        project_dir = tmp_path / "default_test_project"
        init_project(project_dir, project_type="api", force=True)
        pyproject = (project_dir / "pyproject.toml").read_text(encoding="utf-8")
        assert "df-test-framework>=3.5.0" in pyproject
```

**测试结果**: ✅ 全部通过（5个测试用例）

---

## 🚀 未来演进路径

### 阶段 1：当前方案（v3.10.0 ~ v3.x）

**时间**: 2025 Q4 - 2026 Q1
**目标**: 快速迭代，稳定核心功能
**方案**: 环境变量智能切换（方案 C）

**关键指标**:
- ✅ CI 健康检查 100% 通过率
- ✅ 用户反馈 < 5 个依赖相关问题/月
- ✅ 框架发布到 PyPI 后自动切换到 PyPI 依赖

**退出条件**:
- 框架功能趋于稳定（v4.0.0）
- 用户基数 > 1000
- 社区反馈需要更灵活的模板系统

---

### 阶段 2：过渡方案（v4.0.0 ~ v5.0.0）

**时间**: 2026 Q2 - 2026 Q4
**目标**: 引入模板系统，提升灵活性
**方案**: Cookiecutter 模式（方案 B）

**实施步骤**:
1. **创建模板仓库**: `df-test-templates`
2. **迁移现有模板**: API、UI、Full → 独立模板
3. **CLI 支持模板源**:
   ```bash
   df-test init my-project --template github:df-test-templates/api
   df-test init my-project --template local:~/my-template
   ```
4. **保持向后兼容**: 内置模板作为默认选项

**优势**:
- 用户可以贡献自定义模板
- 模板可以独立于框架版本迭代
- 保持 CLI 和 Runtime 在同一个包

**风险**:
- 网络依赖可能导致离线初始化失败
- 模板版本管理复杂度增加

---

### 阶段 3：长期方案（v5.0.0+）

**时间**: 2027 Q1+
**目标**: 彻底解耦，符合业界标准
**方案**: 完全分离（方案 A）

**包结构重组**:
```
df-test-cli (脚手架工具)
├── 发布到 PyPI: df-test-cli
├── 功能: 项目初始化、代码生成
└── 依赖: jinja2, click

df-test-framework (运行时库)
├── 发布到 PyPI: df-test-framework
├── 功能: HTTP、数据库、测试工具
└── 依赖: httpx, sqlalchemy, pytest

df-test-templates (模板仓库)
├── 托管在 GitHub
├── 功能: 项目模板、示例代码
└── 版本控制: Git tags
```

**迁移策略**:
1. **v5.0.0-alpha**: 拆分包，发布预览版
2. **v5.0.0-beta**: 社区测试，收集反馈
3. **v5.0.0**: 正式发布，废弃旧 CLI
4. **v5.1.0**: 移除旧 CLI（通过 `df-test-cli` 安装）

**用户迁移指南**:
```bash
# 旧方式（v4.x）
pip install df-test-framework
df-test init my-project

# 新方式（v5.0+）
pip install df-test-cli df-test-framework
df-test init my-project
```

**优势**:
- 完全符合业界标准
- 各组件独立演进
- 清晰的职责划分

**挑战**:
- 需要维护多个包
- 发布流程更复杂
- 文档需要大幅更新

---

## 📊 方案对比总结

| 维度 | 方案 A (完全分离) | 方案 B (Cookiecutter) | 方案 C (环境变量) |
|-----|------------------|---------------------|------------------|
| **实现成本** | 高（重构） | 中（新增模板仓库） | 低（修改模板） |
| **维护成本** | 高（多包管理） | 中（模板管理） | 低（单包管理） |
| **灵活性** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **解耦程度** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐ |
| **用户体验** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **社区贡献** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **适用阶段** | 成熟期 | 成长期 | 初创期 |
| **典型案例** | Vue CLI | Django | - |

**决策树**:
```
项目是否已发布到 PyPI？
├─ 否（初创期）
│  └─ 使用方案 C（环境变量智能切换）✅ 当前选择
│
└─ 是（成长期）
   ├─ 用户是否需要自定义模板？
   │  ├─ 是 → 使用方案 B（Cookiecutter）
   │  └─ 否 → 继续使用方案 C
   │
   └─ 是否需要完全解耦？
      ├─ 是 → 使用方案 A（完全分离）
      └─ 否 → 使用方案 B 或 C
```

---

## 🔧 实施检查清单

### 方案 C（当前）- 已完成 ✅

- [x] 实现 `_get_framework_dependency()` 函数
- [x] 更新 `pyproject_toml.py` 模板
- [x] 修改 `init_project()` 使用动态依赖
- [x] 更新 CI 工作流验证逻辑
- [x] 编写单元测试（5个测试用例）
- [x] 验证 CI 健康检查通过
- [x] 更新生成项目的 CI/CD 模板（6个文件）

### 方案 B（计划）- 待实施 ⏸️

- [ ] 创建独立的模板仓库 `df-test-templates`
- [ ] 迁移现有模板到新仓库
- [ ] CLI 支持 `--template` 参数
- [ ] 实现模板版本管理
- [ ] 支持本地模板路径
- [ ] 编写模板开发文档
- [ ] 社区模板贡献指南

### 方案 A（长期）- 未来规划 📅

- [ ] 设计 CLI 和 Runtime 的职责边界
- [ ] 创建 `df-test-cli` 包结构
- [ ] 拆分代码到两个独立仓库
- [ ] 协调发布流程（CI/CD）
- [ ] 编写迁移指南
- [ ] 社区公告和迁移支持
- [ ] 废弃旧 CLI（6个月过渡期）

---

## 📚 参考资料

### 相关文档

- [CLAUDE.md - 代码质量检查流程](../../CLAUDE.md)
- [CI/CD 配置指南](../user-guide/ci-cd.md)
- [发布流程](./RELEASE.md)
- [框架架构文档](../architecture/V3_ARCHITECTURE.md)

### 外部资源

- [Vue CLI 源码](https://github.com/vuejs/vue-cli)
- [Create React App 源码](https://github.com/facebook/create-react-app)
- [Vite 源码](https://github.com/vitejs/vite)
- [Cookiecutter 文档](https://cookiecutter.readthedocs.io/)
- [PEP 440 - Version Identification](https://peps.python.org/pep-0440/)
- [PEP 621 - Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/)
- [uv 官方文档](https://github.com/astral-sh/uv)
- [12-Factor App 原则](https://12factor.net/)

### 相关 Issue & PR

- Issue #XXX: CI 健康检查失败 - df-test-framework not found
- PR #XXX: feat: 实现环境变量智能依赖选择
- PR #XXX: docs: 更新 CI/CD 模板为现代化 uv 工作流

---

## 🤝 贡献指南

如果你有更好的依赖管理方案或改进建议，欢迎：

1. 提交 Issue 讨论方案可行性
2. 提交 PR 实现新方案
3. 更新本文档记录新的最佳实践

**联系方式**:
- GitHub Discussions: https://github.com/your-org/df-test-framework/discussions
- 邮件: dev@df-test-framework.org

---

## 📝 变更历史

| 日期 | 版本 | 作者 | 变更说明 |
|------|------|------|---------|
| 2025-11-26 | 1.0.0 | Claude | 初始版本，记录方案 C 实现 |
| - | - | - | - |

---

**文档结束**
