# 贡献指南

感谢您对 DF Test Framework 的贡献！本文档将指导您如何为框架开发做出贡献。

## 📋 目录

- [开发环境设置](#开发环境设置)
- [测试与覆盖率](#测试与覆盖率)
- [代码质量](#代码质量)
- [提交规范](#提交规范)
- [Pull Request 流程](#pull-request-流程)
- [测试编写指南](#测试编写指南)

---

## 🛠️ 开发环境设置

### 1. 克隆仓库

```bash
git clone https://github.com/yourorg/df-test-framework.git
cd df-test-framework
```

### 2. 设置开发环境

#### 2.1 依赖管理方式

框架提供两种依赖管理方式:

##### 方式1: uv sync (推荐)

`uv sync` 是现代化的依赖管理工具,特点:
- ⚡ 更快的依赖解析和安装速度
- 🔒 自动管理 `uv.lock` 锁文件,确保依赖版本一致
- 📦 自动安装 `[dependency-groups.dev]` 开发依赖
- ✅ 推荐用于**开发环境**

```bash
# 安装 uv（如果尚未安装）
pip install uv

# 基础安装（核心依赖 + dev 依赖）
uv sync

# 安装所有可选依赖（推荐用于完整开发/测试）
uv sync --all-extras

# 安装特定功能依赖（多个 --extra 可叠加）
uv sync --extra ui              # UI 测试
uv sync --extra mq              # 消息队列（Kafka/RabbitMQ/RocketMQ）
uv sync --extra opentelemetry   # OpenTelemetry 分布式追踪
uv sync --extra prometheus      # Prometheus 指标监控
uv sync --extra storage         # 存储客户端（S3/OSS）
uv sync --extra observability   # OpenTelemetry + Prometheus

# 组合安装（开发推荐）
uv sync --extra observability --extra storage
```

**重要**: `uv sync` 默认**不安装**可选依赖,需要显式指定 `--extra` 或 `--all-extras`

##### 方式2: pip install (传统方式)

适用于生产环境或需要兼容传统工具链:

```bash
# 开发环境（核心 + dev 依赖）
pip install -e ".[dev]"

# 完整安装（所有可选功能）
pip install -e ".[all,dev]"

# 特定功能组合
pip install -e ".[observability,storage,dev]"
```

### 📦 可选依赖说明

框架采用**按需安装**的设计，核心功能无需额外依赖，可选功能需要安装对应依赖组：

| 功能 | 依赖组 | 安装命令 | 包含的包 |
|-----|--------|---------|---------|
| **UI 测试** | `ui` | `uv sync --extra ui` | playwright, selenium |
| **Kafka** | `kafka` | `uv sync --extra kafka` | confluent-kafka |
| **RabbitMQ** | `rabbitmq` | `uv sync --extra rabbitmq` | pika |
| **RocketMQ** | `rocketmq` | `uv sync --extra rocketmq` | rocketmq-python-client |
| **所有消息队列** | `mq` | `uv sync --extra mq` | 所有 MQ 客户端 |
| **OpenTelemetry** | `opentelemetry` | `uv sync --extra opentelemetry` | opentelemetry-api, opentelemetry-sdk |
| **Prometheus** | `prometheus` | `uv sync --extra prometheus` | prometheus-client |
| **存储客户端** | `storage` | `uv sync --extra storage` | boto3 (S3), oss2 (OSS) |
| **可观测性** | `observability` | `uv sync --extra observability` | OpenTelemetry + Prometheus |
| **所有可选功能** | `all` | `uv sync --all-extras` | 上述所有依赖 |

**不安装可选依赖的影响**：
- ✅ **核心功能正常使用**：HTTP 客户端、数据库、测试工具等
- ⚠️ **可选功能运行时报错**：未安装依赖时使用对应功能会抛出 `ImportError`
- 💡 **按需安装即可**：只使用哪些功能就安装哪些依赖
- 🧪 **测试自动跳过**：未安装可选依赖时,相关测试会自动跳过(使用 `@pytest.mark.skipif`)

#### 2.2 CI/CD 环境配置

在 CI/CD 环境中,推荐安装必要的可选依赖以确保测试覆盖:

```yaml
# .github/workflows/test.yml 示例
- name: 同步依赖
  run: |
    # 安装核心 + dev + 可观测性 + 存储 依赖
    uv sync --extra observability --extra storage
```

**推荐 CI/CD 安装的依赖**:
- `observability`: 用于测试 OpenTelemetry 和 Prometheus 功能
- `storage`: 用于测试 S3/OSS 客户端
- 不建议在 CI 中安装 `ui` (需要浏览器) 和 `mq` (需要外部服务)

### 3. 验证安装

```bash
# 运行测试确认环境正常（使用 uv run）
uv run pytest -v

# 检查覆盖率
uv run pytest --cov=src/df_test_framework --cov-report=term
```

---

## 🧪 测试与覆盖率

### 运行测试

> **推荐使用 `uv run` 运行所有命令**

```bash
# 运行所有测试
uv run pytest -v

# 运行特定测试文件
uv run pytest tests/clients/http/test_client.py -v

# 运行特定测试类
uv run pytest tests/clients/http/test_client.py::TestHTTPClient -v

# 运行特定测试方法
uv run pytest tests/clients/http/test_client.py::TestHTTPClient::test_get_request -v

# 使用标记运行测试
uv run pytest -m smoke -v              # 只运行冒烟测试
uv run pytest -m "not slow" -v         # 排除慢速测试
```

### 生成覆盖率报告

```bash
# 生成终端覆盖率报告（显示未覆盖的行）
uv run pytest --cov=src/df_test_framework --cov-report=term-missing

# 生成 HTML 覆盖率报告
uv run pytest --cov=src/df_test_framework --cov-report=html

# 查看 HTML 报告
# Windows
start reports/coverage/index.html

# Linux/Mac
open reports/coverage/index.html
```

### 覆盖率要求

- **目标覆盖率：80%** （配置在 `pyproject.toml` 中的 `fail_under = 80`）
- 所有新增代码必须包含相应的测试
- PR 提交前确保覆盖率不低于当前水平

### 覆盖率配置

覆盖率配置在 `pyproject.toml` 中：

```toml
[tool.coverage.run]
source = ["src/df_test_framework"]
omit = [
    "*/tests/*",
    "*/__init__.py",
    "*/conftest.py",
]
branch = true

[tool.coverage.report]
fail_under = 80
precision = 2
show_missing = true
```

---

## ✅ 代码质量

### Ruff 代码检查

```bash
# 检查代码风格（使用 uv run）
uv run ruff check src/ tests/

# 自动修复可修复的问题
uv run ruff check --fix src/ tests/

# 格式化代码
uv run ruff format src/ tests/
```

### MyPy 类型检查

```bash
# 运行类型检查（使用 uv run）
uv run mypy src/

# 检查特定模块
uv run mypy src/df_test_framework/clients/
```

### 🔒 安全扫描 (v3.7+)

**提交代码前运行安全扫描** (推荐):

```bash
# Linux/Mac
bash scripts/security-scan.sh

# Windows
scripts\security-scan.bat
```

**安全扫描包含**:
- ✅ **Safety**: 依赖漏洞扫描
- ✅ **Bandit**: 代码安全审计
- ✅ **pip-audit**: 额外依赖检查
- ✅ **敏感信息检查**: 检测硬编码密码/API密钥

**CI/CD 自动扫描**:
- 所有 Push 和 PR 会自动运行安全扫描
- 每周日自动运行一次全面扫描
- 查看扫描报告: GitHub Actions → Security Scan workflow

### Pre-commit Hooks（可选）

安装 pre-commit hooks 以自动化检查：

```bash
# 安装 hooks
pre-commit install

# 手动运行所有 hooks
pre-commit run --all-files
```

---

## 📝 提交规范

### Commit Message 格式

使用语义化的 commit message 格式：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type 类型：**
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `test`: 测试相关
- `refactor`: 代码重构
- `perf`: 性能优化
- `chore`: 构建/工具链更新

**示例：**

```bash
# 新功能
git commit -m "feat(http): 添加Bearer Token拦截器"

# Bug修复
git commit -m "fix(data_generator): 修复date()方法默认参数错误"

# 测试
git commit -m "test(utils): 添加assertion.py的单元测试"

# 文档
git commit -m "docs: 添加测试开发指南"
```

---

## 🔄 Pull Request 流程

### 1. 创建功能分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

### 2. 开发与测试

- 编写代码
- 添加/更新测试
- 确保测试通过
- 检查代码覆盖率

```bash
# 运行测试（使用 uv run）
uv run pytest -v

# 检查覆盖率
uv run pytest --cov=src/df_test_framework --cov-report=term-missing

# 代码质量检查
uv run ruff check src/ tests/
uv run mypy src/
```

### 3. 提交代码

```bash
git add .
git commit -m "feat: 添加新功能"
git push origin feature/your-feature-name
```

### 4. 创建 Pull Request

在 GitHub 上创建 PR，并：
- 提供清晰的标题和描述
- 说明变更内容和影响范围
- 关联相关的 Issue（如果有）
- 确保 CI 检查通过

### 5. Code Review

- 响应审查意见
- 根据反馈进行修改
- 保持 PR 分支更新

---

## 📖 测试编写指南

### 测试文件组织

```
tests/
├── clients/
│   ├── http/
│   │   ├── test_client.py
│   │   ├── interceptors/
│   │   │   └── test_logging.py
│   │   └── ...
│   └── ...
├── utils/
│   ├── test_common.py
│   ├── test_assertion.py
│   └── ...
└── ...
```

**原则：**
- 测试目录结构镜像 `src/` 目录结构
- 测试文件命名：`test_<module_name>.py`
- 测试类命名：`Test<ClassName>` 或 `Test<FunctionGroup>`
- 测试方法命名：`test_<scenario_description>`

### 测试编写模板

```python
"""测试 module_name.py - 模块功能描述

测试覆盖:
- 功能点1
- 功能点2
- 边界条件
- 异常处理
"""

import pytest
from unittest.mock import Mock, patch
from df_test_framework.module import ClassName


class TestClassName:
    """测试 ClassName 类"""

    @pytest.fixture
    def instance(self):
        """测试实例 fixture"""
        return ClassName()

    def test_method_success(self, instance):
        """测试方法成功场景"""
        # Arrange - 准备测试数据
        input_data = "test"

        # Act - 执行测试
        result = instance.method(input_data)

        # Assert - 验证结果
        assert result == expected_value

    def test_method_with_invalid_input(self, instance):
        """测试方法异常场景"""
        with pytest.raises(ValueError, match="错误信息"):
            instance.method(invalid_input)

    @patch('df_test_framework.module.external_dependency')
    def test_method_with_mock(self, mock_dependency, instance):
        """测试使用Mock的场景"""
        mock_dependency.return_value = "mocked"

        result = instance.method_using_dependency()

        assert result == "expected"
        mock_dependency.assert_called_once()


__all__ = [
    "TestClassName",
]
```

### 测试编写最佳实践

#### 1. 使用 AAA 模式

```python
def test_example(self):
    """测试示例"""
    # Arrange - 准备测试数据和环境
    user = {"name": "Alice", "age": 25}

    # Act - 执行被测试的操作
    result = process_user(user)

    # Assert - 验证结果
    assert result["name"] == "Alice"
    assert result["age"] == 25
```

#### 2. 测试命名要清晰描述场景

```python
# ✅ 好的命名
def test_login_with_valid_credentials_returns_token(self):
    """测试使用有效凭证登录返回token"""
    pass

# ❌ 不好的命名
def test_login(self):
    pass
```

#### 3. 每个测试只验证一个行为

```python
# ✅ 好的做法
def test_create_user_returns_user_id(self):
    """测试创建用户返回用户ID"""
    user_id = create_user("Alice")
    assert user_id is not None

def test_create_user_saves_to_database(self):
    """测试创建用户保存到数据库"""
    user_id = create_user("Alice")
    assert db.get_user(user_id) is not None

# ❌ 不好的做法
def test_create_user(self):
    """测试创建用户"""
    user_id = create_user("Alice")
    assert user_id is not None
    assert db.get_user(user_id) is not None
    assert db.get_user(user_id).name == "Alice"
```

#### 4. 使用 fixtures 共享设置

```python
@pytest.fixture
def http_client(self):
    """HTTP客户端 fixture"""
    return HTTPClient(base_url="https://api.test.com")

@pytest.fixture
def mock_response(self):
    """Mock响应对象"""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {"success": True}
    return response

def test_get_request(self, http_client, mock_response):
    """测试GET请求"""
    # 使用 fixtures
    pass
```

#### 5. 测试边界条件和异常

```python
class TestUserValidation:
    """测试用户验证"""

    def test_valid_age(self):
        """测试有效年龄"""
        assert validate_age(25) is True

    def test_age_at_minimum_boundary(self):
        """测试年龄下限边界"""
        assert validate_age(18) is True

    def test_age_below_minimum(self):
        """测试年龄低于下限"""
        assert validate_age(17) is False

    def test_age_at_maximum_boundary(self):
        """测试年龄上限边界"""
        assert validate_age(100) is True

    def test_age_above_maximum(self):
        """测试年龄超过上限"""
        assert validate_age(101) is False

    def test_negative_age_raises_error(self):
        """测试负数年龄抛出异常"""
        with pytest.raises(ValueError):
            validate_age(-1)
```

#### 6. 使用参数化测试减少重复

```python
@pytest.mark.parametrize("input,expected", [
    ("my-test-project", "my_test_project"),
    ("UserLogin", "user_login"),
    ("HTTPClient", "http_client"),
    ("my_test_project", "my_test_project"),
])
def test_to_snake_case(input, expected):
    """测试转蛇形命名"""
    assert to_snake_case(input) == expected
```

#### 7. Mock 外部依赖

```python
@patch('df_test_framework.clients.http.httpx.Client')
def test_http_request_with_mock(self, mock_client):
    """测试使用Mock的HTTP请求"""
    # 配置 Mock
    mock_response = Mock()
    mock_response.status_code = 200
    mock_client.return_value.get.return_value = mock_response

    # 执行测试
    client = HTTPClient()
    response = client.get("/users")

    # 验证
    assert response.status_code == 200
    mock_client.return_value.get.assert_called_once_with("/users")
```

---

## 📊 检查清单

提交 PR 前，请确认以下检查项：

- [ ] 所有测试通过 (`uv run pytest -v`)
- [ ] 代码覆盖率 ≥ 80% (`uv run pytest --cov=src/df_test_framework --cov-report=term`)
- [ ] 代码风格检查通过 (`uv run ruff check src/ tests/`)
- [ ] 代码已格式化 (`uv run ruff format src/ tests/`)
- [ ] 类型检查通过 (`uv run mypy src/`)（如适用）
- [ ] 添加了必要的测试
- [ ] 更新了相关文档
- [ ] Commit message 遵循规范
- [ ] PR 描述清晰完整

---

## 🙋 获取帮助

- 查看 [文档](docs/README.md)
- 提交 [Issue](https://github.com/yourorg/df-test-framework/issues)
- 参考 [示例代码](examples/)
- 阅读 [测试开发文档](docs/user-guide/testing-development.md)

---

## 📄 许可证

通过贡献代码，您同意您的贡献将在 MIT 许可证下发布。
