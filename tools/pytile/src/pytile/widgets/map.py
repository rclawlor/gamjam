# Standard library imports
import typing as t

# Third party imports
from PyQt6.QtCore import QPoint
from PyQt6 import QtGui
from PyQt6.QtGui import QImage, QPainter, QPixmap
from PyQt6.QtWidgets import QLabel
from pysprite.canvas.canvas import TILE_PX
from pysprite.widgets.palette_group import QtPaletteGroup

# Local imports
from pytile.map.map import Map
from pytile.widgets.tiles import QtTiles


# Constants
BORDER_COLOUR = [255, 255, 0]


class QtMap(QLabel):
    def __init__(self, tiles: QtTiles, palette_group: QtPaletteGroup):
        super().__init__()
        self.mouse_clicked = False
        self.tiles = tiles
        self.tiles.tile_selected.connect(self.set_tile_idx)
        self.update_map(Map(tiles.spritesheet, palette_group.palette_group))
        self.update_image()

    def update_map(self, map: Map) -> None:
        """
        Update map
        """
        self.map = map
        self.map.mapChanged.connect(self.update_image)
        self.update_image()

    def getNormalisedPos(self, pos: QPoint) -> tuple[float, float]:
        """
        Get normalised position
        """
        x, y = pos.x(), pos.y()

        img_size = self.img.size()
        xi, yi = img_size.width(), img_size.height()

        return x / xi, y / yi

    def set_tile_idx(self, idx: int) -> None:
        """
        Set brush tile
        """
        self.map.set_tile_idx(idx)

    def get_tile_idx(self) -> int:
        """
        Get brush tile
        """
        return self.map.get_tile_idx()

    def set_palette_idx(self, idx: int) -> None:
        """
        Set brush palette
        """
        self.map.set_palette_idx(idx)

    def get_palette_idx(self) -> int:
        """
        Get brush palette
        """
        return self.map.get_palette_idx()

    def redraw_map(self) -> None:
        """
        Redraw map
        """
        self.map.redraw_map()

    def newFile(self) -> None:
        """
        Create new file
        """
        self.map.new()

    def mousePressEvent(self, ev: t.Optional[QtGui.QMouseEvent]) -> None:
        """
        Triggered when mouse pressed
        """
        if ev is None:
            return

        x, y = self.getNormalisedPos(ev.pos())

        self.mouse_clicked = True
        self.map.draw_tile(x, y)

    def mouseReleaseEvent(self, ev: t.Optional[QtGui.QMouseEvent]) -> None:
        """
        Triggered when mouse released
        """
        self.mouse_clicked = False

    def mouseMoveEvent(self, ev: t.Optional[QtGui.QMouseEvent]) -> None:
        """
        Triggered when mouse moved
        """
        if ev is None:
            return

        if self.mouse_clicked:
            x, y = self.getNormalisedPos(ev.pos())
            self.map.draw_tile(x, y)

    def update_image(self) -> None:
        """
        Update image using data matrix
        """
        self.qImg = QImage(
            self.map.as_rgb_bytes(),
            self.map.w * TILE_PX,
            self.map.h * TILE_PX,
            self.map.w * TILE_PX * 3,
            QImage.Format.Format_RGB888
        )
        self.img = QPixmap.fromImage(self.qImg)
        self.img = self.img.scaledToHeight(800)
        painter = QPainter(self.img)
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor("#444444"))
        painter.setPen(pen)
        for x in range(0, self.img.width(), self.img.width() // 39):
            painter.drawLine(x, 0, x, self.img.height())
            painter.drawLine(0, x, self.img.width(), x)
        painter.end()
        self.setPixmap(self.img)

    def open(self, filename: str) -> None:
        """
        Open map from `.map` file
        """
        self.map.open(filename)

    def save(self, filename: str) -> None:
        """
        Save map to `.map` file
        """
        self.map.save(filename)
