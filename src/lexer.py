from collections import namedtuple


Token = namedtuple('Token', 'type line column value')


def lexer_error(lexem: str, line: int, column: int):
    raise Exception("Некорректная лексема '{0:s}', строка {1:d}, колонка {2:d}".format(lexem, line, column))


def uminus(token: Token) -> Token:
    return token._replace(type='-u')


def word_check(word: str, line: int, column: int) -> Token:
    from src import regexp
    keywords = {
        "module",

        "connections",
        "types",
        "fields",
        "functions",

        "import",
        "use",

        "type",
        "typedef",
        "interface",
        "suit",

        "var",
        "let",

        "extend",

        "func",
        "proc",
        "pure",
        "cort",

        "new",
        "mod",  # TODO: точно ли такое слово ?
        "while",
        "loop",
        "do",
        "until",
        "for",
        "break",
        "continue",
        "if",
        "elif",
        "else",
        "call",  # TODO: точно ли такое слово ?
        "match",
        "lambda",  # TODO: точно ли такое слово ?
        "return",
        "del",

        "True",
        "False",
        "None",  # TODO: точно ли такое слово ? реализация ???
        "and",
        "or",
        "not",
        "in"
    }
    if word[0] in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
        if regexp.returner('i', word):
            return Token("int", line, column, word)
        elif regexp.returner('f', word):
            return Token("double", line, column, word)
        else:
            lexer_error(word, line, column)
    else:
        if word in keywords:
            return Token(word, line, column, None)
        elif regexp.returner('id', word):
            return Token("ident", line, column, word)
        else:
            lexer_error(word, line, column)


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
        '>=': 'greater-equal',
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
        lexer_error(sign, line, column)


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
    composable = {'+', '-', '*', '/', '%', '=', '<', '>', '!', '|'}
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
