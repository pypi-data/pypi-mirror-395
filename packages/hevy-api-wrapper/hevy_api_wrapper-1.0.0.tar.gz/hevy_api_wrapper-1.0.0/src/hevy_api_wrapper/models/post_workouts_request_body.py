from __future__ import annotations

from pydantic import BaseModel

from .post_workouts_request_body_workout import PostWorkoutsRequestBodyWorkout

__all__ = ["PostWorkoutsRequestBody"]


class PostWorkoutsRequestBody(BaseModel):
    workout: PostWorkoutsRequestBodyWorkout
