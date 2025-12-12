from __future__ import annotations

from pydantic import BaseModel

from .create_custom_exercise import CreateCustomExercise

__all__ = ["CreateCustomExerciseRequestBody"]


class CreateCustomExerciseRequestBody(BaseModel):
    exercise: CreateCustomExercise
