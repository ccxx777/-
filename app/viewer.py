from __future__ import annotations

from pathlib import Path

from PySide6 import QtCore, QtGui, QtWidgets

from .image_cache import ImageCache


class SlideShowWindow(QtWidgets.QMainWindow):
    def __init__(self, groups: list[list[Path]], interval_seconds: float, preload_count: int) -> None:
        super().__init__()
        self.setWindowTitle("Win11 Slideshow Photos")
        self._groups = groups
        self._group_index = 0
        self._image_index = 0
        self._zoom = 1.0

        self._label = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)
        self._label.setMinimumSize(640, 360)
        self.setCentralWidget(self._label)

        self._cache = ImageCache(preload_count)
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.next_image)
        self._timer.start(int(max(0.05, interval_seconds) * 1000))

        if not self._groups:
            self._label.setText("No images found. Update app/settings.py")
        else:
            self._show_current()

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        modifiers = event.modifiers()
        delta = event.angleDelta().y()
        if modifiers & QtCore.Qt.ControlModifier:
            step = 0.1 if delta > 0 else -0.1
            self._zoom = max(0.1, min(5.0, self._zoom + step))
            self._render()
        else:
            if delta > 0:
                self.prev_image()
            else:
                self.next_image()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        self._render()

    def next_image(self) -> None:
        if not self._groups:
            return

        if self._image_index + 1 < len(self._groups[self._group_index]):
            self._image_index += 1
        else:
            self._group_index = (self._group_index + 1) % len(self._groups)
            self._image_index = 0

        self._show_current()

    def prev_image(self) -> None:
        if not self._groups:
            return

        if self._image_index > 0:
            self._image_index -= 1
        else:
            self._group_index = (self._group_index - 1) % len(self._groups)
            self._image_index = len(self._groups[self._group_index]) - 1

        self._show_current()

    def _show_current(self) -> None:
        self._preload_next()
        self._render()

    def _preload_next(self) -> None:
        if not self._groups:
            return
        lookahead = self._collect_forward_paths(self._cache.max_items)
        self._cache.preload(lookahead)

    def _collect_forward_paths(self, count: int) -> list[Path]:
        paths: list[Path] = []
        if not self._groups or count <= 0:
            return paths

        gi = self._group_index
        ii = self._image_index
        for _ in range(count):
            if ii + 1 < len(self._groups[gi]):
                ii += 1
            else:
                gi = (gi + 1) % len(self._groups)
                ii = 0
            paths.append(self._groups[gi][ii])
        return paths

    def _current_path(self) -> Path:
        return self._groups[self._group_index][self._image_index]

    def _render(self) -> None:
        if not self._groups:
            return
        path = self._current_path()
        pixmap = QtGui.QPixmap(str(path))
        if pixmap.isNull():
            self._label.setText(f"Failed to load: {path}")
            return

        target_size = self._label.size()
        if self._zoom != 1.0:
            target_size = QtCore.QSize(int(target_size.width() * self._zoom), int(target_size.height() * self._zoom))

        scaled = pixmap.scaled(target_size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self._label.setPixmap(scaled)
