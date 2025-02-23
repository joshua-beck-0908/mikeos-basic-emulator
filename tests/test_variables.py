# Tests for the variables module

import pytest

from variables import VariableManager, InvalidVariableError
from memory import Memory
from debugger import Debugger

memory = Memory()
debugger = Debugger()

def test_get_numeric_variable():
    vars = VariableManager(memory, debugger)
    vars.set_numeric_variable('A', 123)
    assert vars.get_numeric_variable('A') == 123

def test_get_invalid_numeric_variable():
    vars = VariableManager(memory, debugger)
    with pytest.raises(InvalidVariableError):
        vars.get_numeric_variable('a')
        
def test_get_string_variable():
    vars = VariableManager(memory, debugger)
    vars.set_string_variable('$1', 'test')
    assert vars.get_string_variable('$1') == 'test'

def test_get_invalid_string_variable():
    vars = VariableManager(memory, debugger)
    with pytest.raises(InvalidVariableError):
        vars.get_string_variable('9')