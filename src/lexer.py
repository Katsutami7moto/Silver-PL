# coding=utf-8

from regexp import returner

# сначала разбить текст на слова, числа и символы
# с помощью комбинации str.join(list) и str.split(str)
# ограничив все символы пробелами
# затем перевести их в токены

symbols = {'+', '-', '*', '/', '%', '=', '<', '>', '(', ')', '[', ']', '{', '}', ';', ','}
tokens = []
other = ""
r_ident = "(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)" \
          "(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|0|1|2|3|4|5|6|7|8|9)*"
r_int = "0|(1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*"
r_float = "0|(1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*\\.(0|1|2|3|4|5|6|7|8|9)+"
r_string = "\".+\""
r_var = "var"
r_const = "const"
r_let = "let"
r_del = "del"
r_print = "print"
r_input = "input"
r_type = "type"
r_new = "new"
r_while = "while"
r_do = "do"
r_until = "until"
r_if = "if"
r_elif = "elif"
r_else = "else"
r_return = "return"


def reg_cover(reg):
    assert isinstance(reg, str)
    return "(" + reg + ")#"


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
                tokens.append(make_sign_token(sym))
            else:
                other += sym


# if returner("(n..b)#", "n00b"):
#     print "Good!"
# else:
#     print "Bad!"
#
# if returner("(\".+\")#", '"ghjvbjdvg"'):
#     print "Good!"
# else:
#     print "Bad!"
