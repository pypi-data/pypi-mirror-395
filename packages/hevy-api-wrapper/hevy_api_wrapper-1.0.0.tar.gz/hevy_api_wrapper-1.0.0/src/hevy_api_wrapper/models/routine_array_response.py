"""Response model for POST/PUT routine operations."""

from __future__ import annotations

from typing import List

from pydantic import BaseModel

from .routine import Routine

__all__ = ["RoutineArrayResponse"]


class RoutineArrayResponse(BaseModel):
    """Response wrapper for POST/PUT routine operations.

    The API returns routines as an array even for single routine operations.
    """

    routine: List[Routine]
