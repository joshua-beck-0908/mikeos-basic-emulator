# This is the interpreter's built in commands for things like assignment
# and control flow.

from arglist import CommandArgumentList
from environment import Environment

def cmd_numeric_assignment(args: CommandArgumentList, env: Environment) -> None:
    """
    Assigns a value to a variable.
    
    This may be a constant value or the result of an expression.
    e.g. A = 5, B = 3 + A / 2
    """
    
    # Get the variable being assigned to.
    outvar = args.get_numeric_variable()
    
    # Expect it to be followed by an equals sign.
    args.get_specific_symbol('=')
    
    # Use the argument list to evaluate the expression.
    result = args.do_numeric_sum()
    
    # There should be no more arguments after the expression.
    if args.has_any():
        env.debugger.error('COMMAND', 
            'Invalid arguments in numeric assignment.')
        env.debugger.breakpoint(env)

    # Assign the final result to the variable.
    env.variables.set_numeric_variable(outvar, result)
    

def cmd_build_string(args: CommandArgumentList, env: Environment) -> None:
    """
    Builds a string from a series of arguments.
    
    This is used to concatenate strings together.
    """
    
    # Get the variable being assigned to.
    outvar = args.get_string_variable()
    
    # Expect it to be followed by an equals sign.
    args.get_specific_symbol('=')
    
    # Use the argument list to build the string.
    result = args.do_string_building()
    
    # There should be no more arguments after the expression.
    if args.has_any():
        env.debugger.error('COMMAND', 
            'Invalid arguments in string building.')
        env.debugger.breakpoint(env)

    # Assign the final result to the variable.
    env.variables.set_string_variable(outvar, result)
    
all_commands = {
    '(assign)': cmd_numeric_assignment,
    '(build_string)': cmd_build_string,
}
    