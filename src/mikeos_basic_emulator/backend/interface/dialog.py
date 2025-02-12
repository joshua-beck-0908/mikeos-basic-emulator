from backend.interface.area import Area, Position
from backend.interface.display import TextDisplay
from constants import (
    DEFAULT_LIST_DIALOG_X,
    DEFAULT_LIST_DIALOG_Y,
    DEFAULT_LIST_DIALOG_WIDTH,
    DEFAULT_LIST_DIALOG_HEIGHT,
    DEFAULT_MESSAGE_DIALOG_HEIGHT,
    DEFAULT_MESSAGE_DIALOG_WIDTH,
    DEFAULT_MESSAGE_DIALOG_X,
    DEFAULT_MESSAGE_DIALOG_Y
)
from variables import VariableManager

class Listbox:
    def __init__(self, display: TextDisplay, 
                variables: VariableManager) -> None:
        self.display = display
        self.variables = variables
        self.items = []
        self.prompt_line_1 = ''
        self.prompt_line_2 = ''
        self.selector_offset = 0
        self.list_offset = 0
        self.box_drawn = False
        self.prepare_areas()
        self.prepare_colours()
        
    def set_items(self, items: list[str]) -> None:
        self.items = items
        
    def set_prompts(self, line_1: str, line_2: str) -> None:
        self.prompt_line_1 = line_1
        self.prompt_line_2 = line_2
        
    def prepare_areas(self) -> None:
        self.box_area = Area(
            Position(
                DEFAULT_LIST_DIALOG_X, 
                DEFAULT_LIST_DIALOG_Y
            ), 
            Position(
                DEFAULT_LIST_DIALOG_X + DEFAULT_LIST_DIALOG_WIDTH, 
                DEFAULT_LIST_DIALOG_Y + DEFAULT_LIST_DIALOG_HEIGHT
            )
        )
        self.list_area = Area(
            Position(
                DEFAULT_LIST_DIALOG_X + 1,
                DEFAULT_LIST_DIALOG_Y + 4
            ),
            Position(
                DEFAULT_LIST_DIALOG_X + DEFAULT_LIST_DIALOG_WIDTH - 1,
                DEFAULT_LIST_DIALOG_Y + DEFAULT_LIST_DIALOG_HEIGHT - 1
            )
        )
        self.list_length = self.list_area.height - 2
    
    def prepare_colours(self) -> None:
        self.list_colour = self.variables.get_palette_variable(
            'dialog_inner')
        self.selection_colour = self.variables.get_palette_variable(
            'dialog_select')
        self.box_colour = self.variables.get_palette_variable(
            'dialog_outer')

    def draw(self) -> None:
        if not self.box_drawn:
            self.draw_box()
        visible_list = self.items[
            self.list_offset:self.list_offset + self.list_length + 1]
        itempos = self.list_area.start.down(1).right(1)

        for index, item in enumerate(visible_list):
            item = item.ljust(self.list_area.width - 2)
            self.display.move_cursor(itempos.down(index))
            if index == self.selector_offset:
                self.display.print(item, self.selection_colour)
            else:
                self.display.print(item, self.list_colour)
                
    def draw_box(self) -> None:
        self.display.fill_area(self.box_area, ' ', self.box_colour)
        self.display.fill_area(self.list_area, ' ', self.list_colour)
        prompt_position = self.box_area.start.down(1).right(1)
        self.display.move_cursor(prompt_position)
        self.display.print(self.prompt_line_1, self.box_colour)
        self.display.move_cursor(prompt_position.down(1))
        self.display.print(self.prompt_line_2, self.box_colour)

    def move_up(self) -> None:
        if self.selector_offset == 0:
            if self.list_offset > 0:
                self.list_offset -= 1
        else:
            self.selector_offset -= 1
            
    def move_down(self) -> None:
        if (self.selector_offset + 1) == self.list_length:
            if self.list_offset + self.list_length < len(self.items):
                self.list_offset += 1
        else:
            self.selector_offset += 1
    
    def run(self) -> int:
        self.display.hide_cursor()
        self.draw()
        while True:
            inkey = self.display.read_char()
            if inkey == 1:
                self.move_up()
                self.draw()
            elif inkey == 2:
                self.move_down()
                self.draw()
            elif inkey == 13:
                return self.selector_offset + self.list_offset + 1
            elif inkey == 27:
                return 0

class DialogBox:
    def __init__(self, display: TextDisplay,
                variables: VariableManager) -> None:
        self.display = display
        self.variables = variables
        self.message = ''
        self.button = '   OK   '
        self.prepare_areas()
        self.prepare_colours()
        
    def set_message(self, message: str) -> None:
        self.message = message
        
    def prepare_areas(self) -> None:
        self.box_area = Area(
            Position(
                DEFAULT_MESSAGE_DIALOG_X, 
                DEFAULT_MESSAGE_DIALOG_Y
            ), 
            Position(
                DEFAULT_MESSAGE_DIALOG_X + DEFAULT_MESSAGE_DIALOG_WIDTH, 
                DEFAULT_MESSAGE_DIALOG_Y + DEFAULT_MESSAGE_DIALOG_HEIGHT
            )
        )
        self.button_position = Position(
            DEFAULT_MESSAGE_DIALOG_X + 
                DEFAULT_MESSAGE_DIALOG_WIDTH // 2 - 
                len(self.button) // 2,
            DEFAULT_MESSAGE_DIALOG_Y + DEFAULT_MESSAGE_DIALOG_HEIGHT - 2
        )
    
    def prepare_colours(self) -> None:
        self.box_colour = self.variables.get_palette_variable(
            'dialog_outer')
        self.inner_colour = self.variables.get_palette_variable(
            'dialog_inner')
        
    def draw(self) -> None:
        self.display.fill_area(self.box_area, ' ', self.box_colour)
        self.display.move_cursor(Position(
                self.box_area.start.col + 1,
                self.box_area.start.row + 1
        ))
        self.display.print(self.message, self.inner_colour)
        self.display.move_cursor(self.button_position)

    def run(self) -> None:
        self.display.hide_cursor()
        self.draw()
        while self.display.read_char() != 13:
            pass
        self.display.show_cursor()
