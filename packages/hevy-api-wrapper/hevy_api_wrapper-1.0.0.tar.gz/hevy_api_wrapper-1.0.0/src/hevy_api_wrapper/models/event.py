from __future__ import annotations

from typing import Annotated, Union

from pydantic import Field

from .deleted_workout import DeletedWorkout
from .updated_workout import UpdatedWorkout

__all__ = ["Event"]

Event = Annotated[Union[UpdatedWorkout, DeletedWorkout], Field(discriminator="type")]
