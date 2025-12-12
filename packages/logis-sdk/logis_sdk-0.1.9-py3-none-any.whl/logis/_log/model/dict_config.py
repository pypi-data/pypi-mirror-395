import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from typing import Type

from pydantic import BaseModel, Field, field_validator

from logis.data_type import DEFAULT_PYDANTIC_MODEL_CONFIG
from logis.util.pkg_util import get_class_full_path


class LoggerDictConfig(BaseModel):
    """
    Logger配置条目
    """

    name: str
    level: int = logging.INFO
    propagate: bool = False
    handlers: list[str] = []


class HandlerDictConfig(BaseModel):
    """
    Handler配置条目
    """

    model_config = DEFAULT_PYDANTIC_MODEL_CONFIG

    name: str
    clazz: Type[logging.Handler]
    level: int = logging.INFO
    formatter: str | None = None
    filters: list[str] = []

    filename: str | None = None
    max_bytes: int | None = Field(100 * 1024 * 1024, alias="maxBytes")
    backup_count: int | None = Field(3, alias="backupCount")
    when: str | None = "d"
    encoding: str = "utf-8"

    def model_dump(self, by_alias=True, exclude_none=True, **kwargs):
        exclude = kwargs.pop("exclude", set())
        exclude.add("clazz")
        if self.clazz is RotatingFileHandler:
            exclude.update({"when"})
        elif self.clazz is TimedRotatingFileHandler:
            exclude.update({"max_bytes"})
        elif not issubclass(self.clazz, logging.FileHandler):
            exclude.update(
                {"filename", "max_bytes", "backup_count", "when", "encoding"}
            )
        class_path = get_class_full_path(self.clazz)
        return super().model_dump(
            by_alias=by_alias, exclude=exclude, exclude_none=exclude_none, **kwargs
        ) | {"class": class_path}
