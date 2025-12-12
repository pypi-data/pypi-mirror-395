from __future__ import annotations

from pydantic import BaseModel

from .put_routines_request_body_routine import PutRoutinesRequestBodyRoutine

__all__ = ["PutRoutinesRequestBody"]


class PutRoutinesRequestBody(BaseModel):
    routine: PutRoutinesRequestBodyRoutine
