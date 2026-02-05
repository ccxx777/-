from __future__ import annotations

from collections import deque
from pathlib import Path
from typing import Deque

from PIL import Image


class ImageCache:
    """Simple preload cache. Replace with async loading later."""

    def __init__(self, max_items: int = 4) -> None:
        self._max_items = max_items
        self._queue: Deque[Path] = deque()
        self._cache: dict[Path, Image.Image] = {}

    @property
    def max_items(self) -> int:
        return self._max_items

    def set_max_items(self, value: int) -> None:
        self._max_items = max(0, int(value))
        self._trim()

    def preload(self, paths: list[Path]) -> None:
        for path in paths:
            if path in self._cache:
                continue
            try:
                self._cache[path] = Image.open(path)
                self._queue.append(path)
            except Exception:
                continue
        self._trim()

    def get(self, path: Path) -> Image.Image | None:
        return self._cache.get(path)

    def _trim(self) -> None:
        while len(self._queue) > self._max_items:
            old = self._queue.popleft()
            self._cache.pop(old, None)
