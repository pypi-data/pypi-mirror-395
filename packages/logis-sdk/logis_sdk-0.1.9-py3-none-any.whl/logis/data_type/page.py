from typing import Generic, TypeVar

from pydantic import AliasChoices, BaseModel, Field

from .base import DEFAULT_PYDANTIC_MODEL_CONFIG

T = TypeVar("T")


class Pager(BaseModel):
    page_base: int | None = Field(
        default=0, validation_alias=AliasChoices("page_base", "pageBase")
    )
    page_size: int = Field(
        default=100, validation_alias=AliasChoices("page_size", "pageSize")
    )
    page_at: int = Field(
        default=0, validation_alias=AliasChoices("page_at", "pageAt", "page")
    )
    total: int | None = None

    model_config = DEFAULT_PYDANTIC_MODEL_CONFIG

    @property
    def offset(self) -> int:
        return max(0, self.page_at - self.page_base) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size


class PageResult(Pager, Generic[T]):
    items: list[T]

    @staticmethod
    def of_page[T](page: Pager, items: list[T], total: int) -> "PageResult[T]":
        return PageResult[T](
            items=items,
            total=total,
            page_at=page.page_at,
            page_base=page.page_base,
            page_size=page.page_size,
        )

    model_config = DEFAULT_PYDANTIC_MODEL_CONFIG


class TableQuery(Pager):
    database: str | None = None
    table: str

    model_config = DEFAULT_PYDANTIC_MODEL_CONFIG
