"""Fail-closed settings for the unauthenticated local prototype."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    environment: str
    allow_network_api: bool
    max_body_bytes: int

    @classmethod
    def from_env(cls) -> Settings:
        environment = os.getenv("APP_ENV", "development").lower()
        allow_network = os.getenv("ALLOW_NETWORK_API", "false").lower() == "true"
        max_body = int(os.getenv("MAX_BODY_BYTES", "525000"))
        if environment != "development" and not allow_network:
            raise RuntimeError("Unauthenticated API is disabled outside development. Set ALLOW_NETWORK_API=true only for controlled testing.")
        return cls(environment=environment, allow_network_api=allow_network, max_body_bytes=max_body)
