# This tests in argument interpreter in the MikeOS Basic Emulator.

import pytest

from constants import (
    DEFAULT_LOAD_POINT, 
    DEFAULT_STRING_VARIABLES_LOCATION
)
from debugger import Debugger
from parser import Token, TokenType
from argument import CommandArgument, TokenTypeError
from variables import VariableManager
from memory import Memory

memory = Memory()
debugger = Debugger()
memory.write_string(DEFAULT_LOAD_POINT, 'TEST:')
variables = VariableManager(memory, debugger)
variables.set_runtime_variable('prog_size', 5)

def test_numeric_argument_with_number() -> None:
    token = Token(TokenType.NUMBER, 123)
    arg = CommandArgument(token, variables)
    assert arg.to_numeric() == 123

def test_numeric_argument_with_variable() -> None:
    variables.set_numeric_variable('A', 123)
    token = Token(TokenType.VARIABLE, 'A')
    arg = CommandArgument(token, variables)
    assert arg.to_numeric() == 123
    
def test_numeric_argument_with_quoted_char() -> None:
    token = Token(TokenType.CHAR, "'A'")
    arg = CommandArgument(token, variables)
    assert arg.to_numeric() == 65
    
def test_numeric_argument_with_keyword() -> None:
    token = Token(TokenType.WORD, 'PROGSTART')
    arg = CommandArgument(token, variables)
    assert arg.to_numeric() == DEFAULT_LOAD_POINT
    
def test_numeric_argument_with_string_variable_reference() -> None:
    token = Token(TokenType.STRING_VAR_REF, '&$1')
    arg = CommandArgument(token, variables)
    assert arg.to_numeric() == DEFAULT_STRING_VARIABLES_LOCATION
    
def test_numeric_argument_with_invalid_keyword() -> None:
    token = Token(TokenType.WORD, 'INVALID')
    arg = CommandArgument(token, variables)
    with pytest.raises(TokenTypeError):
        arg.to_numeric()
        
def test_numeric_argument_with_invalid_token() -> None:
    token = Token(TokenType.QUOTE, '"test"')
    arg = CommandArgument(token, variables)
    with pytest.raises(TokenTypeError):
        arg.to_numeric()
    
def test_string_argument_with_quote() -> None:
    token = Token(TokenType.QUOTE, '"test"')
    arg = CommandArgument(token, variables)
    assert arg.to_string() == 'test'
    
def test_string_argument_with_variable() -> None:
    variables.set_string_variable('$1', 'test')
    token = Token(TokenType.STRING_VAR, '$1')
    arg = CommandArgument(token, variables)
    assert arg.to_string() == 'test'
    
def test_string_argument_with_invalid_token() -> None:
    token = Token(TokenType.NUMBER, 123)
    arg = CommandArgument(token, variables)
    with pytest.raises(TokenTypeError):
        arg.to_string()
        
def test_numeric_variable_argument_with_variable() -> None:
    token = Token(TokenType.VARIABLE, 'A')
    arg = CommandArgument(token, variables)
    assert arg.to_numeric_variable() == 'A'
    
def test_numeric_variable_argument_with_invalid_token() -> None:
    token = Token(TokenType.NUMBER, 123)
    arg = CommandArgument(token, variables)
    with pytest.raises(TokenTypeError):
        arg.to_numeric_variable()

def test_string_variable_argument_with_string_variable() -> None:
    token = Token(TokenType.STRING_VAR, '$1')
    arg = CommandArgument(token, variables)
    assert arg.to_string_variable() == '$1'

def test_string_variable_argument_with_invalid_token() -> None:
    token = Token(TokenType.QUOTE, '"test"')
    arg = CommandArgument(token, variables)
    with pytest.raises(TokenTypeError):
        arg.to_string_variable()
    

def test_word_argument_with_word() -> None:
    token = Token(TokenType.WORD, 'TEST')
    arg = CommandArgument(token, variables)
    assert arg.to_word() == 'TEST'
    
def test_word_argument_with_invalid_token() -> None:
    token = Token(TokenType.NUMBER, 123)
    arg = CommandArgument(token, variables)
    with pytest.raises(TokenTypeError):
        arg.to_word()
        
def test_symbol_argument_with_symbol() -> None:
    token = Token(TokenType.SYMBOL, '+')
    arg = CommandArgument(token, variables)
    assert arg.to_symbol() == '+'

def test_symbol_argument_with_invalid_token() -> None:
    token = Token(TokenType.NUMBER, 123)
    arg = CommandArgument(token, variables)
    with pytest.raises(TokenTypeError):
        arg.to_symbol()
        
def test_program_pointer_with_label() -> None:
    token = Token(TokenType.WORD, 'TEST')
    arg = CommandArgument(token, variables)
    assert arg.to_program_pointer() == DEFAULT_LOAD_POINT

def test_get_program_pointer_with_word() -> None:
    token = Token(TokenType.WORD, 'TEST')
    arg = CommandArgument(token, variables)
    assert arg.to_program_pointer() == DEFAULT_LOAD_POINT


def test_program_pointer_with_invalid_token() -> None:
    token = Token(TokenType.NUMBER, 123)
    arg = CommandArgument(token, variables)
    with pytest.raises(TokenTypeError):
        arg.to_program_pointer()
