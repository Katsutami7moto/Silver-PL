# coding=utf-8

import silv_parser


def t_var(node):
    assert isinstance(node, silv_parser.Node)
    assert isinstance(node.rchild, silv_parser.Node)
    s = ''
    if not (node.rchild.lchild and node.rchild.rchild):
        s += node.rchild.type
        s += ' '
        s += node.value
        s += ' = '
        s += node.rchild.value
        s += ';'
    else:
        pass  # для сложных параметров
    return s


def translating(code):
    assert isinstance(code, list)
    nodes_list = silv_parser.parsing(code)
    strings_list = []
    for node in nodes_list:
        assert isinstance(node, silv_parser.Node)
        func = 't_' + node.type + '(node)'
        strings_list.append(eval(func))
    return strings_list
