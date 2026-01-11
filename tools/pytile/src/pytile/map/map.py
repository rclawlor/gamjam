# Third party imports
import numpy as np
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal

# Local imports
from pysprite.canvas.canvas import TILE_PX
from pysprite.canvas.palette_group import PaletteGroup
from pysprite.canvas.spritesheet import Spritesheet


# Constants
VERSION = [0, 0, 1]
W_TILES = 40
H_TILES = 25


class Map(QObject):
    mapChanged = pyqtSignal()

    def __init__(
        self,
        spritesheet: Spritesheet,
        palette_group: PaletteGroup
    ) -> None:
        super().__init__()
        self.data = np.full((H_TILES, W_TILES), 0, dtype=np.uint8)
        self.data_rgb = np.full((H_TILES * TILE_PX, W_TILES * TILE_PX, 3), 0, dtype=np.uint8)
        self.palette_data = np.full((H_TILES, W_TILES), 0, dtype=np.uint8)
        self._spritesheet = spritesheet
        self._palette_group = palette_group
        self._tile_idx = 0
        self._palette_idx = 0

    @property
    def w(self) -> int:
        """Width of image"""
        return self.data.shape[1]

    @property
    def h(self) -> int:
        """Height of image"""
        return self.data.shape[0]

    def set_data(self, data: np.ndarray) -> None:
        """
        Set image data
        """
        self.data = data
        self.mapChanged.emit()

    def as_bytes(self) -> bytes:
        """
        Return tile data as bytes
        """
        return self.data.tobytes()

    def as_rgb_bytes(self) -> bytes:
        """
        Return tile data as RGB bytes
        """
        return self.data_rgb.tobytes()

    def redraw_map(self) -> None:
        """
        Map tiles to colour
        """
        c = self._spritesheet.canvases
        for j in range(self.h):
            for i in range(self.w):
                self.data_rgb[TILE_PX * j:TILE_PX * (j + 1), TILE_PX * i:TILE_PX * (i + 1), :] = \
                    c[self.data[j, i]].map_to_colour(
                        self._palette_group.palettes[self.palette_data[j, i]]
                    )
        self.mapChanged.emit()

    def update_tile(self, i: int, j: int) -> None:
        """
        Update RGB data for tile
        """
        self.data_rgb[TILE_PX * j:TILE_PX * (j + 1), TILE_PX * i:TILE_PX * (i + 1), :] = \
            self._spritesheet.canvases[self.data[j, i]].map_to_colour(
                self._palette_group.palettes[self.palette_data[j, i]]
            )

    def set_tile_idx(self, idx: int) -> None:
        """
        Set brush tile
        """
        self._tile_idx = idx

    def get_tile_idx(self) -> int:
        """
        Get brush tile
        """
        return self._tile_idx

    def set_palette_idx(self, idx: int) -> None:
        """
        Set brush palette
        """
        self._palette_idx = idx

    def get_palette_idx(self) -> int:
        """
        Get brush palette
        """
        return self._palette_idx

    def new(self) -> None:
        """
        Create new map
        """
        self.data = np.full((H_TILES, W_TILES), 0, dtype=np.uint8)
        self.mapChanged.emit()

    def draw_tile(self, x: float, y: float) -> None:
        """
        Draw tile at (x, y)
        """
        if (x >= 1) or (y >= 1) or (x < 0) or (y < 0):
            return

        try:
            i, j = int(self.w * x), int(self.h * y)
            self.data[j, i] = self._tile_idx
            self.palette_data[j, i] = self._palette_idx
            self.update_tile(i, j)
        except Exception:
            print(self.h, y, self.w, x)
        self.mapChanged.emit()

    def open(self, filename: str) -> None:
        """
        Open map from `.map` file
        """
        path = Path(filename)
        data_raw = path.read_bytes()
        version = data_raw[:3]
        if version != bytes(VERSION):
            raise AttributeError(".map file has outdated version")
        self._offset = 3
        data = np.full((H_TILES, W_TILES), 0, dtype=np.uint8)
        for j in range(H_TILES):
            for i in range(W_TILES // 2):
                x = data_raw[i + (W_TILES // 2) * j + self._offset]
                a = (x & 0b11110000) >> 4
                b = x & 0b00001111

                data[j, 2 * i] = a
                data[j, 2 * i + 1] = b

        self._offset += H_TILES * W_TILES // 2
        palette_data = np.full((H_TILES, W_TILES), 0, dtype=np.uint8)
        for j in range(H_TILES):
            for i in range(W_TILES // 2):
                x = data_raw[i + (W_TILES // 2) * j + self._offset]
                a = (x & 0b11110000) >> 4
                b = x & 0b00001111

                palette_data[j, 2 * i] = a
                palette_data[j, 2 * i + 1] = b

        self.data = data
        self.palette_data = palette_data
        self.mapChanged.emit()

    def save(self, filename: str) -> None:
        """
        Save data to `.map` file
        """
        if not filename.endswith(".map"):
            path = f"{filename}.map"
        else:
            path = filename

        with open(path, "wb") as f:
            f.write(bytes(VERSION))
            for j in range(self.h):
                for i in range(0, self.w, 2):
                    a = self.data[j, i] & 0b00001111
                    b = self.data[j, i + 1] & 0b00001111

                    d = (a << 4) + b
                    f.write(d.tobytes())
            for j in range(self.h):
                for i in range(0, self.w, 2):
                    a = self.palette_data[j, i] & 0b00001111
                    b = self.palette_data[j, i + 1] & 0b00001111

                    d = (a << 4) + b
                    f.write(d.tobytes())
