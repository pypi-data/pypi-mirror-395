from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from .post_routines_request_exercise import PostRoutinesRequestExercise

__all__ = ["PostRoutinesRequestBodyRoutine"]


class PostRoutinesRequestBodyRoutine(BaseModel):
    title: str
    folder_id: Optional[int] = None
    notes: Optional[str] = None
    exercises: List[PostRoutinesRequestExercise]
