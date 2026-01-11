# Standard library imports
import math

# Third party imports
from PyQt6.QtWidgets import QApplication, QFileDialog, QMainWindow, QMenu
from PyQt6.QtGui import QAction, QScreen

# Local imports
from pytile.widgets.layout import QtMainLayout


WIN_WIDTH = 640
WIN_HEIGHT = 480


class MainWindow(QMainWindow):
    def __init__(self, screen: QScreen) -> None:
        super().__init__()

        self.setWindowTitle("PyTile")

        w, h = screen.size().width(), screen.size().height()
        self.setGeometry(
            math.floor(w / 2 - WIN_WIDTH / 2),
            math.floor(h / 2 - WIN_HEIGHT / 2),
            640,
            480
        )

        self.mainlayout = QtMainLayout()

        self._create_actions()
        self._create_menu_bar()

        self.setCentralWidget(self.mainlayout)

    def _create_actions(self):
        """
        Create menu bar actions
        """
        # File...
        self.new_action = QAction("&New", self)

        # Open...
        self.open_menu = QMenu("&Open...", self)
        self.open_map = QAction("&Map", self)
        self.open_map.triggered.connect(self._open_map)
        self.open_spritesheet = QAction("&Spritesheet", self)
        self.open_spritesheet.triggered.connect(self._open_spritesheet)
        self.open_palette = QAction("&Palette", self)
        self.open_palette.triggered.connect(self._open_palette)
        self.open_menu.addAction(self.open_map)
        self.open_menu.addAction(self.open_spritesheet)
        self.open_menu.addAction(self.open_palette)

        # Save...
        self.save_map = QAction("&Save", self)
        self.save_map.triggered.connect(self._save_map)

        # Exit...
        self.exitAction = QAction("&Exit", self)
        self.exitAction.triggered.connect(self.close)

        # Edit...

        # Help...
        self.helpAction = QAction("&Help...", self)
        self.aboutAction = QAction("&About...", self)

    def _create_menu_bar(self):
        """
        Create menu bar
        """
        menuBar = self.menuBar()
        if menuBar is None:
            raise RuntimeError("Unable to create menu bar")

        fileMenu = menuBar.addMenu("&File")
        if fileMenu is None:
            raise RuntimeError("Unable to add menu bar entry")
        fileMenu.addSeparator()
        fileMenu.addAction(self.new_action)
        fileMenu.addMenu(self.open_menu)
        fileMenu.addAction(self.save_map)
        fileMenu.addAction(self.exitAction)

        editMenu = menuBar.addMenu("&Edit")
        if editMenu is None:
            raise RuntimeError("Unable to add menu bar entry")

        helpMenu = menuBar.addMenu("&Help")
        if helpMenu is None:
            raise RuntimeError("Unable to add menu bar entry")
        helpMenu.addAction(self.helpAction)
        helpMenu.addAction(self.aboutAction)

        self.setMenuBar(menuBar)

    def _open_spritesheet(self) -> None:
        """
        Open and load an existing `.4bpp` file.
        """
        dialog = QFileDialog()
        filename, _ = dialog.getOpenFileName(
            self,
            "Open File",
            "",
            "4bpp Files(*.4bpp);;All Files(*)"
        )

        if filename:
            self.mainlayout.tiles.open(filename)
            self.mainlayout.tiles.update_palette(self.mainlayout.pal.get_active_palette())

    def _open_palette(self) -> None:
        """
        Open and load an existing `.pal` file.
        """
        dialog = QFileDialog()
        filename, _ = dialog.getOpenFileName(
            self,
            "Open File",
            "",
            "Pal Files(*.pal);;All Files(*)"
        )

        if filename:
            self.mainlayout.pal.open_file(filename)
            self.mainlayout.map.redraw_map()

    def _open_map(self) -> None:
        """
        Open and load an existing `.map` file.
        """
        dialog = QFileDialog()
        filename, _ = dialog.getOpenFileName(
            self,
            "Open File",
            "",
            "Map Files(*.map);;All Files(*)"
        )

        if filename:
            self.mainlayout.map.open(filename)
            self.mainlayout.map.redraw_map()

    def _save_map(self) -> None:
        """
        Save to `.map` file
        """
        dialog = QFileDialog()
        filename, _ = dialog.getSaveFileName(
            self,
            "Save File",
            "",
            "Map Files(*.map);;All Files(*)"
        )

        if filename:
            self.mainlayout.map.save(filename)


def run() -> None:
    """
    Run the application
    """
    app = QApplication([])
    screen = app.primaryScreen()
    if screen is None:
        raise RuntimeError("Could not read screen information")

    window = MainWindow(screen)
    window.show()

    app.exec()
