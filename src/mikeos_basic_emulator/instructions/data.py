# This file contains the data commands for the MikeOS BASIC emulator.

from arglist import CommandArgumentList
from environment import Environment

def cmd_peek(args: CommandArgumentList, env: Environment) -> None:
    outvar = args.get_numeric_variable()
    address = args.get_numeric()
    value = env.memory.read_byte(address)
    env.variables.set_numeric_variable(outvar, value)
    
def cmd_poke(args: CommandArgumentList, env: Environment) -> None:
    value = args.get_numeric()
    address = args.get_numeric()
    env.memory.write_byte(address, value)
    
def cmd_peekint(args: CommandArgumentList, env: Environment) -> None:
    outvar = args.get_numeric_variable()
    address = args.get_numeric()
    value = env.memory.read_word(address)
    env.variables.set_numeric_variable(outvar, value)
    
def cmd_pokeint(args: CommandArgumentList, env: Environment) -> None:
    value = args.get_numeric()
    address = args.get_numeric()
    env.memory.write_word(address, value)

    