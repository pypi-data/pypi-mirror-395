from __future__ import annotations

from pydantic import BaseModel

from .post_routines_request_body_routine import PostRoutinesRequestBodyRoutine

__all__ = ["PostRoutinesRequestBody"]


class PostRoutinesRequestBody(BaseModel):
    routine: PostRoutinesRequestBodyRoutine
