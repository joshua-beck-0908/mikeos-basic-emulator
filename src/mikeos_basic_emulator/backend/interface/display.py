from abc import ABC, abstractmethod

from backend.interface.area import Area, Position
from backend.interface.colours import PalettePair

from pygame.font import Font
from pygame.surface import Surface

from debugger import Debugger
from variables import VariableManager

class TextDisplay(ABC):
    @abstractmethod
    def __init__(self, variables: VariableManager, debugger: Debugger) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def open_window(self) -> None:
        """ Starts the main window interface. """
        raise NotImplementedError
    
    @abstractmethod
    def update(self) -> None:
        """ Called from the main thread to update the display. """
        raise NotImplementedError
    
    @abstractmethod
    def move_cursor(self, position: Position) -> None:
        """ Moves the cursor using a Position object. """
        raise NotImplementedError
    
    @abstractmethod
    def advance_cursor(self) -> None:
        """ Moves the cursor to the next position. """
        raise NotImplementedError
    
    @abstractmethod
    def scroll(self) -> None:
        """ Scrolls down one line. """
        raise NotImplementedError
    
    @abstractmethod
    def show_cursor(self) -> None:
        """ Shows the cursor. """
        raise NotImplementedError
    
    @abstractmethod
    def hide_cursor(self) -> None:
        """ Hides the cursor. """
        raise NotImplementedError
    
    @abstractmethod
    def get_cursor_position(self) -> Position:
        """ Returns the current cursor position. """
        raise NotImplementedError
    
    @abstractmethod
    def get_character_at_cursor(self) -> str:
        """ Returns the ASCII character under the cursor. """
        raise NotImplementedError
    
    @abstractmethod
    def get_character_colour_at_cursor(self) -> PalettePair:
        """ Returns the colour of the character under the cursor. """
        raise NotImplementedError
    
    @abstractmethod
    def input_string(self, prompt: str = '') -> str:
        """ Prompts the user for a string input. """
        raise NotImplementedError
    
    @abstractmethod
    def read_char(self, is_blocking: bool = True) -> int:
        """ 
        Reads a single character from the keyboard.
        An ASCII code is returned, or numbers 0-3 for up,down,left,right.
        """

        raise NotImplementedError
    
    @abstractmethod
    def newline(self) -> None:
        """
        Moves the cursor to the start of the next line.
        Scrolls if the cursor is at the bottom of the screen.
        """
        raise NotImplementedError
    
    @abstractmethod
    def print(self, text: str, colour: PalettePair|None = None) -> None:
        """
        Prints a string to the screen at the current cursor position.
        The current text colour is used if none is specified.
        """
        raise NotImplementedError
    
    @abstractmethod
    def clear_screen(self) -> None:
        """ Clears the screen. """
        raise NotImplementedError
    
    @abstractmethod
    def has_exited(self) -> bool:
        """ Called by the worker thread to check if the display has exited. """
        raise NotImplementedError

    @abstractmethod
    def show_alert_dialog(self, message: str) -> None:
        """ Shows a dialog box with a message and an OK button. """
        raise NotImplementedError
    
    @abstractmethod
    def show_list_dialog(self,
        list_items: list[str],
        prompt_line_1: str,
        prompt_line_2: str,
    ) -> int:
        """
        Shows a dialog box with a list of items.
        Returns the selected index starting from one.
        Zero is returned if the dialog was cancelled.
        """
        raise NotImplementedError
    
    @abstractmethod
    def fill_area(self, area: Area, char: str, colour: PalettePair) -> None:
        """
        Fills an area with a character and colour.
        The area is defined to the top left and bottom right corners.
        This is an inclusive range.
        """
        raise NotImplementedError
    
    @abstractmethod
    def handle_events(self) -> None:
        """
        Called from the main thread to handle window events.
        """
        raise NotImplementedError
    
    @abstractmethod
    def exit(self) -> None:
        """
        Called to close the window and clean up resources.
        """
        raise NotImplementedError

    @abstractmethod
    def set_print_colour(self, colour: PalettePair) -> None:
        """ Sets the default text colour. """
        raise NotImplementedError
    
    @abstractmethod
    def get_print_colour(self) -> PalettePair:
        """ Returns the default text colour. """
        raise NotImplementedError
    
    
class GraphicTextDisplay(TextDisplay):
    @abstractmethod
    def get_character_width_and_height(self) -> tuple[int, int]:
        raise NotImplementedError
    
    @abstractmethod
    def get_font(self) -> Font:
        raise NotImplementedError
    
    @abstractmethod
    def get_surface(self) -> Surface:
        raise NotImplementedError
    