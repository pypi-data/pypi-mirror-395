import os
from typing import Optional

import requests
from dotenv import load_dotenv

from .models import SettingsConfig

load_dotenv()


_DEFAULT_HTTP_ENDPOINT = "https://orchestrator.trydojo.ai/api/v1"


def _resolve_http_endpoint() -> str:
    """Resolve the HTTP endpoint for the Dojo backend."""

    return os.getenv("DOJO_HTTP_ENDPOINT") or _DEFAULT_HTTP_ENDPOINT


def _derive_ws_endpoint(http_endpoint: str) -> str:
    """Derive a websocket endpoint from the provided HTTP endpoint."""

    if not http_endpoint:
        return "ws://localhost:8765/api/v1/jobs"

    normalized = http_endpoint.rstrip("/")
    if normalized.startswith("https://"):
        normalized = "wss://" + normalized[len("https://") :]
    elif normalized.startswith("http://"):
        normalized = "ws://" + normalized[len("http://") :]

    if not normalized.endswith("/jobs"):
        normalized = f"{normalized}/jobs"

    return normalized


def _fetch_posthog_api_key_from_url(url: str) -> Optional[str]:
    """Fetch PostHog API key from a URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        api_key = response.text.strip()
        return api_key if api_key else None
    except Exception as e:
        print(f"Failed to fetch PostHog API key from URL: {e}")
        return None


_http_endpoint = _resolve_http_endpoint()
_ws_endpoint = os.getenv("DOJO_WEBSOCKET_ENDPOINT") or _derive_ws_endpoint(_http_endpoint)
_posthog_url = os.getenv(
    "POSTHOG_API_KEY_URL", "https://dojo-shared-config.s3.us-east-1.amazonaws.com/posthog/public_project_key"
)

settings = SettingsConfig(
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
    openai_api_key=os.getenv("OPENAI_API_KEY", ""),
    openai_api_url=os.getenv("OPENAI_API_URL", ""),
    posthog_api_key=os.getenv("POSTHOG_API_KEY", ""),
    # TODO: switch to prod endpoint as default
    dojo_websocket_endpoint=_ws_endpoint,
    dojo_http_endpoint=_http_endpoint,
    engine=os.getenv("DOJO_ENGINE", "docker"),
    browserbase_concurrent_limit=int(os.getenv("BROWSERBASE_CONCURRENT_LIMIT", 1)),
)

if settings.engine != "docker" and settings.engine != "browserbase":
    raise ValueError(f"Invalid engine type: {settings.engine}")

if not settings.posthog_api_key or settings.posthog_api_key == "":
    if _posthog_url and _posthog_url != "":
        _fetched_key = _fetch_posthog_api_key_from_url(_posthog_url)
        if _fetched_key:
            settings.posthog_api_key = _fetched_key
