from __future__ import annotations

import logging
from typing import Any, Mapping

import httpx

from .constants import get_base_url

logger = logging.getLogger(__name__)


class StreamstraightTokenError(Exception):
    """Raised when fetching a Streamstraight client token fails."""


async def fetch_client_token(options: Mapping[str, Any]) -> str:
    api_key = options.get("api_key")
    if not isinstance(api_key, str) or not api_key:
        raise ValueError("api_key is required")

    base_url = options.get("base_url") or get_base_url()

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/v1/token",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=10.0,
            )
    except httpx.HTTPError as exc:  # pragma: no cover - network failure path
        logger.error("[streamstraight] token request failed %s", exc)
        raise StreamstraightTokenError("token request failed") from exc

    if not response.is_success:
        logger.error(
            "[streamstraight] failed to fetch token status=%s body=%s",
            response.status_code,
            response.text,
        )
        raise StreamstraightTokenError(
            f"token endpoint returned {response.status_code}"
        )

    body = response.json()
    token = body.get("token")
    if isinstance(token, str) and token:
        return token

    logger.error("[streamstraight] token response missing token field: %s", body)
    raise StreamstraightTokenError("token response missing token field")
