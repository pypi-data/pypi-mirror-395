# PyPI 发布指南

本文档说明如何将 df-test-framework 发布到 PyPI。

---

## 📋 前置条件

### 1. PyPI 账号设置

**注册账号**:
- 主PyPI: https://pypi.org/account/register/
- 测试PyPI (可选): https://test.pypi.org/account/register/

**创建 API Token**:
1. 登录 PyPI
2. 访问: https://pypi.org/manage/account/token/
3. 创建新token: `Scope: Entire account (发布所有包)`
4. 复制token (格式: `pypi-xxxxx...`)
5. **重要**: Token只显示一次，请立即保存

### 2. GitHub Secrets 配置

在 GitHub 仓库设置中添加 Secret:

```
Settings → Secrets and variables → Actions → New repository secret

Name: PYPI_API_TOKEN
Value: pypi-xxxxx...  (你的PyPI API Token)
```

### 3. 本地工具安装

```bash
# 安装构建工具
pip install build twine

# 验证安装
python -m build --version
twine --version
```

---

## 🚀 发布流程

### 方式1: 自动发布 (推荐)

使用 Git Tag 触发 GitHub Actions 自动发布。

#### 步骤:

**1. 更新版本号**

编辑 `pyproject.toml`:
```toml
[project]
version = "3.7.0"  # 更新版本号
description = "DF通用测试自动化框架 - v3.7.0 ..."  # 更新描述
```

**2. 更新 CHANGELOG.md**

在文件开头添加新版本的变更记录:
```markdown
## [3.7.0] - 2025-11-25

### ✨ 新增 (Added)
- Unit of Work 模式支持
- 熔断器 (Circuit Breaker)
- 安全最佳实践文档
...
```

**3. 提交变更**

```bash
git add pyproject.toml CHANGELOG.md
git commit -m "chore: bump version to 3.7.0"
git push
```

**4. 创建并推送 Tag**

```bash
# 创建tag
git tag v3.7.0

# 推送tag (触发发布)
git push origin v3.7.0
```

**5. 监控发布**

- GitHub Actions: https://github.com/yourorg/df-test-framework/actions
- 发布workflow会自动:
  - ✅ 运行测试
  - ✅ 构建分发包
  - ✅ 发布到PyPI
  - ✅ 创建GitHub Release

**6. 验证发布**

```bash
# 等待2-3分钟后安装
pip install df-test-framework==3.7.0

# 验证导入
python -c "from df_test_framework import Bootstrap; print('OK')"
```

---

### 方式2: 手动发布

适用于需要手动控制的场景。

#### 步骤:

**1. 清理构建目录**

```bash
rm -rf dist/ build/ *.egg-info
```

**2. 构建分发包**

```bash
# 构建 wheel 和 source distribution
python -m build

# 验证构建产物
ls -lh dist/
# 输出示例:
# df_test_framework-3.7.0-py3-none-any.whl
# df_test_framework-3.7.0.tar.gz
```

**3. 验证分发包**

```bash
# 检查包的元数据和结构
twine check dist/*

# 应该输出:
# Checking dist/df_test_framework-3.7.0-py3-none-any.whl: PASSED
# Checking dist/df_test_framework-3.7.0.tar.gz: PASSED
```

**4. 测试发布 (可选)**

先发布到 TestPyPI 测试:

```bash
# 发布到 TestPyPI
twine upload --repository testpypi dist/*

# 测试安装
pip install --index-url https://test.pypi.org/simple/ df-test-framework==3.7.0
```

**5. 正式发布到 PyPI**

```bash
# 使用token发布
twine upload dist/*

# 输入:
# username: __token__
# password: pypi-xxxxx... (你的API Token)
```

**6. 创建 GitHub Release**

手动在 GitHub 创建 Release:
1. 访问: https://github.com/yourorg/df-test-framework/releases/new
2. Tag: `v3.7.0`
3. Title: `v3.7.0`
4. 描述: 从 CHANGELOG.md 复制本版本的变更
5. 上传 `dist/` 中的文件
6. 发布

---

## ✅ 发布检查清单

发布前请确认:

- [ ] 版本号已更新 (pyproject.toml)
- [ ] CHANGELOG.md 已更新
- [ ] 所有测试通过 (`uv run pytest`)
- [ ] 代码质量检查通过 (`uv run ruff check src/`)
- [ ] 安全扫描通过 (`scripts/security-scan.sh`)
- [ ] README.md 准确反映最新功能
- [ ] 文档已更新
- [ ] 示例代码可运行
- [ ] PyPI Token 已配置 (GitHub Secrets)

---

## 🔍 发布验证

### 1. PyPI 页面验证

访问包页面: https://pypi.org/project/df-test-framework/

检查:
- ✅ 版本号正确
- ✅ 描述正确
- ✅ 分类标签正确
- ✅ 依赖列表完整
- ✅ README 渲染正常

### 2. 安装测试

在全新环境中测试安装:

```bash
# 创建虚拟环境
python -m venv test-env
source test-env/bin/activate  # Linux/Mac
# test-env\Scripts\activate  # Windows

# 安装
pip install df-test-framework

# 验证导入
python -c "from df_test_framework import Bootstrap, UnitOfWork; print('OK')"

# 验证CLI
df-test --version
df-test init test-project --type api
cd test-project
pytest -v
```

### 3. 文档验证

检查文档链接:
```bash
# README中的链接
pip install linkchecker
linkchecker README.md

# 文档中的链接
linkchecker docs/
```

---

## 🛠️ 故障排查

### 问题1: Twine上传失败

**错误**: `403 Forbidden` 或 `Invalid credentials`

**解决**:
```bash
# 1. 验证token格式
echo $PYPI_API_TOKEN  # 应该以 pypi- 开头

# 2. 重新生成token
# 访问: https://pypi.org/manage/account/token/

# 3. 使用环境变量
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-xxxxx...
twine upload dist/*
```

### 问题2: 包名冲突

**错误**: `Package name already exists`

**解决**:
- 包名 `df-test-framework` 必须是唯一的
- 如果已被占用，需要更改为其他名称
- 检查: https://pypi.org/search/?q=df-test-framework

### 问题3: Metadata错误

**错误**: `Metadata is invalid`

**解决**:
```bash
# 验证pyproject.toml格式
python -c "import tomllib; tomllib.load(open('pyproject.toml', 'rb'))"

# 检查必填字段
# - name
# - version
# - description
# - authors
```

### 问题4: 构建失败

**错误**: `No module named 'hatchling'`

**解决**:
```bash
# 安装构建后端
pip install hatchling

# 或使用uv
uv pip install hatchling
```

---

## 📝 版本号规范

遵循语义化版本 (Semantic Versioning 2.0.0):

```
MAJOR.MINOR.PATCH

例如: 3.7.0
- MAJOR (3): 不兼容的API变更
- MINOR (7): 向后兼容的新功能
- PATCH (0): 向后兼容的Bug修复
```

**版本递增规则**:
- 🔴 **Breaking Changes** → MAJOR 版本 (3.x.x → 4.0.0)
- 🟡 **New Features** → MINOR 版本 (3.7.x → 3.8.0)
- 🟢 **Bug Fixes** → PATCH 版本 (3.7.0 → 3.7.1)

**示例**:
- `3.7.0` → `3.7.1`: 修复了UnitOfWork的bug
- `3.7.0` → `3.8.0`: 新增AsyncHttpClient
- `3.7.0` → `4.0.0`: 移除了旧的db_transaction API

---

## 🔗 相关资源

- **PyPI官方文档**: https://packaging.python.org/tutorials/packaging-projects/
- **Twine文档**: https://twine.readthedocs.io/
- **语义化版本**: https://semver.org/lang/zh-CN/
- **PEP 440** (版本标识): https://peps.python.org/pep-0440/
- **PEP 621** (pyproject.toml): https://peps.python.org/pep-0621/

---

## 📞 获取帮助

- **PyPI支持**: https://pypi.org/help/
- **GitHub Issues**: https://github.com/yourorg/df-test-framework/issues
- **团队联系**: qa@example.com

---

**最后更新**: 2025-11-25
**文档版本**: v1.0
