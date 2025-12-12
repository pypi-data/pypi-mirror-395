from __future__ import annotations

from enum import Enum

__all__ = ["EquipmentCategory"]


class EquipmentCategory(str, Enum):
    none = "none"
    barbell = "barbell"
    dumbbell = "dumbbell"
    kettlebell = "kettlebell"
    machine = "machine"
    plate = "plate"
    resistance_band = "resistance_band"
    suspension = "suspension"
    other = "other"
