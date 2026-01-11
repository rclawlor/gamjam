# Standard library
from importlib import resources
from string import Template

# Local imports
from csprite.map import MapGenerator
from csprite.palette import PaletteGenerator
from csprite.sprite import SpriteGenerator
from csprite.shared import generate_comment, write_comment
from csprite import templates


TEMPLATE_FILE = resources.files(templates) / "graphics.txt"


class GraphicsGenerator():
    def __init__(
        self,
        sprite: SpriteGenerator,
        background: SpriteGenerator,
        font: SpriteGenerator,
        palette: PaletteGenerator,
        map: MapGenerator
    ) -> None:
        self._sprite = sprite
        self._background = background
        self._font = font
        self._palette = palette
        self._map = map

    def generate_header(self, filename: str) -> None:
        """
        Generate header file from binary data
        """
        header_def = "GRAPHICS_H_"

        with open(filename, "w") as f:
            write_comment(f, "Generated file")
            f.writelines([
                f"#ifndef {header_def}\n",
                f"#define {header_def}\n",
                "\n",
                "#include <stdint.h>\n",
                "\n\n"
            ])
            f.writelines([
                "int GRAPHICS_init();\n",
                "int GRAPHICS_reload();\n"
                "\n\n"
            ])

            write_comment(f, "Sprites")
            for spritesheet in self._sprite.spritesheets:
                f.write(f"extern {spritesheet.pointer};\n")
            f.write("\n\n")

            write_comment(f, "Backgrounds")
            for spritesheet in self._background.spritesheets:
                f.write(f"extern {spritesheet.pointer};\n")
            f.write("\n\n")

            write_comment(f, "Fonts")
            for spritesheet in self._font.spritesheets:
                f.write(f"extern {spritesheet.pointer};\n")
            f.write("\n\n")

            write_comment(f, "Palettes")
            for palette in self._palette.palettes:
                f.write(f"extern {palette.pointer};\n")
            f.write("\n\n")

            write_comment(f, "Maps")
            for map in self._map.maps:
                f.write(f"extern {map.pointer};\n")

            f.writelines([
                "\n\n",
                f"#endif // {header_def}"
            ])

    def generate_src(self, filename: str) -> None:
        """
        Generate source file from binary data
        """
        with TEMPLATE_FILE.open("r") as f:
            template = Template(f.read())

        definitions = ""
        symbol_list = []

        definitions += generate_comment("Sprites")
        for spritesheet in self._sprite.spritesheets:
            definitions += f"{spritesheet.pointer} = NULL;\n"
            symbol_list.append([spritesheet.name, spritesheet.cast])
        definitions += "\n\n"

        definitions += generate_comment("Backgrounds")
        for spritesheet in self._background.spritesheets:
            definitions += f"{spritesheet.pointer} = NULL;\n"
            symbol_list.append([spritesheet.name, spritesheet.cast])
        definitions += "\n\n"

        definitions += generate_comment("Fonts")
        for spritesheet in self._font.spritesheets:
            definitions += f"{spritesheet.pointer} = NULL;\n"
            symbol_list.append([spritesheet.name, spritesheet.cast])
        definitions += "\n\n"

        definitions += generate_comment("Palettes")
        for palette in self._palette.palettes:
            definitions += f"{palette.pointer} = NULL;\n"
            symbol_list.append([palette.name, palette.cast])
        definitions += "\n\n"

        definitions += generate_comment("Maps")
        for map in self._map.maps:
            definitions += f"{map.pointer} = NULL;\n"
            symbol_list.append([map.name, map.cast])

        symbols = '\n'.join([
            (
                f'    {i} = {j}dlsym(libgraphics, "{i}");\n'
                f"    if ({i} == NULL) {{\n"
                '         fprintf(stderr, "Could not find ##name in %s: %s", '
                'LIBGRAPHICS_NAME, dlerror());\n'
                "          return 1;\n"
                "      }\n"
            )
            for i, j in symbol_list])
        output = template.substitute({
            "definitions": definitions,
            "symbols": symbols
        })

        with open(filename, "w") as f:
            f.write(output)

    def generate_lib_header(self, filename: str) -> None:
        """
        Generate library header file from binary data
        """
        with open(filename, "w") as f:
            write_comment(f, "Generated file")
            f.write("\n")
            f.write("#include <stdint.h>\n")
            f.write("\n\n")
            f.write("\n".join([f"extern {i.definition};\n" for i in self._sprite.spritesheets]))
            f.write("\n".join([f"extern {i.definition};\n" for i in self._background.spritesheets]))
            f.write("\n".join([f"extern {i.definition};\n" for i in self._font.spritesheets]))
            f.write("\n".join([f"extern {i.definition};\n" for i in self._palette.palettes]))
            f.write("\n".join([f"extern {i.definition};\n" for i in self._map.maps]))

    def generate_lib_src(self, filename: str) -> None:
        """
        Generate library source file from binary data
        """
        with open(filename, "w") as f:
            write_comment(f, "Generated file")
            f.write("\n")
            f.write('#include "graphics.h"\n')
            f.write("#include <stdint.h>\n")
            f.write("\n\n")
            f.write("\n".join([i.generate_arrays() for i in self._sprite.spritesheets]))
            f.write("\n".join([i.generate_arrays() for i in self._background.spritesheets]))
            f.write("\n".join([i.generate_arrays() for i in self._font.spritesheets]))
            f.write("\n".join([i.generate_array() for i in self._palette.palettes]))
            f.write("\n".join([i.generate_array() for i in self._map.maps]))
