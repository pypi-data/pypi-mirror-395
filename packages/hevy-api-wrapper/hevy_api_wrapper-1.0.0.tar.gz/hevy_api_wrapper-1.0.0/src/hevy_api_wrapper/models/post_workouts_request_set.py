from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, field_validator

__all__ = ["PostWorkoutsRequestSet"]


class PostWorkoutsRequestSet(BaseModel):
    type: str  # 'warmup' | 'normal' | 'failure' | 'dropset'
    weight_kg: Optional[float] = None
    reps: Optional[int] = None
    distance_meters: Optional[int] = None
    duration_seconds: Optional[int] = None
    custom_metric: Optional[float] = None
    rpe: Optional[float] = None

    @field_validator("rpe")
    @classmethod
    def validate_rpe_enum(cls, v: Optional[float]) -> Optional[float]:
        if v is None:
            return v
        allowed = {6, 7, 7.5, 8, 8.5, 9, 9.5, 10}
        if v not in allowed:
            raise ValueError("rpe must be one of 6,7,7.5,8,8.5,9,9.5,10")
        return v
