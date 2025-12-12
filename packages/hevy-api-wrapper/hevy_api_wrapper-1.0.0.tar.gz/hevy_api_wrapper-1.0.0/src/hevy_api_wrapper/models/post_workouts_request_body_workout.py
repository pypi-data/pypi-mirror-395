from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from .post_workouts_request_exercise import PostWorkoutsRequestExercise

__all__ = ["PostWorkoutsRequestBodyWorkout"]


class PostWorkoutsRequestBodyWorkout(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: str
    routine_id: Optional[str] = None
    end_time: str
    is_private: bool
    exercises: List[PostWorkoutsRequestExercise]
