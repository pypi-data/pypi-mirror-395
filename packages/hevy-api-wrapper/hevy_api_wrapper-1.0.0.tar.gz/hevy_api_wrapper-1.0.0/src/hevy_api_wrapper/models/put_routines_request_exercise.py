from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from .put_routines_request_set import PutRoutinesRequestSet

__all__ = ["PutRoutinesRequestExercise"]


class PutRoutinesRequestExercise(BaseModel):
    exercise_template_id: str
    superset_id: Optional[int] = None
    rest_seconds: Optional[int] = None
    notes: Optional[str] = None
    sets: List[PutRoutinesRequestSet]
