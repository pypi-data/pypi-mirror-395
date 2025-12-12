from __future__ import annotations

import secrets
from typing import Optional

from urllib.parse import quote

from .config import ensure_absolute_url


def _build_prefixed_key(prefix: str) -> str:
    token = secrets.token_hex(16)
    return f"{prefix}{token}"


def generate_secret_key(prefix: str = "sk_") -> str:
    return _build_prefixed_key(prefix)


def generate_api_key(prefix: str = "pk_") -> str:
    return _build_prefixed_key(prefix)


def build_webhook_url(agent_id: str, base_url: Optional[str] = None) -> str:
    if not agent_id:
        raise ValueError("Agent identifier is required to build a webhook URL.")
    endpoint = f"/api/webhooks/agent-response?agentId={quote(agent_id)}"
    return ensure_absolute_url(endpoint, base_url)


def generate_integration_credentials(
    *,
    agent_id: str,
    base_url: Optional[str] = None,
    api_key_prefix: str = "pk_",
    secret_key_prefix: str = "sk_",
) -> dict[str, str]:
    secret_key = generate_secret_key(secret_key_prefix)
    api_key = generate_api_key(api_key_prefix)
    webhook_url = build_webhook_url(agent_id, base_url)
    return {"secretKey": secret_key, "apiKey": api_key, "webhookUrl": webhook_url}
