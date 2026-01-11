# Standard library imports
from pathlib import Path

# Third party imports
import numpy as np
from PyQt6.QtCore import QObject, pyqtSignal

# Local imports
from pysprite.canvas.canvas import Canvas
from pysprite.canvas.palette import Palette


# Constants
VERSION = [0, 0, 1]
TILE_PX = 8
SPRITE_PIXELS = TILE_PX**2


def pack_data(idx_a, collision_a, idx_b, collision_b):
    """
    Pack palette index and collision into 1 byte
    """
    a = (idx_a | ((collision_a & 0b00000001) << 3)) & 0b00001111
    b = (idx_b | ((collision_b & 0b00000001) << 3)) & 0b00001111

    return (a << 4) + b


class Spritesheet(QObject):
    spritesheet_changed = pyqtSignal()
    spritesheet_loaded = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self._canvases = [Canvas(Palette())]

    @property
    def canvases(self) -> list[Canvas]:
        """
        Return all canvases in spritesheet
        """
        return self._canvases

    def new_canvas(self) -> None:
        """
        Create new canvas
        """
        self._canvases.append(Canvas(Palette()))

    def swap_canvas(
        self,
        source_idx: int,
        target_idx: int
    ) -> None:
        """
        Swap canvases at specified indexes
        """
        source = self._canvases.pop(source_idx)
        self._canvases.insert(target_idx, source)

    def open(self, filename: str) -> None:
        """
        Open spritesheet from `.4bpp` file
        """
        path = Path(filename)
        data_raw = path.read_bytes()
        version = data_raw[:3]
        if version != bytes(VERSION):
            raise AttributeError(".4bpp file has outdated version")
        self._offset = 3

        canvases = []
        while self._offset < len(data_raw):
            canvases.append(self._extract_canvas(data_raw))

        self._canvases = canvases
        self.spritesheet_loaded.emit()

    def _extract_canvas(self, data_raw: bytes) -> Canvas:
        """
        Extract canvas from `.4bpp` file
        """
        label_length = data_raw[self._offset]
        label = data_raw[1 + self._offset:label_length + 1 + self._offset]

        self._offset += label_length + 1
        data = np.full((TILE_PX, TILE_PX), 0, dtype=np.uint8)
        collision_data = np.full((TILE_PX, TILE_PX), 0, dtype=np.uint8)
        for j in range(TILE_PX):
            for i in range(TILE_PX // 2):
                x = data_raw[i + (TILE_PX // 2) * j + self._offset]
                a = (x & 0b11110000) >> 4
                b = x & 0b00001111

                data[j, 2 * i] = a & 0b00000111
                data[j, 2 * i + 1] = b & 0b00000111

                collision_data[j, 2 * i] = int((a & 0b00001000) == 0b00001000)
                collision_data[j, 2 * i + 1] = int((b & 0b00001000) == 0b00001000)

        self._offset += TILE_PX**2 // 2

        canvas = Canvas(Palette())
        canvas.set_data(data)
        canvas.set_collision_data(collision_data)
        canvas.set_label(str(label, encoding="utf-8"))
        return canvas

    def save(self, filename: str) -> None:
        """
        Save data to `.4bpp` file
        """
        if not filename.endswith(".4bpp"):
            path = f"{filename}.4bpp"
        else:
            path = filename

        with open(path, "wb") as f:
            f.write(bytes(VERSION))
            for canvas in self._canvases:
                label = bytes(canvas.get_label(), encoding="utf-8")
                f.write(bytes([len(label)]))
                f.write(label)
                for j in range(canvas.h):
                    for i in range(0, canvas.w, 2):
                        d = pack_data(
                            canvas.data[j, i],
                            canvas.collision_data[j, i],
                            canvas.data[j, i + 1],
                            canvas.collision_data[j, i + 1]
                        )
                        f.write(d.tobytes())
