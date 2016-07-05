# coding=utf-8

from regexp import returner

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


def check(word):
    assert isinstance(word, str)
    if word in keywords:
        tokens.append(make_token(word))
    else:
        if returner(r_cover(r_ident), word):
            tokens.append(make_token("ident", word))
        elif returner(r_cover(r_int), word):
            tokens.append(make_token("int", int(word)))
        elif returner(r_cover(r_float), word):
            tokens.append(make_token("float", float(word)))
        elif returner(r_cover(r_string), word):
            tokens.append(make_token("string", word))
        else:
            raise NameError, "Некорректная лексема"


def lexer(code):
    assert isinstance(code, list)
    global other
    for line in code:
        assert isinstance(line, str)
        for sym in line:
            if sym in symbols:
                if len(other) != 0:
                    check(other)
                    other = ""
                tokens.append(make_token(symbols[sym]))
            elif sym in ignore:
                continue
            else:
                other += sym
    return tokens

# if returner(r_cover("n..b"), "n00b"):
#     print "Good!"
# else:
#     print "Bad!"
#
# if returner(r_cover("\".+\""), '"ghjvbjdvg"'):
#     print "Good!"
# else:
#     print "Bad!"
