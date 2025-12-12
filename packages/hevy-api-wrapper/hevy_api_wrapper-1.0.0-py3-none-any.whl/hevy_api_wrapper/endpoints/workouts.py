"""Workout endpoint operations (sync and async)."""

from __future__ import annotations

from typing import Any, Dict, Optional

from ..errors import raise_for_status
from ..models import PaginatedWorkoutEvents, PaginatedWorkouts, PostWorkoutsRequestBody, Workout


class WorkoutsSync:
    """Synchronous workout endpoint operations."""

    def __init__(self, client: Any) -> None:
        self._client = client

    def get_workouts(self, *, page: Optional[int] = None, page_size: int = 5) -> PaginatedWorkouts:
        """List workouts with pagination.

        Args:
            page: Page number to retrieve (1-indexed).
            page_size: Number of workouts per page (1-10).

        Returns:
            Paginated list of workouts.

        Raises:
            ValueError: If page_size is not between 1 and 10.
        """
        params: Dict[str, Any] = {}
        if page is not None:
            if page_size < 1 or page_size > 10:
                raise ValueError("page_size must be between 1 and 10 inclusive")
            params["page"] = page
            params["pageSize"] = page_size
        resp = self._client._request("GET", "/v1/workouts", params=params)

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
        return PaginatedWorkouts(**data)

    def create_workout(self, body: PostWorkoutsRequestBody) -> Workout:
        """Create a new workout.

        Args:
            body: Workout data including exercises and sets.

        Returns:
            The created workout.
        """
        resp = self._client._request("POST", "/v1/workouts", json=body.model_dump(exclude_none=True))

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
        if isinstance(data, dict) and "workout" in data:
            workout_data = data["workout"]
            if isinstance(workout_data, list) and len(workout_data) > 0:
                return Workout(**workout_data[0])
            return Workout(**workout_data)
        return Workout(**data)

    def get_workout(self, workout_id: str) -> Workout:
        """Get a single workout by ID.

        Args:
            workout_id: Unique workout identifier.

        Returns:
            The workout details.
        """
        resp = self._client._request("GET", f"/v1/workouts/{workout_id}")

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
        return Workout(**data)

    def update_workout(self, workout_id: str, body: PostWorkoutsRequestBody) -> Workout:
        """Update an existing workout.

        Args:
            workout_id: Unique workout identifier.
            body: Updated workout data.

        Returns:
            The updated workout.
        """
        resp = self._client._request("PUT", f"/v1/workouts/{workout_id}", json=body.model_dump(exclude_none=True))

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
        if isinstance(data, dict) and "workout" in data:
            workout_data = data["workout"]
            if isinstance(workout_data, list) and len(workout_data) > 0:
                return Workout(**workout_data[0])
            return Workout(**workout_data)
        return Workout(**data)

    def get_events(
        self,
        *,
        page: Optional[int] = None,
        page_size: int = 5,
        since: str = "1970-01-01T00:00:00Z",
    ) -> PaginatedWorkoutEvents:
        """Get workout change events since a timestamp.

        Args:
            page: Page number to retrieve (1-indexed).
            page_size: Number of events per page (1-10).
            since: ISO 8601 timestamp to fetch events from (defaults to epoch).

        Returns:
            Paginated list of workout events (updated/deleted).

        Raises:
            ValueError: If page_size is not between 1 and 10.
        """
        params: Dict[str, Any] = {}
        if page is not None:
            if page_size < 1 or page_size > 10:
                raise ValueError("page_size must be between 1 and 10 inclusive")
            params["page"] = page
            params["pageSize"] = page_size
        params["since"] = since
        resp = self._client._request("GET", "/v1/workouts/events", params=params)

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
        return PaginatedWorkoutEvents(**data)

    def get_count(self) -> int:
        """Get the total count of workouts for the user.

        Returns:
            Total number of workouts.
        """
        resp = self._client._request("GET", "/v1/workouts/count")

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
        return int(data.get("workout_count", 0))


class WorkoutsAsync:
    """Asynchronous workout endpoint operations."""

    def __init__(self, client: Any) -> None:
        self._client = client

    async def get_workouts(self, *, page: Optional[int] = None, page_size: int = 5) -> PaginatedWorkouts:
        """List workouts with pagination.

        Args:
            page: Page number to retrieve (1-indexed).
            page_size: Number of workouts per page (1-10).

        Returns:
            Paginated list of workouts.

        Raises:
            ValueError: If page_size is not between 1 and 10.
        """
        params: Dict[str, Any] = {}
        if page is not None:
            if page_size < 1 or page_size > 10:
                raise ValueError("page_size must be between 1 and 10 inclusive")
            params["page"] = page
            params["pageSize"] = page_size
        resp = await self._client._request("GET", "/v1/workouts", params=params)

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
        return PaginatedWorkouts(**data)

    async def create_workout(self, body: PostWorkoutsRequestBody) -> Workout:
        """Create a new workout.

        Args:
            body: Workout data including exercises and sets.

        Returns:
            The created workout.
        """
        resp = await self._client._request("POST", "/v1/workouts", json=body.model_dump(exclude_none=True))

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
        if isinstance(data, dict) and "workout" in data:
            workout_data = data["workout"]
            if isinstance(workout_data, list) and len(workout_data) > 0:
                return Workout(**workout_data[0])
            return Workout(**workout_data)
        return Workout(**data)

    async def get_workout(self, workout_id: str) -> Workout:
        """Get a single workout by ID.

        Args:
            workout_id: Unique workout identifier.

        Returns:
            The workout details.
        """
        resp = await self._client._request("GET", f"/v1/workouts/{workout_id}")

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
        return Workout(**data)

    async def update_workout(self, workout_id: str, body: PostWorkoutsRequestBody) -> Workout:
        """Update an existing workout.

        Args:
            workout_id: Unique workout identifier.
            body: Updated workout data.

        Returns:
            The updated workout.
        """
        resp = await self._client._request("PUT", f"/v1/workouts/{workout_id}", json=body.model_dump(exclude_none=True))

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
        if isinstance(data, dict) and "workout" in data:
            workout_data = data["workout"]
            if isinstance(workout_data, list) and len(workout_data) > 0:
                return Workout(**workout_data[0])
            return Workout(**workout_data)
        return Workout(**data)

    async def get_events(
        self,
        *,
        page: Optional[int] = None,
        page_size: int = 5,
        since: str = "1970-01-01T00:00:00Z",
    ) -> PaginatedWorkoutEvents:
        """Get workout change events since a timestamp.

        Args:
            page: Page number to retrieve (1-indexed).
            page_size: Number of events per page (1-10).
            since: ISO 8601 timestamp to fetch events from (defaults to epoch).

        Returns:
            Paginated list of workout events (updated/deleted).

        Raises:
            ValueError: If page_size is not between 1 and 10.
        """
        params: Dict[str, Any] = {}
        if page is not None:
            if page_size < 1 or page_size > 10:
                raise ValueError("page_size must be between 1 and 10 inclusive")
            params["page"] = page
            params["pageSize"] = page_size
        params["since"] = since
        resp = await self._client._request("GET", "/v1/workouts/events", params=params)

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
        return PaginatedWorkoutEvents(**data)

    async def get_count(self) -> int:
        """Get the total count of workouts for the user.

        Returns:
            Total number of workouts.
        """
        resp = await self._client._request("GET", "/v1/workouts/count")

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
        return int(data.get("workout_count", 0))
