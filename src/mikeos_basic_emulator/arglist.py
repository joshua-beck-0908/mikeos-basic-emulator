from typing import Callable

from argument import ArgumentError, CommandArgument
from parser import Token
from variables import VariableManager
from environment import Environment

class CommandArgumentList:
    """
    Represents a list of arguments in a command.
    
    Each command is passed a list of arguments to interpret.
    The command will consume the arguments as needed.
    
    The class is built with a list of tokens and a variable manager instance.
    The variable manager is used to fetch and set variable values if needed.

    The values of the tokens may vary depending on which interpretation 
    method is called.
    
    The types match those in the CommandArgument class.
    - Numeric (get_numeric/has_numeric)
    - String (get_string/has_string)
    - Numeric Variable 
        - (get_numeric_variable/has_numeric_variable/set_numeric_variable)
    - String Variable
        - (get_string_variable/has_string_variable/set_string_variable)
    - Word (get_word/has_word/has_specific_word/get_word_from_list)
    - Symbol (get_symbol/has_symbol/has_specific_symbol/get_symbol_from_list)
    - Program Pointer (get_program_pointer)

    The methods use the following pattern:
    - get_x() will consume the next argument and return it as type x.
        - Returns any variable or literal as type x.
        - Useful for input arguments.
        - A syntax error is raised if the argument cannot be interpreted as x.
    - has_x() will check if the next argument can be interpreted as type x.
        - Returns True if the next argument can be interpreted as x.
        - Useful for commands with multiple argument types or optionals.
        - Does not raise a syntax error if the argument is a different type.
    - set_x() will consume the next argument and set it as type x.
        - Will set the value of the argument to the next variable of type x.
        - Useful for output arguments.
        - A syntax error is raised if the argument an invalid type or literal.
    - has_specific_x()
        - Will check if the next argument is of type x AND is a specific value.
        - Useful for commands that expect a specific symbol or keyword.
    - has_x_from_list()
        - Will check if the next argument is of type x AND is in a 
        list of values.
        - Useful for commands that have multiple subcommands or symbols.

    """

    
    def __init__(self, tokens: list[Token], vars: VariableManager) -> None:
        self.tokens = tokens
        self.args = [CommandArgument(token, vars) for token in tokens]
        self.index = 0
        self.variables = vars

    def assume_argument_exists(self) -> None:
        """
        Raise a syntax error if the current argument does not exist.
        """
        if self.index >= len(self.args):
            raise ArgumentError('Not enough arguments')

    def expect_more_arguments(self, count: int = 1) -> None:
        if self.index + count > len(self.args):
            raise ArgumentError('Not enough arguments')

    def does_argument_exist(self) -> bool:
        if self.index >= len(self.args):
            return False
        else:
            return True

    def next(self) -> None:
        """
        Consume the argument without returning it.
        """
        self.index += 1

    def syntax_error(self, message: str = 'Syntax Error') -> None:
        raise ArgumentError(message)

    # Functions to provide the next argument as a specific type.
    # If not possible errors will be raised by the underlying CommandArgument.
    def get_numeric(self) -> int:
        """
        Consume the next argument and return it as a number. 

        This will convert any numbers, variables, keywords, etc to a number.
        If the argument is non-numeric a syntax error will be raised.
        """

        self.assume_argument_exists()
        arg = self.args[self.index]
        self.index += 1
        return arg.to_numeric()


    def get_string(self) -> str:
        """
        Consume the next argument and return it as a string.

        This will convert any strings or string variables to a string.
        If the argument is not a string, a syntax error will be raised.
        """

        self.assume_argument_exists()
        arg = self.args[self.index]
        self.index += 1
        return arg.to_string()

    def get_numeric_variable(self) -> str:
        """
        Consume the next argument and return it as a numeric variable.

        This is for when you need to output to a variable.
        If the argument is not a numeric variable, 
        a syntax error will be raised.
        """

        self.assume_argument_exists()
        arg = self.args[self.index]
        self.index += 1
        return arg.to_numeric_variable()
    
    def set_numeric_variable(self, value: int) -> None:
        """
        Consume the next argument as a numeric variable and set it.

        Useful for output arguments.
        If the argument is not a numeric variable, 
        a syntax error will be raised.
        """

        var = self.get_numeric_variable()
        self.variables.set_numeric_variable(var, value)

    def get_string_variable(self) -> str:
        """ 
        Consume the next argument and return it as a string variable. 

        This is for when you need to output to a string variable.
        If the argument is not a string variable,
        a syntax error will be raised.
        """

        self.assume_argument_exists()
        arg = self.args[self.index]
        self.index += 1
        return arg.to_string_variable()
    
    def set_string_variable(self, value: str) -> None:
        """
        Consume the next argument as a string variable and set it to the given
        value.

        Useful for output arguments.
        If the argument is not a string variable, 
        a syntax error will be raised.
        """

        var = self.get_string_variable()
        self.variables.set_string_variable(var, value)

    def get_word(self) -> str:
        """
        Consume the next KEYWORD argument and return it as a string.

        This is for when you need a subcommand.
        If the argument is not a keyword, a syntax error will be raised.
        """

        self.assume_argument_exists()
        arg = self.args[self.index]
        self.index += 1
        return arg.to_word()

    def get_symbol(self) -> str:
        """
        Consume the next argument and return it as a symbol.

        This is for when the syntax expect a symbol, but not a specific one.
        If the argument is not a symbol, a syntax error will be raised.
        """

        self.assume_argument_exists()
        arg = self.args[self.index]
        self.index += 1
        return arg.to_symbol()

    def get_program_pointer(self) -> int:
        """
        Consume the next argument and return it as a program pointer.

        This is for when you need the address of a label.
        """
        self.assume_argument_exists()
        arg = self.args[self.index]
        self.index += 1
        return arg.to_program_pointer()

    def get_specific_symbol(self, symbol: str) -> None:
        """
        Consume the next argument and check if it is a specific symbol.

        This is for when the syntax expects a specific symbol.
        Such as an equals sign or a plus sign.
        """
        self.assume_argument_exists()
        arg = self.args[self.index]
        self.index += 1
        actual_symbol = arg.to_symbol()
        if actual_symbol != symbol:
            raise ArgumentError(
                f'Expected "{symbol}" but got "{actual_symbol}"'
            )

    def get_symbol_from_list(self, symbols: list[str]) -> str:
        """
        Consume the next argument and check if it is a specific symbol.

        This is for when the syntax accept multiple symbols.
        """
        self.assume_argument_exists()
        arg = self.args[self.index]
        self.index += 1
        actual_symbol = arg.to_symbol()
        if actual_symbol not in symbols:
            raise ArgumentError(
                f'Expected one of "{symbols}" but got "{actual_symbol}"'
            )
        return actual_symbol

    def get_specific_word(self, word: str) -> None:
        """
        Consume the next argument and check if it is a specific word.

        This is for when the syntax expects a specific word.
        """
        self.assume_argument_exists()
        arg = self.args[self.index]
        self.index += 1
        actual_word = arg.to_word()
        if actual_word != word:
            raise ArgumentError(
                f'Expected "{word}" but got "{actual_word}"'
            )

    def get_word_from_list(self, words: list[str]) -> str:
        """
        Consume the next argument and check if it is a specific word.

        This is for when the syntax accept multiple words.
        """
        self.assume_argument_exists()
        arg = self.args[self.index]
        self.index += 1
        actual_word = arg.to_word()
        if actual_word not in words:
            raise ArgumentError(
                f'Expected one of "{words}" but got "{actual_word}"'
            )
        return actual_word

    def get_token(self) -> Token:
        """
        Consume the next argument and return it as a token.
        
        Normally you would use the other functions to convert the argument.
        But you can use this if you need to handle the argument yourself.
        """
        self.assume_argument_exists()
        arg = self.args[self.index]
        self.index += 1
        return arg.token

    def has_any(self) -> bool:
        """
        Check if there is another argument to consume.

        This is for when a command has optional arguments.
        """

        return self.does_argument_exist()

    def has_string(self) -> bool:
        """
        Check if the next argument can be converted to a string.

        This is for when the syntax can accept a string or other types.
        """

        if self.does_argument_exist():
            return self.args[self.index].is_valid_string()
        return False

    def has_numeric(self) -> bool:
        """
        Check if the next argument can be converted to a number.

        This is for when the syntax can accept a number or other types.
        """

        if self.does_argument_exist():
            return self.args[self.index].is_valid_numeric()
        return False

    def has_numeric_variable(self) -> bool:
        """
        Check if the next argument is a numeric variable.

        This is for when the syntax can optionally accept a variable.
        """

        if self.does_argument_exist():
            return self.args[self.index].is_valid_numeric_variable()
        return False

    def has_string_variable(self) -> bool:
        """
        Check if the next argument is a string variable.

        This is for when the syntax can optionally accept a string variable.
        """

        if self.does_argument_exist():
            return self.args[self.index].is_valid_string_variable()
        return False

    def has_word(self) -> bool:
        """
        Check if the next argument is a word.

        This is for when the syntax can accept additional subcommands.
        """

        if self.does_argument_exist():
            return self.args[self.index].is_valid_word()
        return False

    def has_symbol(self) -> bool:
        """
        Check if the next argument is a symbol.

        This is for when the syntax can optionally accept a symbol.
        """

        if self.does_argument_exist():
            return self.args[self.index].is_valid_symbol()
        return False

    def has_specific_symbol(self, symbol: str) -> bool:
        """
        Check if the next argument is a specific symbol.

        This is for when the syntax can optionally accept a specific symbol.
        Note this will expect the symbol to be the next argument.
        The symbol will be consumed if it is correct.
        """

        if self.does_argument_exist():
            return self.args[self.index].to_symbol() == symbol
        return False

    def has_specific_word(self, word: str) -> bool:
        """
        Check if the next argument is a specific word.

        This is for when the syntax can optionally accept a specific word.
        Note this will expect the word to be the next argument.
        The word will be consumed if it is correct.
        """

        if self.does_argument_exist():
            return self.args[self.index].to_word() == word
        return False
    
    def has_non_semantic(self) -> bool:
        """
        Check if the next argument is a non-semantic token.

        This is for when the syntax can accept a non-semantic token.
        """

        if self.does_argument_exist():
            return self.args[self.index].is_non_semantic()
        return False

    
    def check_condition(self) -> bool:
        """
        Evaluates a condition in the following arguments.

        All arguments related to the condition will be consumed.
        
        The following arguments should be:
        - the first numeric value
        - a comparison operator (a SYMBOL)
        - the second numeric value

        Valid comparison operators are:
        - `=` (equal)
        - `>` (greater than)
        - `<` (less than)
        - `!` (not equal)
        """

        value1 = self.get_numeric()
        operator = self.get_symbol_from_list(['=', '>', '<', '!'])
        value2 = self.get_numeric()

        if operator == '=':
            return value1 == value2
        elif operator == '>':
            return value1 > value2
        elif operator == '<':
            return value1 < value2
        elif operator == '!':
            return value1 != value2
        else:
            # This branch can't actually happen, but pylance doesn't know that.
            return False
        
    def do_numeric_sum(self) -> int:
        """
        Perform a numeric sum operation.

        This will consume all numeric values and operators in the arguments.
        The result will be returned.
        """

        result = self.get_numeric()
        while self.has_symbol():
            operator = self.get_symbol_from_list(['+', '-', '*', '/', '%'])
            value = self.get_numeric()

            if operator == '+':
                result += value
            elif operator == '-':
                result -= value
            elif operator == '*':
                result *= value
            elif operator == '/':
                result //= value
            elif operator == '%':
                result %= value

        return result
    
    def do_string_building(self) -> str:
        """
        Perform string building operation.
        e.g. '$1 + "Hello" + $2'

        This will consume all string values and operators in the arguments.
        The result will be returned.
        """

        result = self.get_string()
        while self.has_symbol():
            self.get_specific_symbol('+')
            value = self.get_string()
            result += value

        return result
    
    def make_new_arglist_from_remaining(self) -> 'CommandArgumentList':
        """
        Create a new argument list from the remaining arguments.

        This is useful for conditional commands.
        """
        
        return CommandArgumentList(self.tokens[self.index:], self.variables)
        
    

CommandRoutine = Callable[[CommandArgumentList, Environment], None]