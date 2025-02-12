import curses

from backend.interface.colours import Palette, PalettePair

palette_to_curses_colour = {
    Palette.BLACK: curses.COLOR_BLACK,
    Palette.BLUE: curses.COLOR_BLUE,
    Palette.GREEN: curses.COLOR_GREEN,
    Palette.CYAN: curses.COLOR_CYAN,
    Palette.RED: curses.COLOR_RED,
    Palette.MAGENTA: curses.COLOR_MAGENTA,
    Palette.BROWN: curses.COLOR_YELLOW,
    Palette.LIGHT_GRAY: curses.COLOR_WHITE,
    Palette.DARK_GRAY: curses.COLOR_BLACK,
    Palette.LIGHT_BLUE: curses.COLOR_BLUE,
    Palette.LIGHT_GREEN: curses.COLOR_GREEN,
    Palette.LIGHT_CYAN: curses.COLOR_CYAN,
    Palette.LIGHT_RED: curses.COLOR_RED,
    Palette.LIGHT_MAGENTA: curses.COLOR_MAGENTA,
    Palette.YELLOW: curses.COLOR_YELLOW,
    Palette.WHITE: curses.COLOR_WHITE
}

curses_to_palette = {
    curses.COLOR_BLACK: Palette.BLACK,
    curses.COLOR_BLUE: Palette.BLUE,
    curses.COLOR_GREEN: Palette.GREEN,
    curses.COLOR_CYAN: Palette.CYAN,
    curses.COLOR_RED: Palette.RED,
    curses.COLOR_MAGENTA: Palette.MAGENTA,
    curses.COLOR_YELLOW: Palette.BROWN,
    curses.COLOR_WHITE: Palette.LIGHT_GRAY
}

curses_colours = [
    curses.COLOR_BLACK,
    curses.COLOR_BLUE,
    curses.COLOR_GREEN,
    curses.COLOR_CYAN,
    curses.COLOR_RED,
    curses.COLOR_MAGENTA,
    curses.COLOR_YELLOW,
    curses.COLOR_WHITE,
]

def palette_pair_to_attribute(pair: PalettePair) -> int:
    fg = curses_colours.index(palette_to_curses_colour[pair.text])
    bg = curses_colours.index(palette_to_curses_colour[pair.bg])
    return curses.color_pair((bg << 3 | fg) + 1)
