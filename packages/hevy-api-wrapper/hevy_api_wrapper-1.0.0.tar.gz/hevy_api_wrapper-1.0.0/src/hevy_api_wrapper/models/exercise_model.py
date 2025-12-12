from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from .set_model import Set

__all__ = ["Exercise"]


class Exercise(BaseModel):
    index: int
    title: str
    notes: Optional[str] = None
    exercise_template_id: str
    supersets_id: Optional[int] = None
    sets: List[Set]
