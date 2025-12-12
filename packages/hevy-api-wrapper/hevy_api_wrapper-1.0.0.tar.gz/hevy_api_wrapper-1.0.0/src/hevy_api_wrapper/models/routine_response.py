from __future__ import annotations

from pydantic import BaseModel

from .routine import Routine

__all__ = ["RoutineResponse"]


class RoutineResponse(BaseModel):
    routine: Routine
