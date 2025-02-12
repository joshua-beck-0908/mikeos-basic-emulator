# This is the module for the curses interface of the MikeOS Basic Emulator.
import curses
import string

from backend.interface.dialog import DialogBox, Listbox
from constants import (
    DEFAULT_COLUMNS,
    DEFAULT_LINES,
    DEFAULT_BACKGROUND_COLOUR,
    DEFAULT_PRINT_COLOUR,
)

from backend.interface.display import TextDisplay
from backend.interface.area import Position, Area
from backend.interface.colours import (
    Palette, 
    PalettePair, 
)

from backend.ncurses.colours import (
    curses_colours,
    curses_to_palette,
    palette_pair_to_attribute,
)
from debugger import Debugger
from variables import VariableManager

class CursesTextDisplay(TextDisplay):
    def __init__(self, variables: VariableManager, debugger: Debugger) -> None:
        self.stdscr = curses.initscr()
        self.initialise_display()
        self.set_print_colour(DEFAULT_PRINT_COLOUR)
        self.finished = False
        self.variables = variables
        self.debugger = debugger
        
    def initialise_display(self) -> None:
        curses.resize_term(DEFAULT_LINES, DEFAULT_COLUMNS)
        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        self.stdscr.scrollok(True)
        self.stdscr.keypad(True)
        for i, bg in enumerate(curses_colours):
            for j, fg in enumerate(curses_colours):
                curses.init_pair(i * len(curses_colours) + j + 1, fg, bg)
        self.fill_area(
            Area(Position(0, 0), 
            Position(DEFAULT_LINES, DEFAULT_COLUMNS)), 
            ' ', 
            DEFAULT_BACKGROUND_COLOUR
        )
        self.move_cursor(Position(0, 0))
        
    def open_window(self) -> None:
        pass

        
    def update(self) -> None:
        self.stdscr.refresh()
        
    def move_cursor(self, position: Position) -> None:
        self.stdscr.move(position.row, position.col)
        
    def advance_cursor(self) -> None:
        y, x = self.stdscr.getyx()
        _, max_x = self.stdscr.getmaxyx()
        x += 1
        if x >= max_x:
            self.newline()
        else:
            self.stdscr.move(y, x)


    def scroll(self) -> None:
        self.stdscr.scroll()
        
    def show_cursor(self) -> None:
        curses.curs_set(1)

    def hide_cursor(self) -> None:
        curses.curs_set(0)
        
    def get_cursor_position(self) -> Position:
        row, col = self.stdscr.getyx()
        return Position(col, row)
    
    def get_character_at_cursor(self) -> str:
        return chr(self.stdscr.inch() % 256)
    
    def get_character_colour_at_cursor(self) -> PalettePair:
        colour = self.stdscr.inch() >> 8
        colour = colour & curses.A_ATTRIBUTES
        text = colour % len(curses_colours) + 1
        background = colour // len(curses_colours) + 1
        return PalettePair(
            curses_to_palette[text],
            curses_to_palette[background]
        )
        

    def input_string(self, prompt: str = '') -> str:
        #return self.stdscr.getstr().decode('ascii', errors='replace')
        if prompt != '':
            self.print(prompt)
        output = ''
        key = ''
        while key != 13:
            key = self.read_char()
            if key == 13:
                continue
            elif chr(key) in string.printable:
                self.print(chr(key))
                output += chr(key)
        self.newline()
        return output
    
    def read_char(self, is_blocking: bool = True) -> int:
        self.stdscr.nodelay(not is_blocking)
        char = self.stdscr.getch()
        if char == -1:
            return 0
        elif char == curses.KEY_UP:
            return 1
        elif char == curses.KEY_DOWN:
            return 2
        elif char == curses.KEY_LEFT:
            return 3
        elif char == curses.KEY_RIGHT:
            return 4
        else:
            return self.stdscr.getch() % 256

    def newline(self) -> None:
        y, _ = self.stdscr.getyx()
        max_y, _ = self.stdscr.getmaxyx()
        if y + 1 >= max_y:
            self.scroll()
            self.stdscr.move(max_y, 0)
        else:
            self.stdscr.move(y + 1, 0)

    def print(self, text: str, colour: PalettePair|None = None) -> None:
        self.stdscr.addstr(text, self.curses_print_attribute)
        
    def clear_screen(self) -> None:
        self.stdscr.clear()
        
    def has_exited(self) -> bool:
        return self.finished
        
    def show_alert_dialog(self, message: str) -> None:
        alert_dialog = DialogBox(self, self.variables)
        alert_dialog.set_message(message)
        alert_dialog.run()
        
    def show_list_dialog(self,
        list_items: list[str],
        prompt_line_1: str,
        prompt_line_2: str,
    ) -> int:

        list_dialog = Listbox(self, self.variables)
        list_dialog.set_items(list_items)
        list_dialog.set_prompts(prompt_line_1, prompt_line_2)
        return list_dialog.run()

    def fill_area(self, area: Area, char: str, colour: PalettePair) -> None:
        self.stdscr.scrollok(False)
        rows, cols = self.stdscr.getmaxyx()
        attribute = palette_pair_to_attribute(colour)
        for row in range(rows - 1):
            self.stdscr.insstr(row, 0, ' ' * cols, attribute)
        self.stdscr.scrollok(True)

    def handle_events(self) -> None:
        pass

    def exit(self) -> None:
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.noecho()
        curses.endwin()

    def set_print_colour(self, colour: PalettePair) -> None:
        self.print_colour = colour
        self.curses_print_attribute = palette_pair_to_attribute(colour)

    def get_print_colour(self) -> PalettePair:
        return self.print_colour
    
