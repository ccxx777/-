from __future__ import annotations

import sys
from pathlib import Path

from PySide6 import QtWidgets

from .paths import collect_image_paths
from .settings import SETTINGS
from .viewer import SlideShowWindow


def main() -> int:
    app = QtWidgets.QApplication(sys.argv)

    root = Path(SETTINGS.root_folder)
    paths = collect_image_paths(root)

    window = SlideShowWindow(paths, SETTINGS.interval_seconds, SETTINGS.preload_count)
    window.resize(1280, 720)
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
