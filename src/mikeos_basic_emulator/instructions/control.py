from arglist import CommandArgumentList
from environment import Environment
from constants import DEFAULT_LOAD_POINT
from variables import ForVariable

def cmd_break(args: CommandArgumentList, env: Environment) -> None:
    env.debugger.breakpoint(env)
    
def cmd_call(args: CommandArgumentList, env: Environment) -> None:
    env.debugger.error('COMMAND', 'CALL command not supported.')
    env.debugger.breakpoint(env)

def cmd_do(args: CommandArgumentList, env: Environment) -> None:
    env.do_stack.append(env.next_line_address)
    
def cmd_else(args: CommandArgumentList, env: Environment) -> None:
    # If the previous IF was not true, run the rest of the line next.
    # Otherwise it is skipped.
    if not env.last_if_true:
        env.next_command = args.make_new_arglist_from_remaining()

def cmd_end(args: CommandArgumentList, env: Environment) -> None:
    env.debugger.on_program_exit(env)

def cmd_for(args: CommandArgumentList, env: Environment) -> None:
    iteration_variable = args.get_numeric_variable()
    args.get_specific_symbol('=')
    start_value = args.do_numeric_sum()
    args.get_specific_word('TO')
    end_value = args.do_numeric_sum()

    forvar = ForVariable(iteration_variable, env.variables)
    forvar.set_range(start_value, end_value)
    forvar.set_loop_start_position(env.next_line_address)
    env.for_variables[iteration_variable] = forvar

def cmd_goto(args: CommandArgumentList, env: Environment) -> None:
    new_position = args.get_program_pointer()
    env.next_line_address = new_position
    
def cmd_gosub(args: CommandArgumentList, env: Environment) -> None:
    # Return to the address after the GOSUB command
    next_line = env.memory.find_next_line(env.program_counter)
    # Push the return address onto the stack
    env.gosub_stack.append(next_line)
    
    # Find the new position from the next argument.
    new_position = args.get_program_pointer()
    # Now set it as the next line to run.
    env.next_line_address = new_position

def cmd_if(args: CommandArgumentList, env: Environment) -> None:
    result = args.check_condition()
    while args.has_specific_word('AND'):
        result = result and args.check_condition()
    env.last_if_true = result
    
    args.get_specific_word('THEN')
    
    # If true then make a new command from the remaining arguments.
    # Otherwise ignore the remaining arguments.
    if result == True:
        new_command = args.make_new_arglist_from_remaining()
        env.next_command = new_command
    
def cmd_include(args: CommandArgumentList, env: Environment) -> None:
    filename = args.get_string()
    progsize = env.variables.get_runtime_variable('prog_size')
    loadpoint = DEFAULT_LOAD_POINT + progsize
    try:
        size = env.filesystem.get_file_size(filename)
        env.filesystem.load_file(filename, loadpoint)
    except FileNotFoundError:
        env.debugger.error('FILE', f'File not found: {filename}')
        env.debugger.breakpoint(env)
    else:
        env.variables.set_runtime_variable('prog_size', progsize + size)
        
        
def cmd_loop(args: CommandArgumentList, env: Environment) -> None:
    loop_type = args.get_word_from_list(['WHILE', 'UNTIL', 'ENDLESS'])
    
    if loop_type == 'WHILE':
        continue_loop = args.check_condition()
    elif loop_type == 'UNTIL':
        continue_loop = not args.check_condition()
    else:
        continue_loop = True

    loop_start = env.do_stack.pop()
    if continue_loop:
        env.next_line_address = loop_start

def cmd_next(args: CommandArgumentList, env: Environment) -> None:
    for_variable = args.get_numeric_variable()
    if for_variable not in env.for_variables:
        env.debugger.error('COMMAND', f'NEXT without FOR: {for_variable}')
        env.debugger.breakpoint(env)
    else:
        for_var = env.for_variables[for_variable]
        for_var.increment()
        if for_var.is_finished():
            del env.for_variables[for_variable]
        else:
            env.next_line_address = for_var.get_loop_start_position()
            
def cmd_pause(args: CommandArgumentList, env: Environment) -> None:
    seconds = args.get_numeric() / 10
    env.delay(seconds)
    
def cmd_return(args: CommandArgumentList, env: Environment) -> None:
    if len(env.gosub_stack) == 0:
        env.debugger.error('COMMAND', 'RETURN without GOSUB.')
        env.debugger.breakpoint(env)
    else:
        env.next_line_address = env.gosub_stack.pop()
        

    
all_commands = {
    'BREAK': cmd_break,
    'CALL': cmd_call,
    'DO': cmd_do,
    'ELSE': cmd_else,
    'END': cmd_end,
    'FOR': cmd_for,
    'GOSUB': cmd_gosub,
    'GOTO': cmd_goto,
    'IF': cmd_if,
    'INCLUDE': cmd_include,
    'LOOP': cmd_loop,
    'NEXT': cmd_next,
    'PAUSE': cmd_pause,
    'RETURN': cmd_return,
}