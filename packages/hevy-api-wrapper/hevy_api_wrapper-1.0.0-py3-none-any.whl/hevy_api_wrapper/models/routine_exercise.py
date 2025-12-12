from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from .routine_set import RoutineSet

__all__ = ["RoutineExercise"]


class RoutineExercise(BaseModel):
    index: int
    title: str
    rest_seconds: Optional[int] = None
    notes: Optional[str] = None
    exercise_template_id: str
    supersets_id: Optional[int] = None
    sets: List[RoutineSet]
