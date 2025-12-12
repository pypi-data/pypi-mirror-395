from __future__ import annotations

from typing import List

from pydantic import BaseModel

from .event import Event

__all__ = ["PaginatedWorkoutEvents"]


class PaginatedWorkoutEvents(BaseModel):
    page: int
    page_count: int
    events: List[Event]
