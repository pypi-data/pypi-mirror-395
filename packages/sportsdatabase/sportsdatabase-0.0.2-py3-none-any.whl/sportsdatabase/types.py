from __future__ import annotations

from typing import Any, Dict, Literal, TypedDict


class PaginationMeta(TypedDict, total=False):
    limit: int
    cursor: str | None
    nextCursor: str | None
    previousCursor: str | None
    rateLimit: Dict[str, Any]
    requestId: str


class PaginatedResponse(TypedDict):
    data: list[Dict[str, Any]]
    meta: PaginationMeta


SportSlug = Literal["soccer", "basketball", "football", "baseball", "hockey", "cricket", "tennis", "golf"]
EventStatus = Literal["scheduled", "in_progress", "final", "postponed", "canceled"]
