from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from .workout import Workout

__all__ = ["UpdatedWorkout"]


class UpdatedWorkout(BaseModel):
    type: Literal["updated"]
    workout: Workout
