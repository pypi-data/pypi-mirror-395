from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Mapping, MutableMapping, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import requests

ABSOLUTE_URL_REGEX = re.compile(r"^https?://", re.IGNORECASE)
ENV_BASE_URL_KEYS = (
  "CREWHIVE_BASE_URL",
  "NEXT_PUBLIC_APP_URL",
  "NEXT_PUBLIC_SITE_URL",
  "NEXT_PUBLIC_BASE_URL",
  "APP_URL",
)


@dataclass
class CrewhiveSDKConfig:
    """Configuration shared by the SDK clients."""

    base_url: Optional[str] = None
    default_headers: Optional[Mapping[str, str]] = None
    session: Optional["requests.Session"] = None  # type: ignore[name-defined]
    timeout: Optional[float] = None

    def headers(self) -> MutableMapping[str, str]:
        return dict(self.default_headers or {})


def resolve_base_url(override: Optional[str] = None) -> str:
    """Resolve the base Crewhive URL using an explicit override, env vars, or localhost."""

    if override and override.strip():
        return override.rstrip("/")

    for key in ENV_BASE_URL_KEYS:
        env_value = os.getenv(key)
        if env_value:
            return env_value.rstrip("/")

    return "http://localhost:3000"


def ensure_absolute_url(path_or_url: str, base_url: Optional[str] = None) -> str:
    """Convert a relative path to an absolute URL when needed."""

    if ABSOLUTE_URL_REGEX.search(path_or_url):
        return path_or_url

    resolved_base = resolve_base_url(base_url)
    prefix = "" if path_or_url.startswith("/") else "/"
    return f"{resolved_base}{prefix}{path_or_url}"


def resolve_default_headers(config: Optional[CrewhiveSDKConfig], headers: Optional[Mapping[str, str]]) -> dict[str, str]:
    merged: dict[str, str] = {"Content-Type": "application/json"}
    if config and config.default_headers:
        merged.update(config.default_headers)
    if headers:
        merged.update({key: value for key, value in headers.items() if value is not None})
    return merged
