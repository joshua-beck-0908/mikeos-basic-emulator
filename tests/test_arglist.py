# This tests the argument list parser in the MikeOS Basic Emulator.

import pytest

from arglist import CommandArgumentList
from argument import ArgumentError, TokenTypeError
from constants import DEFAULT_LOAD_POINT
from parser import Token, TokenType
from variables import VariableManager
from memory import Memory

memory = Memory()
variables = VariableManager(memory)
memory.write_string(DEFAULT_LOAD_POINT, 'TEST:')
variables.set_runtime_variable('prog_size', 5)

def test_assume_argument_exists() -> None:
    args = CommandArgumentList([Token(TokenType.NUMBER, 123)], variables)
    args.assume_argument_exists()

def test_assume_argument_exists_when_no_arguments() -> None:
    args = CommandArgumentList([], variables)
    with pytest.raises(ArgumentError):
        args.assume_argument_exists()
        
def test_expect_more_arguments_with_two_arguments() -> None:
    args = CommandArgumentList([
        Token(TokenType.NUMBER, 123), 
        Token(TokenType.NUMBER, 456)
    ], variables)
    args.expect_more_arguments(2)
    
def test_expect_more_arguments_with_one_argument() -> None:
    args = CommandArgumentList([Token(TokenType.NUMBER, 123)], variables)
    with pytest.raises(ArgumentError):
        args.expect_more_arguments(2)
        
def test_does_argument_exist_when_true() -> None:
    args = CommandArgumentList([Token(TokenType.NUMBER, 123)], variables)
    assert args.does_argument_exist() == True

def test_does_argument_exist_when_false() -> None:
    args = CommandArgumentList([], variables)
    assert args.does_argument_exist() == False
        
def test_next() -> None:
    args = CommandArgumentList([
        Token(TokenType.NUMBER, 123),
        Token(TokenType.NUMBER, 456)
    ], variables)
    args.next()
    assert args.get_numeric() == 456

def test_get_numeric() -> None:
    args = CommandArgumentList([Token(TokenType.NUMBER, 123)], variables)
    assert args.get_numeric() == 123
    
def test_get_numeric_when_wrong_type() -> None:
    args = CommandArgumentList([Token(TokenType.QUOTE, '"test"')], variables)
    with pytest.raises(TokenTypeError):
        args.get_numeric()
        
def test_get_numeric_when_no_arguments() -> None:
    args = CommandArgumentList([], variables)
    with pytest.raises(ArgumentError):
        args.get_numeric()

def test_get_string() -> None:
    args = CommandArgumentList([Token(TokenType.QUOTE, '"test"')], variables)
    assert args.get_string() == 'test'
    
def test_get_numeric_variable() -> None:
    args = CommandArgumentList([Token(TokenType.VARIABLE, 'A')], variables)
    assert args.get_numeric_variable() == 'A'
    
def test_get_string_variable() -> None:
    args = CommandArgumentList([Token(TokenType.STRING_VAR, '$1')], variables)
    assert args.get_string_variable() == '$1'
    
def test_get_word() -> None:
    args = CommandArgumentList([Token(TokenType.WORD, 'TEST')], variables)
    assert args.get_word() == 'TEST'
    
def test_get_symbol() -> None:
    args = CommandArgumentList([Token(TokenType.SYMBOL, '+')], variables)
    assert args.get_symbol() == '+'

def test_get_program_pointer() -> None:
    args = CommandArgumentList([Token(TokenType.WORD, 'TEST')], variables)
    assert args.get_program_pointer() == DEFAULT_LOAD_POINT
    
def test_get_specific_symbol() -> None:
    args = CommandArgumentList([Token(TokenType.SYMBOL, '+')], variables)
    args.get_specific_symbol('+')

def test_get_specific_symbol_when_wrong_symbol() -> None:
    args = CommandArgumentList([Token(TokenType.SYMBOL, '+')], variables)
    with pytest.raises(ArgumentError):
        args.get_specific_symbol('-')

def test_get_specific_symbol_when_not_symbol() -> None:
    args = CommandArgumentList([Token(TokenType.NUMBER, 123)], variables)
    with pytest.raises(TokenTypeError):
        args.get_specific_symbol('+')

def test_get_specific_word() -> None:
    args = CommandArgumentList([Token(TokenType.WORD, 'TEST')], variables)
    args.get_specific_word('TEST')
    
def test_get_specific_word_when_wrong_word() -> None:
    args = CommandArgumentList([Token(TokenType.WORD, 'TEST')], variables)
    with pytest.raises(ArgumentError):
        args.get_specific_word('TEST2')
        
def test_get_specific_word_when_not_word() -> None:
    args = CommandArgumentList([Token(TokenType.NUMBER, 123)], variables)
    with pytest.raises(TokenTypeError):
        args.get_specific_word('TEST')

def test_get_symbol_from_list() -> None:
    args = CommandArgumentList([Token(TokenType.SYMBOL, '+')], variables)
    assert args.get_symbol_from_list(['+', '-']) == '+'
    
def test_get_symbol_from_list_when_wrong_symbol() -> None:
    args = CommandArgumentList([Token(TokenType.SYMBOL, '+')], variables)
    with pytest.raises(ArgumentError):
        args.get_symbol_from_list(['-', '*'])
        
def test_get_symbol_from_list_when_not_symbol() -> None:
    args = CommandArgumentList([Token(TokenType.NUMBER, 123)], variables)
    with pytest.raises(TokenTypeError):
        args.get_symbol_from_list(['+', '-'])

def test_get_word_from_list() -> None:
    args = CommandArgumentList([Token(TokenType.WORD, 'TEST')], variables)
    assert args.get_word_from_list(['TEST', 'TEST2']) == 'TEST'

def test_get_word_from_list_when_wrong_word() -> None:
    args = CommandArgumentList([Token(TokenType.WORD, 'TEST')], variables)
    with pytest.raises(ArgumentError):
        args.get_word_from_list(['TEST2', 'TEST3'])

def test_get_word_from_list_when_not_word() -> None:
    args = CommandArgumentList([Token(TokenType.NUMBER, 123)], variables)
    with pytest.raises(TokenTypeError):
        args.get_word_from_list(['TEST', 'TEST2'])

def test_get_token() -> None:
    args = CommandArgumentList([Token(TokenType.NUMBER, 123)], variables)
    assert args.get_token() == Token(TokenType.NUMBER, 123)

def test_has_any_when_true() -> None:
    args = CommandArgumentList([
        Token(TokenType.NUMBER, 123),
        Token(TokenType.NUMBER, 456)
    ], variables)
    args.next()
    assert args.has_any() == True

def test_has_any_when_false() -> None:
    args = CommandArgumentList([Token(TokenType.NUMBER, 123)], variables)
    args.next()
    assert args.has_any() == False

def test_has_any_when_no_arguments() -> None:
    args = CommandArgumentList([], variables)
    assert args.has_any() == False

def test_has_string_when_true() -> None:
    args = CommandArgumentList([Token(TokenType.QUOTE, '"test"')], variables)
    assert args.has_string() == True
    
def test_has_string_when_false() -> None:
    args = CommandArgumentList([Token(TokenType.NUMBER, 123)], variables)
    assert args.has_string() == False
    
def test_has_string_when_empty() -> None:
    args = CommandArgumentList([], variables)
    assert args.has_string() == False
    
def test_has_numeric_when_true() -> None:
    args = CommandArgumentList([Token(TokenType.NUMBER, 123)], variables)
    assert args.has_numeric() == True

def test_has_numeric_when_false() -> None:
    args = CommandArgumentList([Token(TokenType.QUOTE, '"test"')], variables)
    assert args.has_numeric() == False

def test_has_numeric_when_empty() -> None:
    args = CommandArgumentList([], variables)
    assert args.has_numeric() == False
    
def test_has_numeric_variable_when_true() -> None:
    args = CommandArgumentList([Token(TokenType.VARIABLE, 'A')], variables)
    assert args.has_numeric_variable() == True

def test_has_numeric_variable_when_false() -> None:
    args = CommandArgumentList([Token(TokenType.NUMBER, 123)], variables)
    assert args.has_numeric_variable() == False

def test_has_numeric_variable_when_empty() -> None:
    args = CommandArgumentList([], variables)
    assert args.has_numeric_variable() == False

def test_has_string_variable_when_true() -> None:
    args = CommandArgumentList([Token(TokenType.STRING_VAR, '$1')], variables)
    assert args.has_string_variable() == True

def test_has_string_variable_when_false() -> None:
    args = CommandArgumentList([Token(TokenType.NUMBER, 123)], variables)
    assert args.has_string_variable() == False

def test_has_string_variable_when_empty() -> None:
    args = CommandArgumentList([], variables)
    assert args.has_string_variable() == False

def test_has_word_when_true() -> None:
    args = CommandArgumentList([Token(TokenType.WORD, 'TEST')], variables)
    assert args.has_word() == True

def test_has_word_when_false() -> None:
    args = CommandArgumentList([Token(TokenType.NUMBER, 123)], variables)
    assert args.has_word() == False

def test_has_word_when_empty() -> None:
    args = CommandArgumentList([], variables)
    assert args.has_word() == False

def test_has_symbol_when_true() -> None:
    args = CommandArgumentList([Token(TokenType.SYMBOL, '+')], variables)
    assert args.has_symbol() == True

def test_has_symbol_when_false() -> None:
    args = CommandArgumentList([Token(TokenType.NUMBER, 123)], variables)
    assert args.has_symbol() == False

def test_has_symbol_when_empty() -> None:
    args = CommandArgumentList([], variables)
    assert args.has_symbol() == False

def test_has_specific_symbol_when_true() -> None:
    args = CommandArgumentList([Token(TokenType.SYMBOL, '+')], variables)
    assert args.has_specific_symbol('+') == True

def test_has_specific_symbol_when_false() -> None:
    args = CommandArgumentList([Token(TokenType.SYMBOL, '+')], variables)
    assert args.has_specific_symbol('-') == False

def test_has_specific_symbol_when_empty() -> None:
    args = CommandArgumentList([], variables)
    assert args.has_specific_symbol('+') == False

def test_has_specific_word_when_true() -> None:
    args = CommandArgumentList([Token(TokenType.WORD, 'TEST')], variables)
    assert args.has_specific_word('TEST') == True

def test_has_specific_word_when_false() -> None:
    args = CommandArgumentList([Token(TokenType.WORD, 'TEST')], variables)
    assert args.has_specific_word('TEST2') == False

def test_has_specific_word_when_empty() -> None:
    args = CommandArgumentList([], variables)
    assert args.has_specific_word('TEST') == False
    
def test_set_numeric_variable() -> None:
    args = CommandArgumentList([Token(TokenType.VARIABLE, 'A')], variables)
    args.set_numeric_variable(123)
    assert variables.get_numeric_variable('A') == 123

def test_set_string_variable() -> None:
    args = CommandArgumentList([Token(TokenType.STRING_VAR, '$1')], variables)
    args.set_string_variable('test')
    assert variables.get_string_variable('$1') == 'test'
