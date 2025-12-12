"""Muscle group enumeration."""

from __future__ import annotations

from enum import Enum

__all__ = ["MuscleGroup"]


class MuscleGroup(str, Enum):
    """Supported muscle groups in Hevy."""

    abdominals = "abdominals"
    shoulders = "shoulders"
    biceps = "biceps"
    triceps = "triceps"
    forearms = "forearms"
    quadriceps = "quadriceps"
    hamstrings = "hamstrings"
    calves = "calves"
    glutes = "glutes"
    abductors = "abductors"
    adductors = "adductors"
    lats = "lats"
    upper_back = "upper_back"
    traps = "traps"
    lower_back = "lower_back"
    chest = "chest"
    cardio = "cardio"
    neck = "neck"
    full_body = "full_body"
    other = "other"
