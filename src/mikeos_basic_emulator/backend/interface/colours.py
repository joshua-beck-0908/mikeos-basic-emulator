# This file holds the colours for the emulator.
# Both RGB and palette colours are defined here.

from enum import Enum
from typing import NamedTuple

class RGBColour(Enum):
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 170)
    GREEN = (0, 170, 0)
    CYAN = (0, 170, 170)
    RED = (170, 0, 0)
    MAGENTA = (170, 0, 170)
    BROWN = (170, 85, 0)
    LIGHT_GREY = (170, 170, 170)
    DARK_GREY = (85, 85, 85)
    LIGHT_BLUE = (85, 85, 255)
    LIGHT_GREEN = (85, 255, 85)
    LIGHT_CYAN = (85, 255, 255)
    LIGHT_RED = (255, 85, 85)
    LIGHT_MAGENTA = (255, 85, 255)
    YELLOW = (255, 255, 85)
    WHITE = (255, 255, 255)
    
class RGBPair(NamedTuple):
    text: RGBColour
    bg: RGBColour
    
class Palette(Enum):
    BLACK = 0
    BLUE = 1
    GREEN = 2
    CYAN = 3
    RED = 4
    MAGENTA = 5
    BROWN = 6
    LIGHT_GREY = 7
    DARK_GREY = 8
    LIGHT_BLUE = 9
    LIGHT_GREEN = 10
    LIGHT_CYAN = 11
    LIGHT_RED = 12
    LIGHT_MAGENTA = 13
    YELLOW = 14
    WHITE = 15

class PalettePair(NamedTuple):
    text: Palette
    bg: Palette

rgb_colour_to_palette = {
    RGBColour.BLACK: Palette.BLACK,
    RGBColour.BLUE: Palette.BLUE,
    RGBColour.GREEN: Palette.GREEN,
    RGBColour.CYAN: Palette.CYAN,
    RGBColour.RED: Palette.RED,
    RGBColour.MAGENTA: Palette.MAGENTA,
    RGBColour.BROWN: Palette.BROWN,
    RGBColour.LIGHT_GREY: Palette.LIGHT_GREY,
    RGBColour.DARK_GREY: Palette.DARK_GREY,
    RGBColour.LIGHT_BLUE: Palette.LIGHT_BLUE,
    RGBColour.LIGHT_GREEN: Palette.LIGHT_GREEN,
    RGBColour.LIGHT_CYAN: Palette.LIGHT_CYAN,
    RGBColour.LIGHT_RED: Palette.LIGHT_RED,
    RGBColour.LIGHT_MAGENTA: Palette.LIGHT_MAGENTA,
    RGBColour.YELLOW: Palette.YELLOW,
    RGBColour.WHITE: Palette.WHITE,
}

palette_to_rgb_colour = {v: k for k, v in rgb_colour_to_palette.items()}

def palette_pair_to_int(pair: PalettePair) -> int:
    """ Converts a PalettePair to the number formated used by BIOS. """
    return pair.text.value | pair.bg.value << 4

def int_to_palette_pair(vgacode: int) -> PalettePair:
    return PalettePair(
        Palette(vgacode & 0xF),
        Palette(vgacode >> 4)
    )

def palette_pair_to_rgb(pair: PalettePair) -> RGBPair:
    """ Converts a PalettePair to an (R, G, B) tuple. """
    return RGBPair(
        palette_to_rgb_colour[pair.text],
        palette_to_rgb_colour[pair.bg]
    )


def text_to_palette_pair(value: str) -> PalettePair:
    """
    This converts a string from the TOML file into a PalettePair 
    used by the emulator.
    """

    # In the config file it's formatted like: "WHITE, BLACK".
    # But the user could input it as "white, black" or "white,black".
    fg, bg = value.split(", ")
    fg = fg.strip().upper()
    bg = bg.strip().upper()
    try:
        return PalettePair(getattr(Palette, fg), getattr(Palette, bg))
    except AttributeError:
        raise ValueError(f'Invalid colour: {fg}, {bg} used in config file.')

