# Standard library imports
import os
from pathlib import Path

# Local imports
from csprite.display import DisplayTable
from csprite.sprite import SpriteGenerator
from csprite.palette import PaletteGenerator
from csprite.map import MapGenerator
from csprite.graphics import GraphicsGenerator


def generate_sprites() -> SpriteGenerator:
    """
    Generate sprite headers
    """
    sprite_generator = SpriteGenerator()
    for file in os.listdir("assets/sprites"):
        if not file.endswith(".4bpp"):
            continue
        table = DisplayTable(file)
        sprite_generator.parse_spritesheet(f"assets/sprites/{file}")

        version = sprite_generator.spritesheets[-1].version
        table.add_row("Version", '.'.join([f"{i}" for i in version]))

        sprites = sprite_generator.spritesheets[-1].sprites
        table.add_row("Sprites", len(sprites))
        table.draw()

    Path("include/assets").mkdir(parents=True, exist_ok=True)
    sprite_generator.generate_header("include/assets/sprite.h")

    return sprite_generator


def generate_backgrounds() -> SpriteGenerator:
    """
    Generate background headers
    """
    sprite_generator = SpriteGenerator()
    for file in os.listdir("assets/backgrounds"):
        if not file.endswith(".4bpp"):
            continue
        table = DisplayTable(file)
        sprite_generator.parse_spritesheet(f"assets/backgrounds/{file}")

        version = sprite_generator.spritesheets[-1].version
        table.add_row("Version", '.'.join([f"{i}" for i in version]))

        sprites = sprite_generator.spritesheets[-1].sprites
        table.add_row("Tiles", len(sprites))
        table.draw()

    Path("include/assets").mkdir(parents=True, exist_ok=True)
    sprite_generator.generate_header("include/assets/background.h")

    return sprite_generator


def generate_fonts() -> SpriteGenerator:
    """
    Generate font headers
    """
    sprite_generator = SpriteGenerator()
    for file in os.listdir("assets/fonts"):
        if not file.endswith(".4bpp"):
            continue
        table = DisplayTable(file)
        sprite_generator.parse_spritesheet(f"assets/fonts/{file}")

        version = sprite_generator.spritesheets[-1].version
        table.add_row("Version", '.'.join([f"{i}" for i in version]))

        sprites = sprite_generator.spritesheets[-1].sprites
        table.add_row("Characters", len(sprites))
        table.draw()

    Path("include/assets").mkdir(parents=True, exist_ok=True)
    sprite_generator.generate_header("include/assets/font.h")

    return sprite_generator


def generate_palettes() -> PaletteGenerator:
    """
    Generate palette headers
    """
    palette_generator = PaletteGenerator()
    for file in os.listdir("assets/palettes"):
        if not file.endswith(".pal"):
            continue
        table = DisplayTable(file)
        palette_generator.parse_palette(f"assets/palettes/{file}")

        version = palette_generator.palettes[-1].version
        table.add_row("Version", '.'.join([f"{i}" for i in version]))

        palettes = palette_generator.palettes[-1]
        for label, colours in zip(palettes.labels, palettes.colours):
            table.add_palette(label, colours)
        table.draw()

    Path("include/assets").mkdir(parents=True, exist_ok=True)
    palette_generator.generate_header("include/assets/palette.h")

    return palette_generator


def generate_maps() -> MapGenerator:
    """
    Generate map headers
    """
    map_generator = MapGenerator()
    for file in os.listdir("assets/maps"):
        if not file.endswith(".map"):
            continue
        table = DisplayTable(file)
        map_generator.parse_map(f"assets/maps/{file}")

        version = map_generator.maps[0].version
        table.add_row("Version", '.'.join([f"{i}" for i in version]))

        table.draw()

    Path("include/assets").mkdir(parents=True, exist_ok=True)
    map_generator.generate_header("include/assets/map.h")

    return map_generator


def generate_assets() -> None:
    """
    Generate c header files from binary assets
    """
    sprite = generate_sprites()
    background = generate_backgrounds()
    font = generate_fonts()
    palette = generate_palettes()
    map = generate_maps()

    graphics = GraphicsGenerator(sprite, background, font, palette, map)

    Path("include/assets").mkdir(parents=True, exist_ok=True)
    graphics.generate_header("include/assets/graphics.h")

    Path("src/assets").mkdir(parents=True, exist_ok=True)
    graphics.generate_src("src/assets/graphics.c")

    Path("src/lib").mkdir(parents=True, exist_ok=True)
    graphics.generate_lib_header("src/lib/graphics.h")
    graphics.generate_lib_src("src/lib/graphics.c")


if __name__ == "__main__":
    generate_assets()
