"""Template HTTP client for generated MCP servers.

generate-mcp copies this structure per service, substituting the SERVICE_*
placeholders from spec.yaml. All backend I/O lives here; server.py holds
only tool definitions.
"""

import os

import httpx

SERVICE_NAME = "SERVICE_NAME"  # e.g. "orders"
BASE_URL_ENV = "SERVICE_BASE_URL_ENV"  # e.g. "ORDERS_BASE_URL"
API_KEY_ENV = "SERVICE_API_KEY_ENV"  # e.g. "ORDERS_API_KEY"; None if auth.type == none
AUTH_HEADER = "SERVICE_AUTH_HEADER"  # e.g. "X-Api-Key"; from spec auth.name

DEFAULT_TIMEOUT = 10.0
MAX_RESPONSE_CHARS = 10_000


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise SystemExit(
            f"Missing required env var {name} for the {SERVICE_NAME} MCP server. "
            f"Required: {BASE_URL_ENV}" + (f", {API_KEY_ENV}" if API_KEY_ENV else "")
        )
    return value


def make_client() -> httpx.AsyncClient:
    headers = {}
    if API_KEY_ENV:
        headers[AUTH_HEADER] = _require_env(API_KEY_ENV)
    return httpx.AsyncClient(
        base_url=_require_env(BASE_URL_ENV),
        headers=headers,
        timeout=DEFAULT_TIMEOUT,
    )


async def call(
    client: httpx.AsyncClient,
    method: str,
    path: str,
    *,
    error_map: dict[int, str] | None = None,
    retry_readonly: bool = False,
    **kwargs,
) -> str:
    """Perform a request and return an agent-legible string result.

    error_map: status -> "meaning. agent_action" text taken from spec.yaml's
    errors[] entries. Unknown statuses fall back to status + truncated body.
    retry_readonly: one retry on connect errors, readonly calls only.
    """
    try:
        response = await client.request(method, path, **kwargs)
    except httpx.ConnectError:
        if not retry_readonly:
            raise
        response = await client.request(method, path, **kwargs)

    if response.is_success:
        text = response.text
        if len(text) > MAX_RESPONSE_CHARS:
            return text[:MAX_RESPONSE_CHARS] + "\n[truncated — refine your query]"
        return text

    if error_map and response.status_code in error_map:
        return f"Error {response.status_code}: {error_map[response.status_code]}"
    return f"Unexpected error {response.status_code}: {response.text[:500]}"
