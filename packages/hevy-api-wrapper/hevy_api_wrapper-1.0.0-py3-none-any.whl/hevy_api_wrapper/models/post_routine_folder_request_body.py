from __future__ import annotations

from pydantic import BaseModel

from .post_routine_folder import PostRoutineFolder

__all__ = ["PostRoutineFolderRequestBody"]


class PostRoutineFolderRequestBody(BaseModel):
    routine_folder: PostRoutineFolder
