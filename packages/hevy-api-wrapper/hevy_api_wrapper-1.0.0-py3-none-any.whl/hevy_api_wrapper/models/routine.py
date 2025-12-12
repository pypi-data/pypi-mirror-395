"""Routine model."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from .routine_exercise import RoutineExercise

__all__ = ["Routine"]


class Routine(BaseModel):
    """Represents a workout routine/template.

    Attributes:
        id: Unique routine identifier.
        title: Routine title/name.
        folder_id: Optional folder ID for organization.
        updated_at: ISO 8601 timestamp of last update.
        created_at: ISO 8601 timestamp of creation.
        exercises: List of exercises in the routine.
    """

    id: str
    title: str
    folder_id: Optional[int] = None
    updated_at: str
    created_at: str
    exercises: List[RoutineExercise]
