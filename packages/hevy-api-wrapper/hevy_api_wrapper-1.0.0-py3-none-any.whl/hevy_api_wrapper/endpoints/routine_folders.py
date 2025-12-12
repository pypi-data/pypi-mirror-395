"""Routine folder endpoint operations (sync and async)."""

from __future__ import annotations

from typing import Any, Dict, Optional

from ..errors import raise_for_status
from ..models import PaginatedRoutineFolders, PostRoutineFolderRequestBody, RoutineFolder, RoutineFolderResponse


class RoutineFoldersSync:
    """Synchronous routine folder endpoint operations."""

    def __init__(self, client: Any) -> None:
        self._client = client

    def get_routine_folders(self, *, page: Optional[int] = None, page_size: int = 5) -> PaginatedRoutineFolders:
        """List routine folders with pagination.

        Args:
            page: Page number to retrieve (1-indexed).
            page_size: Number of folders per page (1-10).

        Returns:
            Paginated list of routine folders.

        Raises:
            ValueError: If page_size is not between 1 and 10.
        """
        params: Dict[str, Any] = {}
        if page is not None:
            if page_size < 1 or page_size > 10:
                raise ValueError("page_size must be between 1 and 10 inclusive")
            params["page"] = page
            params["pageSize"] = page_size
        resp = self._client._request("GET", "/v1/routine_folders", params=params)

        data = resp.json()
        if resp.status_code >= 400:
            message = (data.get("message") if isinstance(data, dict) else None) or resp.text
            code = data.get("code") if isinstance(data, dict) else None
            raise_for_status(
                status_code=resp.status_code,
                message=message,
                error_code=code,
                details=data,
                request_id=None,
            )
        return PaginatedRoutineFolders(**data)

    def create_routine_folder(self, body: PostRoutineFolderRequestBody) -> RoutineFolder:
        """Create a new routine folder.

        Args:
            body: Folder data including title.

        Returns:
            The created routine folder.
        """
        resp = self._client._request("POST", "/v1/routine_folders", json=body.model_dump())

        data = resp.json()
        if resp.status_code >= 400:
            message = (data.get("message") if isinstance(data, dict) else None) or resp.text
            code = data.get("code") if isinstance(data, dict) else None
            raise_for_status(
                status_code=resp.status_code,
                message=message,
                error_code=code,
                details=data,
                request_id=None,
            )
        return RoutineFolderResponse(**data).routine_folder

    def get_routine_folder(self, folder_id: int) -> RoutineFolder:
        """Get a single routine folder by ID.

        Args:
            folder_id: Unique folder identifier.

        Returns:
            The routine folder details.
        """
        resp = self._client._request("GET", f"/v1/routine_folders/{folder_id}")

        data = resp.json()
        if resp.status_code >= 400:
            message = (data.get("message") if isinstance(data, dict) else None) or resp.text
            code = data.get("code") if isinstance(data, dict) else None
            raise_for_status(
                status_code=resp.status_code,
                message=message,
                error_code=code,
                details=data,
                request_id=None,
            )
        return RoutineFolder(**data)


class RoutineFoldersAsync:
    """Asynchronous routine folder endpoint operations."""

    def __init__(self, client: Any) -> None:
        self._client = client

    async def get_routine_folders(self, *, page: Optional[int] = None, page_size: int = 5) -> PaginatedRoutineFolders:
        """List routine folders with pagination.

        Args:
            page: Page number to retrieve (1-indexed).
            page_size: Number of folders per page (1-10).

        Returns:
            Paginated list of routine folders.

        Raises:
            ValueError: If page_size is not between 1 and 10.
        """
        params: Dict[str, Any] = {}
        if page is not None:
            if page_size < 1 or page_size > 10:
                raise ValueError("page_size must be between 1 and 10 inclusive")
            params["page"] = page
            params["pageSize"] = page_size
        resp = await self._client._request("GET", "/v1/routine_folders", params=params)

        data = resp.json()
        if resp.status_code >= 400:
            message = (data.get("message") if isinstance(data, dict) else None) or resp.text
            code = data.get("code") if isinstance(data, dict) else None
            raise_for_status(
                status_code=resp.status_code,
                message=message,
                error_code=code,
                details=data,
                request_id=None,
            )
        return PaginatedRoutineFolders(**data)

    async def create_routine_folder(self, body: PostRoutineFolderRequestBody) -> RoutineFolder:
        """Create a new routine folder.

        Args:
            body: Folder data including title.

        Returns:
            The created routine folder.
        """
        resp = await self._client._request("POST", "/v1/routine_folders", json=body.model_dump())

        data = resp.json()
        if resp.status_code >= 400:
            message = (data.get("message") if isinstance(data, dict) else None) or resp.text
            code = data.get("code") if isinstance(data, dict) else None
            raise_for_status(
                status_code=resp.status_code,
                message=message,
                error_code=code,
                details=data,
                request_id=None,
            )
        return RoutineFolderResponse(**data).routine_folder

    async def get_routine_folder(self, folder_id: int) -> RoutineFolder:
        """Get a single routine folder by ID.

        Args:
            folder_id: Unique folder identifier.

        Returns:
            The routine folder details.
        """
        resp = await self._client._request("GET", f"/v1/routine_folders/{folder_id}")

        data = resp.json()
        if resp.status_code >= 400:
            message = (data.get("message") if isinstance(data, dict) else None) or resp.text
            code = data.get("code") if isinstance(data, dict) else None
            raise_for_status(
                status_code=resp.status_code,
                message=message,
                error_code=code,
                details=data,
                request_id=None,
            )
        return RoutineFolder(**data)
