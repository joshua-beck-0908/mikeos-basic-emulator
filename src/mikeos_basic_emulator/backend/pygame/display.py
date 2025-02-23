# This is the VGA module of the MikeOS Basic Emulator.
# It is responsible for emulating a 80x25 VGA text mode display.
# Roughly based on the mode 3 of the VGA standard.

import time
from pathlib import Path

import pygame
from pygame.font import Font

from backend.interface.display import GraphicTextDisplay
from backend.interface.dialog import DialogBox, FileSelector, Listbox
from constants import (
    DEFAULT_BACKGROUND_COLOUR,
    DEFAULT_CHARACTER_HEIGHT,
    DEFAULT_CHARACTER_WIDTH,
    DEFAULT_COLUMNS,
    DEFAULT_CURSOR_BLINK,
    DEFAULT_CURSOR_BLINK_INTERVAL,
    DEFAULT_CURSOR_HEIGHT,
    DEFAULT_CURSOR_VISIBILITY,
    DEFAULT_LINES,
    DEFAULT_WINDOW_TITLE,
)

from backend.interface.area import Area, Position
from backend.interface.colours import PalettePair
from backend.pygame.cursor import Cursor
from backend.pygame.keyboard import Keyboard
from backend.pygame.character import TextCharacter
from debugger import Debugger
from filesystem import SFNDirectory
from variables import VariableManager

VGA_FONT_PATH = Path('uni_vga/u_vga16.bdf')

class PygameTextDisplay(GraphicTextDisplay):
    def __init__(self, variables: VariableManager, debugger: Debugger) -> None:
        self.set_defaults()
        self.initialise_display()
        self.setup_text_characters()
        self.debugger = debugger
        self.variables = variables
        self.cursor = Cursor(limits=Position(self.columns, self.lines))
        self.finished = False
        self.keyboard = Keyboard(self, debugger)
        self.cursor_state = False
        

    def initialise_display(self) -> None:
        pygame.init()
        self.screen: pygame.Surface|None = None
        self.font = pygame.font.Font(VGA_FONT_PATH, self.character_height)
        self.surface = pygame.Surface(
            (self.character_width * self.columns, self.character_height * self.lines)
        )
        

    def set_defaults(self) -> None:
        self.character_width = DEFAULT_CHARACTER_WIDTH
        self.character_height = DEFAULT_CHARACTER_HEIGHT
        self.columns = DEFAULT_COLUMNS
        self.lines = DEFAULT_LINES
        self.pixel_width = self.character_width * self.columns
        self.pixel_height = self.character_height * self.lines
        self.default_colour = DEFAULT_BACKGROUND_COLOUR
        self.cursor_visible = DEFAULT_CURSOR_VISIBILITY
        self.cursor_blink = DEFAULT_CURSOR_BLINK
        self.cursor_blink_interval = DEFAULT_CURSOR_BLINK_INTERVAL
        self.cursor_height = DEFAULT_CURSOR_HEIGHT
        self.window_title = DEFAULT_WINDOW_TITLE
        
    def setup_text_characters(self) -> None:
        self.characters: list[TextCharacter] = []
        for y in range(self.lines):
            for x in range(self.columns):
                self.characters.append(TextCharacter(self, Position(x, y)))
                
    def open_window(self) -> None:
        self.screen = pygame.display.set_mode((
            self.pixel_width, self.pixel_height
        ))
        pygame.display.set_caption(self.window_title)
        
    def get_font(self) -> Font:
        return self.font
    
    def get_surface(self) -> pygame.Surface:
        return self.surface
    
    def get_character_width_and_height(self) -> tuple[int, int]:
        return self.character_width, self.character_height
    
    def update(self) -> None:
        is_updated = False
        self.draw_cursor()
        for character in self.characters:
            character.draw()
            is_updated |= character.updated
            
        if self.screen and is_updated:
            self.screen.blit(self.surface, (0, 0))
            pygame.display.update()
        
    def move_cursor(self, position: Position) -> None:
        self.set_cursor_state(False)
        self.cursor.move(position)

    def advance_cursor(self) -> None:
        self.set_cursor_state(False)
        self.cursor.advance()
        
    def scroll(self) -> None:
        for y in range(1, self.lines):
            for x in range(self.columns):
                self.get_cell(Position(x, y - 1)).copy_from(
                    self.get_cell(Position(x, y))
                )
        for x in range(self.columns):
            self.get_cell(Position(x, self.lines - 1)).set_char_and_colour(
                ' ', self.default_colour
            )
    
    def show_cursor(self) -> None:
        self.cursor_visible = True
        
    def hide_cursor(self) -> None:
        self.cursor_visible = False

    def get_cursor_position(self) -> Position:
        return self.cursor.get_position()
    
    def get_character_at_cursor(self) -> str:
        return self.get_cursor_cell().get_char()
    
    def get_character_colour_at_cursor(self) -> PalettePair:
        return self.get_cursor_cell().get_colour()
        
    def set_print_colour(self, colour: PalettePair) -> None:
        self.default_colour = colour
        self.variables.set_palette_variable('text', colour)
        
    def get_print_colour(self) -> PalettePair:
        return self.default_colour

    def set_cursor_state(self, state: bool) -> None:
        if state != self.cursor_state:
            if state == True:
                self.characters[self.cursor.get_offset()].show_cursor(
                    self.cursor_height
                )
            else:
                self.characters[self.cursor.get_offset()].hide_cursor()
            self.cursor_state = state
            
    def input_string(self, prompt: str = '') -> str:
        return self.keyboard.read_string(prompt)
    
    def read_char(self, is_blocking: bool = True) -> int:
        return self.keyboard.read_char(is_blocking)

    def draw_cursor(self) -> None:
        if self.cursor_visible:
            if self.cursor_blink:
                if (time.time() % self.cursor_blink_interval < 
                    self.cursor_blink_interval / 2):
                    self.set_cursor_state(False)
                else:
                    self.set_cursor_state(True)
            else:
                self.set_cursor_state(True)
        else:
            self.set_cursor_state(False)
            
    def get_cursor_cell(self) -> 'TextCharacter':
        return self.get_cell(self.cursor.get_position())
    
    def get_cell(self, position: Position) -> 'TextCharacter':
        return self.characters[position.row * self.columns + position.col]

    def newline(self) -> None:
        self.set_cursor_state(False)
        self.cursor.newline()
        if self.cursor.wants_scroll():
            self.scroll()


    def print(self, text: str, colour: PalettePair|None = None) -> None:
        self.debugger.log_print(text)
        colour = colour or self.default_colour
        for char in text:
            if char == '\n':
                self.newline()
            else:
                cell = self.characters[self.cursor.get_offset()]
                cell.set_char_and_colour(char, colour)
                self.advance_cursor()
                
    def clear_screen(self) -> None:
        for cell in self.characters:
            cell.set_char_and_colour(' ', self.default_colour)
        self.move_cursor(Position(0, 0))
        
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

    def show_file_dialog(self, filesystem: SFNDirectory) -> str:
        file_dialog = FileSelector(self, self.variables, filesystem)
        return file_dialog.run()
        
    def fill_area(self, 
        area: Area,
        char: str, 
        colour: PalettePair) -> None:
        
        for y in range(area.start.row, area.end.row + 1):
            for x in range(area.start.col, area.end.col + 1):
                self.get_cell(Position(x, y)).set_char_and_colour(char, colour)

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.finished = True
            elif event.type == pygame.KEYDOWN:
                self.keyboard.handle_input(event)
                
                
    def exit(self) -> None:
        self.finished = True
        pygame.quit()
            

        