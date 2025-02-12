import pytest

from environment import Environment
from runcmd import CommandRunner
from parser import CommandParser as Parser

env = Environment()

def test_command_with_no_command() -> None:
    runner = CommandRunner(env)
    runner.run_command('')
    
def test_command_with_comment() -> None:
    runner = CommandRunner(env)
    runner.run_command('REM')
    
def test_command_with_variable_assignment() -> None:
    runner = CommandRunner(env)
    runner.run_command('A = 1')
    assert env.variables.get_numeric_variable('A') == 1

def test_command_with_string_assignment() -> None:
    runner = CommandRunner(env)
    runner.run_command('$1 = "test"')
    assert env.variables.get_string_variable('$1') == 'test'

def test_command_with_sum() -> None:
    runner = CommandRunner(env)
    runner.run_command('A = 1 + 2')
    assert env.variables.get_numeric_variable('A') == 3
    
def test_command_with_multiple_sum() -> None:
    runner = CommandRunner(env)
    runner.run_command('A = 1 + 20 + 300')
    runner.run_command('B = A + 4000')
    assert env.variables.get_numeric_variable('B') == 4321
    
def test_command_with_string_sum() -> None:
    runner = CommandRunner(env)
    runner.run_command('$1 = "test" + "test"')
    assert env.variables.get_string_variable('$1') == 'testtest'

def test_command_with_string_multiple_sum() -> None:
    runner = CommandRunner(env)
    runner.run_command('$1 = "test" + "test"')
    runner.run_command('$2 = $1 + "test"')
    assert env.variables.get_string_variable('$2') == 'testtesttest'
    
def test_multiplication() -> None:
    runner = CommandRunner(env)
    runner.run_command('A = 2 * 3')
    assert env.variables.get_numeric_variable('A') == 6
    
def test_division() -> None:
    runner = CommandRunner(env)
    runner.run_command('A = 6 / 2')
    assert env.variables.get_numeric_variable('A') == 3
    
def test_inexact_division() -> None:
    runner = CommandRunner(env)
    runner.run_command('A = 5 / 2')
    assert env.variables.get_numeric_variable('A') == 2
    
def test_negative_number() -> None:
    runner = CommandRunner(env)
    runner.run_command('A = 5')
    runner.run_command('A = A - 6')
    assert env.variables.get_numeric_variable('A') == 2**16 - 1
    
def test_overflow() -> None:
    runner = CommandRunner(env)
    runner.run_command('A = 65535')
    runner.run_command('A = A + 1')
    assert env.variables.get_numeric_variable('A') == 0
    
def test_modulo() -> None:
    runner = CommandRunner(env)
    runner.run_command('A = 5 % 2')
    assert env.variables.get_numeric_variable('A') == 1