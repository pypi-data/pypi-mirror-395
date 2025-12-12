"""Exercise template model."""

from __future__ import annotations

from typing import List

from pydantic import BaseModel

from .custom_exercise_type import CustomExerciseType
from .muscle_group import MuscleGroup

__all__ = ["ExerciseTemplate"]


class ExerciseTemplate(BaseModel):
    """Represents an exercise template from Hevy's library or custom exercises.

    Attributes:
        id: Unique exercise template identifier.
        title: Exercise name/title.
        type: Exercise type (weight_reps, bodyweight_reps, etc.).
        primary_muscle_group: Primary muscle group targeted.
        secondary_muscle_groups: List of secondary muscle groups.
        is_custom: Whether this is a user-created custom exercise.
    """

    id: str
    title: str
    type: CustomExerciseType
    primary_muscle_group: MuscleGroup
    secondary_muscle_groups: List[str] = []
    is_custom: bool
