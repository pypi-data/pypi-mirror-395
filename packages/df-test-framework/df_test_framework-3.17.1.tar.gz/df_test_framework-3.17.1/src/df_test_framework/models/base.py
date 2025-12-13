"""基础数据模型"""

from datetime import datetime
from typing import TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class BaseRequest(BaseModel):
    """请求基类"""

    model_config = {
        "extra": "forbid",  # 禁止额外字段
        "str_strip_whitespace": True,  # 自动去除字符串前后空格
    }


class BaseResponse[T](BaseModel):
    """
    通用响应模型

    适用于标准的API响应格式:
    {
        "success": true,
        "code": "200",
        "message": "操作成功",
        "data": {...},
        "timestamp": "2025-10-29T14:30:00"
    }
    """

    success: bool = Field(description="是否成功")
    code: str = Field(description="响应码")
    message: str = Field(description="响应消息")
    data: T | None = Field(default=None, description="响应数据")
    timestamp: datetime | None = Field(default=None, description="时间戳")

    model_config = {
        "extra": "allow",  # 允许额外字段
    }


class PageResponse[T](BaseModel):
    """
    分页响应模型

    适用于分页查询的响应:
    {
        "items": [...],
        "total": 100,
        "page": 1,
        "page_size": 20,
        "total_pages": 5
    }
    """

    items: list[T] = Field(default_factory=list, description="数据列表")
    total: int = Field(description="总记录数")
    page: int = Field(default=1, description="当前页码")
    page_size: int = Field(default=20, description="每页大小")
    total_pages: int | None = Field(default=None, description="总页数")

    model_config = {
        "extra": "allow",
    }

    def __init__(self, **data):
        super().__init__(**data)
        # 自动计算总页数
        if self.total_pages is None and self.page_size > 0:
            self.total_pages = (self.total + self.page_size - 1) // self.page_size


__all__ = ["BaseRequest", "BaseResponse", "PageResponse"]
