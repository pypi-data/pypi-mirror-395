"""Hevy API client implementations (sync and async)."""

from __future__ import annotations

import asyncio
import os
import time
from dataclasses import dataclass
from typing import Any, Optional, cast

import httpx

from . import endpoints as _endpoints

DEFAULT_BASE_URL = "https://api.hevyapp.com/"
DEFAULT_API_KEY_HEADER = "api-key"


@dataclass
class ClientConfig:
    """Configuration options for Hevy API clients.

    Attributes:
        base_url: Base URL for the Hevy API.
        api_key: API key for authentication.
        api_key_header: Header name for the API key.
        timeout: Request timeout in seconds.
        max_retries: Maximum number of retry attempts for failed requests.
        backoff_factor: Multiplier for exponential backoff between retries.
    """

    base_url: str = DEFAULT_BASE_URL
    api_key: Optional[str] = None
    api_key_header: str = DEFAULT_API_KEY_HEADER
    timeout: float = 30.0
    max_retries: int = 3
    backoff_factor: float = 0.5


class _BaseClient:
    """Base client with shared configuration and header building."""

    def __init__(self, *, config: ClientConfig) -> None:
        self._config = config

    @property
    def config(self) -> ClientConfig:
        return self._config

    def _build_headers(self) -> dict[str, str]:
        """Build request headers including API key authentication."""
        headers: dict[str, str] = {"accept": "application/json"}
        if self._config.api_key:
            headers[self._config.api_key_header] = self._config.api_key
        return headers


class Client(_BaseClient):
    """Synchronous Hevy API client.

    Provides access to all Hevy API endpoints with automatic retries
    and exponential backoff for rate limits and server errors.

    Attributes:
        workouts: Workout endpoint operations.
        routines: Routine endpoint operations.
        exercise_templates: Exercise template endpoint operations.
        routine_folders: Routine folder endpoint operations.
        exercise_history: Exercise history endpoint operations.
    """

    def __init__(
        self,
        *,
        base_url: str = DEFAULT_BASE_URL,
        api_key: Optional[str] = None,
        api_key_header: str = DEFAULT_API_KEY_HEADER,
        timeout: float = 30.0,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
        transport: Optional[httpx.BaseTransport] = None,
    ) -> None:
        """Initialize the synchronous client.

        Args:
            base_url: Base URL for the Hevy API.
            api_key: API key for authentication.
            api_key_header: Header name for the API key.
            timeout: Request timeout in seconds.
            max_retries: Maximum number of retry attempts.
            backoff_factor: Multiplier for exponential backoff.
            transport: Optional custom httpx transport.
        """
        super().__init__(
            config=ClientConfig(
                base_url=base_url,
                api_key=api_key,
                api_key_header=api_key_header,
                timeout=timeout,
                max_retries=max_retries,
                backoff_factor=backoff_factor,
            )
        )
        self._client = httpx.Client(
            base_url=self.config.base_url,
            timeout=self.config.timeout,
            transport=transport,
        )

        self.workouts = _endpoints.WorkoutsSync(self)
        self.routines = _endpoints.RoutinesSync(self)
        self.exercise_templates = _endpoints.ExerciseTemplatesSync(self)
        self.routine_folders = _endpoints.RoutineFoldersSync(self)
        self.exercise_history = _endpoints.ExerciseHistorySync(self)

    @classmethod
    def from_env(cls, *, env_var: str = "HEVY_API_TOKEN", **kwargs: Any) -> "Client":
        """Create client from environment variable.

        Args:
            env_var: Name of the environment variable containing the API key.
            **kwargs: Additional arguments passed to Client.__init__.

        Returns:
            Configured Client instance.
        """
        token = os.getenv(env_var)
        return cls(api_key=token, **kwargs)

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()

    def __enter__(self) -> "Client":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # type: ignore[override]
        self.close()

    def _request(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        """Execute HTTP request with automatic retries for rate limits and server errors."""
        headers = kwargs.pop("headers", {})
        merged_headers = {**self._build_headers(), **headers}

        retries = 0
        while True:
            resp = cast(
                httpx.Response,
                self._client.request(method, url, headers=merged_headers, **kwargs),
            )
            if resp.status_code in (429, 500, 502, 503, 504) and retries < self.config.max_retries:
                retries += 1
                sleep_time = self.config.backoff_factor * (2 ** (retries - 1))
                time.sleep(sleep_time)
                continue
            return resp


class AsyncClient(_BaseClient):
    """Asynchronous Hevy API client.

    Async version of the Hevy API client for use with asyncio.
    Provides the same functionality as Client but with async/await support.

    Attributes:
        workouts: Workout endpoint operations.
        routines: Routine endpoint operations.
        exercise_templates: Exercise template endpoint operations.
        routine_folders: Routine folder endpoint operations.
        exercise_history: Exercise history endpoint operations.
    """

    def __init__(
        self,
        *,
        base_url: str = DEFAULT_BASE_URL,
        api_key: Optional[str] = None,
        api_key_header: str = DEFAULT_API_KEY_HEADER,
        timeout: float = 30.0,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
        transport: Optional[httpx.AsyncBaseTransport] = None,
    ) -> None:
        """Initialize the asynchronous client.

        Args:
            base_url: Base URL for the Hevy API.
            api_key: API key for authentication.
            api_key_header: Header name for the API key.
            timeout: Request timeout in seconds.
            max_retries: Maximum number of retry attempts.
            backoff_factor: Multiplier for exponential backoff.
            transport: Optional custom httpx async transport.
        """
        super().__init__(
            config=ClientConfig(
                base_url=base_url,
                api_key=api_key,
                api_key_header=api_key_header,
                timeout=timeout,
                max_retries=max_retries,
                backoff_factor=backoff_factor,
            )
        )
        self._client = httpx.AsyncClient(
            base_url=self.config.base_url,
            timeout=self.config.timeout,
            transport=transport,
        )

        self.workouts = _endpoints.WorkoutsAsync(self)
        self.routines = _endpoints.RoutinesAsync(self)
        self.exercise_templates = _endpoints.ExerciseTemplatesAsync(self)
        self.routine_folders = _endpoints.RoutineFoldersAsync(self)
        self.exercise_history = _endpoints.ExerciseHistoryAsync(self)

    @classmethod
    def from_env(cls, *, env_var: str = "HEVY_API_TOKEN", **kwargs: Any) -> "AsyncClient":
        """Create async client from environment variable.

        Args:
            env_var: Name of the environment variable containing the API key.
            **kwargs: Additional arguments passed to AsyncClient.__init__.

        Returns:
            Configured AsyncClient instance.
        """
        token = os.getenv(env_var)
        return cls(api_key=token, **kwargs)

    async def aclose(self) -> None:
        """Close the underlying async HTTP client."""
        await self._client.aclose()

    async def __aenter__(self) -> "AsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:  # type: ignore[override]
        await self.aclose()

    async def _request(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        """Execute async HTTP request with automatic retries for rate limits and server errors."""
        headers = kwargs.pop("headers", {})
        merged_headers = {**self._build_headers(), **headers}

        retries = 0
        while True:
            resp = cast(
                httpx.Response,
                await self._client.request(method, url, headers=merged_headers, **kwargs),
            )
            if resp.status_code in (429, 500, 502, 503, 504) and retries < self.config.max_retries:
                retries += 1
                sleep_time = self.config.backoff_factor * (2 ** (retries - 1))
                await asyncio.sleep(sleep_time)
                continue
            return resp
