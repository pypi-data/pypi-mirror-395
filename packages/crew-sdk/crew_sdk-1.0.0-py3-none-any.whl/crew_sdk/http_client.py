from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Optional

import requests
from requests import Response, Session

from .config import CrewhiveSDKConfig, ensure_absolute_url, resolve_default_headers


class CrewhiveHTTPError(RuntimeError):
    """Raised when the Crewhive API responds with a non-success status."""

    def __init__(self, status_code: int, reason: str, body: str) -> None:
        message = f"HTTP {status_code}: {reason}".strip()
        if body:
            message = f"{message} {body}"
        super().__init__(message.strip())
        self.status_code = status_code
        self.reason = reason
        self.body = body


def create_http_client(config: Optional[CrewhiveSDKConfig] = None) -> Callable[..., Any]:
    """Create a thin wrapper around `requests` that matches the TS SDK ergonomics."""

    cfg = config or CrewhiveSDKConfig()
    session: Session = cfg.session or requests.Session()

    def request(
        *,
        path: str,
        method: str = "GET",
        parse_json: bool = True,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[float] = None,
        **kwargs: Any,
    ) -> Any:
        target = ensure_absolute_url(path, cfg.base_url)
        merged_headers = resolve_default_headers(cfg, headers)
        response = session.request(method=method, url=target, headers=merged_headers, timeout=timeout or cfg.timeout, **kwargs)

        if not response.ok:
            body = response.text
            raise CrewhiveHTTPError(response.status_code, response.reason or "Request failed", body)

        if not parse_json:
            return response

        if not response.content:
            return None

        try:
            return response.json()
        except json.JSONDecodeError as exc:
            raise ValueError(f"Failed to parse JSON response: {exc}") from exc

    return request
