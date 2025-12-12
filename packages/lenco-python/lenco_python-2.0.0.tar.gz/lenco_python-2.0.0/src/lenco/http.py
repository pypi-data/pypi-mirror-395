"""HTTP client for Lenco API"""

import time
from typing import Any, TypeVar

import httpx

from lenco.exceptions import (
    AuthenticationError,
    LencoError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from lenco.types import Environment

T = TypeVar("T")

BASE_URLS = {
    Environment.PRODUCTION: "https://api.lenco.co/access/v2",
    Environment.SANDBOX: "https://sandbox.lenco.co/access/v2",
}


class HttpClient:
    """Synchronous HTTP client"""

    def __init__(
        self,
        api_key: str,
        environment: Environment = Environment.PRODUCTION,
        timeout: float = 30.0,
        max_retries: int = 3,
        debug: bool = False,
    ) -> None:
        self.api_key = api_key
        self.base_url = BASE_URLS[environment]
        self.timeout = timeout
        self.max_retries = max_retries
        self.debug = debug

        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=timeout,
            headers=self._get_headers(),
        )

    def _get_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "lenco-sdk-python/2.0.0",
        }

    def _log(self, message: str, data: Any = None) -> None:
        if self.debug:
            print(f"[Lenco SDK] {message}", data or "")

    def _should_retry(self, status_code: int, attempt: int) -> bool:
        if attempt >= self.max_retries:
            return False
        return status_code >= 500 or status_code == 429

    def _get_retry_delay(self, attempt: int) -> float:
        return min(1.0 * (2**attempt), 10.0)

    def _handle_error(self, response: httpx.Response) -> None:
        try:
            data = response.json()
            message = data.get("message", "An error occurred")
        except Exception:
            message = "An error occurred"
            data = None

        status = response.status_code

        if status == 400:
            raise ValidationError(message, data)
        elif status == 401:
            raise AuthenticationError(message)
        elif status == 404:
            raise NotFoundError(message)
        elif status == 429:
            retry_after = response.headers.get("Retry-After")
            raise RateLimitError(message, int(retry_after) if retry_after else None)
        elif status >= 500:
            raise ServerError(message)
        else:
            raise LencoError(message, status, data.get("errorCode", "UNKNOWN") if data else "UNKNOWN", data)

    def request(
        self,
        method: str,
        path: str,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        attempt = 0

        # Filter out None values from params
        if params:
            params = {k: v for k, v in params.items() if v is not None}

        while True:
            try:
                self._log(f"{method} {path}", json)

                response = self._client.request(
                    method=method,
                    url=path,
                    json=json,
                    params=params,
                )

                self._log(f"Response {response.status_code}")

                if not response.is_success:
                    if self._should_retry(response.status_code, attempt):
                        delay = self._get_retry_delay(attempt)
                        self._log(f"Retrying in {delay}s (attempt {attempt + 1}/{self.max_retries})")
                        time.sleep(delay)
                        attempt += 1
                        continue
                    self._handle_error(response)

                data = response.json()
                return data.get("data")

            except httpx.RequestError as e:
                raise NetworkError(str(e)) from e

    def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        return self.request("GET", path, params=params)

    def post(self, path: str, json: dict[str, Any] | None = None) -> Any:
        return self.request("POST", path, json=json)

    def close(self) -> None:
        self._client.close()


class AsyncHttpClient:
    """Asynchronous HTTP client"""

    def __init__(
        self,
        api_key: str,
        environment: Environment = Environment.PRODUCTION,
        timeout: float = 30.0,
        max_retries: int = 3,
        debug: bool = False,
    ) -> None:
        self.api_key = api_key
        self.base_url = BASE_URLS[environment]
        self.timeout = timeout
        self.max_retries = max_retries
        self.debug = debug

        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=timeout,
            headers=self._get_headers(),
        )

    def _get_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "lenco-sdk-python/2.0.0",
        }

    def _log(self, message: str, data: Any = None) -> None:
        if self.debug:
            print(f"[Lenco SDK] {message}", data or "")

    def _should_retry(self, status_code: int, attempt: int) -> bool:
        if attempt >= self.max_retries:
            return False
        return status_code >= 500 or status_code == 429

    def _get_retry_delay(self, attempt: int) -> float:
        return min(1.0 * (2**attempt), 10.0)

    def _handle_error(self, response: httpx.Response) -> None:
        try:
            data = response.json()
            message = data.get("message", "An error occurred")
        except Exception:
            message = "An error occurred"
            data = None

        status = response.status_code

        if status == 400:
            raise ValidationError(message, data)
        elif status == 401:
            raise AuthenticationError(message)
        elif status == 404:
            raise NotFoundError(message)
        elif status == 429:
            retry_after = response.headers.get("Retry-After")
            raise RateLimitError(message, int(retry_after) if retry_after else None)
        elif status >= 500:
            raise ServerError(message)
        else:
            raise LencoError(message, status, data.get("errorCode", "UNKNOWN") if data else "UNKNOWN", data)

    async def request(
        self,
        method: str,
        path: str,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        import asyncio

        attempt = 0

        # Filter out None values from params
        if params:
            params = {k: v for k, v in params.items() if v is not None}

        while True:
            try:
                self._log(f"{method} {path}", json)

                response = await self._client.request(
                    method=method,
                    url=path,
                    json=json,
                    params=params,
                )

                self._log(f"Response {response.status_code}")

                if not response.is_success:
                    if self._should_retry(response.status_code, attempt):
                        delay = self._get_retry_delay(attempt)
                        self._log(f"Retrying in {delay}s (attempt {attempt + 1}/{self.max_retries})")
                        await asyncio.sleep(delay)
                        attempt += 1
                        continue
                    self._handle_error(response)

                data = response.json()
                return data.get("data")

            except httpx.RequestError as e:
                raise NetworkError(str(e)) from e

    async def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        return await self.request("GET", path, params=params)

    async def post(self, path: str, json: dict[str, Any] | None = None) -> Any:
        return await self.request("POST", path, json=json)

    async def close(self) -> None:
        await self._client.aclose()
