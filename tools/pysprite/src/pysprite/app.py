# Standard library imports
import math

# Third party imports
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMenu
from PyQt6.QtGui import QAction, QScreen

# Local imports
from pysprite.widgets.layout import QtMainLayout


WIN_WIDTH = 640
WIN_HEIGHT = 480


class MainWindow(QMainWindow):
    def __init__(self, screen: QScreen) -> None:
        super().__init__()

        self.setWindowTitle("PySprite")

        w, h = screen.size().width(), screen.size().height()
        self.setGeometry(
            math.floor(w / 2 - WIN_WIDTH / 2),
            math.floor(h / 2 - WIN_HEIGHT / 2),
            640,
            480
        )

        self.mainlayout = QtMainLayout()

        self._createActions()
        self._createMenuBar()

        self.setCentralWidget(self.mainlayout)

    def _createActions(self):
        """
        Create menu bar actions
        """
        # File...
        self.newAction = QAction("&New", self)
        self.newAction.triggered.connect(self._newFile)

        # Open...
        self.openMenu = QMenu("&Open...", self)
        self.open_spritesheet = QAction("&Spritesheet", self)
        self.open_palette = QAction("&Palette", self)
        self.openMenu.addAction(self.open_spritesheet)
        self.openMenu.addAction(self.open_palette)
        self.open_spritesheet.triggered.connect(self._open_spritesheet)
        self.open_palette.triggered.connect(self._open_palette)

        # Save...
        self.saveMenu = QMenu("&Save...", self)
        self.save_spritesheet = QAction("&Spritesheet", self)
        self.save_palette = QAction("&Palette", self)
        self.saveMenu.addAction(self.save_spritesheet)
        self.saveMenu.addAction(self.save_palette)
        self.save_spritesheet.triggered.connect(self._save_spritesheet)
        self.save_palette.triggered.connect(self._save_palette)

        # Toolbar...
        self.mainlayout.canvas_add_button.pressed.connect(
            self.mainlayout.new_canvas
        )
        self.mainlayout.canvas_save_button.pressed.connect(self._save_spritesheet)

        self.mainlayout.palette_add_button.pressed.connect(
            self.mainlayout.new_palette
        )
        self.mainlayout.palette_save_button.pressed.connect(self._save_palette)

        # Exit...
        self.exitAction = QAction("&Exit", self)
        self.exitAction.triggered.connect(self.close)

        # Edit...

        # Help...
        self.helpAction = QAction("&Help...", self)
        self.aboutAction = QAction("&About...", self)

    def _createMenuBar(self):
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
        fileMenu.addAction(self.newAction)
        fileMenu.addMenu(self.openMenu)
        fileMenu.addMenu(self.saveMenu)
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

    def _newFile(self) -> None:
        """
        Create new `.4bpp` file
        """
        self.mainlayout.canvas.newFile()

    def _save_spritesheet(self) -> None:
        """
        Save to `.4bpp` file
        """
        dialog = QFileDialog()
        filename, _ = dialog.getSaveFileName(
            self,
            "Save File",
            "",
            "4bpp Files(*.4bpp);;All Files(*)"
        )

        if filename:
            self.mainlayout.spritesheet.save(filename)

    def _save_palette(self) -> None:
        """
        Save to `.pal` file
        """
        dialog = QFileDialog()
        filename, _ = dialog.getSaveFileName(
            self,
            "Save File",
            "",
            "Pal Files(*.pal);;All Files(*)"
        )

        if filename:
            self.mainlayout.pal.save_file(filename)

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
            self.mainlayout.spritesheet.open(filename)

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
