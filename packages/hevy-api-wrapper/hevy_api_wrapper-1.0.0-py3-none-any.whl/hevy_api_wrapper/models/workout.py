"""Workout model."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from .workout_exercise import WorkoutExercise

__all__ = ["Workout"]


class Workout(BaseModel):
    """Represents a workout session.

    Attributes:
        id: Unique workout identifier.
        title: Workout title/name.
        routine_id: Associated routine ID (if any).
        description: Optional workout description.
        start_time: ISO 8601 timestamp when workout started.
        end_time: ISO 8601 timestamp when workout ended.
        updated_at: ISO 8601 timestamp of last update.
        created_at: ISO 8601 timestamp of creation.
        exercises: List of exercises performed in the workout.
    """

    id: str
    title: str
    routine_id: Optional[str] = None
    description: Optional[str] = None
    start_time: str
    end_time: str
    updated_at: str
    created_at: str
    exercises: List[WorkoutExercise]
