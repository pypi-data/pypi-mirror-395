"""Routine endpoint operations (sync and async)."""

from __future__ import annotations

from typing import Any, Dict, Optional

from ..errors import raise_for_status
from ..models import (
    PaginatedRoutines,
    PostRoutinesRequestBody,
    PutRoutinesRequestBody,
    Routine,
    RoutineArrayResponse,
    RoutineResponse,
)


class RoutinesSync:
    """Synchronous routine endpoint operations."""

    def __init__(self, client: Any) -> None:
        self._client = client

    def get_routines(self, *, page: Optional[int] = None, page_size: int = 5) -> PaginatedRoutines:
        """List routines with pagination.

        Args:
            page: Page number to retrieve (1-indexed).
            page_size: Number of routines per page (1-10).

        Returns:
            Paginated list of routines.

        Raises:
            ValueError: If page_size is not between 1 and 10.
        """
        params: Dict[str, Any] = {}
        if page is not None:
            if page_size < 1 or page_size > 10:
                raise ValueError("page_size must be between 1 and 10 inclusive")
            params["page"] = page
            params["pageSize"] = page_size
        resp = self._client._request("GET", "/v1/routines", params=params)

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
        return PaginatedRoutines(**data)

    def create_routine(self, body: PostRoutinesRequestBody) -> Routine:
        """Create a new routine.

        Args:
            body: Routine data including title, exercises, and sets.

        Returns:
            The created routine.
        """
        resp = self._client._request("POST", "/v1/routines", json=body.model_dump())

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
        return RoutineArrayResponse(**data).routine[0]

    def get_routine(self, routine_id: str) -> RoutineResponse:
        """Get a single routine by ID.

        Args:
            routine_id: Unique routine identifier.

        Returns:
            The routine details wrapped in a response object.
        """
        resp = self._client._request("GET", f"/v1/routines/{routine_id}")

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
        return RoutineResponse(**data)

    def update_routine(self, routine_id: str, body: PutRoutinesRequestBody) -> Routine:
        """Update an existing routine.

        Args:
            routine_id: Unique routine identifier.
            body: Updated routine data.

        Returns:
            The updated routine.
        """
        resp = self._client._request("PUT", f"/v1/routines/{routine_id}", json=body.model_dump())

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
        return RoutineArrayResponse(**data).routine[0]


class RoutinesAsync:
    """Asynchronous routine endpoint operations."""

    def __init__(self, client: Any) -> None:
        self._client = client

    async def get_routines(self, *, page: Optional[int] = None, page_size: int = 5) -> PaginatedRoutines:
        """List routines with pagination.

        Args:
            page: Page number to retrieve (1-indexed).
            page_size: Number of routines per page (1-10).

        Returns:
            Paginated list of routines.

        Raises:
            ValueError: If page_size is not between 1 and 10.
        """
        params: Dict[str, Any] = {}
        if page is not None:
            if page_size < 1 or page_size > 10:
                raise ValueError("page_size must be between 1 and 10 inclusive")
            params["page"] = page
            params["pageSize"] = page_size
        resp = await self._client._request("GET", "/v1/routines", params=params)

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
        return PaginatedRoutines(**data)

    async def create_routine(self, body: PostRoutinesRequestBody) -> Routine:
        """Create a new routine.

        Args:
            body: Routine data including title, exercises, and sets.

        Returns:
            The created routine.
        """
        resp = await self._client._request("POST", "/v1/routines", json=body.model_dump())

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
        return RoutineArrayResponse(**data).routine[0]

    async def get_routine(self, routine_id: str) -> RoutineResponse:
        """Get a single routine by ID.

        Args:
            routine_id: Unique routine identifier.

        Returns:
            The routine details wrapped in a response object.
        """
        resp = await self._client._request("GET", f"/v1/routines/{routine_id}")

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
        return RoutineResponse(**data)

    async def update_routine(self, routine_id: str, body: PutRoutinesRequestBody) -> Routine:
        """Update an existing routine.

        Args:
            routine_id: Unique routine identifier.
            body: Updated routine data.

        Returns:
            The updated routine.
        """
        resp = await self._client._request("PUT", f"/v1/routines/{routine_id}", json=body.model_dump())

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
        return RoutineArrayResponse(**data).routine[0]
