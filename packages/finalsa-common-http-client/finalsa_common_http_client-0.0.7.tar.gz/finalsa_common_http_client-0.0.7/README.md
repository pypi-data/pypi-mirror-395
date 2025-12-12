# Finalsa HTTP Client

`finalsa-http-client` provides small, well-tested base classes for building HTTP
clients that share a consistent set of defaults across Finalsa services. One
implementation wraps `requests` for synchronous workloads and the other wraps
`aiohttp` for asyncio-aware code.

- Normalizes `base_url` values and fills in schemes automatically.
- Builds a predictable `User-Agent` header (e.g. `finalsa-http-client/0.0.1`).
- Merges per-request headers with service defaults.
- Manages the underlying session lifecycle (context manager friendly).
- Lets you opt into strict `raise_for_status` behavior on every request.

## Installation

```bash
python -m pip install finalsa-http-client
```

## Synchronous usage

```python
from finalsa.http.sync import BaseSyncHttpClient

with BaseSyncHttpClient(
    base_url="https://api.example.test",
    service_name="billing-api",
    default_headers={"X-App": "billing"},
    timeout=5,  # seconds
    trust_env=False,
) as client:
    response = client.post(
        "/v1/invoices",
        json={"customer_id": "cust_123", "total": 1999},
        params={"dry_run": False},
    )
    print(response.json())
```

Key synchronous notes:

- `base_url` can be provided without a scheme (`api.example.test`), the client
  will inject the configured `default_scheme` (defaults to `http`).
- Use `.build_url()` when you need the normalized URL without sending a request.
- `service_name` is used to stamp the `User-Agent`. You can still call
  `.update_default_headers()` later if you need to augment the defaults.
- Set `trust_env=False` (default is `True`) to keep the underlying `requests`
  session from honoring proxy-related environment variables.
- Pass `url="https://status.example.test/health"` to `.request()` to bypass the
  configured `base_url`.

## Asynchronous usage

```python
import asyncio

from finalsa.http.async import BaseAsyncHttpClient


async def main() -> None:
    async with BaseAsyncHttpClient(
        base_url="https://api.example.test",
        service_name="billing-api",
        trust_env=True,  # honor proxy-related env vars
        timeout=10,
    ) as client:
        response = await client.get("/v1/health", params={"extended": True})
        payload = await response.json()
        print(payload)


asyncio.run(main())
```

Asynchronous specifics:

- Timeouts accept either a float (seconds) or an explicit `aiohttp.ClientTimeout`.
- `service_name` mirrors the sync client parameter and controls the leading
  portion of the `User-Agent` header.
- `trust_env=True` allows `aiohttp` to reuse proxy / SSL options from the host
  environment.
- You can supply an existing `aiohttp.ClientSession` via the `session` keyword
  when you want to keep full control over connection pooling. The client will
  detect that it does not own the session and skip closing it.

## URL handling & headers

- Both clients share helpers in `finalsa.http._shared` for URL resolution,
  header merging, and scheme enforcement.
- Per-request headers passed to `.request()` (or `.get()`, `.post()`, etc.) are
  merged on top of the client's defaults without mutating the stored defaults.
- When neither `path` nor `url` is provided, `.request()` raises `ValueError` to
  surface misconfigurations early.

## Sessions, timeouts & errors

- Entering the client as a context manager ensures the underlying session is
  created once and cleaned up automatically. You can also call `.close()` when
  managing the lifecycle manually.
- `BaseSyncHttpClient` defaults to `raise_for_status=True` and will immediately
  raise any non-2xx response. The async variant passes the same flag through to
  `aiohttp.ClientSession`.
- Supplying your own session (`requests.Session` or `aiohttp.ClientSession`)
  allows you to plug in custom retry adapters, authentication, or tracing
  middleware while still benefiting from URL building and header management.

## Migrating from `@responses.activate`

Many of our legacy tests used the `responses` package to stub outgoing HTTP
traffic. You can keep the same ergonomics with `BaseSyncHttpClient` and adopt a
similar pattern for asyncio-based code.

### Sync tests (requests + responses)

```python
import responses
from finalsa.http.sync import BaseSyncHttpClient


@responses.activate
def test_creates_invoice() -> None:
    responses.add(
        method=responses.POST,
        url="https://api.example.test/v1/invoices",
        json={"id": "inv_123", "status": "draft"},
        status=201,
    )

    client = BaseSyncHttpClient(base_url="https://api.example.test")

    response = client.post("/v1/invoices", json={"total": 5000})

    assert response.json()["status"] == "draft"
    assert len(responses.calls) == 1
```

Nothing special is required: because the client reuses `requests.Session`, any
`responses.activate` or `responses.RequestsMock` context automatically captures
the outgoing call.

### Async tests (aiohttp + aioresponses)

Use [`aioresponses`](https://github.com/pnuckowski/aioresponses) (or your async
HTTP mock of choice) to intercept `aiohttp` traffic:

```python
import pytest
from aioresponses import aioresponses
from finalsa.http.async import BaseAsyncHttpClient


@pytest.mark.asyncio
async def test_health_check() -> None:
    client = BaseAsyncHttpClient(base_url="https://api.example.test")

    with aioresponses() as mocked:
        mocked.get(
            "https://api.example.test/v1/health",
            payload={"status": "ok"},
            status=200,
        )

        response = await client.get("/v1/health")
        assert await response.json() == {"status": "ok"}
        assert ("GET", "https://api.example.test/v1/health") in mocked.requests
```

Behind the scenes the async client creates an `aiohttp.ClientSession`, so tools
like `aioresponses`, `aresponses`, or `pytest-aiohttp` slot in naturally. For
more brittle tests you can also inject your own `ClientSession` (e.g. one backed
by a stub transport) through the `session` constructor argument.

## Development

```bash
python -m pip install -e ".[test]"
pytest
```

The test suite demonstrates additional patterns (custom timeouts, header
merging, session injection) if you need more examples. Feel free to open an
issue or pull request on GitHub with improvements or questions.