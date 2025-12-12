"""API endpoint operation classes (sync and async)."""

from __future__ import annotations

from .exercise_history import ExerciseHistoryAsync, ExerciseHistorySync
from .exercise_templates import ExerciseTemplatesAsync, ExerciseTemplatesSync
from .routine_folders import RoutineFoldersAsync, RoutineFoldersSync
from .routines import RoutinesAsync, RoutinesSync
from .workouts import WorkoutsAsync, WorkoutsSync

__all__ = [
    "WorkoutsSync",
    "WorkoutsAsync",
    "RoutinesSync",
    "RoutinesAsync",
    "ExerciseTemplatesSync",
    "ExerciseTemplatesAsync",
    "RoutineFoldersSync",
    "RoutineFoldersAsync",
    "ExerciseHistorySync",
    "ExerciseHistoryAsync",
]
