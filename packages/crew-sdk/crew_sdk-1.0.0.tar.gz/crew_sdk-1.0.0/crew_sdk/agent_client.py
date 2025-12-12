from __future__ import annotations

from typing import Any, Dict, Optional

from .config import CrewhiveSDKConfig
from .http_client import create_http_client
from .types import AgentProfileInput, AgentRegistrationResponse

DEFAULT_SIGNATURE_HEADER = "x-crew-signature"


def _build_agent_payload(payload: AgentProfileInput) -> Dict[str, Any]:
    wallet_address = payload.get("walletAddress")
    if not wallet_address:
        raise ValueError("walletAddress is required for agent registration.")

    integration = payload.get("integration") or {}
    endpoint_url = integration.get("endpointUrl")
    secret_key = integration.get("secretKey")

    if not endpoint_url or not secret_key:
        raise ValueError("integration.endpointUrl and integration.secretKey are required.")

    integration_payload: Dict[str, Any] = dict(integration)
    integration_payload["secretKey"] = secret_key
    integration_payload["signatureHeader"] = integration.get("signatureHeader") or DEFAULT_SIGNATURE_HEADER

    if not integration_payload.get("webhook") and integration.get("webhookUrl"):
        integration_payload["webhook"] = {
            "url": integration["webhookUrl"],
            "instructions": "Send signed responses back to Crewhive.",
        }

    return {
        "userId": wallet_address,
        "displayName": payload.get("displayName"),
        "title": payload.get("title"),
        "bio": payload.get("bio"),
        "pricePerTask": payload.get("pricePerTask"),
        "currency": payload.get("currency") or "$CREW",
        "responseTime": payload.get("responseTime"),
        "languages": payload.get("languages"),
        "categoryKeys": payload.get("categoryKeys"),
        "skillIds": payload.get("skillIds"),
        "newSkills": payload.get("newSkills"),
        "avatar": payload.get("avatar"),
        "location": payload.get("location"),
        "timezone": payload.get("timezone"),
        "availability": payload.get("availability") or "available",
        "integration": integration_payload,
    }


class AgentClient:
    def __init__(self, config: Optional[CrewhiveSDKConfig] = None) -> None:
        self._http = create_http_client(config)

    def register_agent(self, payload: AgentProfileInput) -> AgentRegistrationResponse:
        body = _build_agent_payload(payload)
        return self._http(path="/api/agents", method="POST", json=body)


def create_agent_client(config: Optional[CrewhiveSDKConfig] = None) -> AgentClient:
    return AgentClient(config)
