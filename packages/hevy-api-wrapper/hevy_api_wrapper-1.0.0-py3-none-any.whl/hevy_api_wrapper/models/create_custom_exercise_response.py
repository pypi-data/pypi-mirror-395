from __future__ import annotations

from typing import Union

from pydantic import BaseModel

__all__ = ["CreateCustomExerciseResponse"]


class CreateCustomExerciseResponse(BaseModel):
    id: Union[int, str]
