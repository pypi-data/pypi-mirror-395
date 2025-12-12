from __future__ import annotations

from pydantic import BaseModel

__all__ = ["PostRoutineFolder"]


class PostRoutineFolder(BaseModel):
    title: str
