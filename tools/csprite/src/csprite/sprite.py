# Standard library
import os
from pathlib import Path

# Local imports
from csprite.shared import chunks


# Constants
SPRITE_WIDTH = 8
SPRITE_PIXELS = SPRITE_WIDTH**2


class Spritesheet():
    def __init__(
        self,
        name: str,
        data: bytes
    ) -> None:
        self._name = name
        self._data = data
        self._version = [int(i) for i in self._data[:3]]
        self._sprites = []
        self._parse_spritesheet()

    @property
    def version(self) -> list[int]:
        return self._version

    @property
    def sprites(self) -> list[bytes]:
        return self._sprites

    @property
    def name(self) -> str:
        return f"{self._name.upper()}_SPRITE"

    @property
    def definition(self) -> str:
        return (
            f"uint8_t {self._name.upper()}_SPRITE"
            f"[{len(self.sprites)}][{SPRITE_PIXELS // 2}]"
        )

    @property
    def pointer(self) -> str:
        return f"uint8_t (*{self._name.upper()}_SPRITE)[{len(self.sprites)}][{SPRITE_PIXELS // 2}]"

    @property
    def cast(self) -> str:
        return f"(uint8_t (*)[{len(self.sprites)}][{SPRITE_PIXELS // 2}])"

    def _parse_spritesheet(self) -> None:
        """
        Parse spritesheet into labels/sprites
        """
        self._offset = 3
        labels = []
        sprites = []
        while self._offset < len(self._data):
            label, sprite = self._extract_sprite()

            labels.append(label)
            sprites.append(sprite)
        self._labels = labels
        self._sprites = sprites

    def _extract_sprite(self) -> tuple[str, bytes]:
        """
        Extract sprite from `.4bpp` file
        """
        label_length = self._data[self._offset]
        label = str(
            self._data[1 + self._offset:label_length + 1 + self._offset],
            encoding="utf-8"
        )

        self._offset += label_length + 1
        data = self._data[self._offset:self._offset + SPRITE_PIXELS // 2]

        self._offset += SPRITE_PIXELS // 2

        return label, data

    def generate_enum(self) -> str:
        """
        Generate enum from sprite names
        """
        enum_name = self._name.lower().capitalize()

        output = "typedef enum {\n"
        for idx, label in enumerate(self._labels):
            if idx == 0:
                output += f"    {label.upper()} = 0,\n"
            else:
                output += f"    {label.upper()},\n"

        output += f"    NUM_{enum_name.upper()}_SPRITES\n"
        output += f"}} {enum_name}Spr_e;\n"

        return output

    def generate_arrays(self) -> str:
        """
        Format byte data into c arrays
        """
        output = (
            f"uint8_t {self._name.upper()}_SPRITE[][{SPRITE_PIXELS // 2}] = {{\n"
        )
        for sprite in self._sprites:
            array = "    {\n"
            for row in chunks(sprite, SPRITE_WIDTH // 2):
                array += "    " + ", ".join([f"0x{i:02X}" for i in row]) + ",\n"
            array += "    },\n"
            output += array
        output += "};\n"

        return output


class SpriteGenerator():
    def __init__(self) -> None:
        self._spritesheets = []

    @property
    def spritesheets(self) -> list[Spritesheet]:
        return self._spritesheets

    def parse_spritesheet(
        self,
        filename: str
    ) -> None:
        """
        Load and parse spritesheet
        """
        if not Path(filename).is_file():
            raise FileNotFoundError(filename)

        name = filename.split(os.sep)[-1].split('.')[0]
        data = Path(filename).read_bytes()

        self._spritesheets.append(
            Spritesheet(name, data)
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
            f.write("\n".join([i.generate_enum() for i in self._spritesheets]))
            f.writelines([
                "\n\n",
                f"#endif // {header_def}"
            ])
