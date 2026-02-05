from __future__ import annotations

from pathlib import Path

SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"}


def collect_image_paths(root: Path) -> list[Path]:
    if not root.exists():
        return []
    folders = [p for p in root.iterdir() if p.is_dir()]
    if not folders:
        folders = [root]

    paths: list[Path] = []
    for folder in sorted(folders):
        images = [p for p in folder.iterdir() if p.suffix.lower() in SUPPORTED_EXTS]
        paths.extend(sorted(images))
    return paths
