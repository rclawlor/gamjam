# Third party imports
from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QGridLayout, QPushButton

# Local imports
from pysprite.canvas.palette import PALETTE, Colour


BUTTON_SIZE = 24


class QtColourButton(QPushButton):
    def __init__(self, colour: Colour):
        super().__init__()
        self.setFixedSize(QSize(BUTTON_SIZE, BUTTON_SIZE))
        self._colour = colour
        self.setStyleSheet(
            "background-color: %s; border: 1px black;" % self._colour.hex
        )

    @property
    def colour(self) -> Colour:
        return self._colour


class QtColourSelector(QFrame):
    colour_selected = pyqtSignal(Colour)

    def __init__(self):
        super().__init__()
        self.glayout = QGridLayout()
        self.buttons: list[QtColourButton] = []
        for idx, hex in enumerate(PALETTE):
            self.buttons.append(
                QtColourButton(Colour.from_hex(hex))
            )
            self.glayout.addWidget(
                self.buttons[-1],
                1 + idx // 16,
                1 + idx % 16,
                alignment=Qt.AlignmentFlag.AlignCenter
            )
            self.buttons[-1].pressed.connect(lambda x=idx: self._button_pressed(x))
        self.glayout.setColumnStretch(0, 1)
        self.glayout.setColumnStretch(17, 1)
        self.glayout.setRowStretch(0, 1)
        self.glayout.setRowStretch(17, 1)
        self.setLayout(self.glayout)
        self.setFrameStyle(QFrame.Shape.StyledPanel)
        self.setLineWidth(1)

    def map_idx_to_rgb(self, idx: int) -> Colour:
        """
        Map palette index to RGB colour
        """
        return self.buttons[idx].colour

    def _button_pressed(self, idx: int) -> None:
        """
        Called if button pressed
        """
        self.colour_selected.emit(self.buttons[idx].colour)
