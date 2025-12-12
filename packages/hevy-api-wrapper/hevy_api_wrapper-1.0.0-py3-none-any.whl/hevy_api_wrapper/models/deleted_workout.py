from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

__all__ = ["DeletedWorkout"]


class DeletedWorkout(BaseModel):
    type: Literal["deleted"]
    id: str
    deleted_at: str
