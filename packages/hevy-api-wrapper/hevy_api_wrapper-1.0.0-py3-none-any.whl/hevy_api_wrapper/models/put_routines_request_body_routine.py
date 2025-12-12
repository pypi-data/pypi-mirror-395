from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from .put_routines_request_exercise import PutRoutinesRequestExercise

__all__ = ["PutRoutinesRequestBodyRoutine"]


class PutRoutinesRequestBodyRoutine(BaseModel):
    title: str
    notes: Optional[str] = None
    exercises: List[PutRoutinesRequestExercise]
