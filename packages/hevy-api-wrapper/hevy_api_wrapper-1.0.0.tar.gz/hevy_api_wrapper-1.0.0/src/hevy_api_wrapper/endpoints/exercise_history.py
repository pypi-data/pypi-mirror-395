"""Exercise history endpoint operations (sync and async)."""

from __future__ import annotations

from typing import Any, Dict, Optional

from ..errors import raise_for_status
from ..models import ExerciseHistoryResponse


class ExerciseHistorySync:
    """Synchronous exercise history endpoint operations."""

    def __init__(self, client: Any) -> None:
        self._client = client

    def get_exercise_history(
        self,
        exercise_template_id: str,
        *,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> ExerciseHistoryResponse:
        """Get exercise history for a specific exercise template.

        Args:
            exercise_template_id: Unique exercise template identifier.
            start_date: Optional ISO 8601 start date filter.
            end_date: Optional ISO 8601 end date filter.

        Returns:
            Exercise history response with list of historical entries.
        """
        params: Dict[str, Any] = {}
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        resp = self._client._request("GET", f"/v1/exercise_history/{exercise_template_id}", params=params)

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
        return ExerciseHistoryResponse(**data)


class ExerciseHistoryAsync:
    """Asynchronous exercise history endpoint operations."""

    def __init__(self, client: Any) -> None:
        self._client = client

    async def get_exercise_history(
        self,
        exercise_template_id: str,
        *,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> ExerciseHistoryResponse:
        """Get exercise history for a specific exercise template.

        Args:
            exercise_template_id: Unique exercise template identifier.
            start_date: Optional ISO 8601 start date filter.
            end_date: Optional ISO 8601 end date filter.

        Returns:
            Exercise history response with list of historical entries.
        """
        params: Dict[str, Any] = {}
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        resp = await self._client._request("GET", f"/v1/exercise_history/{exercise_template_id}", params=params)

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
        return ExerciseHistoryResponse(**data)
