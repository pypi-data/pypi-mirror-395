from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from .post_routines_request_set import PostRoutinesRequestSet

__all__ = ["PostRoutinesRequestExercise"]


class PostRoutinesRequestExercise(BaseModel):
    exercise_template_id: str
    superset_id: Optional[int] = None
    rest_seconds: Optional[int] = None
    notes: Optional[str] = None
    sets: List[PostRoutinesRequestSet]
