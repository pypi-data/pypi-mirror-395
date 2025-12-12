from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from .rep_range import RepRange

__all__ = ["PostRoutinesRequestSet"]


class PostRoutinesRequestSet(BaseModel):
    type: str  # 'warmup' | 'normal' | 'failure' | 'dropset'
    weight_kg: Optional[float] = None
    reps: Optional[int] = None
    distance_meters: Optional[int] = None
    duration_seconds: Optional[int] = None
    custom_metric: Optional[float] = None
    rep_range: Optional[RepRange] = None
