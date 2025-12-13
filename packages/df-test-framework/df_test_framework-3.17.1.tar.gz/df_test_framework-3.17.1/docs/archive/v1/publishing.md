# PyPI 发布指南

本文档说明如何将 `df-test-framework` 发布到 PyPI (Python Package Index)。

## 前置准备

### 1. 注册 PyPI 账号

- **生产环境**: https://pypi.org/account/register/
- **测试环境**: https://test.pypi.org/account/register/

建议先在测试环境验证发布流程。

### 2. 配置 API Token

为了安全地发布包,建议使用 API Token 而不是用户名密码。

#### 生成 API Token:

1. 登录 PyPI: https://pypi.org/manage/account/
2. 滚动到 "API tokens" 部分
3. 点击 "Add API token"
4. 设置 token 名称(如 `df-test-framework-upload`)
5. 选择 Scope:
   - 首次发布选择 "Entire account"
   - 之后可以为特定项目创建专用 token
6. 复制生成的 token (只显示一次!)

#### 配置 Token:

创建或编辑 `~/.pypirc` 文件:

```ini
[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmcC...  # 你的 API token

[testpypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmcC...  # 测试环境的 API token
```

**注意**: 将此文件权限设置为只有你可读: `chmod 600 ~/.pypirc`

### 3. 安装发布工具

```bash
# 安装 build 和 twine
uv pip install build twine

# 或使用 pip
pip install build twine
```

## 发布前检查清单

在发布前,请确认以下事项:

- [ ] 更新了版本号 (`pyproject.toml` 中的 `version`)
- [ ] 更新了 `README.md` 和 `CHANGELOG.md`
- [ ] 更新了 `pyproject.toml` 中的作者邮箱和项目 URL
- [ ] 确保所有测试通过: `pytest`
- [ ] 确保代码格式正确: `ruff check .`
- [ ] 提交所有改动到 Git
- [ ] 创建 Git tag: `git tag v1.1.0`

## 发布步骤

### 步骤 1: 清理旧的构建产物

```bash
cd D:\Git\DF\qa\test-framework
rm -rf dist/ build/ *.egg-info
```

### 步骤 2: 构建发布包

```bash
# 使用 build 工具构建
python -m build

# 构建完成后,dist/ 目录会包含:
# - df_test_framework-1.1.0-py3-none-any.whl (wheel 格式)
# - df_test_framework-1.1.0.tar.gz (源码格式)
```

### 步骤 3: 检查构建产物

```bash
# 检查 wheel 包的内容
python -m zipfile -l dist/df_test_framework-1.1.0-py3-none-any.whl

# 使用 twine 检查包的元数据
twine check dist/*
```

应该看到类似输出:
```
Checking dist/df_test_framework-1.1.0-py3-none-any.whl: PASSED
Checking dist/df_test_framework-1.1.0.tar.gz: PASSED
```

### 步骤 4: 先发布到测试环境 (推荐)

```bash
# 上传到 TestPyPI
twine upload --repository testpypi dist/*

# 测试安装
pip install --index-url https://test.pypi.org/simple/ df-test-framework
```

### 步骤 5: 发布到正式 PyPI

确认测试环境没问题后,发布到正式 PyPI:

```bash
twine upload dist/*
```

发布成功后,你会看到包的 URL:
```
https://pypi.org/project/df-test-framework/
```

### 步骤 6: 验证发布

```bash
# 安装发布的包
pip install df-test-framework

# 验证版本
python -c "import df_test_framework; print(df_test_framework.__version__)"

# 测试导入核心模块
python -c "from df_test_framework.api import APIClient; print('OK')"
```

## 更新项目使用新发布的包

发布到 PyPI 后,需要更新使用该框架的测试项目(如 `gift-card-test`):

### 修改 `gift-card-test/pyproject.toml`:

```toml
dependencies = [
    # 从 PyPI 安装
    "df-test-framework>=1.1.0",

    # 本地开发时,可以使用本地路径覆盖
    # "df-test-framework @ file:///D:/Git/DF/qa/test-framework",
]
```

### 重新同步依赖:

```bash
cd D:\Git\DF\qa\gift-card-test
uv sync
```

## 版本管理最佳实践

### 语义化版本 (Semantic Versioning)

遵循 `MAJOR.MINOR.PATCH` 格式:

- **MAJOR**: 不兼容的 API 变更 (如 `2.0.0`)
- **MINOR**: 向后兼容的功能新增 (如 `1.2.0`)
- **PATCH**: 向后兼容的 bug 修复 (如 `1.1.1`)

### 版本更新流程

1. 修改 `pyproject.toml` 中的 `version`
2. 更新 `CHANGELOG.md` 记录变更
3. 提交改动: `git commit -am "chore: bump version to 1.2.0"`
4. 创建 Git tag: `git tag v1.2.0`
5. 推送代码和 tag: `git push && git push --tags`
6. 构建并发布新版本

## 常见问题

### Q: 如何删除已发布的版本?

**A**: PyPI 不允许删除已发布的版本,但可以 "yank" (标记为不推荐):

```bash
# 使用 PyPI Web UI 或 API
# 注意: 一旦发布,版本号就被永久占用了
```

建议在发布前充分测试。

### Q: 如何发布预发布版本?

**A**: 使用预发布版本号:

```toml
version = "1.2.0a1"  # alpha
version = "1.2.0b1"  # beta
version = "1.2.0rc1" # release candidate
```

### Q: 如何支持本地开发和 PyPI 安装?

**A**: 在项目的 `pyproject.toml` 中:

```toml
dependencies = [
    # 默认从 PyPI 安装
    "df-test-framework>=1.1.0",
]

# 本地开发时,在虚拟环境中手动安装本地版本
# uv pip install -e /path/to/test-framework
```

或者使用环境变量:

```bash
# 本地开发
export USE_LOCAL_FRAMEWORK=1

# 在 pyproject.toml 中根据环境变量选择依赖源
```

### Q: 发布失败怎么办?

**A**: 常见问题:

1. **包名已存在**: 改用不同的包名
2. **版本号已存在**: 更新版本号
3. **认证失败**: 检查 `~/.pypirc` 配置
4. **元数据错误**: 运行 `twine check dist/*` 查看详情

## 自动化发布 (可选)

可以使用 GitHub Actions 自动发布:

```yaml
# .github/workflows/publish.yml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install build twine
      - name: Build package
        run: python -m build
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*
```

## 参考资源

- [PyPI 官方文档](https://packaging.python.org/tutorials/packaging-projects/)
- [Semantic Versioning](https://semver.org/)
- [Twine 文档](https://twine.readthedocs.io/)
- [PEP 517/518 - Build System](https://www.python.org/dev/peps/pep-0517/)