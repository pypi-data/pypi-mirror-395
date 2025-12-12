from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from .post_workouts_request_set import PostWorkoutsRequestSet

__all__ = ["PostWorkoutsRequestExercise"]


class PostWorkoutsRequestExercise(BaseModel):
    exercise_template_id: str
    superset_id: Optional[int] = None
    notes: Optional[str] = None
    sets: List[PostWorkoutsRequestSet]
