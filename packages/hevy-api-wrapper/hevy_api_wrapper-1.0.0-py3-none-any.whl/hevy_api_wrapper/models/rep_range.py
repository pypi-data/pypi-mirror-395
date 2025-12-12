from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

__all__ = ["RepRange"]


class RepRange(BaseModel):
    start: Optional[float] = None
    end: Optional[float] = None
