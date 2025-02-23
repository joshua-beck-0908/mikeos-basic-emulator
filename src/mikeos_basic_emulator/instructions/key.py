from arglist import CommandArgumentList
from environment import Environment

def do_getkey(args: CommandArgumentList, env: Environment) -> None:
    key = env.display.read_char(is_blocking=False)
    args.set_numeric_variable(key)

def do_waitkey(args: CommandArgumentList, env: Environment) -> None:
    key = env.display.read_char(is_blocking=True)
    args.set_numeric_variable(key)
    
all_commands = {
    'GETKEY': do_getkey,
    'WAITKEY': do_waitkey,
}