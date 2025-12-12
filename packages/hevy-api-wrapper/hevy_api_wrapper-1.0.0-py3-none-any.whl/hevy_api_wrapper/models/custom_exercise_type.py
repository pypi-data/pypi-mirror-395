"""Exercise type enumeration."""

from __future__ import annotations

from enum import Enum

__all__ = ["CustomExerciseType"]


class CustomExerciseType(str, Enum):
    """Supported exercise types in Hevy.

    Attributes:
        weight_reps: Weight-based with rep count (e.g., barbell bench press).
        reps_only: Repetition-only exercises (e.g., push-ups).
        bodyweight_reps: Bodyweight exercises with reps.
        bodyweight_assisted: Assisted bodyweight exercises (legacy).
        bodyweight_assisted_reps: Assisted bodyweight exercises.
        bodyweight_weighted: Weighted bodyweight exercises.
        duration: Time-based exercises (e.g., plank).
        weight_duration: Weight-based time exercises.
        distance_duration: Distance and time tracking (e.g., running).
        short_distance_weight: Short distance with weight (e.g., farmer's walk).
    """

    weight_reps = "weight_reps"
    reps_only = "reps_only"
    bodyweight_reps = "bodyweight_reps"
    bodyweight_assisted = "bodyweight_assisted"
    bodyweight_assisted_reps = "bodyweight_assisted_reps"
    bodyweight_weighted = "bodyweight_weighted"
    duration = "duration"
    weight_duration = "weight_duration"
    distance_duration = "distance_duration"
    short_distance_weight = "short_distance_weight"
