# CI/CD集成指南

> 📚 **版本**: v2.0.0
> 🎯 **目标**: 在主流CI/CD平台上自动化运行测试

---

## 📖 目录

- [简介](#简介)
- [支持的CI/CD平台](#支持的cicd平台)
- [GitHub Actions](#github-actions)
- [GitLab CI](#gitlab-ci)
- [Jenkins](#jenkins)
- [Docker支持](#docker支持)
- [最佳实践](#最佳实践)
- [常见问题](#常见问题)

---

## 简介

DF Test Framework提供了完整的CI/CD集成模板，支持主流的CI/CD平台。通过这些模板，您可以快速配置自动化测试流程。

### 核心特性

| 特性 | 说明 |
|-----|------|
| **多平台支持** | GitHub Actions、GitLab CI、Jenkins |
| **Docker化** | 提供标准化的测试环境镜像 |
| **测试报告** | Allure、HTML、覆盖率报告 |
| **通知机制** | 邮件、钉钉、Slack集成 |
| **并行测试** | 多Python版本、多OS矩阵测试 |
| **性能优化** | 依赖缓存、增量测试 |

---

## 支持的CI/CD平台

### 平台对比

| 平台 | 推荐度 | 优势 | 适用场景 |
|-----|--------|------|---------|
| **GitHub Actions** | ⭐⭐⭐⭐⭐ | 云原生、配置简单、免费额度高 | 开源项目、小团队 |
| **GitLab CI** | ⭐⭐⭐⭐ | 功能强大、私有部署、企业级 | 企业项目、私有仓库 |
| **Jenkins** | ⭐⭐⭐ | 高度可定制、插件丰富 | 传统企业、复杂流程 |

---

## GitHub Actions

### 快速开始

#### 1. 初始化项目时选择CI/CD支持

```bash
df-test init my-project --ci github-actions
```

#### 2. 或手动复制模板

```bash
# 复制GitHub Actions工作流文件
cp templates/cicd/.github/workflows/*.yml .github/workflows/
```

#### 3. 配置Secrets

在GitHub仓库设置中添加以下Secrets：

| Secret名称 | 说明 | 示例值 |
|-----------|------|--------|
| `HTTP_BASE_URL` | API基础URL | `https://api.example.com` |
| `DB_HOST` | 数据库主机 | `db.example.com` |
| `DB_USER` | 数据库用户 | `test_user` |
| `DB_PASSWORD` | 数据库密码 | `your_password` |
| `DINGTALK_WEBHOOK` | 钉钉Webhook | `https://oapi.dingtalk.com/...` |
| `CODECOV_TOKEN` | Codecov令牌 | `获取自codecov.io` |

### 可用的工作流

#### 📄 test.yml - 基础测试

**触发条件**:
- Push到`main`或`master`分支
- 创建Pull Request

**功能**:
- 运行完整测试套件
- 生成覆盖率报告
- 上传Allure报告
- 发布到GitHub Pages

**手动触发**:
```bash
# 在GitHub Actions页面点击"Run workflow"
```

#### 📄 test-full.yml - 完整测试矩阵

**测试矩阵**:
- Python版本: 3.10, 3.11, 3.12
- 操作系统: Ubuntu, Windows, macOS
- 数据库: SQLite, PostgreSQL, MySQL

**使用场景**: 发版前的全面测试

#### 📄 scheduled.yml - 定时测试

**触发时间**: 每天凌晨2点（UTC 18:00）

**功能**:
- 运行回归测试
- 发送钉钉通知
- 保留测试报告90天

**配置定时任务**:
```yaml
on:
  schedule:
    # 修改为您需要的时间（Cron表达式）
    - cron: '0 18 * * *'
```

#### 📄 release.yml - 发布流程

**触发条件**: 创建版本tag（如`v1.0.0`）

**流程**:
1. 运行完整测试
2. 构建Python包
3. 发布到PyPI（可选）
4. 创建GitHub Release
5. 发送发布通知

**创建发布**:
```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### 查看报告

#### Allure报告
访问: `https://<username>.github.io/<repo>/allure-report/`

#### 覆盖率报告
访问: `https://<username>.github.io/<repo>/coverage/`

---

## GitLab CI

### 快速开始

#### 1. 初始化项目

```bash
df-test init my-project --ci gitlab-ci
```

#### 2. 配置CI/CD变量

在GitLab项目设置 → CI/CD → Variables中添加：

| 变量名 | 说明 | Protected | Masked |
|-------|------|-----------|---------|
| `HTTP_BASE_URL` | API基础URL | ✅ | ❌ |
| `DB_HOST` | 数据库主机 | ✅ | ❌ |
| `DB_PASSWORD` | 数据库密码 | ✅ | ✅ |
| `DINGTALK_WEBHOOK` | 钉钉Webhook | ❌ | ✅ |
| `PYPI_API_TOKEN` | PyPI令牌 | ✅ | ✅ |

### Pipeline阶段

```
test (Python 3.12, 3.13)
  ↓
coverage (覆盖率分析)
  ↓
report (生成Allure报告)
  ↓
deploy (发布到Pages/PyPI)
```

### 查看测试报告

GitLab Pages URL: `https://<namespace>.gitlab.io/<project>/`

### 定时Pipeline

在GitLab项目设置 → CI/CD → Schedules中创建：

- **描述**: 每日回归测试
- **间隔**: `0 2 * * *` (每天凌晨2点)
- **目标分支**: `main`
- **变量**: 可添加特定的测试变量

---

## Jenkins

### 快速开始

#### 1. 创建Pipeline任务

1. 登录Jenkins
2. 点击"新建任务"
3. 选择"Pipeline"
4. 配置Pipeline

#### 2. 配置Pipeline

**Definition**: Pipeline script from SCM

**SCM**: Git
- Repository URL: `https://github.com/your-org/your-repo.git`
- Branch: `*/main`
- Script Path: `Jenkinsfile`

#### 3. 配置凭据

在Jenkins凭据管理中添加：

| ID | 类型 | 说明 |
|----|-----|------|
| `database-credentials` | Username with password | 数据库凭据 |
| `api-token` | Secret text | API令牌 |
| `dingtalk-webhook` | Secret text | 钉钉Webhook |

#### 4. 安装必要的插件

- Allure Plugin
- HTML Publisher Plugin
- Email Extension Plugin
- Pipeline Plugin

### Pipeline参数

可在构建时配置的参数：

| 参数 | 类型 | 默认值 | 说明 |
|-----|------|--------|------|
| `TEST_ENV` | Choice | test | 测试环境 |
| `RUN_INTEGRATION_TESTS` | Boolean | true | 是否运行集成测试 |
| `GENERATE_ALLURE_REPORT` | Boolean | true | 是否生成Allure报告 |

### 触发器配置

**定时构建**:
```groovy
triggers {
    cron('0 2 * * *')  // 每天凌晨2点
}
```

**轮询SCM**:
```groovy
triggers {
    pollSCM('H/15 * * * *')  // 每15分钟检查一次
}
```

---

## Docker支持

### 使用Docker运行测试

#### 构建测试镜像

```bash
cd docker
docker build -t my-test-env:latest -f Dockerfile ..
```

#### 运行测试

```bash
docker run --rm \
  -v $(pwd):/app \
  -e HTTP_BASE_URL=https://api.example.com \
  my-test-env:latest \
  pytest tests/ --verbose
```

### 使用Docker Compose

#### 启动完整测试环境

```bash
# 启动所有服务（PostgreSQL + Redis）
docker-compose up -d

# 运行测试
docker-compose run test-runner pytest tests/ -v

# 查看日志
docker-compose logs -f test-runner

# 停止服务
docker-compose down
```

#### 使用MySQL而非PostgreSQL

```bash
docker-compose --profile mysql up -d
```

#### 启动Allure报告服务

```bash
docker-compose --profile allure up -d
# 访问 http://localhost:5050
```

### 本地CI环境

完全模拟CI环境运行测试：

```bash
# 1. 构建镜像
docker-compose build

# 2. 运行完整测试套件
docker-compose run test-runner pytest tests/ \
  --verbose \
  --cov=. \
  --cov-report=html \
  --alluredir=reports/allure-results

# 3. 生成报告
docker-compose --profile allure up -d

# 4. 访问报告
open http://localhost:5050
```

---

## 最佳实践

### 1. 环境隔离

```python
# conftest.py
import pytest

@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """确保测试环境隔离"""
    import os
    os.environ["TEST_MODE"] = "true"
    # 使用独立的测试数据库
    os.environ["DB_NAME"] = "test_db"
```

### 2. 标记测试

```python
import pytest

@pytest.mark.smoke
def test_critical_path():
    """冒烟测试 - CI中快速运行"""
    pass

@pytest.mark.integration
def test_with_database():
    """集成测试 - 需要外部服务"""
    pass

@pytest.mark.skip_scheduled
def test_manual_only():
    """手动测试 - 跳过定时任务"""
    pass
```

**CI配置**:
```bash
# 只运行冒烟测试（快速反馈）
pytest -m smoke

# 跳过定时任务测试
pytest -m "not skip_scheduled"
```

### 3. 依赖缓存

**GitHub Actions**:
```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/uv
    key: ${{ runner.os }}-uv-${{ hashFiles('requirements.txt') }}
```

**GitLab CI**:
```yaml
cache:
  paths:
    - .cache/pip
    - .cache/uv
```

### 4. 并行执行

使用pytest-xdist加速测试：

```bash
# 安装
pip install pytest-xdist

# 运行（使用所有CPU核心）
pytest -n auto

# CI配置
pytest -n 4  # 使用4个进程
```

### 5. 失败重试

```python
# conftest.py
import pytest

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    """失败时自动重试"""
    if call.excinfo is not None:
        # 重试逻辑
        pass
```

或使用pytest-rerunfailures：

```bash
pip install pytest-rerunfailures
pytest --reruns 3 --reruns-delay 1
```

### 6. 测试数据管理

```python
# 使用fixture提供测试数据
@pytest.fixture
def test_data():
    return {
        "user": {"name": "test", "email": "test@example.com"},
        "api_key": os.environ.get("API_KEY")
    }
```

---

## 常见问题

### Q1: GitHub Actions中如何使用私有PyPI源？

在`.github/workflows/test.yml`中：

```yaml
- name: 配置私有PyPI
  run: |
    pip config set global.index-url https://pypi.your-company.com/simple/
    pip config set global.trusted-host pypi.your-company.com
```

### Q2: 如何在CI中运行UI测试？

确保安装Playwright并启用headless模式：

```yaml
- name: 安装Playwright
  run: |
    pip install playwright
    playwright install --with-deps chromium

- name: 运行UI测试
  run: pytest tests/ui/ --headed=false
```

### Q3: 测试失败时如何保存截图？

在`conftest.py`中：

```python
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        # 保存截图
        if hasattr(item, 'funcargs') and 'page' in item.funcargs:
            page = item.funcargs['page']
            page.screenshot(path=f"reports/screenshots/{item.name}.png")
```

### Q4: 如何配置钉钉通知？

获取钉钉机器人Webhook后，在CI平台添加为Secret，然后：

```bash
curl -X POST "$DINGTALK_WEBHOOK" \
  -H 'Content-Type: application/json' \
  -d '{
    "msgtype": "markdown",
    "markdown": {
      "title": "测试结果",
      "text": "### 测试完成 ✅\n\n**项目**: My Project"
    }
  }'
```

### Q5: 如何加速CI构建？

1. **使用缓存**: 缓存pip/uv依赖
2. **并行测试**: 使用pytest-xdist
3. **增量测试**: 只测试变更的代码
4. **分层Docker镜像**: 依赖层单独缓存
5. **选择性运行**: 使用test markers

### Q6: 数据库迁移如何处理？

在CI中添加迁移步骤：

```yaml
- name: 运行数据库迁移
  run: |
    # 使用Alembic
    alembic upgrade head

    # 或使用Django
    python manage.py migrate
```

---

## 相关资源

- [GitHub Actions文档](https://docs.github.com/en/actions)
- [GitLab CI文档](https://docs.gitlab.com/ee/ci/)
- [Jenkins Pipeline文档](https://www.jenkins.io/doc/book/pipeline/)
- [Allure报告](https://docs.qameta.io/allure/)
- [Pytest文档](https://docs.pytest.org/)

---

**返回**: [用户指南](README.md) | [文档首页](../README.md)
