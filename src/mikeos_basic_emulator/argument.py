from keywords import KeywordManager
from parser import TokenType, Token
from variables import VariableManager


class TokenTypeError(Exception):
    """ For when a token is the wrong type. """
    pass

class ArgumentError(Exception):
    """ For when an argument is invalid. """
    pass

class CommandArgument:
    def __init__(self, token: Token, vars: VariableManager) -> None:
        self.token = token
        self.variables = vars
        self.keywords = KeywordManager(self.variables)

    def to_numeric(self) -> int:
        if self.token.type == TokenType.NUMBER:
            return self.token.value
        elif self.token.type == TokenType.VARIABLE:
            return self.variables.get_numeric_variable(self.token.value)
        elif self.token.type == TokenType.STRING_VAR_REF:
            return self.variables.get_string_variable_pointer(
                self.token.value[1:])
        elif self.token.type == TokenType.WORD:
            if self.keywords.is_valid_keyword(self.token.value):
                return self.keywords.get_keyword_value(self.token.value)
            else:
                raise TokenTypeError('Unknown numeric keyword')
        else:
            raise TokenTypeError('Expected numeric token')
        
    def to_string(self) -> str:
        if self.token.type == TokenType.QUOTE:
            return self.token.value[1:-1]
        elif self.token.type == TokenType.STRING_VAR:
            return self.variables.get_string_variable(self.token.value)
        else:
            raise TokenTypeError('Expected string token')
        
    def to_numeric_variable(self) -> str:
        if self.token.type == TokenType.VARIABLE:
            return self.token.value
        else:
            raise TokenTypeError('Expected numeric variable token')
        
    def to_string_variable(self) -> str:
        if self.token.type == TokenType.STRING_VAR:
            return self.token.value
        else:
            raise TokenTypeError('Expected string variable token')
        
    def to_word(self) -> str:
        if self.token.type == TokenType.WORD:
            return self.token.value
        else:
            raise TokenTypeError('Expected word token')
        
    def to_symbol(self) -> str:
        if self.token.type == TokenType.SYMBOL:
            return self.token.value
        else:
            raise TokenTypeError('Expected symbol token')
        
    def to_program_pointer(self) -> int:
        if self.token.type == TokenType.LABEL:
            return self.variables.get_label_pointer(self.token.value)
        elif self.token.type == TokenType.WORD:
            if self.keywords.is_valid_keyword(self.token.value):
                return self.keywords.get_keyword_value(self.token.value)
            else:
                return self.variables.get_label_pointer(self.token.value)
        else:
            raise TokenTypeError('Expected label token')

    def is_valid_string(self) -> bool:
        return self.token.type in [TokenType.QUOTE, TokenType.STRING_VAR]
    
    def is_valid_numeric(self) -> bool:
        if self.token.type in [
            TokenType.NUMBER, 
            TokenType.VARIABLE,
            TokenType.STRING_VAR_REF
            ]:

            return True
        elif self.token.type == TokenType.WORD:
            return self.keywords.is_valid_keyword(self.token.value)
        else:
            return False
        
    def is_valid_numeric_variable(self) -> bool:
        return self.token.type == TokenType.VARIABLE
    
    def is_valid_string_variable(self) -> bool:
        return self.token.type == TokenType.STRING_VAR
    
    def is_valid_symbol(self) -> bool:
        return self.token.type == TokenType.SYMBOL
    
    def is_valid_word(self) -> bool:
        return self.token.type == TokenType.WORD
    



