# Standard library imports
import os
from pathlib import Path

# Local
from csprite.shared import chunks


# Constants
W_TILES = 40
H_TILES = 25


class Map():
    def __init__(
        self,
        name: str,
        data: bytes
    ) -> None:
        self._name = name
        self._data = data
        self._version = [int(i) for i in self._data[:3]]
        self._parse_map()

    @property
    def version(self) -> list[int]:
        return self._version

    @property
    def name(self) -> str:
        return f"{self._name.upper()}_MAP"

    @property
    def definition(self) -> str:
        return (
            f"uint8_t {self._name.upper()}_MAP"
            f"[1][2][{H_TILES * W_TILES}]"
        )

    @property
    def pointer(self) -> str:
        return f"uint8_t (*{self._name.upper()}_MAP)[1][2][{H_TILES * W_TILES}]"

    @property
    def cast(self) -> str:
        return f"(uint8_t (*)[1][2][{H_TILES * W_TILES}])"

    def _parse_map(self) -> None:
        """
        Parse map data into tile and palette indexes
        """
        offset = 3
        data = []
        for j in range(H_TILES):
            for i in range(W_TILES // 2):
                x = self._data[i + (W_TILES // 2) * j + offset]
                a = (x & 0b11110000) >> 4
                b = x & 0b00001111

                data.append(a)
                data.append(b)

        offset += H_TILES * W_TILES // 2
        palette_data = []
        for j in range(H_TILES):
            for i in range(W_TILES // 2):
                x = self._data[i + (W_TILES // 2) * j + offset]
                a = (x & 0b11110000) >> 4
                b = x & 0b00001111

                palette_data.append(a)
                palette_data.append(b)

        self.data = data
        self.palette_data = palette_data

    def generate_array(self) -> str:
        """
        Format byte data into c array
        """
        output = (
            f"uint8_t {self._name.upper()}_MAP[][2][{H_TILES * W_TILES}] = {{\n"
        )
        output += "    {\n"
        output += "        {\n"
        for row in chunks(self.data, 8):
            output += 12 * ' ' + ", ".join([f"0x{i:02X}" for i in row]) + ",\n"
        output += "        },\n"
        output += "        {\n"
        for row in chunks(self.palette_data, 8):
            output += 12 * ' ' + ", ".join([f"0x{i:02X}" for i in row]) + ",\n"

        output += "        },\n"
        output += "    },\n"
        output += "};\n"

        return output


class MapGenerator():
    def __init__(self) -> None:
        self._maps = []

    @property
    def maps(self) -> list[Map]:
        return self._maps

    def parse_map(
        self,
        filename: str
    ) -> None:
        """
        Load and parse map
        """
        if not Path(filename).is_file():
            raise FileNotFoundError(filename)

        name = filename.split(os.sep)[-1].split('.')[0]
        with open(filename, "rb") as f:
            data = f.read()

        self._maps.append(Map(name, data))

    def generate_header(self, filename: str) -> None:
        """
        Generate header file from map
        """
        header_def = filename.split(os.sep)[-1].upper().replace('.', '_') + '_'
        with open(filename, "w") as f:
            f.writelines([
                "/**\n"
                " * Generated file\n"
                "**/\n"
                f"#ifndef {header_def}\n",
                f"#define {header_def}\n",
                "\n",
                "#include <stdint.h>\n",
                "\n",
                "\n"
            ])
            f.writelines([
                "\n\n",
                f"#endif // {header_def}"
            ])
