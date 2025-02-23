# This file contains the parser for the MikeOS BASIC language
# Commands are converted into token.
# The tokens are then executed by the CommandRunner.
# The commands themselves are implemented as functions in other modules.

from typing import Any, NamedTuple
from enum import Enum

class DecodingError(Exception):
    """ For malformed tokens. """
    pass

class TokenType(Enum):
    WORD = 1,
    NUMBER = 2,
    QUOTE = 3,
    SYMBOL = 4,
    COMMENT = 5,
    VARIABLE = 6
    STRING_VAR = 7,
    STRING_VAR_REF = 8,
    LABEL = 9,
    CHAR = 10,

class Token(NamedTuple):
    type: TokenType
    value: Any



class CommandParser:
    def __init__(self) -> None:
        pass

    def parse(self, command: str) -> list[Token]:
        tokens: list[Token] = []
        
        for token in self.split_line(command):
            tokens.append(self.decode_token(token))
            
        if len(tokens) == 0:
            return []
        elif tokens[0].type == TokenType.COMMENT:
            return [Token(TokenType.COMMENT, command.strip()[4:])]
        else:
            return tokens

    # Split the line into tokens.
    # Separate by spaces, except for quoted strings, and symbols.
    def split_line(self, line: str) -> list[str]:
        line = line.strip()
        output: list[str] = []
        word = ''
        in_quote = False
        in_char = False
        in_comment = False
        include_next = False
        for char in line:
            # Windows adds a carriage return at the end of the line.
            if char == '\r':
                continue
            # If we're in a comment, just add the rest of the line as a token.
            elif in_comment:
                word += char
            # Is it the start or end of a quote?
            elif char == '"':
                word += char
                if in_quote:
                    output.append(word)
                    word = ''
                in_quote = not in_quote
            # If we're continuing a quote ignore spaces and other boundries.
            elif in_quote:
                word += char
                
            elif char == "'":
                word += char
                if in_char:
                    output.append(word)
                    word = ''
                in_char = not in_char
            elif in_char:
                if len(word) > 2:
                    raise DecodingError('Character literal too long')
                word += char
                

            # Different rules apply at the start of a word.
            elif len(word) == 0:
                # Look for string or string reference variables.
                if char == '$' or char == '&':
                    word += char
                    if char == '&':
                        include_next = True
                elif char == ' ':
                    continue
                else:
                    word += char


            # If there's a space, end the token.
            elif char == ' ':
                if include_next:
                    continue
                else:
                    if len(output) == 0 and word.upper() == 'REM':
                        # Do not try to parse a comment.
                        word += char
                        in_comment = True
                    else:
                        output.append(word)
                        word = ''
            # If it's alphanumeric, continue the word.
            # The parser will later decide if it's valid and what type it is.
            elif char.isalnum() or include_next:
                    word += char
                    include_next = False
            # If it a colon, it might be the end of a label.
            elif char == ':':
                word += char
                output.append(word)
                word = ''
            # Everything else is a symbol.
            # Symbols are always single characters.
            else:
                output.append(word)
                output.append(char)
                word = ''
                
        # If the line ends during a word, add it to the output.
        if len(word) > 0:
            output.append(word)

        # If the line end halfway through a quote, raise an error.
        if in_quote:
            raise DecodingError('Unmatched quote in line')
        return output

    # Convert a token into a tuple of TokenType and the value.
    # This just guesses the type and passes it to a more specific method.
    def decode_token(self, raw_token: str) -> Token:
        token = raw_token
        if token.startswith('$'):
            return self.as_string_var(token)
        elif token[0].isnumeric():
            return self.as_number(token)
        elif token.startswith('"'):
            return self.as_quote(token)
        elif token.startswith("'"):
            return self.as_char(token)
        elif token[0].isalpha():
            # Single letter words are variables.
            if len(token) == 1:
                return self.as_numeric_variable(token)
            # If it has the command REM, it's a comment.
            elif token.upper().startswith('REM '):
                return Token(TokenType.COMMENT, '')
            # If it ends with a colon, it's a label.
            elif token[-1] == ':':
                return Token(TokenType.LABEL, token)
            else:
                return self.as_word(token)
        elif token.startswith('&'):
            return self.as_string_var_ref(token)
        else:
            return self.as_symbol(token)

    def as_string_var(self, token: str) -> Token:
        if len(token) == 2 and token.startswith('$'):
            if token[1].isnumeric() and 0 < int(token[1]) < 9:
                return Token(TokenType.STRING_VAR, token)
        raise DecodingError(f'Invalid string token: "{token}"')
        
    def as_number(self, token: str) -> Token:
        try:
            return Token(TokenType.NUMBER, int(token))
        except ValueError:
            raise DecodingError(f'Invalid number token: "{token}"')
        
    def as_quote(self, token: str) -> Token:
        if token.startswith('"') and token.endswith('"'):
            return Token(TokenType.QUOTE, token)
        raise DecodingError(f'Invalid quote token: "{token}"')
    
    def as_symbol(self, token: str) -> Token:
        return Token(TokenType.SYMBOL, token[0])
    
    def as_numeric_variable(self, token: str) -> Token:
        if token.isalpha() and len(token) == 1:
            return Token(TokenType.VARIABLE, token.upper())
        raise DecodingError(f'Invalid variable token: "{token}"')

    def as_word(self, token: str) -> Token:
        if token.isalpha():
            return Token(TokenType.WORD, token)
        else:
            raise DecodingError(f'Invalid word token: "{token}"')
        
    def as_string_var_ref(self, token: str) -> Token:
        token = token.replace(' ', '')
        if (token.startswith('&') 
            and len(token) == 3
            and token[1] == '$'
            and token[2].isnumeric()
            and 0 < int(token[2]) < 9):
                return Token(TokenType.STRING_VAR_REF, token)
        raise DecodingError(f'Invalid string reference token: "{token}"');
    
    def as_label(self, token: str) -> Token:
        if token[-1] == ':':
            return Token(TokenType.LABEL, token)
        raise DecodingError(f'Invalid label token: "{token}"')
    
    def as_char(self, token: str) -> Token:
        if token.startswith("'") and token.endswith("'") and len(token) == 3:
            return Token(TokenType.CHAR, token)
        else:
            raise DecodingError(f'Invalid character token: "{token}"')



