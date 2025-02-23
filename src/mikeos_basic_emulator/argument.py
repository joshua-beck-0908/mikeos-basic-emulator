from keywords import KeywordManager
from parser import TokenType, Token
from variables import VariableManager

NUMERIC_TOKEN_TYPES: list[TokenType] = [
    TokenType.NUMBER, 
    TokenType.VARIABLE,
    TokenType.STRING_VAR_REF,
    TokenType.CHAR,
    TokenType.WORD,
]

STRING_TOKEN_TYPES: list[TokenType] = [
    TokenType.QUOTE, 
    TokenType.STRING_VAR,
]


class TokenTypeError(Exception):
    """ For when a token is the wrong type. """
    pass

class ArgumentError(Exception):
    """ For when an argument is invalid. """
    pass

class CommandArgument:
    """
    Represents a single argument in a command.
    
    Built from a token and a variable manager instance.
    We may need to retrieve variable values for some methods.

    The class provides methods to interpret the token as different types.
    - As a numeric value (to_numeric/is_valid_numeric).
    - As a string value (to_string/is_valid_string).
    - As a numeric variable (to_numeric_variable/is_valid_numeric_variable).
    - As a string variable (to_string_variable/is_valid_string_variable).
    - As a word (to_word/is_valid_word).
    - As a symbol (to_symbol/is_valid_symbol).
    - As a program pointer (to_program_pointer).

    The same token may be interpreted as multiple types depending on the 
    method called. The to_x() methods will raise TokenTypeError if the token is
    not of the expected type.
    
    Usually this is what you'd want as it indicates a syntax error that should
    propagate up to the command interpreter.

    However some commands may accept multiple types of arguments.
    So the is_valid_x() methods can be used to check if the token can be
    used to check if the token can be interpreted as a certain type.
    """
    def __init__(self, token: Token, vars: VariableManager) -> None:
        self.token = token
        self.variables = vars
        self.keywords = KeywordManager(self.variables)

    def to_numeric(self) -> int:
        """
        Interprets the current token as a number.
        - A literal number will be returned as an integer.
        - For a numeric variable, the value will be fetched and returned.
        - For a string pointer, the address will be returned.
        - For a special keyword, the current value will be returned.
        - Any other token type will raise a TokenTypeError.
        """
        if self.token.type == TokenType.NUMBER:
            return self.token.value
        elif self.token.type == TokenType.VARIABLE:
            return self.variables.get_numeric_variable(self.token.value)
        elif self.token.type == TokenType.STRING_VAR_REF:
            return self.variables.get_string_variable_pointer(
                self.token.value[1:])
        elif self.token.type == TokenType.CHAR:
            return self.token.value[1].encode('cp437')[0]
        elif self.token.type == TokenType.WORD:
            if self.keywords.is_valid_keyword(self.token.value):
                return self.keywords.get_keyword_value(self.token.value)
            else:
                raise TokenTypeError('Unknown numeric keyword')
        else:
            raise TokenTypeError('Expected numeric token')
        
    def to_string(self) -> str:
        """
        Interprets the current token as a string.
        - A literal string will be returned without quotes.
        - For a string variable, the value with be fetched and returned.
        - Any other token type will raise a TokenTypeError.
        """
        if self.token.type == TokenType.QUOTE:
            return self.token.value[1:-1]
        elif self.token.type == TokenType.STRING_VAR:
            return self.variables.get_string_variable(self.token.value)
        else:
            raise TokenTypeError('Expected string token')
        
    def to_numeric_variable(self) -> str:
        """
        Interprets the current token as a numeric variable.
        - For a numeric variable, the variable name will be returned.
        - Any other token type will raise a TokenTypeError.
        
        The variable name can them be used to fetch the value,
        with variables.get_numeric_variable(variable_name).
        """
        if self.token.type == TokenType.VARIABLE:
            return self.token.value
        else:
            raise TokenTypeError('Expected numeric variable token')
        
    def to_string_variable(self) -> str:
        """
        Interprets the current token as a string variable.
        - For a string variable, the variable name will be returned.
        - Any other token type will raise a TokenTypeError.
        
        The returned variable name can then be used to fetch the value,
        with variables.get_string_variable(variable_name).
        """
        if self.token.type == TokenType.STRING_VAR:
            return self.token.value
        else:
            raise TokenTypeError('Expected string variable token')
        
    def to_word(self) -> str:
        """
        Interprets the current token as a command or keyword.
        - For a word, the literal text will be returned.
        - Any other token type will raise a TokenTypeError.
        """
        if self.token.type == TokenType.WORD:
            return self.token.value.upper()
        else:
            raise TokenTypeError('Expected word token')
        
    def to_symbol(self) -> str:
        """
        Interprets the current token as a symbol.
        - For a symbol, the literal text will be returned.
        - Any other token type will raise a TokenTypeError.
        
        Symbols are used for operators like +, -, *, /, etc.
        They are any single character that is not a number or letter, 
        or part of some other token type.
        """
        if self.token.type == TokenType.SYMBOL:
            return self.token.value
        else:
            raise TokenTypeError('Expected symbol token')
        
    def to_program_pointer(self) -> int:
        """
        Interprets the current token as a program pointer.
        - For a word, the address of the label will be found and returned.
        - For a label, the same as above.
        - For a keyword, the value of the keyword will be returned.
        - Any other token type will raise a TokenTypeError.
        """
        if self.token.type == TokenType.LABEL:
            return self.variables.get_label_pointer(self.token.value[:-1])
        elif self.token.type == TokenType.WORD:
            if self.keywords.is_valid_keyword(self.token.value):
                return self.keywords.get_keyword_value(self.token.value)
            else:
                return self.variables.get_label_pointer(self.token.value)
        else:
            raise TokenTypeError('Expected label token')
        
    def to_label_and_pointer(self) -> tuple[str, int]:
        """
        Interprets the current token as a label and program pointer.
        - For a label, the label name and address will be returned.
        - For a word, the same as above.
        - Any other token type will raise a TokenTypeError.
        
        The name and address are returned as a tuple in that order.
        """
        
        # We can reused the to_program_pointer method here.
        # But a keyword is not a valid label, so we need to check for that.
        if self.token.type == TokenType.WORD and \
        self.keywords.is_valid_keyword(self.token.value):
                raise TokenTypeError('Expected label token')
        else:
            return (self.token.value, self.to_program_pointer())
            


    def is_valid_string(self) -> bool:
        """
        Returns True if the current token can be interpreted as a string.
        It may be useful to check if a syntax accepts multiple types.
        """
        return self.token.type in STRING_TOKEN_TYPES
    
    def is_valid_numeric(self) -> bool:
        """
        Returns True if the current token can be interpreted as a number.
        It may be useful to check if a syntax accepts multiple types.
        """
        if self.token.type in NUMERIC_TOKEN_TYPES:
            if self.token.type == TokenType.WORD:
                return self.keywords.is_valid_keyword(self.token.value)
            else:
                return True
        else:
            return False
        
    def is_valid_numeric_variable(self) -> bool:
        """
        Returns True if the current token is a valid numeric variable.
        It may be useful to check if a syntax accepts multiple types.
        """
        return self.token.type == TokenType.VARIABLE
    
    def is_valid_string_variable(self) -> bool:
        """
        Returns True if the current token is a valid string variable.
        It may be useful to check if a syntax accepts multiple types.
        """
        return self.token.type == TokenType.STRING_VAR
    
    def is_valid_symbol(self) -> bool:
        """
        Returns True if the current token is a valid symbol.
        It may be useful to check if a syntax accepts multiple types.
        """
        return self.token.type == TokenType.SYMBOL
    
    def is_valid_word(self) -> bool:
        """
        Returns True if the current token is a valid word.
        It may be useful to check if a syntax accepts multiple types.
        """
        return self.token.type == TokenType.WORD
    
    def is_non_semantic(self) -> bool:
        """
        Returns True if the token is to be ignored by the command interpreter.
        
        These include comments and labels.
        """
        return self.token.type in [TokenType.COMMENT, TokenType.LABEL]



