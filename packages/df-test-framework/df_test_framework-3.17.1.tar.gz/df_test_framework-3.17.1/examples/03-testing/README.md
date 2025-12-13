# Pytest测试示例

本目录包含使用pytest进行测试的完整示例。

## 📋 示例列表

### 1. 配置文件 (`conftest.py`)
pytest配置和fixture定义。

**包含内容**:
- 全局fixture
- 测试配置
- 测试数据清理

### 2. API测试 (`test_api.py`)
HTTP API测试示例。

**功能展示**:
- GET/POST请求测试
- 响应断言
- 参数化测试

**运行**:
```bash
pytest examples/03-testing/test_api.py -v
```

### 3. 数据库测试 (`test_database.py`)
数据库操作测试示例。

**功能展示**:
- CRUD操作测试
- 事务测试
- 数据清理

**运行**:
```bash
pytest examples/03-testing/test_database.py -v
```

### 4. Fixture测试 (`test_with_fixtures.py`)
使用框架提供的fixture进行测试。

**功能展示**:
- 使用runtime fixture
- 使用http_client fixture
- 使用database fixture

**运行**:
```bash
pytest examples/03-testing/test_with_fixtures.py -v
```

## 🎯 运行所有测试

```bash
# 运行所有测试
pytest examples/03-testing/ -v

# 运行特定测试
pytest examples/03-testing/test_api.py::test_get_user -v

# 显示详细输出
pytest examples/03-testing/ -v -s
```

## 📚 相关文档

- [用户指南 - 使用示例](../../docs/user-guide/examples.md)
- [Pytest文档](https://docs.pytest.org/)

---

**返回**: [示例首页](../README.md)
