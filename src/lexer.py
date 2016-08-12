from src import regexp

symbols = {
    '+': 'plus',
    '-': 'minus',
    '*': 'asterisk',
    '/': 'slash',
    '%': 'percent',
    '=': 'equal',
    '<': 'left-chev',
    '>': 'right-chev',
    '(': 'left-paren',
    ')': 'right-paren',
    '[': 'left-brack',
    ']': 'right-brack',
    '{': 'left-curl',
    '}': 'right-curl',
    ':': 'colon',
    ';': 'semicolon',
    ',': 'comma',
    '!': 'exclam'
}
composites = {
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
ignore = {'\n', '\t', ' '}
keywords = {
    "module",
    "use",
    "import",
    "var",
    "let",
    "mod",  # TODO: точно ли такое слово ?
    "def",
    "print",
    "printline",
    "input",
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
other = ""
sign = ""
tokens = []
LINE = 0
SYMBOL = 0


class Token:
    def __init__(self, t, ln, sm, v=None):
        self.type = t
        self.value = v
        self.line = ln
        self.symbol = sm


def lexer_error():
    raise Exception("Некорректная лексема %d:%d" % (LINE, SYMBOL))


def word_check():
    global other
    if len(other) > 0:
        if other[0] not in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
            if other in keywords:
                tokens.append(Token(other, LINE, SYMBOL))
            elif regexp.returner('id', other):
                tokens.append(Token("ident", LINE, SYMBOL, other))
            else:
                lexer_error()
        else:
            if regexp.returner('i', other):
                tokens.append(Token("int", LINE, SYMBOL, other))
            elif regexp.returner('f', other):
                tokens.append(Token("double", LINE, SYMBOL, other))
            else:
                lexer_error()
        other = ''


def sign_check():
    global sign
    if len(sign) > 0:
        if sign in symbols:
            tokens.append(Token(symbols[sign], LINE, SYMBOL))
        elif sign in composites:
            tokens.append(Token(composites[sign], LINE, SYMBOL))
        else:
            lexer_error()
        sign = ''


def paren_check():
    global sign
    if len(sign) > 0:
        if sign == '(' or sign == ')':
            tokens.append(Token(symbols[sign], LINE, SYMBOL))
            sign = ''


def lexing(code: list) -> list:
    global other, sign, LINE, SYMBOL
    for line in code:
        assert isinstance(line, str)
        LINE += 1
        for sym in line:
            SYMBOL += 1
            if sym in symbols:
                word_check()
                paren_check()
                sign += sym
            elif sym in ignore:
                paren_check()
                sign_check()
                word_check()
            else:
                paren_check()
                sign_check()
                other += sym
        SYMBOL = 0
    LINE = 0
    return tokens
