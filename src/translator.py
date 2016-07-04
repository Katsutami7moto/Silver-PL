# coding=utf-8

from parser import parser


def translator(code):
    assert isinstance(code, list)
    syntax_tree = parser(code)
    pass
