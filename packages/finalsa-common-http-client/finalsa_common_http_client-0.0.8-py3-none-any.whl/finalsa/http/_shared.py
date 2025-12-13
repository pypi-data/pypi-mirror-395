from __future__ import annotations

from collections.abc import Mapping
from importlib import metadata
from typing import Any, Dict
from urllib.parse import urljoin

from finalsa.common.models import BaseDomainException
from finalsa.traceability import get_w3c_traceparent, get_w3c_tracestate
from finalsa.traceability.functions import (
    HTTP_HEADER_TRACEPARENT,
    HTTP_HEADER_TRACESTATE,
)

Headers = Mapping[str, str]


class InternalHttpError(BaseDomainException):
    """Exception raised when a service is unavailable."""
    response_code = 500

    def __init__(self, response_code: int | None = None):
        super().__init__(
            message=f"Internal HTTP error: {response_code}",
            response_code=response_code or self.response_code,
            name="InternalHttpError"
        )


def normalize_base_url(
    base_url: str | None,
    default_scheme: str,
) -> str | None:
    """Return a normalized base URL or None when no usable value is provided."""
    if not base_url:
        return None
    value = base_url.strip()
    if not value:
        return None
    if "://" not in value:
        value = f"{default_scheme}://{value}"
    return value.rstrip("/")


def ensure_scheme(candidate: str, default_scheme: str) -> str:
    """Ensure that the provided candidate has an explicit scheme."""
    trimmed = candidate.strip()
    if "://" in trimmed:
        return trimmed
    return f"{default_scheme}://{trimmed}"


def build_url(
    *,
    path: str | None,
    url: str | None,
    base_url: str | None,
    default_scheme: str,
) -> str:
    """Resolve the final request URL from the supplied inputs."""
    if url:
        return ensure_scheme(url, default_scheme)

    if path is None:
        raise ValueError("Either 'path' or 'url' must be provided.")

    candidate = path.strip()
    if candidate.startswith(("http://", "https://")):
        return candidate
    if base_url:
        base = base_url if base_url.endswith("/") else f"{base_url}/"
        return urljoin(base, candidate.lstrip("/"))
    return ensure_scheme(candidate, default_scheme)


def merge_headers(
    default_headers: Mapping[str, str],
    headers: Mapping[str, str] | None,
) -> dict[str, str]:
    """Merge default headers with any per-request overrides."""
    merged = dict(default_headers)
    if headers:
        merged.update(headers)
    merged[HTTP_HEADER_TRACEPARENT] = get_w3c_traceparent()
    merged[HTTP_HEADER_TRACESTATE] = get_w3c_tracestate()
    return merged


def build_default_headers(
    default_headers: Mapping[str, str],
    user_headers: Mapping[str, str] | None,
    service_name: str,
) -> dict[str, str]:
    """Construct the default header set for an HTTP client."""
    headers = dict(default_headers)
    headers.setdefault("User-Agent", f"{service_name}/{get_package_version()}")
    if user_headers:
        headers.update(user_headers)
    return headers


def get_package_version(package_name: str = "finalsa-http-client") -> str:
    """Return the installed package version or a sensible fallback in dev mode."""
    try:
        return metadata.version(package_name)
    except metadata.PackageNotFoundError:
        return "0.0.0"


def raise_for_response(response: Dict[str, Any], status: int) -> None:
    if response.get("message") and response.get("name"):
        raise BaseDomainException(
            message=response.get("message"),
            response_code=status,
            name=response.get("name")
        )
