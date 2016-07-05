# coding=utf-8

import parser


def translator(code):
    assert isinstance(code, list)
    syntax_tree = parser.parser(code)
    pass
