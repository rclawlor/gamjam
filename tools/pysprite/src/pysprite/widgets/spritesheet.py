# Standard library imports
import typing as t

# Third party imports
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from PyQt6.QtWidgets import QGridLayout, QWidget

# Local imports
from pysprite.canvas.canvas import Canvas
from pysprite.canvas.palette import Palette
from pysprite.canvas.spritesheet import Spritesheet
from pysprite.widgets.canvas import QtCanvasPreview


SPRITESHEET_COLUMN = 12


class QtSpritesheet(QWidget):
    canvas_selected = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.spritesheet = Spritesheet()
        self.spritesheet.spritesheet_changed.connect(self._update_previews)
        self.spritesheet.spritesheet_loaded.connect(self._spritesheet_loaded)
        self.glayout = QGridLayout()

        self._previews: list[QtCanvasPreview] = []
        self._update_previews()
        self._previews[0].select(True)

        self.glayout.setColumnStretch(0, 1)
        self.glayout.setColumnStretch(SPRITESHEET_COLUMN, 1)
        self._update_layout()
        self.setLayout(self.glayout)
        self.setAcceptDrops(True)

    def _spritesheet_loaded(self) -> None:
        """
        Handle spritesheet loading
        """
        self._update_previews()
        self._previews[0].select(True)
        self.canvas_selected.emit()

    def _update_previews(self) -> None:
        """
        Update previews from spritesheet
        """
        for preview in self._previews:
            self.glayout.removeWidget(preview)
        self._previews: list[QtCanvasPreview] = []
        for idx, canvas in enumerate(self.spritesheet.canvases):
            self._previews.append(QtCanvasPreview(canvas))
            self.glayout.addWidget(
                self._previews[-1],
                idx // SPRITESHEET_COLUMN,
                idx % SPRITESHEET_COLUMN
            )
            self._previews[-1].selected.connect(lambda x=idx: self._canvas_selected(x))
            self._previews[-1].update_image()

    def _canvas_selected(self, idx: int) -> None:
        """
        Called if canvas selected
        """
        for i, preview in enumerate(self._previews):
            preview.select(i == idx)
        self.canvas_selected.emit()

    def _update_layout(self) -> None:
        """
        Update grid layout
        """
        for row in range(self.glayout.rowCount()):
            self.glayout.setRowStretch(row, 0)
        self.glayout.setRowStretch(self.glayout.rowCount() + 1, 1)

    def open(self, filename: str) -> None:
        """
        Open spritesheet from `.4bpp` file
        """
        self.spritesheet.open(filename)

    def save(self, filename: str) -> None:
        """
        Save data to `.4bpp` file
        """
        self.spritesheet.save(filename)

    def new_canvas(self) -> None:
        """
        Create new canvas
        """
        self.spritesheet.new_canvas()
        self._previews.append(
            QtCanvasPreview(self.spritesheet.canvases[-1])
        )
        idx = len(self._previews) - 1
        self.glayout.addWidget(
            self._previews[-1],
            idx // SPRITESHEET_COLUMN,
            idx % SPRITESHEET_COLUMN
        )
        self._previews[-1].selected.connect(lambda x=idx: self._canvas_selected(x))
        self._update_layout()
        self._canvas_selected(idx)

    def get_active_canvas(self) -> Canvas:
        """
        Return active canvas
        """
        for preview in self._previews:
            if preview.active:
                return preview._canvas
        else:
            raise IndexError("No canvases active")

    def update_palette(self, palette: Palette) -> None:
        """
        Update palette for each canvas
        """
        for preview in self._previews:
            preview.update_palette(palette)
            preview.update_image()

    def dragEnterEvent(
        self,
        a0: t.Optional[QDragEnterEvent]
    ) -> None:
        """
        Called on mouse drag
        """
        if a0 is None:
            return
        else:
            a0.accept()

    def dropEvent(
        self,
        a0: t.Optional[QDropEvent]
    ) -> None:
        """
        Called on item drop
        """
        if a0 is None:
            return
        pos = a0.position()
        widget = a0.source()

        source_idx = 0
        for n in range(self.glayout.count()):
            item = self.glayout.itemAt(n)
            if item is None:
                continue

            if widget == item.widget():
                source_idx = n
                break
        else:
            a0.ignore()
            return

        for n in range(self.glayout.count()):
            # Get the widget at each index in turn.
            item = self.glayout.itemAt(n)
            if item is None:
                continue
            else:
                w = item.widget()
            if w is not None:
                if (
                    pos.x() < w.x()
                    and abs(pos.y() - w.y()) < w.size().height()
                ):
                    # We didn't drag past this widget.
                    # insert before it.
                    target_idx = max(n - 1, 0)
                    self.spritesheet.swap_canvas(source_idx, target_idx)
                    self._update_previews()
                    self._canvas_selected(target_idx)
                    break

        a0.accept()
