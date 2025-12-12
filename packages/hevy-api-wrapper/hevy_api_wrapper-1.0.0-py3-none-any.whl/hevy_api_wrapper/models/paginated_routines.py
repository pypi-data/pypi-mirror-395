from __future__ import annotations

from typing import List

from pydantic import BaseModel

from .routine import Routine

__all__ = ["PaginatedRoutines"]


class PaginatedRoutines(BaseModel):
    page: int
    page_count: int
    routines: List[Routine]
