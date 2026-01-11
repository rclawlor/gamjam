# Standard library imports
from pathlib import Path

# Third party imports
from PyQt6.QtCore import QObject, pyqtSignal

# Local imports
from pysprite.canvas.palette import Colour, Palette


# Constants
VERSION = [0, 0, 1]
PALETTE_LENGTH = 8


class PaletteGroup(QObject):
    changed = pyqtSignal()
    loaded = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self._palettes = [Palette()]

    @property
    def palettes(self) -> list[Palette]:
        """
        Return all palettes in palette group
        """
        return self._palettes

    def new_palette(self) -> None:
        """
        Create new canvas
        """
        self._palettes.append(Palette())

    def swap_palette(
        self,
        source_idx: int,
        target_idx: int
    ) -> None:
        """
        Swap palettes at specified indexes
        """
        source = self._palettes.pop(source_idx)
        self._palettes.insert(target_idx, source)

    def open(self, filename: str) -> None:
        """
        Open and load an existing `.pal` file
        """
        path = Path(filename)
        data_raw = path.read_bytes()
        version = data_raw[:3]
        if version != bytes(VERSION):
            raise AttributeError(".pal file has outdated version")
        self._offset = 3

        palettes = []
        while self._offset < len(data_raw):
            palettes.append(self._extract_palette(data_raw))
        self._palettes = palettes
        self.loaded.emit()

    def _extract_palette(self, data_raw: bytes) -> Palette:
        """
        Extract palette from `.pal` file
        """
        label_length = data_raw[self._offset]
        label = data_raw[1 + self._offset:label_length + 1 + self._offset]

        self._offset += label_length + 1
        colours = []
        for idx in range(0, PALETTE_LENGTH * 3, 3):
            colours.append(
                Colour(*data_raw[idx + self._offset:idx + self._offset + 3])
            )
        self._offset += PALETTE_LENGTH * 3

        return Palette(colours, str(label, encoding="utf-8"))

    def save(self, filename: str) -> None:
        """
        Save palette to `.pal` file
        """
        if not filename.endswith(".pal"):
            path = f"{filename}.pal"
        else:
            path = filename

        with open(path, "wb") as f:
            f.write(bytes(VERSION))
            for palette in self.palettes:
                label = bytes(palette.get_label(), encoding="utf-8")
                f.write(bytes([len(label)]))
                f.write(label)
                for colour in palette.colours:
                    for chan in colour.rgb:
                        f.write(chan.to_bytes())
