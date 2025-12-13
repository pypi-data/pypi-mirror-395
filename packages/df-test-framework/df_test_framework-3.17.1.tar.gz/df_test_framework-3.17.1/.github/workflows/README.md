# GitHub Actions工作流说明

本目录包含DF Test Framework框架自身的CI/CD配置。

---

## 📋 工作流列表

### 1. 代码质量检查 (`lint.yml`)

**触发条件**:
- Push到main/master/develop分支
- Pull Request到main/master/develop分支

**执行内容**:
- ✅ Ruff代码检查（语法、导入、命名等）
- ✅ Ruff格式检查（代码风格）
- ⚠️ MyPy类型检查（允许失败）

**作用**: 确保代码质量和一致性

---

### 2. 测试 (`test.yml`)

**触发条件**:
- Push到main/master/develop分支
- Pull Request到main/master/develop分支
- 手动触发

**测试矩阵**:
- **操作系统**: Ubuntu, Windows, macOS
- **Python版本**: 3.12, 3.13

**执行内容**:
- ✅ CLI工具安装验证
- ✅ `df-test init` 命令测试
- ✅ `df-test gen` 命令测试
- ✅ 单元测试（如果存在）
- ✅ CLI集成测试（完整项目初始化和代码生成）

**作用**: 确保CLI工具在所有平台和Python版本上正常工作

---

### 3. 发布 (`release.yml`)

**触发条件**:
- 推送版本标签（如`v2.0.0`）
- 手动触发（需指定版本号）

**执行流程**:
```
发布前测试
  ↓
构建分发包 (wheel + sdist)
  ↓
发布到PyPI (需要PYPI_API_TOKEN)
  ↓
创建GitHub Release (包含changelog和构建产物)
  ↓
发送钉钉通知 (可选)
```

**所需Secrets**:
- `PYPI_API_TOKEN`: PyPI API令牌
- `DINGTALK_WEBHOOK`: 钉钉机器人Webhook（可选）

**作用**: 自动化发布流程，确保版本一致性

**使用方法**:
```bash
# 1. 更新版本号 (pyproject.toml)
# 2. 更新CHANGELOG.md
# 3. 提交并推送
git add pyproject.toml CHANGELOG.md
git commit -m "chore: bump version to 2.1.0"
git push

# 4. 创建并推送标签
git tag -a v2.1.0 -m "Release v2.1.0"
git push origin v2.1.0

# 5. GitHub Actions自动执行发布流程
```

---

### 4. 定时检查 (`scheduled.yml`)

**触发条件**:
- 每天凌晨2点（UTC 18:00）
- 手动触发

**执行内容**:
- ✅ 代码质量检查
- ✅ CLI命令健康检查
- ✅ 项目初始化功能测试
- ✅ 代码生成功能测试
- ✅ 文档完整性检查
- ✅ 示例代码存在性检查
- ✅ 依赖安全漏洞扫描

**作用**: 每日健康检查，及时发现潜在问题

---

## 🔧 配置说明

### GitHub Secrets

在GitHub仓库Settings → Secrets and variables → Actions中配置：

| Secret名称 | 说明 | 必需 | 用于 |
|-----------|------|------|------|
| `PYPI_API_TOKEN` | PyPI API令牌 | 是 | 发布到PyPI |
| `DINGTALK_WEBHOOK` | 钉钉机器人Webhook | 否 | 发送通知 |

### GitHub Environments

创建`release`环境（Settings → Environments）：
- 启用保护规则
- 要求审批（可选）
- 限制到main分支

---

## 📊 工作流徽章

在README.md中添加以下徽章：

```markdown
![Lint](https://github.com/yourorg/df-test-framework/actions/workflows/lint.yml/badge.svg)
![Test](https://github.com/yourorg/df-test-framework/actions/workflows/test.yml/badge.svg)
![Release](https://github.com/yourorg/df-test-framework/actions/workflows/release.yml/badge.svg)
```

---

## 🎯 最佳实践

### 1. 提交前本地检查

```bash
# 代码质量检查
ruff check src/
ruff format src/ --check

# CLI功能测试
df-test --help
df-test init test-temp --type api
```

### 2. 版本发布流程

1. **更新版本号**: 修改`pyproject.toml`
2. **更新变更日志**: 在`CHANGELOG.md`中添加版本信息
3. **提交更改**: `git commit -m "chore: bump version to X.Y.Z"`
4. **创建标签**: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
5. **推送**: `git push && git push --tags`
6. **等待CI**: 自动测试、构建、发布

### 3. Pull Request流程

1. 创建PR后自动触发lint和test工作流
2. 确保所有检查通过
3. 合并到main分支
4. main分支再次运行检查

---

## 🐛 故障排查

### Q: 发布到PyPI失败

检查：
- `PYPI_API_TOKEN` Secret是否正确配置
- PyPI项目名称是否已存在
- 版本号是否已被使用

### Q: CLI测试失败

检查：
- 框架是否正确安装（`pip install -e .`）
- CLI入口点是否正确配置（`pyproject.toml`中的`[project.scripts]`）
- 权限问题（Windows文件系统）

### Q: 定时任务未运行

检查：
- 仓库是否超过60天无活动（GitHub会禁用scheduled工作流）
- Cron表达式是否正确
- 手动触发测试是否正常

---

## 📚 相关文档

- [GitHub Actions文档](https://docs.github.com/en/actions)
- [PyPI Publishing](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/)
- [框架CI/CD用户指南](../../docs/user-guide/ci-cd.md)

---

**最后更新**: 2025-11-02
