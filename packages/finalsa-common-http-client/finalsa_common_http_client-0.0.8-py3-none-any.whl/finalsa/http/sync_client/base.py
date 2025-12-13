from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import requests

from finalsa.http import _shared as shared


class BaseSyncHttpClient:
    """Reusable requests-based HTTP client with sane defaults."""

    DEFAULT_HEADERS: Mapping[str, str] = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    def __init__(
        self,
        *,
        base_url: str | None = None,
        default_headers: Mapping[str, str] | None = None,
        timeout: float | tuple[float, float] | None = None,
        default_scheme: str = "http",
        service_name: str = "finalsa-http-client",
        trust_env: bool = True,
        raise_for_status: bool = True,
        session: requests.Session | None = None,
    ) -> None:
        self._default_scheme = default_scheme
        self.base_url = shared.normalize_base_url(base_url, default_scheme)
        self._timeout = timeout
        self._trust_env = trust_env
        self._raise_for_status = raise_for_status
        self._session = session
        self._owns_session = session is None
        self._default_headers = shared.build_default_headers(
            self.DEFAULT_HEADERS,
            default_headers,
            service_name,
        )

    def __enter__(self) -> BaseSyncHttpClient:
        self._ensure_session()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # type: ignore[override]
        self.close()

    @property
    def session(self) -> requests.Session | None:
        """Return the underlying requests session, if it has been created."""
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

    def request(
        self,
        method: str,
        path: str | None = None,
        *,
        url: str | None = None,
        headers: Mapping[str, str] | None = None,
        params: Mapping[str, str | int | float | None] | None = None,
        json: Any | None = None,
        data: Any | None = None,
        timeout: float | tuple[float, float] | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        """Send an HTTP request using requests.Session.request."""
        if path is None and url is None:
            raise ValueError("Either 'path' or 'url' must be provided.")

        session = self._ensure_session()
        resolved_url = shared.build_url(
            path=path,
            url=url,
            base_url=self.base_url,
            default_scheme=self._default_scheme,
        )
        merged_headers = shared.merge_headers(self._default_headers, headers)
        request_timeout = timeout if timeout is not None else self._timeout
        try:
            response = session.request(
                method.upper(),
                resolved_url,
                headers=merged_headers,
                params=params,
                json=json,
                data=data,
                timeout=request_timeout,
                **kwargs,
            )
            if self._raise_for_status:
                response.raise_for_status()
            return response
        except requests.RequestException as e:
            if e.response is not None and "Content-Type" in e.response.headers and e.response.headers["Content-Type"] == "application/json":
                data = e.response.json()
                shared.raise_for_response(data, e.response.status_code)
            raise e

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("DELETE", path, **kwargs)

    def close(self) -> None:
        """Close the underlying requests session if we created it."""
        if self._session and self._owns_session:
            self._session.close()
            self._session = None

    def _ensure_session(self) -> requests.Session:
        if self._session is None:
            session = requests.Session()
            session.trust_env = self._trust_env
            self._session = session
        return self._session
