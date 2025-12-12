from __future__ import annotations

import json
import hmac
from dataclasses import dataclass
from hashlib import sha256
from typing import Any, Mapping, MutableMapping, Optional

from .types import CrewAgentRequest, CrewRequestMetadata

DEFAULT_SIGNATURE_HEADER = "x-crew-signature"
DEFAULT_TIMESTAMP_HEADER = "x-crew-request-timestamp"
AGENT_HEADER = "x-crew-agent-id"
SESSION_HEADER = "x-crew-session-id"


def _normalize_headers(headers: Mapping[str, Any] | MutableMapping[str, Any] | Any) -> dict[str, str]:
    normalized: dict[str, str] = {}

    if hasattr(headers, "items"):
        iterable = headers.items()
    elif isinstance(headers, (list, tuple)):
        iterable = headers
    else:
        raise TypeError("Unsupported headers structure.")

    for key, value in iterable:
        if key is None:
            continue
        lowered = str(key).lower()

        if isinstance(value, str):
            normalized[lowered] = value
        elif isinstance(value, (list, tuple)):
            for entry in value:
                if isinstance(entry, str):
                    normalized[lowered] = entry
                    break
        elif hasattr(value, "__iter__") and not isinstance(value, (bytes, bytearray)):
            iterator = iter(value)
            for entry in iterator:
                if isinstance(entry, str):
                    normalized[lowered] = entry
                    break
        else:
            normalized[lowered] = str(value)

    return normalized


def _safe_compare(expected: str, actual: str) -> bool:
    return hmac.compare_digest(expected, actual)


@dataclass
class VerifyCrewRequestResult:
    valid: bool
    reason: Optional[str] = None
    metadata: Optional[CrewRequestMetadata] = None
    payload: Optional[dict[str, Any]] = None
    raw_body: str = ""


def verify_crew_request(
    *,
    headers: Mapping[str, Any] | MutableMapping[str, Any] | Any,
    body: str | bytes | bytearray,
    secret: str,
    signature_header: str = DEFAULT_SIGNATURE_HEADER,
    timestamp_header: str = DEFAULT_TIMESTAMP_HEADER,
    parse_body: bool = True,
) -> VerifyCrewRequestResult:
    normalized = _normalize_headers(headers)
    signature = normalized.get(signature_header.lower())
    timestamp = normalized.get(timestamp_header.lower())
    agent_id = normalized.get(AGENT_HEADER)
    session_id = normalized.get(SESSION_HEADER)
    raw_body = body.decode("utf-8") if isinstance(body, (bytes, bytearray)) else body

    if not signature or not timestamp:
        return VerifyCrewRequestResult(valid=False, reason="Missing signature headers", raw_body=raw_body)

    if not agent_id or not session_id:
        return VerifyCrewRequestResult(valid=False, reason="Missing agent or session identifiers", raw_body=raw_body)

    expected_signature = hmac.new(secret.encode(), (timestamp + raw_body).encode(), sha256).hexdigest()
    provided_signature = signature.strip().lower()

    if not _safe_compare(expected_signature, provided_signature):
        return VerifyCrewRequestResult(valid=False, reason="Invalid signature", raw_body=raw_body)

    payload: Optional[dict[str, Any]] = None
    if parse_body and raw_body:
        try:
            payload = json.loads(raw_body)
        except json.JSONDecodeError:
            return VerifyCrewRequestResult(valid=False, reason="Invalid JSON payload", raw_body=raw_body)

    metadata = CrewRequestMetadata(
        agent_id=agent_id,
        session_id=session_id,
        request_timestamp=timestamp,
        signature_header=signature_header,
    )

    return VerifyCrewRequestResult(valid=True, metadata=metadata, payload=payload, raw_body=raw_body)


def parse_crew_request(verification: VerifyCrewRequestResult) -> CrewAgentRequest:
    if not verification.valid or not verification.metadata or verification.payload is None:
        raise ValueError("Cannot parse invalid Crewhive request.")

    return CrewAgentRequest(metadata=verification.metadata, payload=verification.payload)
