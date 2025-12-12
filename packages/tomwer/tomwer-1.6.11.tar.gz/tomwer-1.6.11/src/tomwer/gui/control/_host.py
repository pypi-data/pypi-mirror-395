from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Host:
    name: str | None
    port: int
