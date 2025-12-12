from __future__ import annotations

from typing import List

from pydantic import BaseModel

from .exercise_template import ExerciseTemplate

__all__ = ["PaginatedExerciseTemplates"]


class PaginatedExerciseTemplates(BaseModel):
    page: int
    page_count: int
    exercise_templates: List[ExerciseTemplate]
