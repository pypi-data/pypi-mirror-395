from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

__all__ = ["ExerciseHistoryEntry"]


class ExerciseHistoryEntry(BaseModel):
    workout_id: str
    workout_title: str
    workout_start_time: str
    workout_end_time: str
    exercise_template_id: str
    weight_kg: Optional[float] = None
    reps: Optional[int] = None
    distance_meters: Optional[int] = None
    duration_seconds: Optional[int] = None
    rpe: Optional[float] = None
    custom_metric: Optional[float] = None
    set_type: str  # 'warmup' | 'normal' | 'failure' | 'dropset'
