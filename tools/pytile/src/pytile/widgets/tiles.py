# Third party imports
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QGridLayout, QWidget

# Local imports
from pysprite.canvas.canvas import Canvas
from pysprite.canvas.palette import Palette
from pysprite.canvas.spritesheet import Spritesheet
from pysprite.widgets.canvas import QtCanvasPreview


SPRITESHEET_COLUMN = 12


class QtTiles(QWidget):
    tile_selected = pyqtSignal(int)

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
        self.tile_selected.emit(self.get_active_canvas())

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
            self._previews[-1].selected.connect(lambda x=idx: self._tile_selected(x))
            self._previews[-1].update_image()

    def _tile_selected(self, idx: int) -> None:
        """
        Called if canvas selected
        """
        for i, preview in enumerate(self._previews):
            preview.select(i == idx)
        self.tile_selected.emit(idx)

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
