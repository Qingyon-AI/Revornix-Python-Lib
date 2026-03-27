from typing import Generic, TypeVar

from pydantic import BaseModel


T = TypeVar("T")


class InfiniteScrollPagination(BaseModel, Generic[T]):
    total: int
    start: int | None = None
    limit: int
    has_more: bool
    elements: list[T]
    next_start: int | None = None


InifiniteScrollPagnition = InfiniteScrollPagination
