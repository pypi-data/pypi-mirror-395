from typing import Required

from typing_extensions import TypedDict


class PaginatedResponseBody[T](TypedDict):
    count: Required[int]
    next: Required[str | None]
    previous: Required[str | None]
    results: Required[list[T]]
