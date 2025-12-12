"""Response model for routine folder operations."""

from __future__ import annotations

from pydantic import BaseModel

from .routine_folder import RoutineFolder

__all__ = ["RoutineFolderResponse"]


class RoutineFolderResponse(BaseModel):
    """Response wrapper for routine folder operations.

    The API returns the folder wrapped in a routine_folder field.
    """

    routine_folder: RoutineFolder
