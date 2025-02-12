from typing import Optional, Type

from PySide6.QtCore import QPoint
from PySide6.QtGui import QPixmap, QPainter, QColor
from PySide6.QtWidgets import QLabel

from tilings.abstract.tiling import Tiling as AbstractTiling


class TileWidget(QLabel):

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.corners = []
        self._path = ""
        self._tiling_cls: Optional[Type[AbstractTiling]] = None

        self.render_window = None

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value
        self.reset_corners()

    @property
    def tiling_cls(self) -> Optional[AbstractTiling]:
        return self._tiling_cls

    @tiling_cls.setter
    def tiling_cls(self, value):
        self._tiling_cls = value

    def draw_background(self):
        pixmap = QPixmap(self.path)
        ratio = pixmap.height() / pixmap.width()
        w = self.width()
        h = int(ratio * w)
        pixmap = pixmap.scaled(w, h)
        self.setPixmap(pixmap)

    def draw_corner(self, p: QPoint) -> None:
        canvas = self.pixmap()
        painter = QPainter(canvas)
        color = QColor('red')
        painter.setPen(color)
        painter.setBrush(color)
        painter.drawEllipse(p, 3, 3)
        painter.end()
        self.setPixmap(canvas)

    def add_corner(self, p: QPoint):
        if self.tiling_cls is None:
            return

        if len(self.corners) >= self.tiling_cls.CORNER_NB:
            return

        self.corners.append(p)
        self.draw_corner(p)
        self.parent().toogle_render_btn()
        self.parent().update_status_tip()

    def reset_corners(self):
        self.corners = []
        self.parent().toogle_render_btn()
        self.parent().update_status_tip()
        self.draw_background()

    def mousePressEvent(self, event):
        self.add_corner(event.position())

    def render_tiling(self, checked: bool, resolution=None):
        self.render_window = self.tiling_cls.init(
            self.path,
            self.size(),
            self.corners,
            resolution
        )
        self.render_window.show()
