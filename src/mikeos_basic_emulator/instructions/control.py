from arglist import CommandArgumentList, CommandRoutine
from backend.interface.area import Position
from backend.interface.colours import int_to_palette_pair, palette_pair_to_int
from environment import Environment

def cmd_break(args: CommandArgumentList, env: Environment) -> None:
    env.debugger.breakpoint(env)
    
def cmd_call(args: CommandArgumentList, env: Environment) -> None:
    env.debugger.error('COMMAND', 'CALL command not supported.')
    env.debugger.breakpoint(env)

def cmd_end(args: CommandArgumentList, env: Environment) -> None:
    env.debugger.program_exit(env)
    
    
all_commands = {
    'BREAK': cmd_break,
    'CALL': cmd_call,
    'END': cmd_end,
}