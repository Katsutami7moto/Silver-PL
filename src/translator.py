# coding=utf-8

import silv_parser


def walk_expr_tree(node):
    s = ''
    if node.value:
        s += node.value
    else:
        s += '('
        if node.lchild:
            s += walk_expr_tree(node.lchild)
        s += node.type
        if node.rchild:
            s += walk_expr_tree(node.rchild)
        s += ')'
    return s


def t_def(node, const=False):
    assert isinstance(node, silv_parser.Node)
    s = ''
    if const:
        s += 'const '
    if node.type[1] == 'string':
        s += 'char '
        s += node.value
        s += '[] = '
        s += walk_expr_tree(node.rchild)
        s += ';'
    else:
        s += node.type[1]
        s += ' '
        s += node.value
        s += ' = '
        s += walk_expr_tree(node.rchild)
        s += ';'
    return s


def t_var(node):
    return t_def(node)


def t_const(node):
    return t_def(node, True)


def t_let(node):
    assert isinstance(node, silv_parser.Node)
    s = ''
    if node.type[1] != 'string':
        s += node.value
        s += ' = '
        s += walk_expr_tree(node.rchild)
        s += ';'
    return s


def t_print(node):
    assert isinstance(node, silv_parser.Node)
    s = ''
    mod = ''
    if node.type[1] == 'int':
        mod = '%d'
    elif node.type[1] == 'double':
        mod = '%f'
    elif node.type[1] == 'string':
        mod = '%s'
    s += 'printf("'
    s += mod
    s += '", '
    s += walk_expr_tree(node.rchild)
    s += ');'
    return s


def t_printline(node):
    assert isinstance(node, silv_parser.Node)
    s = ''
    mod = ''
    if node.type[1] == 'int':
        mod = '%d\\n'
    elif node.type[1] == 'double':
        mod = '%f\\n'
    elif node.type[1] == 'string':
        mod = '%s\\n'
    elif node.type[1] == 'line':
        mod = '\\n'
    s += 'printf("'
    s += mod
    s += '"'
    if node.rchild:
        s += ', '
        s += walk_expr_tree(node.rchild)
    s += ');'
    return s


def t_input(node):
    assert isinstance(node, silv_parser.Node)
    s = ''
    mod = ''
    if node.type[1] == 'int':
        mod = '%d'
    elif node.type[1] == 'double':
        mod = '%f'
    if len(node.type) == 3:
        s += node.type[1]
        s += ' '
        s += node.value
        s += ';\n'
    s += 'scanf("'
    s += mod
    s += '", &'
    s += node.value
    s += ');'
    return s


def t_loop(node):
    assert isinstance(node, silv_parser.Node)
    s = 'while (1)\n{\n'
    ltmp = nlist_walk(node.rchild)
    for line in ltmp:
        s += line
        s += '\n'
    s += '}'
    return s


def t_do(node):
    assert isinstance(node, silv_parser.Node)
    s = 'do\n{\n'
    ltmp = nlist_walk(node.rchild)
    for line in ltmp:
        s += line
        s += '\n'
    s += '} while '
    s += walk_expr_tree(node.lchild)
    s += ';'
    return s


def t_while(node):
    assert isinstance(node, silv_parser.Node)
    s = 'while '
    s += walk_expr_tree(node.lchild)
    s += '\n{\n'
    ltmp = nlist_walk(node.rchild)
    for line in ltmp:
        s += line
        s += '\n'
    s += '}'
    return s


def t_until(node):
    assert isinstance(node, silv_parser.Node)
    s = 'while (!'
    s += walk_expr_tree(node.lchild)
    s += ')\n{\n'
    ltmp = nlist_walk(node.rchild)
    for line in ltmp:
        s += line
        s += '\n'
    s += '}'
    return s


def t_break(node):
    assert isinstance(node, silv_parser.Node)
    s = node.type[0]
    s += ';'
    return s


def t_continue(node):
    assert isinstance(node, silv_parser.Node)
    s = node.type[0]
    s += ';'
    return s


def t_if(node):
    assert isinstance(node, silv_parser.Node)
    s = 'if '
    s += walk_expr_tree(node.lchild)
    s += '\n{\n'
    ltmp = nlist_walk(node.rchild)
    for line in ltmp:
        s += line
        s += '\n'
    s += '}'
    return s


def t_elif(node):
    assert isinstance(node, silv_parser.Node)
    s = 'else if '
    s += walk_expr_tree(node.lchild)
    s += '\n{\n'
    ltmp = nlist_walk(node.rchild)
    for line in ltmp:
        s += line
        s += '\n'
    s += '}'
    return s


def t_else(node):
    assert isinstance(node, silv_parser.Node)
    s = 'else\n{\n'
    ltmp = nlist_walk(node.rchild)
    for line in ltmp:
        s += line
        s += '\n'
    s += '}'
    return s


def translating(code):
    assert isinstance(code, list)
    nodes_list = silv_parser.parsing(code)
    return nlist_walk(nodes_list)


def nlist_walk(nlist):
    slist = []
    for node in nlist:
        assert isinstance(node, silv_parser.Node)
        func = 't_' + node.type[0] + '(node)'
        slist.append(eval(func))
    return slist
