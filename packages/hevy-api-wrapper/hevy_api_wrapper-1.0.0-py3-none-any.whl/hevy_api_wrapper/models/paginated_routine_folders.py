from __future__ import annotations

from typing import List

from pydantic import BaseModel

from .routine_folder import RoutineFolder

__all__ = ["PaginatedRoutineFolders"]


class PaginatedRoutineFolders(BaseModel):
    page: int
    page_count: int
    routine_folders: List[RoutineFolder]
