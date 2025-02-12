import pytest

from parser import CommandParser, TokenType, DecodingError

def test_valid_string_var():
    parser = CommandParser()
    assert parser.decode_token('$1') == (TokenType.STRING_VAR, '$1')
    
def test_letter_string_var():
    parser = CommandParser()
    with pytest.raises(DecodingError):
        parser.decode_token('$a')
        
def test_too_low_numbered_string_var():
    parser = CommandParser()
    with pytest.raises(DecodingError):
        parser.decode_token('$0')
        
def test_too_high_numbered_string_var():
    parser = CommandParser()
    with pytest.raises(DecodingError):
        parser.decode_token('$9')
        
def test_multiple_digit_string_var():
    parser = CommandParser()
    with pytest.raises(DecodingError):
        parser.decode_token('$10')
        
def test_valid_number():
    parser = CommandParser()
    assert parser.decode_token('123') == (TokenType.NUMBER, 123)
    
def test_invalid_partial_number():
    parser = CommandParser()
    with pytest.raises(DecodingError):
        parser.decode_token('12a')
        
def test_valid_quote():
    parser = CommandParser()
    assert parser.decode_token('"test"') == (TokenType.QUOTE, '"test"')
    
def test_invalid_quote():
    parser = CommandParser()
    with pytest.raises(DecodingError):
        parser.decode_token('"test')
        
def test_letter_variable():
    parser = CommandParser()
    assert parser.decode_token('a') == (TokenType.VARIABLE, 'A')
    
def test_word():
    parser = CommandParser()
    assert parser.decode_token('test') == (TokenType.WORD, 'TEST')

def test_invalid_word():
    parser = CommandParser()
    with pytest.raises(DecodingError):
        parser.decode_token('te34t')
        
def test_comment():
    parser = CommandParser()
    assert parser.decode_token('REM') == (TokenType.COMMENT, '')

def test_symbol():
    parser = CommandParser()
    assert parser.decode_token('+') == (TokenType.SYMBOL, '+')
    
def test_label():
    parser = CommandParser()
    assert parser.decode_token('LABEL:') == (TokenType.LABEL, 'LABEL:')
    
def test_string_var_ref():
    parser = CommandParser()
    assert parser.decode_token('&$1') == (TokenType.STRING_VAR_REF, '&$1')

def test_split_line_with_one_word():
    parser = CommandParser()
    assert parser.split_line('TEST') == ['TEST']

def test_split_line_with_two_words():
    parser = CommandParser()
    assert parser.split_line('TEST TEST2') == ['TEST', 'TEST2']
    
def test_split_line_with_quote():
    parser = CommandParser()
    assert parser.split_line('this is "a test"') == ['this', 'is', '"a test"']

def test_split_line_with_invalid_quote():
    parser = CommandParser()
    with pytest.raises(DecodingError):
        parser.split_line('this is "a test')

def test_split_line_with_sum():
    parser = CommandParser()
    assert parser.split_line('1 + 2') == ['1', '+', '2']

def test_split_line_with_unspaced_sum():
    parser = CommandParser()
    assert parser.split_line('1+2') == ['1', '+', '2']
    
def test_split_line_with_variable():
    parser = CommandParser()
    assert parser.split_line('A = 1') == ['A', '=', '1']

def test_split_line_with_unspaced_variable():
    parser = CommandParser()
    assert parser.split_line('A=1') == ['A', '=', '1']
    
def test_split_line_with_string_reference():
    parser = CommandParser()
    assert parser.split_line('A = & $1') == ['A', '=', '&$1']
    
def test_split_line_with_label():
    parser = CommandParser()
    assert parser.split_line('LABEL:') == ['LABEL:']

def test_parser_with_blank_line():
    parser = CommandParser()
    assert parser.parse('') == []
    
def test_parser_with_comment():
    parser = CommandParser()
    assert parser.parse('REM') == [(TokenType.COMMENT, '')]
    
def test_parser_with_long_comment():
    parser = CommandParser()
    assert parser.parse('REM this is a comment') == [(TokenType.COMMENT, 'this is a comment')]
    
def test_parser_with_prespaced_comment():
    parser = CommandParser()
    assert parser.parse(' REM this is a comment') == [(TokenType.COMMENT, 'this is a comment')]
    
def test_parser_with_variable():
    parser = CommandParser()
    assert parser.parse('A = 1') == [(TokenType.VARIABLE, 'A'), (TokenType.SYMBOL, '='), (TokenType.NUMBER, 1)]
    
def test_parser_with_complex_quotes():
    parser = CommandParser()
    assert parser.parse('$1 = "this is a test" + $4 + " please test it"') == [
        (TokenType.STRING_VAR, '$1'),
        (TokenType.SYMBOL, '='),
        (TokenType.QUOTE, '"this is a test"'),
        (TokenType.SYMBOL, '+'),
        (TokenType.STRING_VAR, '$4'),
        (TokenType.SYMBOL, '+'),
        (TokenType.QUOTE, '" please test it"')
    ]
    
def test_parser_with_string_var():
    parser = CommandParser()
    assert parser.parse('$1') == [(TokenType.STRING_VAR, '$1')]
    
def test_parser_with_long_sum():
    parser = CommandParser()
    assert parser.parse('A=1+ 2 + 3') == [
        (TokenType.VARIABLE, 'A'),
        (TokenType.SYMBOL, '='),
        (TokenType.NUMBER, 1), 
        (TokenType.SYMBOL, '+'), 
        (TokenType.NUMBER, 2), 
        (TokenType.SYMBOL, '+'), 
        (TokenType.NUMBER, 3)
    ]
    
def test_parser_with_string_reference():
    parser = CommandParser()
    assert parser.parse('A = & $1') == [
        (TokenType.VARIABLE, 'A'),
        (TokenType.SYMBOL, '='),
        (TokenType.STRING_VAR_REF, '&$1')
    ]