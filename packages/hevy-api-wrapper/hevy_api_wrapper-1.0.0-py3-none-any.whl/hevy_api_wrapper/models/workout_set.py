from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

__all__ = ["WorkoutSet"]


class WorkoutSet(BaseModel):
    index: int
    type: str  # 'normal' | 'warmup' | 'dropset' | 'failure'
    weight_kg: Optional[float] = None
    reps: Optional[int] = None
    distance_meters: Optional[float] = None
    duration_seconds: Optional[float] = None
    rpe: Optional[float] = None
    custom_metric: Optional[float] = None
