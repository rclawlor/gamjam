# Standard library imports
import typing as t

# Third party imports
from PyQt6.QtCore import QMimeData, QPoint, QSize, Qt, pyqtSignal
from PyQt6 import QtGui
from PyQt6.QtGui import QBrush, QDrag, QImage, QPainter, QPixmap
from PyQt6.QtWidgets import QGridLayout, QLabel, QLineEdit, QWidget

# Local imports
from pysprite.canvas.canvas import TILE_PX, Canvas
from pysprite.canvas.palette import Colour, Palette
from pysprite.widgets.palette_group import QtPaletteGroup


BORDER_COLOUR = [255, 255, 0]


class QtCanvas(QLabel):
    def __init__(self, palette_group: QtPaletteGroup):
        super().__init__()
        self.mouse_clicked = False
        self._collision_mode = False
        self.mouse_button = Qt.MouseButton.LeftButton
        self.update_canvas(Canvas(palette_group.get_active_palette()))
        self._palette_group = palette_group
        self._palette_group.palette_update.connect(self.update_palette)
        self._palette_group.colour_update.connect(self.set_colour_idx)
        self.update_image()

    def set_collision_mode(self, mode: bool) -> None:
        """
        Enable/disable collision mode
        """
        self._collision_mode = mode

    def get_active_palette(self) -> Palette:
        """
        Get active palette
        """
        return self._palette_group.get_active_palette()

    def set_label(self, label: str) -> None:
        """
        Set canvas label
        """
        self.canvas.set_label(label)

    def get_label(self) -> str:
        """
        Canvas label
        """
        return self.canvas.get_label()

    def update_canvas(self, canvas: Canvas) -> None:
        """
        Update canvas
        """
        self.canvas = canvas
        self.canvas.canvasChanged.connect(self.update_image)
        self.update_image()

    def update_colour(self, colour: Colour) -> None:
        """
        Update currently selected colour
        """
        self._palette_group.update_colour(colour)
        self.update_image()

    def update_palette(self) -> None:
        """
        Update palette used in drawing
        """
        self.canvas.set_palette(self._palette_group.get_active_palette())
        self.update_image()

    def getNormalisedPos(self, pos: QPoint) -> tuple[float, float]:
        """
        Get normalised position
        """
        x, y = pos.x(), pos.y()

        img_size = self.img.size()
        xi, yi = img_size.width(), img_size.height()

        return x / xi, y / yi

    def set_colour_idx(self, idx: int) -> None:
        """
        Set brush colour
        """
        self.canvas.set_colour_idx(idx)
        self._collision_mode = False

    def get_colour_idx(self) -> int:
        """
        Get brush colour
        """
        return self.canvas.get_colour_idx()

    def newFile(self) -> None:
        """
        Create new file
        """
        self.canvas.new()

    def mousePressEvent(self, ev: t.Optional[QtGui.QMouseEvent]) -> None:
        """
        Triggered when mouse pressed
        """
        if ev is None:
            return

        x, y = self.getNormalisedPos(ev.pos())

        self.mouse_clicked = True
        self.mouse_button = ev.button()
        if self._collision_mode:
            self.canvas.draw_collision(
                x, y, self.mouse_button == Qt.MouseButton.LeftButton
            )
        else:
            self.canvas.draw_pixel(x, y)

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
            if self._collision_mode:
                self.canvas.draw_collision(
                    x, y, self.mouse_button == Qt.MouseButton.LeftButton
                )
            else:
                self.canvas.draw_pixel(x, y)

    def update_image(self) -> None:
        """
        Update image using data matrix
        """
        self.qImg = QImage(
            self.canvas.as_rgb_bytes(self._collision_mode),
            self.canvas.w,
            self.canvas.h,
            self.canvas.w * 3,
            QImage.Format.Format_RGB888
        )
        self.qImg = self.qImg.scaledToHeight(497)
        self.img = QPixmap.fromImage(self.qImg)
        painter = QPainter(self.img)
        painter.setBrush(QBrush(QtGui.QColor("#ff0000"), Qt.BrushStyle.SolidPattern))
        pen = QtGui.QPen()
        if self._collision_mode:
            pen.setColor(QtGui.QColor("#ff0000"))
            pen.setWidth(2)
            painter.setPen(pen)
            for i in range(self.canvas.h):
                for j in range(self.canvas.w):
                    if self.canvas.collision_data[j, i] == 1:
                        painter.drawLine(
                            62 * i + 6,
                            62 * j + 6,
                            62 * i + 56,
                            62 * j + 56,
                        )
                        painter.drawLine(
                            62 * i + 6,
                            62 * j + 56,
                            62 * i + 56,
                            62 * j + 6,
                        )

        pen.setColor(QtGui.QColor("#444444"))
        pen.setWidth(1)
        painter.setPen(pen)
        for x in range(0, self.img.width(), self.img.width() // TILE_PX):
            painter.drawLine(x, 0, x, self.img.height())
            painter.drawLine(0, x, self.img.width(), x)
        painter.end()
        self.setPixmap(self.img)


class QtCanvasLabel(QWidget):
    changed = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.glayout = QGridLayout()

        self.label = QLabel("Sprite ID: ")
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.line_edit = QLineEdit(parent=self)
        self.line_edit.setFixedWidth(150)
        self.line_edit.textChanged.connect(self.changed.emit)

        self.glayout.addWidget(self.label, 0, 0)
        self.glayout.addWidget(self.line_edit, 0, 1)
        self.glayout.setColumnStretch(0, 1)
        self.glayout.setColumnStretch(2, 1)
        self.setLayout(self.glayout)

    def get_label(self) -> str:
        """
        Return canvas label
        """
        return self.line_edit.text()

    def set_label(self, label: str) -> None:
        """
        Set canvas label
        """
        self.line_edit.setText(label)


class QtCanvasPreview(QLabel):
    selected = pyqtSignal()

    def __init__(self, canvas: Canvas) -> None:
        super().__init__()
        self._active = False
        self._canvas = canvas
        self._canvas.canvasChanged.connect(self.update_image)
        self.setFixedSize(QSize(32, 32))
        self.update_image()

    @property
    def active(self) -> bool:
        return self._active

    @property
    def canvas(self) -> Canvas:
        return self._canvas

    def select(self, s: bool) -> None:
        """
        Select canvas
        """
        self._active = s
        self.update_image()

    def update_palette(self, palette: Palette) -> None:
        """
        Update palette for canvases
        """
        self._canvas.set_palette(palette)

    def update_image(self) -> None:
        """
        Update image using data matrix
        """
        if self._active:
            data = self._canvas.map_to_colour()
            data[:, 0] = BORDER_COLOUR
            data[:, -1] = BORDER_COLOUR
            data[0, :] = BORDER_COLOUR
            data[-1, :] = BORDER_COLOUR
            data_bytes = data.tobytes()
        else:
            data_bytes = self._canvas.as_rgb_bytes()

        self.qImg = QImage(
            data_bytes,
            self._canvas.w,
            self._canvas.h,
            self._canvas.w * 3,
            QImage.Format.Format_RGB888
        )
        self.img = QPixmap.fromImage(self.qImg)
        self.img = self.img.scaledToHeight(32)
        self.setPixmap(self.img)

    def mousePressEvent(
        self,
        ev: t.Optional[QtGui.QMouseEvent]
    ) -> None:
        """
        Called on mouse double click
        """
        self.selected.emit()

    def mouseMoveEvent(
        self,
        ev: t.Optional[QtGui.QMouseEvent]
    ) -> None:
        """
        Event triggered when element is dragged.
        """
        if ev is None:
            return

        if ev.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)

            drag.exec(Qt.DropAction.MoveAction)
