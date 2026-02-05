from __future__ import annotations

from pathlib import Path

SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"}


def collect_image_groups(root: Path) -> list[list[Path]]:
    if not root.exists():
        return []

    folders = [p for p in root.iterdir() if p.is_dir()]
    if not folders:
        folders = [root]

    groups: list[list[Path]] = []
    for folder in sorted(folders):
        images = [p for p in folder.iterdir() if p.suffix.lower() in SUPPORTED_EXTS]
        images = sorted(images)
        if images:
            groups.append(images)

    return groups
