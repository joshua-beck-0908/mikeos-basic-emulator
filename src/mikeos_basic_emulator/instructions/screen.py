from itertools import zip_longest

from arglist import CommandArgumentList, CommandRoutine
from backend.interface.area import Position
from backend.interface.colours import int_to_palette_pair, palette_pair_to_int
from environment import Environment

def cmd_print(args: CommandArgumentList, env: Environment) -> None:
    args.expect_more_arguments(1)

    if args.has_string():
        env.display.print(args.get_string())
    elif args.has_numeric():
        env.display.print(str(args.get_numeric()))
    elif args.has_word():
        keyword = args.get_word_from_list(['CHR', 'HEX'])
        if keyword == 'CHR':
            env.display.print(chr(args.get_numeric()))
        elif keyword == 'HEX':
            value = hex(args.get_numeric()) % 256
            env.display.print(f'{value:02X}')
    else:
        args.syntax_error('Invalid argument type for PRINT command.')
    
    if not args.has_specific_symbol(';'):
        env.display.print('\n')
    
def cmd_cls(args: CommandArgumentList, env: Environment) -> None:
    env.display.clear_screen()
    
def cmd_cursor(args: CommandArgumentList, env: Environment) -> None:
    keyword = args.get_word_from_list(['ON', 'OFF'])
    if keyword == 'ON':
        env.display.show_cursor()
    elif keyword == 'OFF':
        env.display.hide_cursor()
        
def cmd_curschar(args: CommandArgumentList, env: Environment) -> None:
    char = env.display.get_character_at_cursor()
    args.set_numeric_variable(ord(char))
    
def cmd_curscol(args: CommandArgumentList, env: Environment) -> None:
    colour = env.display.get_character_colour_at_cursor()
    args.set_numeric_variable(palette_pair_to_int(colour))
    
def cmd_curspos(args: CommandArgumentList, env: Environment) -> None:
    pos = env.display.get_cursor_position()
    args.set_numeric_variable(pos.col)
    args.set_numeric_variable(pos.row)
    
def cmd_ink(args: CommandArgumentList, env: Environment) -> None:
    colour = int_to_palette_pair(args.get_numeric())
    env.variables.set_palette_variable('text', colour)
    
def cmd_move(args: CommandArgumentList, env: Environment) -> None:
    x = args.get_numeric()
    y = args.get_numeric()
    env.display.move_cursor(Position(x, y))
    
def cmd_input(args: CommandArgumentList, env: Environment) -> None:
    value = env.display.input_string()
    if args.has_string_variable():
        args.set_string_variable(value)
    elif args.has_numeric_variable():
        try:
            args.set_numeric_variable(int(value))
        except ValueError:
            args.syntax_error('Invalid numeric input')
    else:
        args.syntax_error('Invalid argument type for INPUT command.')

def cmd_alert(args: CommandArgumentList, env: Environment) -> None:
    env.display.show_alert_dialog(args.get_string())
    
def cmd_listbox(args: CommandArgumentList, env: Environment) -> None:
    env.display.show_list_dialog(
        ['item 1', 'item 2', 'item 3'], 
        'Select an item', '')
    
def cmd_askfile(args: CommandArgumentList, env: Environment) -> None:
    files = env.filesystem.list_files()
    choice = env.display.show_list_dialog(
        files,
        'Please select a file using the cursor',
        'keys from the list below...'
    )
    if choice > 0:
        args.set_string_variable(files[choice - 1])
    else:
        args.set_string_variable('')
        
def cmd_files(args: CommandArgumentList, env: Environment) -> None:
    files = env.filesystem.list_files()
    iterator = [iter(files)] * 5
    lines = zip(*iterator)
    for line in lines:
        for file in line:
            env.display.print(file.ljust(15))
        env.display.newline()

all_commands: dict[str, CommandRoutine] = {
    'ALERT': cmd_alert,
    'ASKFILE': cmd_askfile,
    'CLS': cmd_cls,
    'CURSCHAR': cmd_curschar,
    'CURSCOL': cmd_curscol,
    'CURSOR': cmd_cursor,
    'CURSPOS': cmd_curspos,
    'FILES': cmd_files,
    'INK': cmd_ink,
    'INPUT': cmd_input,
    'LISTBOX': cmd_listbox,
    'MOVE': cmd_move,
    'PRINT': cmd_print,
}
