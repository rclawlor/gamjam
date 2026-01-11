# Standard library imports
import random

# Third party imports
from PyQt6.QtCore import QObject, pyqtSignal


# Constants
N_PALETTE_COLOURS = 8

# Global variables
G_PALETTE_COUNT = 1


def hex_to_rgb(hex: str) -> list[int]:
    """
    Convert colour in #012345 format to RGB
    """
    n = hex.strip('#')
    return [int(n[i:i + 2], 16) for i in range(0, 6, 2)]


class Colour():
    def __init__(self, r: int, g: int, b: int) -> None:
        self._r = r
        self._g = g
        self._b = b

    @classmethod
    def from_hex(cls, hex: str):
        n = hex.strip('#')
        return cls(*[int(n[i:i + 2], 16) for i in range(0, 6, 2)])

    @property
    def hex(self) -> str:
        return f"#{self._r:02x}{self._g:02x}{self._b:02x}"

    @property
    def rgb(self) -> list[int]:
        return [self._r, self._g, self._b]


class Palette(QObject):
    palette_changed = pyqtSignal()

    def __init__(
        self,
        colours: list[Colour] | None = None,
        label: str | None = None
    ) -> None:
        super().__init__()

        if label is None:
            global G_PALETTE_COUNT
            self._label = f"palette_{G_PALETTE_COUNT}"
            G_PALETTE_COUNT += 1
        else:
            self._label = label

        if colours is not None:
            self._colours = colours
        else:
            self._colours = []
            for idx in range(N_PALETTE_COLOURS):
                c = "#000000" if idx == 0 else PALETTE[random.randrange(255)]
                self._colours.append(Colour.from_hex(c))

    @property
    def length(self) -> int:
        return len(self._colours)

    @property
    def colours(self) -> list[Colour]:
        return self._colours

    @property
    def label(self) -> str:
        return self._label

    def get_label(self) -> str:
        """
        Canvas label
        """
        return self._label

    def set_label(self, label: str) -> None:
        """
        Set canvas label
        """
        self._label = label

    def map_idx_to_rgb(self, idx: int) -> Colour:
        """
        Map palette index to RGB colour
        """
        if idx >= self.length:
            raise IndexError(
                f"Colour index {idx} is outside the palette range 0-{self.length}"
            )
        return self._colours[idx]

    def update_colour(self, idx: int, colour: Colour) -> None:
        """
        Update colour at idx
        """
        if idx >= self.length:
            raise IndexError(
                f"Colour index {idx} is outside the palette range 0-{self.length}"
            )
        self._colours[idx] = colour


# Constants
PALETTE = [
    "#000000", "#2b180c", "#a74b27", "#542524",
    "#a72b25", "#554848", "#a84b49", "#a72b48",
    "#a72c6c", "#542647", "#a82c90", "#a82db4",
    "#54266c", "#55278f", "#55486c", "#5627b4",
    "#566d6d", "#566c49", "#556c27", "#a86e29",
    "#a86e4a", "#fb504a", "#fb506d", "#a84b6d",
    "#fb5190", "#fb51b5", "#a84c90", "#a84cb4",
    "#a92ed8", "#564990", "#5749b4", "#584ad8",
    "#586db5", "#576d90", "#57904b", "#57902b",
    "#a9912c", "#fb724b", "#a86e6d", "#fb726e",
    "#fb7291", "#a86f90", "#fc52d8", "#fc52fd",
    "#a96fb5", "#a94dd8", "#aa4dfc", "#594afc",
    "#5a6efd", "#596dd8", "#5990b5", "#589091",
    "#58906e", "#59b42f", "#a9914b", "#a9916e",
    "#fc944c", "#fc946f", "#a99191", "#fc72b5",
    "#fc73d8", "#fc73fd", "#a96fd8", "#aa70fd",
    "#5c91fd", "#5a91d8", "#5bb592", "#5ab56f",
    "#5ab54d", "#aab670", "#aab54d", "#aab530",
    "#fcb74e", "#fcb770", "#fc9492", "#fc94b6",
    "#fc94d9", "#aa92b5", "#aa92d9", "#ab92fd",
    "#abb6d9", "#5eb5fd", "#5cb5d9", "#5bb5b6",
    "#abb6b6", "#5dd893", "#5dd871", "#5cd84f",
    "#abd971", "#abd950", "#aab692", "#fdda51",
    "#fcb793", "#fdb8b6", "#fdb8d9", "#fd95fd",
    "#acb6fd", "#60d9fe", "#5fd9da", "#acd9da",
    "#5ed8b7", "#acd9b7", "#60fd73", "#60fd53",
    "#abd993", "#adfd73", "#acfd53", "#feff54",
    "#fdda72", "#fdda94", "#fddbb7", "#fdb8fe",
    "#ffffff", "#add9fe", "#64fdff", "#aefeff",
    "#62fddb", "#61fdb8", "#aefedb", "#61fd95",
    "#adfeb8", "#adfe95", "#feff74", "#feff95",
    "#feffb8", "#ffffdb", "#fedbda", "#fedbfe",
    "#31d8fe", "#38fdff", "#2ed8da", "#35fddb",
    "#2cd8b7", "#33fdb8", "#31fd95", "#30fd73",
    "#2ffd52", "#2ffd38", "#5ffd38", "#5ffd2a",
    "#acfd39", "#acfd2b", "#feff3a", "#feff2d",
    "#2690fd", "#2bb5fd", "#28b5d9", "#25b5b6",
    "#22b492", "#2ad893", "#28d871", "#27d84f",
    "#26d833", "#2efd29", "#5cd833", "#5cd822",
    "#abd934", "#abd923", "#fdda26", "#fdda35",
    "#216dfd", "#1d6dd8", "#2290d8", "#1e90b5",
    "#1b9091", "#19906e", "#20b46f", "#1fb44d",
    "#1eb42e", "#26d822", "#1eb41a", "#59b41b",
    "#aab51d", "#fcb71f", "#fcb731", "#fc942e",
    "#1c28fc", "#1e49fc", "#1949d8", "#196cb4",
    "#156c90", "#126c6d", "#0f6c49", "#17904a",
    "#16902a", "#169013", "#579013", "#a99116",
    "#fc9419", "#fb7214", "#fb722b", "#fc37fd",
    "#1b0dfc", "#1727d8", "#1448b4", "#0f4890",
    "#0b486c", "#0e6c27", "#0d6c0b", "#556c0c",
    "#a86e0f", "#fb5029", "#fb3590", "#fb36b5",
    "#fc37d8", "#a92ffc", "#5729d8", "#592afc",
    "#160ad8", "#1126b4", "#0c258f", "#084748",
    "#064725", "#544806", "#a74b09", "#fb500f",
    "#fb3449", "#fb356d", "#fb26b4", "#fc27d8",
    "#a919d8", "#a91bfc", "#570ed8", "#5811fc",
    "#1006b4", "#0a048f", "#07246c", "#042447",
    "#064705", "#a72b06", "#fb340c", "#fb3427",
    "#fb2449", "#fb246d", "#fb2590", "#a7156c",
    "#a81690", "#a817b4", "#55098f", "#560bb4",
    "#06026c", "#020147", "#010023", "#022424",
    "#022302", "#542502", "#fb240b", "#a71404",
    "#530501", "#fb2427", "#a71425", "#a71548",
    "#530624", "#540647", "#54076c", "#fc28fd",
]
