from __future__ import annotations

from pydantic import BaseModel

__all__ = ["RoutineFolder"]


class RoutineFolder(BaseModel):
    id: int
    index: int
    title: str
    updated_at: str
    created_at: str
