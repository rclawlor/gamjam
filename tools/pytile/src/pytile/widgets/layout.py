# Standard library imports
from importlib.resources import files

# Third party imports
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QGridLayout, QToolBar, QToolButton, QWidget
from PyQt6.QtCore import Qt

# Local imports
from pysprite.widgets.palette_group import QtPaletteGroup
from pysprite.widgets.palette import QtPaletteLabel

from pytile.widgets.map import QtMap
from pytile.widgets.tiles import QtTiles


ASSET_PATH = files("pytile").joinpath("assets")


class QtMainLayout(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.mainlayout = QGridLayout()

        self._create_map_toolbar()
        self._create_tile_toolbar()

        self.pal = QtPaletteGroup()
        self.pal.palette_update.connect(self._update_palette)

        self.tiles = QtTiles()
        self.map = QtMap(self.tiles, self.pal)

        self.palette_label = QtPaletteLabel()
        self.palette_label.changed.connect(self._update_palette_label)
        self.palette_label.set_label(self.pal.get_active_palette().get_label())

        # Set layout widgets
        self.mainlayout.addWidget(self.map_toolbar, 1, 0)
        self.mainlayout.addWidget(self.map, 1, 1)
        self.mainlayout.addWidget(self.pal, 1, 3)
        self.mainlayout.addWidget(self.palette_label, 0, 3)
        self.mainlayout.addWidget(self.tiles, 2, 1)
        self.mainlayout.addWidget(self.tile_toolbar, 1, 2)

        self.mainlayout.setColumnStretch(3, 1)
        self.mainlayout.setRowStretch(3, 1)

        self.setLayout(self.mainlayout)

    def new_palette(self) -> None:
        """
        Add new palette
        """
        self.pal.new_palette()
        self.palette_label.set_label(self.pal.get_active_palette().get_label())

    def _update_palette(self) -> None:
        """
        Update palette in map/tiles
        """
        self.palette_label.set_label(self.pal.get_active_palette().get_label())
        self.tiles.update_palette(self.pal.get_active_palette())
        self.map.set_palette_idx(self.pal.get_active_palette_idx())

    def _update_palette_label(self) -> None:
        """
        Update canvas label
        """
        self.pal.get_active_palette().set_label(self.palette_label.get_label())

    def _create_map_toolbar(self) -> None:
        """
        Create map tool bar and actions
        """
        self.map_toolbar = QToolBar()
        self.map_toolbar.setOrientation(Qt.Orientation.Vertical)

        # Create add button
        self.map_add_button = QToolButton()
        add_icon = QIcon(str(ASSET_PATH.joinpath("add.svg")))
        self.map_add_button.setIcon(add_icon)

        # Create save button
        self.map_save_button = QToolButton()
        save_icon = QIcon(str(ASSET_PATH.joinpath("save.svg")))
        self.map_save_button.setIcon(save_icon)

    def _create_tile_toolbar(self) -> None:
        """
        Create tile tool bar and actions
        """
        self.tile_toolbar = QToolBar()
        self.tile_toolbar.setOrientation(Qt.Orientation.Vertical)

        # Create add button
        self.tile_add_button = QToolButton()
        add_icon = QIcon(str(ASSET_PATH.joinpath("add.svg")))
        self.tile_add_button.setIcon(add_icon)

        # Create save button
        self.tile_save_button = QToolButton()
        save_icon = QIcon(str(ASSET_PATH.joinpath("save.svg")))
        self.tile_save_button.setIcon(save_icon)

        self.tile_toolbar.addWidget(self.tile_add_button)
        self.tile_toolbar.addWidget(self.tile_save_button)
