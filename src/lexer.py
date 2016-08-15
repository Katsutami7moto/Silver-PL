from src import regexp
from collections import namedtuple


Token = namedtuple('Token', 'type line column value')


def lexer_error(line, column):
    raise Exception("Некорректная лексема %d:%d" % (line, column))


def uminus(token: Token) -> Token:
    return token._replace(type='-u')


def word_check(other: str, line: int, column: int) -> Token:
    keywords = {
        "module",
        "import",
        "var",
        "let",
        "varblock",
        "letblock",
        "mod",  # TODO: точно ли такое слово ?
        "def"
        "type",
        "typedef",
        "new",
        "del",
        "while",
        "loop",
        "do",
        "until",
        "break",
        "continue",
        "if",
        "elif",
        "else",
        "return",
        "True",
        "False",
        "None",
        "and",
        "or",
        "not",
        "in"
    }
    if other[0] not in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
        if other in keywords:
            return Token(other, line, column, None)
        elif regexp.returner('id', other):
            return Token("ident", line, column, other)
        else:
            lexer_error(line, column)
    else:
        if regexp.returner('i', other):
            return Token("int", line, column, other)
        elif regexp.returner('f', other):
            return Token("double", line, column, other)
        else:
            lexer_error(line, column)


def sign_check(sign: str, line: int, column: int) -> Token:
    all_signs = {
        '+': 'plus',
        '-': 'minus',
        '*': 'asterisk',
        '/': 'slash',
        '%': 'percent',
        '=': 'equal',
        '<': 'left-chev',
        '>': 'right-chev',
        '<=': 'less-equal',
        '>=': 'more-equal',
        '==': 'is-equal',
        '!=': 'not-equal',
        '**': 'exponent',
        '//': 'floor-div',
        '+=': 'self-inc',
        '-=': 'self-dec',
        '*=': 'self-mul',
        '/=': 'self-div',
        '%=': 'self-mod',
        '**=': 'self-exp',
        '//=': 'self-floor',
        '=>': 'arrow',
        '|>': 'pipe'
    }
    if sign in all_signs:
        return Token(all_signs[sign], line, column, None)
    else:
        lexer_error(line, column)


def lexing(code: list) -> list:
    ignore = {'\n', '\t', ' '}
    alone = {
        '(': 'left-paren',
        ')': 'right-paren',
        '[': 'left-brack',
        ']': 'right-brack',
        '{': 'left-curl',
        '}': 'right-curl',
        ':': 'colon',
        ';': 'semicolon',
        ',': 'comma'
    }
    composable = {
        '+': 'plus',
        '-': 'minus',
        '*': 'asterisk',
        '/': 'slash',
        '%': 'percent',
        '=': 'equal',
        '<': 'left-chev',
        '>': 'right-chev',
        '!': 'exclam',
        '|': 'vertical'
    }
    some_word = ''
    some_sign = ''
    tokens = []
    line = 0
    column = 0
    for codeline in code:
        line += 1
        for sym in codeline:
            column += 1
            if sym in composable:
                some_sign += sym
            elif sym in alone:
                if some_sign:
                    tokens.append(sign_check(some_sign, line, column))
                    some_sign = ''
                tokens.append(Token(alone[sym], line, column, None))
            elif sym in ignore:
                if some_sign:
                    tokens.append(sign_check(some_sign, line, column))
                    some_sign = ''
                if some_word:
                    tokens.append(word_check(some_word, line, column))
                    some_word = ''
            else:
                if some_sign:
                    tokens.append(sign_check(some_sign, line, column))
                    some_sign = ''
                some_word += sym
            column = 0
    return tokens
