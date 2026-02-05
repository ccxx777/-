from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Settings:
    root_folder: Path = Path("C:/Pictures")
    interval_seconds: float = 2.0
    preload_count: int = 4


SETTINGS = Settings()
