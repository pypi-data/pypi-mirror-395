"""Pagination module."""

from dataclasses import dataclass
from typing import Generic, TypedDict, TypeVar

from wriftai.common_types import NotRequired

T = TypeVar("T")


# Only expose PaginatedResponse to avoid duplicate references in Sphinx docs.
# Including PaginationOptions here will cause it to appear both as
# wriftai.PaginationOptions and wriftai.pagination.PaginationOptions,
# leading to cross-reference warning
__all__ = ["PaginatedResponse"]


class PaginationOptions(TypedDict):
    """Options for pagination."""

    cursor: NotRequired[str]
    """Cursor for pagination."""
    page_size: NotRequired[int]
    """Number of items per page."""


@dataclass
class PaginatedResponse(Generic[T]):
    """Represents a paginated response."""

    items: list[T]
    """List of items returned in the current page."""
    next_cursor: str | None
    """Cursor pointing to the next page."""
    previous_cursor: str | None
    """Cursor pointing to the previous page."""
    next_url: str | None
    """URL to fetch the next page."""
    previous_url: str | None
    """URL to fetch the previous page."""
