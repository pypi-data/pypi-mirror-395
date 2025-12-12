from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import aiohttp
from aiohttp import ClientSession, ClientTimeout

from finalsa.http import _shared as shared


class BaseAsyncHttpClient:
    """Reusable aiohttp-based HTTP client with sane defaults."""

    DEFAULT_HEADERS: Mapping[str, str] = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    def __init__(
        self,
        *,
        base_url: str | None = None,
        default_headers: Mapping[str, str] | None = None,
        timeout: float | ClientTimeout | None = None,
        default_scheme: str = "http",
        service_name: str = "finalsa-http-client",
        trust_env: bool = False,
        session: ClientSession | None = None,
    ) -> None:
        self._default_scheme = default_scheme
        self.base_url = shared.normalize_base_url(base_url, default_scheme)
        self._timeout = self._normalize_timeout(timeout)
        self._trust_env = trust_env
        self._session = session
        self._owns_session = session is None
        self._default_headers = shared.build_default_headers(
            self.DEFAULT_HEADERS,
            default_headers,
            service_name,
        )

    async def __aenter__(self) -> BaseAsyncHttpClient:
        await self._ensure_session()
        return self

    # type: ignore[override]
    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    @property
    def session(self) -> ClientSession | None:
        """Return the underlying aiohttp session, if it has been created."""
        return self._session

    @property
    def default_headers(self) -> Mapping[str, str]:
        """Return a copy of the default headers."""
        return dict(self._default_headers)

    def update_default_headers(self, headers: Mapping[str, str]) -> None:
        """Update the headers that will be sent with every request."""
        if not headers:
            return
        self._default_headers.update(headers)

    def build_url(self, path_or_url: str) -> str:
        """Resolve the final URL for a request."""
        return shared.build_url(
            path=path_or_url,
            url=None,
            base_url=self.base_url,
            default_scheme=self._default_scheme,
        )

    async def raise_for_status(self, response: aiohttp.ClientResponse) -> None:
        headers = response.headers if isinstance(
            response.headers, Mapping) else response['headers']
        if response.status < 400:
            return
        if "Content-Type" in headers and headers["Content-Type"] == "application/json":
            data = await response.json()
            shared.raise_for_response(data, response.status)
        raise shared.InternalHttpError(response.status)

    async def request(
        self,
        method: str,
        path: str | None = None,
        *,
        url: str | None = None,
        headers: Mapping[str, str] | None = None,
        params: Mapping[str, str | int | float | None] | None = None,
        json: Any | None = None,
        data: Any | None = None,
        timeout: float | ClientTimeout | None = None,
        **kwargs: Any,
    ) -> aiohttp.ClientResponse:
        """Send an HTTP request using aiohttp.ClientSession.request."""
        if path is None and url is None:
            raise ValueError("Either 'path' or 'url' must be provided.")

        session = await self._ensure_session()
        resolved_url = shared.build_url(
            path=path,
            url=url,
            base_url=self.base_url,
            default_scheme=self._default_scheme,
        )
        merged_headers = shared.merge_headers(self._default_headers, headers)
        request_timeout = self._normalize_timeout(timeout) or self._timeout
        response = await session.request(
            method.upper(),
            resolved_url,
            headers=merged_headers,
            params=params,
            json=json,
            data=data,
            timeout=request_timeout,
            **kwargs,
        )
        return response

    async def get(self, path: str, **kwargs: Any) -> aiohttp.ClientResponse:
        return await self.request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs: Any) -> aiohttp.ClientResponse:
        return await self.request("POST", path, **kwargs)

    async def put(self, path: str, **kwargs: Any) -> aiohttp.ClientResponse:
        return await self.request("PUT", path, **kwargs)

    async def patch(self, path: str, **kwargs: Any) -> aiohttp.ClientResponse:
        return await self.request("PATCH", path, **kwargs)

    async def delete(self, path: str, **kwargs: Any) -> aiohttp.ClientResponse:
        return await self.request("DELETE", path, **kwargs)

    async def close(self) -> None:
        """Close the underlying aiohttp session if we created it."""
        if self._session and self._owns_session and not self._session.closed:
            await self._session.close()
        if self._owns_session:
            self._session = None

    async def _ensure_session(self) -> ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=self._timeout,
                trust_env=self._trust_env,
                raise_for_status=self.raise_for_status,
            )
        return self._session

    def _normalize_timeout(
        self,
        timeout: float | ClientTimeout | None,
    ) -> ClientTimeout | None:
        if timeout is None:
            return None
        if isinstance(timeout, ClientTimeout):
            return timeout
        return ClientTimeout(total=timeout)
