# coding=utf-8

from lexer import lexer


def parser(code):
    assert isinstance(code, list)
    tokens_list = lexer(code)
    pass
