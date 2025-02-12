from arglist import CommandArgumentList
from environment import Environment

def cmd_delete(args: CommandArgumentList, env: Environment) -> None:
    try:
        env.filesystem.delete_file(args.get_string())
    except FileNotFoundError:
        env.variables.set_numeric_variable('R', 2)
    except (PermissionError, OSError):
        env.variables.set_numeric_variable('R', 1)
    else:
        env.variables.set_numeric_variable('R', 0)
    
def cmd_load(args: CommandArgumentList, env: Environment) -> None:
    try:
        filename = args.get_string()
        address = args.get_numeric()
        size = env.filesystem.get_file_size(filename)
        env.filesystem.load_file(filename, address)
    except (FileNotFoundError,PermissionError, OSError):
        env.variables.set_numeric_variable('R', 1)
    else:
        env.variables.set_numeric_variable('R', 0)
        env.variables.set_numeric_variable('S', size)

def cmd_rename(args: CommandArgumentList, env: Environment) -> None:
    try:
        env.filesystem.rename_file(args.get_string(), args.get_string())
    except FileExistsError:
        env.variables.set_numeric_variable('R', 3)
    except FileNotFoundError:
        env.variables.set_numeric_variable('R', 2)
    except (PermissionError, OSError):
        env.variables.set_numeric_variable('R', 1)
    else:
        env.variables.set_numeric_variable('R', 0)
        
def cmd_save(args: CommandArgumentList, env: Environment) -> None:
    try:
        filename = args.get_string()
        address = args.get_numeric()
        length = args.get_numeric()
        if env.filesystem.does_file_exist(filename):
            env.variables.set_numeric_variable('R', 2)
        else:
            env.filesystem.save_file(filename, address, length)
            env.variables.set_numeric_variable('R', 0)
    except (PermissionError, OSError):
        env.variables.set_numeric_variable('R', 1)
    else:
        env.variables.set_numeric_variable('R', 0)
        
def cmd_size(args: CommandArgumentList, env: Environment) -> None:
    try:
        size = env.filesystem.get_file_size(args.get_string())
    except FileNotFoundError:
        env.variables.set_numeric_variable('R', 1)
    else:
        env.variables.set_numeric_variable('R', 0)
        env.variables.set_numeric_variable('S', size)
        
all_commands = {
    'DELETE': cmd_delete,
    'LOAD': cmd_load,
    'RENAME': cmd_rename,
    'SAVE': cmd_save,
    'SIZE': cmd_size
}