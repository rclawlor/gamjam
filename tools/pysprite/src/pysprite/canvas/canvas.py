# Third party imports
import numpy as np
from PyQt6.QtCore import QObject, pyqtSignal

# Local imports
from pysprite.canvas.palette import Palette


# Constants
TILE_PX = 8
SPRITE_PIXELS = TILE_PX**2

# Global variables
G_CANVAS_COUNT = 0


class Canvas(QObject):
    canvasChanged = pyqtSignal()

    def __init__(self, palette: Palette) -> None:
        super().__init__()
        global G_CANVAS_COUNT
        self._label = f"canvas_{G_CANVAS_COUNT}"
        G_CANVAS_COUNT += 1

        self.data = np.full((TILE_PX, TILE_PX), 0, dtype=np.uint8)
        self.collision_data = np.full((TILE_PX, TILE_PX), 0, dtype=np.uint8)
        self._colour_idx = 0
        self._palette = palette

    @property
    def w(self) -> int:
        """Width of image"""
        return self.data.shape[1]

    @property
    def h(self) -> int:
        """Height of image"""
        return self.data.shape[0]

    def get_label(self) -> str:
        """
        Canvas label
        """
        return self._label

    def set_data(self, data: np.ndarray) -> None:
        """
        Set image data
        """
        self.data = data
        self.canvasChanged.emit()

    def set_collision_data(self, data: np.ndarray) -> None:
        """
        Set collision data
        """
        self.collision_data = data
        self.canvasChanged.emit()

    def set_label(self, label: str) -> None:
        """
        Set canvas label
        """
        self._label = label

    def as_bytes(self) -> bytes:
        """
        Return pixel data as bytes
        """
        return self.data.tobytes()

    def as_rgb_bytes(self, desaturate: bool = False) -> bytes:
        """
        Return pixel data as RGB bytes
        """
        if desaturate:
            return (self.map_to_colour() // 2).tobytes()
        else:
            return self.map_to_colour().tobytes()

    def set_palette(self, palette: Palette) -> None:
        """
        Set colour palette
        """
        self._palette = palette

    def map_to_colour(self, palette: Palette | None = None) -> np.ndarray:
        """
        Map data to RGB image using palette
        """
        p = self._palette if palette is None else palette
        data_rgb = np.zeros((self.w, self.h, 3), dtype=np.uint8)
        for j in range(self.h):
            for i in range(self.w):
                data_rgb[j, i] = p.map_idx_to_rgb(self.data[j, i]).rgb

        self._changed = False
        return data_rgb

    def set_colour_idx(self, idx: int) -> None:
        """
        Set brush colour
        """
        self._colour_idx = idx

    def get_colour_idx(self) -> int:
        """
        Get brush colour
        """
        return self._colour_idx

    def new(self) -> None:
        """
        Create new canvas
        """
        self.data = np.full((TILE_PX, TILE_PX), 0, dtype=np.uint8)
        self.collision_data = np.full((TILE_PX, TILE_PX), 0, dtype=np.uint8)
        self.canvasChanged.emit()

    def draw_collision(
        self,
        x: float,
        y: float,
        collision: bool
    ) -> None:
        """
        Set pixel collision at (x, y)
        """
        if (x >= 1) or (y >= 1) or (x < 0) or (y < 0):
            return
        self.collision_data[int(TILE_PX * y), int(TILE_PX * x)] = int(collision)
        self.canvasChanged.emit()

    def draw_pixel(self, x: float, y: float) -> None:
        """
        Draw pixel at (x, y)
        """
        if (x >= 1) or (y >= 1) or (x < 0) or (y < 0):
            return
        self.data[int(TILE_PX * y), int(TILE_PX * x)] = self._colour_idx
        self.canvasChanged.emit()
