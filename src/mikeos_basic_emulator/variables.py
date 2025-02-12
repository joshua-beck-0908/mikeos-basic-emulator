# This file manages the variables in the MikeOS Basic Emulator.
# It is responsible for storing and retrieving variables.

from backend.interface.colours import PalettePair
from constants import (
    DEFAULT_BACKGROUND_COLOUR,
    DEFAULT_DIALOG_INNER_COLOUR,
    DEFAULT_DIALOG_OUTER_COLOUR,
    DEFAULT_DIALOG_SELECTOR_COLOUR,
    DEFAULT_LIST_DIALOG_HEIGHT,
    DEFAULT_LIST_DIALOG_WIDTH,
    DEFAULT_LIST_DIALOG_X,
    DEFAULT_LIST_DIALOG_Y,
    DEFAULT_LOAD_POINT,
    DEFAULT_NUMERIC_VARIABLES_LOCATION,
    DEFAULT_PRINT_COLOUR, 
    DEFAULT_STRING_VARIABLES_LOCATION,
    DEFAULT_STRING_LENGTH,
)
from memory import Memory
from debugger import Debugger

class InvalidVariableError(Exception):
    """ For when an invalid variable is used. """
    pass

class UndefinedLabelError(Exception):
    """ For when a non-existent label is requested. """
    pass

class UndefinedRuntimeVariableError(Exception):
    """ For when a runtime variable is not defined. """
    pass

class VariableManager:
    def __init__(self, memory: Memory) -> None:

        self.memory = memory
        self.numeric_variable_base_pointer = DEFAULT_NUMERIC_VARIABLES_LOCATION
        self.string_variable_base_pointer = DEFAULT_STRING_VARIABLES_LOCATION
        self.debugger = None
        self.runtime_variables: dict[str, int] = {}
        self.palette_variables: dict[str, PalettePair] = {}
        self.set_default_runtime_variables()
        self.set_default_palette_variables()
        
    def get_numeric_variable(self, variable: str) -> int:
        addr = self.get_numeric_variable_pointer(variable)
        return self.memory.read_word(addr)
    
    def get_string_variable(self, variable: str) -> str:
        addr = self.get_string_variable_pointer(variable)
        return self.memory.read_string(addr, DEFAULT_STRING_LENGTH);
        
    def set_numeric_variable(self, variable: str, value: int) -> None:
        if self.debugger:
            self.debugger.log_set_variable(variable, value)
        addr = self.get_numeric_variable_pointer(variable)
        self.memory.write_word(addr, value)
        
    def set_string_variable(self, variable: str, value: str) -> None:
        addr = self.get_string_variable_pointer(variable)
        self.memory.write_string(addr, value, DEFAULT_STRING_LENGTH)
        
    def get_numeric_variable_pointer(self, variable: str) -> int:
        n = ord(variable) - ord('A')
        if n < 0 or n > 25:
            raise InvalidVariableError(f'Invalid numeric variable: {variable}')
        return self.numeric_variable_base_pointer + n * 2
    
    def get_string_variable_pointer(self, variable: str) -> int:
        if variable[0] != '$':
            raise InvalidVariableError(f'Invalid string variable: {variable}')

        try:
            n = int(variable[1]) - 1
        except ValueError:
            raise InvalidVariableError(f'Invalid string variable: {variable}')

        if n < 0 or n > 7:
            raise InvalidVariableError(f'Invalid string variable: {variable}')
        return (self.string_variable_base_pointer + n * 
            (DEFAULT_STRING_LENGTH + 1))

    def get_label_pointer(self, label: str) -> int:
        progbase = DEFAULT_LOAD_POINT
        progsize = self.get_runtime_variable('prog_size')
        loc = self.memory.find_string(label, progbase, progbase + progsize)
        if loc == -1:
            raise UndefinedLabelError(f'Invalid label: {label}')
        else:
            return loc

    def set_debugger(self, debugger: Debugger) -> None:
        self.debugger = debugger
        
    def get_runtime_variable(self, variable: str) -> int:
        if variable in self.runtime_variables:
            return self.runtime_variables[variable]
        else:
            return 0
        
    def set_runtime_variable(self, variable: str, value: int) -> None:
        self.runtime_variables[variable] = value

    def set_default_runtime_variables(self) -> None:
        self.runtime_variables = {}
        self.runtime_variables['prog_size'] = 0
        self.runtime_variables['list_dialog_x'] = DEFAULT_LIST_DIALOG_X
        self.runtime_variables['list_dialog_y'] = DEFAULT_LIST_DIALOG_Y
        self.runtime_variables['list_dialog_width'] = DEFAULT_LIST_DIALOG_WIDTH
        self.runtime_variables['list_dialog_height'] = \
            DEFAULT_LIST_DIALOG_HEIGHT

    def get_palette_variable(self, variable: str) -> PalettePair:
        if variable in self.palette_variables:
            return self.palette_variables[variable]
        else:
            raise UndefinedRuntimeVariableError(
                f'Invalid runtime variable: COLOUR:{variable}')
            
    def set_palette_variable(self, variable: str, value: PalettePair) -> None:
        self.palette_variables[variable] = value
        
    def set_default_palette_variables(self) -> None:
        self.palette_variables = {}
        self.palette_variables['text'] = DEFAULT_PRINT_COLOUR
        self.palette_variables['background'] = DEFAULT_BACKGROUND_COLOUR
        self.palette_variables['dialog_outer'] = DEFAULT_DIALOG_OUTER_COLOUR
        self.palette_variables['dialog_inner'] = DEFAULT_DIALOG_INNER_COLOUR
        self.palette_variables['dialog_select'] = DEFAULT_DIALOG_SELECTOR_COLOUR
        
    def dump_runtime_variables(self) -> None:
        for key, value in self.runtime_variables.items():
            print(f'{key}: {value}')
    
    def dump_palette_variables(self) -> None:
        for key, value in self.palette_variables.items():
            print(f'{key}: {value}')
            
    def dump_numeric_variables(self) -> None:
        for i in range(26):
            variable = chr(ord('A') + i)
            value = self.get_numeric_variable(variable)
            print(f'{variable}: {value}')
            
    def dump_string_variables(self) -> None:
        for i in range(8):
            variable = f'${i + 1}'
            value = self.get_string_variable(variable)
            print(f'{variable}: "{value}"')

    