from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field

from .custom_exercise_type import CustomExerciseType
from .equipment_category import EquipmentCategory
from .muscle_group import MuscleGroup

__all__ = ["CreateCustomExercise"]


class CreateCustomExercise(BaseModel):
    title: str
    exercise_type: CustomExerciseType
    equipment_category: EquipmentCategory
    muscle_group: MuscleGroup
    other_muscles: List[MuscleGroup] = Field(default_factory=list)
