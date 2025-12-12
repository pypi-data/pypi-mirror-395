"""Exercise template endpoint operations (sync and async)."""

from __future__ import annotations

from typing import Any, Dict, Optional

from ..errors import raise_for_status
from ..models import (
    CreateCustomExerciseRequestBody,
    CreateCustomExerciseResponse,
    ExerciseTemplate,
    PaginatedExerciseTemplates,
)


class ExerciseTemplatesSync:
    """Synchronous exercise template endpoint operations."""

    def __init__(self, client: Any) -> None:
        self._client = client

    def get_exercise_templates(self, *, page: Optional[int] = None, page_size: int = 5) -> PaginatedExerciseTemplates:
        """List exercise templates with pagination.

        Args:
            page: Page number to retrieve (1-indexed).
            page_size: Number of templates per page (1-100).

        Returns:
            Paginated list of exercise templates.

        Raises:
            ValueError: If page_size is not between 1 and 100.
        """
        params: Dict[str, Any] = {}
        if page is not None:
            if page_size < 1 or page_size > 100:
                raise ValueError("page_size must be between 1 and 100 inclusive")
            params["page"] = page
            params["pageSize"] = page_size
        resp = self._client._request("GET", "/v1/exercise_templates", params=params)

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
        return PaginatedExerciseTemplates(**data)

    def create_custom_exercise(self, body: CreateCustomExerciseRequestBody) -> CreateCustomExerciseResponse:
        """Create a custom exercise template.

        Args:
            body: Custom exercise data including title, type, and muscle groups.

        Returns:
            Response containing the ID of the created custom exercise.
        """
        resp = self._client._request("POST", "/v1/exercise_templates", json=body.model_dump())

        if resp.status_code >= 400:
            try:
                data = resp.json()
                message = (data.get("message") if isinstance(data, dict) else None) or resp.text
                code = data.get("code") if isinstance(data, dict) else None
            except Exception:
                data = {}
                message = resp.text
                code = None
            raise_for_status(
                status_code=resp.status_code,
                message=message,
                error_code=code,
                details=data,
                request_id=None,
            )

        content_type = resp.headers.get("content-type", "")

        if "application/json" in content_type:
            data = resp.json()
            return CreateCustomExerciseResponse(**data)
        else:
            return CreateCustomExerciseResponse(id=resp.text)

    def get_exercise_template(self, exercise_template_id: str) -> ExerciseTemplate:
        """Get a single exercise template by ID.

        Args:
            exercise_template_id: Unique exercise template identifier.

        Returns:
            The exercise template details.
        """
        resp = self._client._request("GET", f"/v1/exercise_templates/{exercise_template_id}")

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
        return ExerciseTemplate(**data)


class ExerciseTemplatesAsync:
    """Asynchronous exercise template endpoint operations."""

    def __init__(self, client: Any) -> None:
        self._client = client

    async def get_exercise_templates(
        self, *, page: Optional[int] = None, page_size: int = 5
    ) -> PaginatedExerciseTemplates:
        """List exercise templates with pagination.

        Args:
            page: Page number to retrieve (1-indexed).
            page_size: Number of templates per page (1-100).

        Returns:
            Paginated list of exercise templates.

        Raises:
            ValueError: If page_size is not between 1 and 100.
        """
        params: Dict[str, Any] = {}
        if page is not None:
            if page_size < 1 or page_size > 100:
                raise ValueError("page_size must be between 1 and 100 inclusive")
            params["page"] = page
            params["pageSize"] = page_size
        resp = await self._client._request("GET", "/v1/exercise_templates", params=params)

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
        return PaginatedExerciseTemplates(**data)

    async def create_custom_exercise(self, body: CreateCustomExerciseRequestBody) -> CreateCustomExerciseResponse:
        """Create a custom exercise template.

        Args:
            body: Custom exercise data including title, type, and muscle groups.

        Returns:
            Response containing the ID of the created custom exercise.
        """
        resp = await self._client._request("POST", "/v1/exercise_templates", json=body.model_dump())

        if resp.status_code >= 400:
            try:
                data = resp.json()
                message = (data.get("message") if isinstance(data, dict) else None) or resp.text
                code = data.get("code") if isinstance(data, dict) else None
            except Exception:
                data = {}
                message = resp.text
                code = None
            raise_for_status(
                status_code=resp.status_code,
                message=message,
                error_code=code,
                details=data,
                request_id=None,
            )

        content_type = resp.headers.get("content-type", "")

        if "application/json" in content_type:
            data = resp.json()
            return CreateCustomExerciseResponse(**data)
        else:
            return CreateCustomExerciseResponse(id=resp.text)

    async def get_exercise_template(self, exercise_template_id: str) -> ExerciseTemplate:
        """Get a single exercise template by ID.

        Args:
            exercise_template_id: Unique exercise template identifier.

        Returns:
            The exercise template details.
        """
        resp = await self._client._request("GET", f"/v1/exercise_templates/{exercise_template_id}")
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
        return ExerciseTemplate(**data)
