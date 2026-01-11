# Standard library imports
import typing as t

# Third party imports
from PyQt6 import QtGui
from PyQt6.QtCore import QMimeData, QSize, Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QGridLayout, QLabel, QLineEdit, QPushButton, QWidget

# Local imports
from pysprite.canvas.palette import N_PALETTE_COLOURS, Colour, Palette


class QtCollisionButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(24, 24))
        self._active = False

    @property
    def active(self) -> bool:
        return self._active

    def select(self, s: bool) -> None:
        """
        Select colour
        """
        self._active = s

    def paintEvent(self, a0: t.Optional[QtGui.QPaintEvent]):
        """
        Draw red cross on button
        """
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setPen(QtGui.QPen(Qt.GlobalColor.red, 2))
        painter.drawLine(4, 4, 20, 20)
        painter.drawLine(4, 20, 20, 4)
        if self.active:
            painter.setPen(QtGui.QPen(Qt.GlobalColor.yellow, 4))
            painter.drawLine(1, 1, 1, 23)
            painter.drawLine(1, 23, 23, 23)
            painter.drawLine(23, 23, 23, 1)
            painter.drawLine(23, 1, 1, 1)


class QtPaletteButton(QPushButton):
    def __init__(self, idx: int, colour: Colour):
        super().__init__()
        self.setFixedSize(QSize(24, 24))
        self._active = False
        self._idx = idx
        self._colour = colour
        self._update_border()

    @property
    def idx(self) -> int:
        return self._idx

    @property
    def active(self) -> bool:
        return self._active

    @property
    def colour(self) -> Colour:
        return self._colour

    def set_colour(self, colour: Colour) -> None:
        """
        Update button colour
        """
        self._colour = colour
        self._update_border()

    def select(self, s: bool) -> None:
        """
        Select colour
        """
        self._active = s
        self._update_border()

    def _update_border(self) -> None:
        """
        Update border depending on selected state
        """
        if self._active:
            self.setStyleSheet(
                "border: 3px solid yellow;"
                "border-style: inset;"
                "background-color: %s;" % self.colour.hex
            )
        else:
            self.setStyleSheet(
                "background-color: %s; border: 1px black;" % self.colour.hex
            )


class QtPalette(QFrame):
    row_selected = pyqtSignal()
    colour_selected = pyqtSignal(int)
    collision_selected = pyqtSignal()

    def __init__(self, palette: Palette):
        super().__init__()
        self._palette = palette
        self._palette.palette_changed.connect(self._palette_changed)
        self._active = False
        self.glayout = QGridLayout()
        self.buttons = []
        for idx, c in enumerate(self._palette.colours):
            self.buttons.append(
                QtPaletteButton(idx, c)
            )
            self.glayout.addWidget(
                self.buttons[-1],
                0,
                1 + idx,
                alignment=Qt.AlignmentFlag.AlignCenter
            )
            self.buttons[-1].pressed.connect(lambda x=idx: self._button_pressed(x))

        self.buttons.append(
            QtCollisionButton()
        )
        idx = len(self._palette.colours)
        self.glayout.addWidget(
            self.buttons[-1],
            0,
            1 + idx,
            alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.buttons[-1].pressed.connect(lambda x=idx: self._button_pressed(x))

        self.glayout.setColumnStretch(len(self.buttons) + 1, 1)
        self.glayout.setRowStretch(1, 1)
        self.setLayout(self.glayout)
        self.setFrameStyle(QFrame.Shape.StyledPanel)
        self.setLineWidth(1)
        self._update_border()

    @property
    def selected(self) -> bool:
        return self._active

    def _palette_changed(self) -> None:
        """
        Handle palette change
        """
        self._refresh_palette()
        self.row_selected.emit()

    def select(self, s: bool) -> None:
        """
        Select palette
        """
        self._active = s
        if not self._active:
            for button in self.buttons:
                button.select(False)
        self._update_border()

    def get_active_idx(self) -> int:
        """
        Get currently active button idx
        """
        for idx, button in enumerate(self.buttons):
            if button.active:
                return idx
        else:
            raise IndexError("No buttons active")

    def update_colour(self, colour: Colour) -> None:
        """
        Update currently selected colour
        """
        self._palette.update_colour(
            self.get_active_idx(),
            colour
        )
        self._refresh_palette()

    def _refresh_palette(self) -> None:
        """
        Refresh button colours from palette
        """
        for idx, colour in enumerate(self._palette.colours):
            self.buttons[idx].set_colour(colour)

    def _update_border(self) -> None:
        """
        Update border depending on selected state
        """
        if self._active:
            self.setStyleSheet("border: 1px solid lightgray;")
        else:
            self.setStyleSheet("border: 1px solid black;")

    def _button_pressed(self, idx: int) -> None:
        """
        Called if button pressed
        """
        self.active = True
        for i, button in enumerate(self.buttons):
            button.select(i == idx)
        self._update_border()
        self.row_selected.emit()
        if idx < N_PALETTE_COLOURS:
            self.colour_selected.emit(self.buttons[idx].idx)
        else:
            self.collision_selected.emit()

    def mouseMoveEvent(
        self,
        a0: t.Optional[QtGui.QMouseEvent]
    ) -> None:
        """
        Event triggered when element is dragged.
        """
        if a0 is None:
            return

        if a0.buttons() == Qt.MouseButton.LeftButton:
            drag = QtGui.QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)

            pixmap = QtGui.QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)

            drag.exec(Qt.DropAction.MoveAction)


class QtPaletteLabel(QWidget):
    changed = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.glayout = QGridLayout()

        self.label = QLabel("Palette ID: ")
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
