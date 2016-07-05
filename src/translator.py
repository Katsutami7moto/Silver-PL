# coding=utf-8

import parser


def t_var(node):
    assert isinstance(node, parser.Node)
    assert isinstance(node.rchild, parser.Node)
    s = ''
    if not (node.rchild.lchild and node.rchild.rchild):
        s += node.rchild.type
        s += node.value
        s += node.rchild.value
        s += ';'
    else:
        pass  # для сложных параметров
    return s


def translator(code):
    assert isinstance(code, list)
    nodes_list = parser.parser(code)
    strings_list = []
    for node in nodes_list:
        assert isinstance(node, parser.Node)
        func = 't_' + node.type + '(node)'
        strings_list.append(eval(func))
    return strings_list
