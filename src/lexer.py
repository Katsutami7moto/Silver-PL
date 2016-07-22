# coding=utf-8

import regexp

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
    '**': 'exponentiation',
    '//': 'floor-div',
    '=>': 'arrow',
    '|>': 'pipe'
}
ignore = {'\n', '\t', ' '}
keywords = {
    "var",
    "const",
    "let",
    "print",
    "printline",
    "input",
    "type",
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
    "and",
    "or",
    "not"
}
other = ""
tokens = []
eqp = ''
eqplus = False
LINE = 0
SYMBOL = 0


class Token:
    def __init__(self, t, ln, sm, v=None):
        self.type = t
        self.value = v
        self.line = ln
        self.symbol = sm


def check():
    global other
    if len(other) > 0:
        if other[0] not in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
            if other in keywords:
                tokens.append(Token(other, LINE, SYMBOL))
            elif regexp.returner('id', other):
                tokens.append(Token("ident", LINE, SYMBOL, other))
            else:
                raise Exception, "Некорректная лексема %d:%d" % (LINE, SYMBOL)
        else:
            if regexp.returner('i', other):
                tokens.append(Token("int", LINE, SYMBOL, other))
            elif regexp.returner('f', other):
                tokens.append(Token("double", LINE, SYMBOL, other))
            else:
                raise Exception, "Некорректная лексема %d:%d" % (LINE, SYMBOL)
        other = ''


def lexing(code):
    # type: (list) -> list
    global other, eqplus, eqp, LINE, SYMBOL
    for line in code:
        assert isinstance(line, str)
        LINE += 1
        for sym in line:
            SYMBOL += 1
            if sym in symbols:
                check()
                if sym == '<' or sym == '>' or sym == '!':
                    eqplus = True
                    eqp = sym
                elif sym == '=':
                    if eqplus:
                        eqp += '='
                        tokens.append(Token(eqp, LINE, SYMBOL))
                        eqp = ''
                        eqplus = False
                    else:
                        tokens.append(Token('=', LINE, SYMBOL))
                else:
                    if eqplus:
                        tokens.append(Token(eqp, LINE, SYMBOL))
                        eqp = ''
                        eqplus = False
                    tokens.append(Token(symbols[sym], LINE, SYMBOL))
            elif sym in ignore:
                check()
            else:
                if eqplus:
                    tokens.append(Token(eqp, LINE, SYMBOL))
                    eqp = ''
                    eqplus = False
                other += sym
        SYMBOL = 0
    LINE = 0
    return tokens
