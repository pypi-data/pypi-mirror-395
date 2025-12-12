"""Paginated workouts response model."""

from __future__ import annotations

from typing import List

from pydantic import BaseModel

from .workout import Workout

__all__ = ["PaginatedWorkouts"]


class PaginatedWorkouts(BaseModel):
    """Paginated response for workout list queries.

    Attributes:
        page: Current page number (1-indexed).
        page_count: Total number of pages available.
        workouts: List of workouts in the current page.
    """

    page: int
    page_count: int
    workouts: List[Workout]
