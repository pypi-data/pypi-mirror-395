"""数据模型模块

提供 Pydantic 基础数据模型:
- BaseRequest: 请求基类
- BaseResponse[T]: 通用响应模型
- PageResponse[T]: 分页响应模型

注意:
- 类型和枚举请从 df_test_framework.core.types 导入
- 或直接从顶层 df_test_framework 导入
"""

from .base import BaseRequest, BaseResponse, PageResponse

__all__ = [
    "BaseRequest",
    "BaseResponse",
    "PageResponse",
]
