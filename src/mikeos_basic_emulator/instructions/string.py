from arglist import CommandArgumentList
from environment import Environment

def do_case(args: CommandArgumentList, env: Environment) -> None:
    keyword = args.get_word_from_list(['UPPER', 'LOWER'])
    variable = args.get_string_variable()
    variable_text = env.variables.get_string_variable(variable)

    if keyword == 'UPPER':
        variable_text = variable_text.upper()
    elif keyword == 'LOWER':
        variable_text = variable_text.lower()
    env.variables.set_string_variable(variable, variable_text)
    
def do_len(args: CommandArgumentList, env: Environment) -> None:
    text = args.get_string()
    args.set_numeric_variable(len(text))
    
def do_number(args: CommandArgumentList, env: Environment) -> None:
    args.expect_more_arguments(2)
    
    if args.has_string():
        value = args.get_string()
        try:
            args.set_numeric_variable(int(value))
        except ValueError:
            args.syntax_error(f'Invalid number: "{value}"')
    elif args.has_numeric():
        value = args.get_numeric()
        args.set_string_variable(str(value))

def do_string(args: CommandArgumentList, env: Environment) -> None:
    variable = args.get_string_variable()
    variable_text = env.variables.get_string_variable(variable)
    offset = args.get_numeric()
    value = args.get_numeric()
    variable_text = variable_text[:offset] + chr(value) + \
        variable_text[offset + 1:]
    env.variables.set_string_variable(variable, variable_text)
    

all_commands = {
    'CASE': do_case,
    'LEN': do_len,
    'NUMBER': do_number,
    'STRING': do_string
}
    