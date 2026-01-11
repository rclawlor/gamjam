# Standard library imports
import typing as t

# Third party imports
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from PyQt6.QtWidgets import QGridLayout, QWidget

# Local imports
from pysprite.canvas.palette import Colour, Palette
from pysprite.canvas.palette_group import PaletteGroup
from pysprite.widgets.palette import QtPalette


class QtPaletteGroup(QWidget):
    colour_update = pyqtSignal(int)
    palette_update = pyqtSignal()
    collision_selected = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._palette_group = PaletteGroup()
        self._palette_group.loaded.connect(self._palette_group_loaded)
        self.glayout = QGridLayout()

        self._palettes: list[QtPalette] = []
        self._update_palettes()

        self.glayout.setColumnStretch(0, 1)
        self.glayout.setColumnStretch(2, 1)
        self.glayout.setRowStretch(len(self._palettes), 1)
        self.setLayout(self.glayout)
        self._palettes[0].select(True)
        self._palettes[0].buttons[0].select(True)
        self.setAcceptDrops(True)

    @property
    def palette_group(self) -> PaletteGroup:
        return self._palette_group

    def _palette_group_loaded(self) -> None:
        """
        Handle new palette group
        """
        self.glayout.setRowStretch(len(self._palettes), 0)
        self._update_palettes()
        self.glayout.setRowStretch(len(self._palettes), 1)

    def _update_palettes(self) -> None:
        """
        Update previews
        """
        for idx, palette in enumerate(self._palettes):
            self.glayout.removeWidget(palette)
        self._palettes: list[QtPalette] = []
        for idx, palette in enumerate(self._palette_group.palettes):
            self._palettes.append(QtPalette(palette))
            self.glayout.addWidget(self._palettes[-1], idx, 1)
            self._palettes[-1].row_selected.connect(
                lambda x=idx: self.select_palette(x)
            )
            self._palettes[-1].colour_selected.connect(
                lambda x: self.colour_update.emit(x)
            )
            self._palettes[-1].collision_selected.connect(
                self.collision_selected.emit
            )

    def open_file(self, filename: str) -> None:
        """
        Open and load an existing `.pal` file
        """
        self._palette_group.open(filename)

    def save_file(self, filename: str) -> None:
        """
        Save to `.pal` file
        """
        self._palette_group.save(filename)

    def new_palette(self) -> None:
        """
        Create new palette
        """
        self.glayout.setRowStretch(len(self._palettes), 0)
        self._palette_group.new_palette()
        self._update_palettes()
        self.select_palette(len(self._palettes) - 1)
        self.glayout.setRowStretch(len(self._palettes), 1)

    def select_palette(self, x: int) -> None:
        """
        Select palette `x`
        """
        for idx, palette in enumerate(self._palettes):
            palette.select(idx == x)
        self.palette_update.emit()

    def get_active_palette(self) -> Palette:
        """
        Get currently active palette
        """
        for qtpalette in self._palettes:
            if qtpalette.selected:
                return qtpalette._palette
        else:
            raise IndexError("No palettes active")

    def get_active_palette_idx(self) -> int:
        """
        Get index of currently active palette
        """
        for idx, palette in enumerate(self._palettes):
            if palette.selected:
                return idx
        else:
            raise IndexError("No palettes active")

    def update_colour(self, colour: Colour) -> None:
        """
        Update currently selected colour
        """
        for qtpalette in self._palettes:
            if qtpalette.selected:
                qtpalette.update_colour(colour)
                return
        else:
            raise IndexError("No palettes active")

    def dragEnterEvent(
        self,
        a0: t.Optional[QDragEnterEvent]
    ) -> None:
        """
        Called on mouse drag
        """
        if a0 is None:
            print("aohuaoe")
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
                    pos.y() < w.y()
                ):
                    # We didn't drag past this widget.
                    # insert before it.
                    target_idx = max(n - 1, 0)
                    self._palette_group.swap_palette(source_idx, target_idx)
                    self._update_palettes()
                    self._palettes[target_idx].select(True)
                    self.palette_update.emit()
                    break

        a0.accept()
