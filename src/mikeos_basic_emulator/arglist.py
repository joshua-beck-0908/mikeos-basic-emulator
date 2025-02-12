from typing import Callable

from argument import ArgumentError, CommandArgument
from parser import Token
from variables import VariableManager
from environment import Environment

class CommandArgumentList:
    def __init__(self, tokens: list[Token], vars: VariableManager) -> None:
        self.args = [CommandArgument(token, vars) for token in tokens]
        self.index = 0
        self.variables = vars

    def assume_argument_exists(self) -> None:
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

        This is a shortcut if the next variable is an output.
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
        Consume the next argument as a string variable and set it.

        This is a shortcut if the next variable is an output.
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
    
    

CommandRoutine = Callable[[CommandArgumentList, Environment], None]