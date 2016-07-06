# coding=utf-8

import silv_parser


def t_var(node):
    return t_def(node)


def t_const(node):
    return t_def(node, True)


def t_def(node, const=False):
    assert isinstance(node, silv_parser.Node)
    assert isinstance(node.rchild, silv_parser.Node)
    s = ''
    if not (node.rchild.lchild and node.rchild.rchild):
        if const:
            s += 'const '
        if node.type[1] == 'string':
            s += 'char '
            s += node.value
            s += '[] = '
            s += node.rchild.value
            s += ';'
        else:
            s += node.type[1]
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
        func = 't_' + node.type[0] + '(node)'
        strings_list.append(eval(func))
    return strings_list
