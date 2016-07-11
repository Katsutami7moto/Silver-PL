# coding=utf-8

import regexp

symbols = {
    '+': 'plus',
    '-': 'minus',
    '*': 'mul',
    '/': 'div',
    '%': 'mod',
    '=': 'equal',
    '<': 'left-chev',
    '>': 'right-chev',
    '(': 'left-paren',
    ')': 'right-paren',
    '[': 'left-brack',
    ']': 'right-brack',
    '{': 'left-curl',
    '}': 'right-curl',
    ';': 'semicolon',
    ',': 'comma',
    '!': 'exclam'
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
    "False",
    "and",
    "or",
    "not"
}
other = ""
tokens = []
r_ident = "(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)" \
          "(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|0|1|2|3|4|5|6|7|8|9)*"
r_int = "0|(1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*"
r_float = "0|(1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*\\.(0|1|2|3|4|5|6|7|8|9)+"
r_string = "\".+\""
eqp = ''
eqplus = False


class Token:
    def __init__(self, t, v=None):
        self.type = t
        self.value = v


def r_cover(reg):
    assert isinstance(reg, str)
    return "(" + reg + ")#"


def check():
    global other
    if len(other) != 0:
        if other in keywords:
            tokens.append(Token(other))
        else:
            if regexp.returner(r_cover(r_ident), other):
                tokens.append(Token("ident", other))
            elif regexp.returner(r_cover(r_int), other):
                tokens.append(Token("int", other))
            elif regexp.returner(r_cover(r_float), other):
                tokens.append(Token("double", other))
            elif regexp.returner(r_cover(r_string), other):
                tokens.append(Token("string", other))
            else:
                raise Exception, "Некорректная лексема"
        other = ''


def lexing(code):
    assert isinstance(code, list)
    global other, eqplus, eqp
    in_string = False
    for line in code:
        assert isinstance(line, str)
        for sym in line:
            if sym in symbols and not in_string:
                check()
                if sym == '<' or sym == '>' or sym == '!':
                    eqplus = True
                    eqp = sym
                elif sym == '=':
                    if eqplus:
                        eqp += '='
                        tokens.append(Token(eqp))
                        eqp = ''
                        eqplus = False
                    else:
                        tokens.append(Token('='))
                else:
                    tokens.append(Token(symbols[sym]))
            elif sym in ignore and not in_string:
                check()
                continue
            else:
                if eqplus:
                    tokens.append(Token(eqp))
                    eqp = ''
                    eqplus = False
                other += sym
                if sym == '"':
                    if not in_string:
                        in_string = True
                    else:
                        in_string = False
    return tokens
