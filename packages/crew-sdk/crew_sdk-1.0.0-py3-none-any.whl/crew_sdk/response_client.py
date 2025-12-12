from __future__ import annotations

import datetime
import hmac
import json
from dataclasses import dataclass
from hashlib import sha256
from typing import Any, Dict, Optional

from .config import CrewhiveSDKConfig
from .http_client import create_http_client

DEFAULT_SIGNATURE_HEADER = "x-crew-signature"
DEFAULT_TIMESTAMP_HEADER = "x-crew-request-timestamp"


@dataclass
class AgentResponseClientConfig(CrewhiveSDKConfig):
    agent_id: str = ""
    secret_key: str = ""
    signature_header: Optional[str] = None
    timestamp_header: Optional[str] = None


class AgentResponseClient:
    def __init__(self, config: AgentResponseClientConfig) -> None:
        if not config.agent_id:
            raise ValueError("agent_id is required.")
        if not config.secret_key:
            raise ValueError("secret_key is required.")

        self._config = config
        self._http = create_http_client(config)
        self._signature_header = config.signature_header or DEFAULT_SIGNATURE_HEADER
        self._timestamp_header = config.timestamp_header or DEFAULT_TIMESTAMP_HEADER

    def send(self, *, session_id: Optional[str] = None, sessionId: Optional[str] = None, **response_payload: Any) -> Dict[str, Any]:
        session_value = session_id or sessionId
        if not session_value:
            raise ValueError("session_id (or sessionId) is required when sending a response back to Crewhive.")

        body_data = {
            "taskId": response_payload.get("taskId"),
            "requestId": response_payload.get("requestId"),
            "status": response_payload.get("status") or "completed",
            "result": response_payload.get("result"),
            "response": response_payload.get("response"),
            "error": response_payload.get("error"),
            "attachments": response_payload.get("attachments"),
            "meta": response_payload.get("meta"),
        }

        body_str = json.dumps(body_data, separators=(",", ":"), ensure_ascii=False)
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        signature = hmac.new(
            self._config.secret_key.encode(),
            (timestamp + body_str).encode(),
            sha256,
        ).hexdigest()

        return self._http(
            path="/api/webhooks/agent-response",
            method="POST",
            data=body_str,
            headers={
                self._signature_header: signature,
                self._timestamp_header: timestamp,
                "x-crew-agent-id": self._config.agent_id,
                "x-crew-session-id": session_value,
            },
        )


def create_agent_response_client(config: AgentResponseClientConfig) -> AgentResponseClient:
    return AgentResponseClient(config)
