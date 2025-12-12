from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from .workout_set import WorkoutSet

__all__ = ["WorkoutExercise"]


class WorkoutExercise(BaseModel):
    index: int
    title: str
    notes: Optional[str] = None
    exercise_template_id: str
    supersets_id: Optional[int] = None
    sets: List[WorkoutSet]
