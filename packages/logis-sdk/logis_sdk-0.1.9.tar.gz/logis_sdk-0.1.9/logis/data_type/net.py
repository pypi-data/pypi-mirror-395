import logging
from typing import Generic, Literal

import requests
from pydantic import BaseModel

from .base import DEFAULT_PYDANTIC_MODEL_CONFIG, T


class ApiError(BaseModel):
    code: int = -1
    message: str = "错误"


class ApiResponse(BaseModel, Generic[T]):

    success: bool
    data: T | None = None
    error: ApiError | str | None = None
    message: str | None = None
    extra: dict | None = None

    model_config = DEFAULT_PYDANTIC_MODEL_CONFIG

    @staticmethod
    def positive[T](data: T, **kwargs):
        return ApiResponse[T](success=True, data=data, **kwargs)

    @staticmethod
    def negative(error: ApiError | str, **kwargs):
        return ApiResponse[None](success=False, error=error, **kwargs)

    @staticmethod
    def from_http_response(
        r: requests.Response, content_type: Literal["json", "text"] | None = None
    ):
        ct = content_type or r.headers.get("content-type") or ""
        try:
            data = r.json() if "json" in ct else r.text
        except Exception as e:
            logging.warning("解析响应体失败: %s", e)
            data = r.text
        return (
            ApiResponse.positive(data)
            if r.status_code == 200
            else ApiResponse.negative(
                ApiError(code=r.status_code, message=str(r.status_code))
            )
        )
