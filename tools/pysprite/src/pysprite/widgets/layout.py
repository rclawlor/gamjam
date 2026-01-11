# Standard library imports
from importlib.resources import files

# Third party imports
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QGridLayout, QToolBar, QToolButton, QWidget
from PyQt6.QtCore import Qt

# Local imports
from pysprite.canvas.palette import Colour
from pysprite.widgets.canvas import QtCanvas, QtCanvasLabel
from pysprite.widgets.colour_selector import QtColourSelector
from pysprite.widgets.palette import QtPaletteLabel
from pysprite.widgets.palette_group import QtPaletteGroup
from pysprite.widgets.spritesheet import QtSpritesheet


ASSET_PATH = files("pysprite").joinpath("assets")


class QtMainLayout(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.mainlayout = QGridLayout()

        self._create_canvas_toolbar()
        self._create_palette_toolbar()
        self.pal = QtPaletteGroup()
        self.pal.palette_update.connect(self._update_palette)
        self.pal.collision_selected.connect(self._select_collision_mode)

        self.canvas = QtCanvas(self.pal)

        self.spritesheet = QtSpritesheet()
        self.spritesheet.canvas_selected.connect(self._update_canvas)
        self.canvas.update_canvas(self.spritesheet.get_active_canvas())

        self.canvas_label = QtCanvasLabel()
        self.canvas_label.changed.connect(self._update_canvas_label)
        self.canvas_label.set_label(self.canvas.get_label())

        self.palette_label = QtPaletteLabel()
        self.palette_label.changed.connect(self._update_palette_label)
        self.palette_label.set_label(self.pal.get_active_palette().get_label())

        self.colour_selector = QtColourSelector()
        self.colour_selector.colour_selected.connect(self._update_colour)

        # Set layout widgets
        self.mainlayout.addWidget(self.canvas_toolbar, 1, 0)
        self.mainlayout.addWidget(self.canvas_label, 0, 1)
        self.mainlayout.addWidget(self.canvas, 1, 1)
        self.mainlayout.addWidget(self.pal, 1, 3)
        self.mainlayout.addWidget(self.palette_label, 0, 3)
        self.mainlayout.addWidget(self.colour_selector, 1, 4)
        self.mainlayout.addWidget(self.spritesheet, 2, 1)
        self.mainlayout.addWidget(self.palette_toolbar, 1, 2)

        self.mainlayout.setColumnStretch(3, 1)
        self.mainlayout.setRowStretch(3, 1)

        self.setLayout(self.mainlayout)

    def new_canvas(self) -> None:
        """
        Add new canvas to spritesheet
        """
        self.spritesheet.new_canvas()
        self._update_palette()
        self.canvas_label.set_label(self.canvas.get_label())

    def new_palette(self) -> None:
        """
        Add new palette
        """
        self.pal.new_palette()
        self.palette_label.set_label(self.pal.get_active_palette().get_label())

    def _update_canvas_label(self) -> None:
        """
        Update canvas label
        """
        self.canvas.set_label(self.canvas_label.get_label())

    def _update_palette_label(self) -> None:
        """
        Update canvas label
        """
        self.pal.get_active_palette().set_label(self.palette_label.get_label())

    def _update_palette(self) -> None:
        """
        Update palette in spritesheet
        """
        self.spritesheet.update_palette(self.canvas.get_active_palette())
        self.palette_label.set_label(self.pal.get_active_palette().get_label())

    def _update_canvas(self) -> None:
        """
        Update canvas from spritesheet selection
        """
        idx = self.canvas.get_colour_idx()
        self.canvas.update_canvas(self.spritesheet.get_active_canvas())
        if not self.canvas._collision_mode:
            self.canvas.set_colour_idx(idx)
        self.canvas_label.set_label(self.canvas.get_label())

    def _update_colour(self, colour: Colour) -> None:
        """
        Update canvas/spritesheet colour
        """
        self.canvas.update_colour(colour)
        self.spritesheet.update_palette(self.canvas.get_active_palette())

    def _select_collision_mode(self) -> None:
        """
        Select collision mode in canvas
        """
        self.canvas.set_collision_mode(True)
        self._update_canvas()

    def _create_canvas_toolbar(self) -> None:
        """
        Create canvas tool bar and actions
        """
        self.canvas_toolbar = QToolBar()
        self.canvas_toolbar.setOrientation(Qt.Orientation.Vertical)

        # Create add button
        self.canvas_add_button = QToolButton()
        add_icon = QIcon(str(ASSET_PATH.joinpath("add.svg")))
        self.canvas_add_button.setIcon(add_icon)

        # Create save button
        self.canvas_save_button = QToolButton()
        save_icon = QIcon(str(ASSET_PATH.joinpath("save.svg")))
        self.canvas_save_button.setIcon(save_icon)

        self.canvas_toolbar.addWidget(self.canvas_add_button)
        self.canvas_toolbar.addWidget(self.canvas_save_button)

    def _create_palette_toolbar(self) -> None:
        """
        Create palette tool bar and actions
        """
        self.palette_toolbar = QToolBar()
        self.palette_toolbar.setOrientation(Qt.Orientation.Vertical)

        # Create add button
        self.palette_add_button = QToolButton()
        add_icon = QIcon(str(ASSET_PATH.joinpath("add.svg")))
        self.palette_add_button.setIcon(add_icon)

        # Create save button
        self.palette_save_button = QToolButton()
        save_icon = QIcon(str(ASSET_PATH.joinpath("save.svg")))
        self.palette_save_button.setIcon(save_icon)

        self.palette_toolbar.addWidget(self.palette_add_button)
        self.palette_toolbar.addWidget(self.palette_save_button)
