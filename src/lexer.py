# coding=utf-8

import regexp

symbols = {
    '+': 'plus',
    '-': 'minus',
    '*': 'mul',
    '/': 'div',
    '%': 'mod',
    '=': 'equal',
    '<': 'less',
    '>': 'more',
    '(': 'left-paren',
    ')': 'right-paren',
    '[': 'left-brack',
    ']': 'right-brack',
    '{': 'left-curl',
    '}': 'right-curl',
    ';': 'semicolon',
    ',': 'comma'
}
ignore = {'\n', '\t', ' '}
keywords = {
    "var",
    "const",
    "let",
    "del",
    "print",
    "input",
    "type",
    "new",
    "while",
    "do",
    "until",
    "if",
    "elif",
    "else",
    "return",
    "True",
    "False"
}
other = ""
tokens = []
r_ident = "(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)" \
          "(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|0|1|2|3|4|5|6|7|8|9)*"
r_int = "0|(1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*"
r_float = "0|(1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*\\.(0|1|2|3|4|5|6|7|8|9)+"
r_string = "\".+\""


class Token:
    def __init__(self, t, v):
        self.type = t
        self.value = v


def make_token(typ, value=None):
    return Token(typ, value)


def r_cover(reg):
    assert isinstance(reg, str)
    return "(" + reg + ")#"


def check():
    global other
    if len(other) != 0:
        if other in keywords:
            tokens.append(make_token(other))
        else:
            if regexp.returner(r_cover(r_ident), other):
                tokens.append(make_token("ident", other))
            elif regexp.returner(r_cover(r_int), other):
                tokens.append(make_token("int", other))
            elif regexp.returner(r_cover(r_float), other):
                tokens.append(make_token("double", other))
            elif regexp.returner(r_cover(r_string), other):
                tokens.append(make_token("string", other))
            else:
                raise NameError, "Некорректная лексема"
        other = ''


def lexing(code):
    assert isinstance(code, list)
    global other
    in_string = False
    for line in code:
        assert isinstance(line, str)
        for sym in line:
            if sym in symbols and not in_string:
                check()
                tokens.append(make_token(symbols[sym]))
            elif sym in ignore and not in_string:
                check()
                continue
            else:
                other += sym
                if sym == '"':
                    if not in_string:
                        in_string = True
                    else:
                        in_string = False
    return tokens
