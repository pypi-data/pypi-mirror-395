from __future__ import annotations

from typing import List

from pydantic import BaseModel

from .exercise_history_entry import ExerciseHistoryEntry

__all__ = ["ExerciseHistoryResponse"]


class ExerciseHistoryResponse(BaseModel):
    exercise_history: List[ExerciseHistoryEntry]
