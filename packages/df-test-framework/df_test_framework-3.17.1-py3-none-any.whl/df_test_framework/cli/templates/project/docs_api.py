"""docs/api.md 文档模板"""

DOCS_API_TEMPLATE = """# API文档

记录测试项目涉及的API接口。

## 用户相关API

### 1. 获取用户信息

**接口**: `GET /api/users/{id}`

**请求参数**:
- `id` (path): 用户ID

**响应示例**:
```json
{
  "code": 200,
  "message": "成功",
  "data": {
    "id": 1,
    "name": "张三",
    "email": "zhangsan@example.com",
    "created_at": "2025-01-01T00:00:00Z"
  }
}
```

### 2. 创建用户

**接口**: `POST /api/users`

**请求体**:
```json
{
  "name": "张三",
  "email": "zhangsan@example.com",
  "password": "password123"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "创建成功",
  "data": {
    "id": 1,
    "name": "张三",
    "email": "zhangsan@example.com"
  }
}
```

## TODO

- [ ] 补充更多API接口文档
- [ ] 添加错误码说明
- [ ] 添加认证说明
"""

__all__ = ["DOCS_API_TEMPLATE"]
