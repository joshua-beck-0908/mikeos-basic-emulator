# This file manages interactive keywords for the MikeOS Basic Emulator.
import time

from typing import Callable

from constants import (
    DEFAULT_LOAD_POINT, 
    DEFAULT_NUMERIC_VARIABLES_LOCATION,
    EMULATED_MIKEOS_VERSION,
)

from variables import VariableManager

class InvalidKeywordError(Exception):
    """ For when an invalid keyword is used. """
    pass

class KeywordManager:
    def __init__(self, variables: VariableManager) -> None:
        self.keywords: dict[str, Callable[[VariableManager], int]] = {}
        self.variables = variables
        for keyword, func in all_keywords.items():
            self.add_keyword(keyword, func)

    def add_keyword(self, 
        keyword: str, 
        func: Callable[[VariableManager], int]
        ) -> None:

        self.keywords[keyword] = func

    def is_valid_keyword(self, keyword: str) -> bool:
        return keyword in self.keywords

    def get_keyword_value(self, keyword: str) -> int:
        try:
            return self.keywords[keyword](self.variables)
        except KeyError:
            raise InvalidKeywordError(f'Invalid keyword: {keyword}')
        

def do_keyword_progstart(vars: VariableManager) -> int:
    return DEFAULT_LOAD_POINT

def do_keyword_ramstart(vars: VariableManager) -> int:
    return DEFAULT_LOAD_POINT + vars.get_runtime_variable('prog_offset')

def do_keyword_variables(vars: VariableManager) -> int:
    return DEFAULT_NUMERIC_VARIABLES_LOCATION

def do_keyword_version(vars: VariableManager) -> int:
    return EMULATED_MIKEOS_VERSION

def do_keyword_timer(vars: VariableManager) -> int:
    # Simulate the BIOS system timer.
    return round(time.time() * 18.206 % 65535)

def do_keyword_ink(vars: VariableManager) -> int:
    return vars.get_runtime_variable('text')

all_keywords: dict[str, Callable[[VariableManager], int]] = {
    'PROGSTART': do_keyword_progstart,
    'RAMSTART': do_keyword_ramstart,
    'VARIABLES': do_keyword_variables,
    'VERSION': do_keyword_version,
    'TIMER': do_keyword_timer,
    'INK': do_keyword_ink,
}