# Standard library imports
import os
from pathlib import Path

# Local
from csprite.shared import chunks


PALETTE_LENGTH = 8


class PaletteGroup():
    def __init__(
        self,
        name: str,
        data: bytes
    ) -> None:
        self._name = name
        self._data = data
        self._version = [int(i) for i in self._data[:3]]
        self._palettes = []
        self._labels = []
        self._parse_palette()

    @property
    def version(self) -> list[int]:
        return self._version

    @property
    def labels(self) -> list[str]:
        return self._labels

    @property
    def palettes(self) -> list[bytes]:
        return self._palettes

    @property
    def colours(self) -> list[list[int]]:
        colours = []
        for palette in self._palettes:
            colours.append([[r, g, b] for r, g, b in chunks(palette, 3)])

        return colours

    @property
    def name(self) -> str:
        return f"{self._name.upper()}_PAL"

    @property
    def definition(self) -> str:
        return (
            f"uint32_t {self._name.upper()}_PAL"
            f"[{len(self.palettes)}][{PALETTE_LENGTH}]"
        )

    @property
    def pointer(self) -> str:
        return f"uint32_t (*{self._name.upper()}_PAL)[{len(self.palettes)}][{PALETTE_LENGTH}]"

    @property
    def cast(self) -> str:
        return f"(uint32_t (*)[{len(self.palettes)}][{PALETTE_LENGTH}])"

    def _parse_palette(self) -> None:
        """
        Parse palette into list of colours
        """
        offset = 3
        labels = []
        palettes = []
        while offset < len(self._data):
            offset, label, palette = self._extract_palette(self._data, offset)
            labels.append(label)
            palettes.append(palette)
        self._labels = labels
        self._palettes = palettes

    def _extract_palette(
        self,
        data: bytes,
        offset: int
    ) -> tuple[int, str, bytes]:
        """
        Extract palette from `.pal` file
        """
        label_length = data[offset]
        label = str(
            data[1 + offset:label_length + 1 + offset],
            encoding="utf-8"
        )

        offset += label_length + 1
        data = data[offset:offset + PALETTE_LENGTH * 3]

        offset += PALETTE_LENGTH * 3

        return offset, label, data

    def generate_enum(self) -> str:
        """
        Generate enum from palette names
        """
        enum_name = self._name.lower().capitalize()

        output = "typedef enum {\n"
        for idx, label in enumerate(self._labels):
            if idx == 0:
                output += f"    {label.upper()} = 0,\n"
            else:
                output += f"    {label.upper()},\n"

        output += f"    NUM_{enum_name.upper()}_PALETTES\n"
        output += f"}} {enum_name}Pal_e;\n"

        return output

    def generate_array(self) -> str:
        """
        Format byte data into c array
        """
        output = (
            f"uint32_t {self._name.upper()}_PAL[][{PALETTE_LENGTH}] = {{\n"
        )
        for palette in self._palettes:
            array = "    {\n"
            for r, g, b in chunks(palette, 3):
                array += f"        0xff{r:02x}{g:02x}{b:02x},\n"
            array += "    },\n"
            output += array

        output += "};\n"

        return output


class PaletteGenerator():
    def __init__(self) -> None:
        self._palettes = []

    @property
    def palettes(self) -> list[PaletteGroup]:
        return self._palettes

    def parse_palette(
        self,
        filename: str
    ) -> None:
        """
        Load and parse palette
        """
        if not Path(filename).is_file():
            raise FileNotFoundError(filename)

        name = filename.split(os.sep)[-1].split('.')[0]
        with open(filename, "rb") as f:
            data = f.read()

        self._palettes.append(
            PaletteGroup(name, data)
        )

    def generate_header(self, filename: str) -> None:
        """
        Generate header file from spritesheets
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
            f.write("\n".join([i.generate_enum() for i in self._palettes]))
            f.writelines([
                "\n\n",
                f"#endif // {header_def}"
            ])
