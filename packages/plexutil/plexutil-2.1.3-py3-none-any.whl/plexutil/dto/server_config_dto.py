from __future__ import annotations

from dataclasses import dataclass


# Frozen=True creates an implicit hash method, eq is created by default
@dataclass(frozen=True)
class ServerConfigDTO:
    host: str | None = None
    port: int | None = None
    token: str | None = None
