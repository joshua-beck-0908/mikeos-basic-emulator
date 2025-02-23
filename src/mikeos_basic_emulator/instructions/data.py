# This file contains the data commands for the MikeOS BASIC emulator.

import random

from arglist import CommandArgumentList
from environment import Environment

def cmd_peek(args: CommandArgumentList, env: Environment) -> None:
    outvar = args.get_numeric_variable()
    address = args.get_numeric()
    value = env.memory.read_byte(address)
    env.variables.set_numeric_variable(outvar, value)
    
def cmd_peekint(args: CommandArgumentList, env: Environment) -> None:
    outvar = args.get_numeric_variable()
    address = args.get_numeric()
    value = env.memory.read_word(address)
    env.variables.set_numeric_variable(outvar, value)
    
def cmd_poke(args: CommandArgumentList, env: Environment) -> None:
    value = args.get_numeric()
    address = args.get_numeric()
    env.memory.write_byte(address, value)
    
def cmd_pokeint(args: CommandArgumentList, env: Environment) -> None:
    value = args.get_numeric()
    address = args.get_numeric()
    env.memory.write_word(address, value)

def cmd_rand(args: CommandArgumentList, env: Environment) -> None:
    outvar = args.get_numeric_variable()
    minimum = args.get_numeric()
    maximum = args.get_numeric()
    value = random.randint(minimum, maximum)
    env.variables.set_numeric_variable(outvar, value)
    
def cmd_read(args: CommandArgumentList, env: Environment) -> None:
    block_name, start_position = args.get_label_and_pointer()

    if block_name not in env.read_blocks.keys():
        interpreter = env.get_command_runner()
        start_position = env.memory.find_next_line(start_position)
        raw_data = env.memory.read_line(start_position)
        data_args = interpreter.decode_arguments(raw_data)
        
        data: list[int] = []
        while data_args.has_numeric():
            data.append(data_args.get_numeric())
        env.read_blocks[block_name] = data
    else:
        data = env.read_blocks[block_name]
            
    position = args.get_numeric()

    if position >= len(data):
        raise ValueError('End of data block reached')
    else:
        args.set_numeric_variable(data[position])
    

all_commands = {
    'PEEK': cmd_peek,
    'POKE': cmd_poke,
    'PEEKINT': cmd_peekint,
    'POKEINT': cmd_pokeint,
    'RAND': cmd_rand,
    'READ': cmd_read,
}
