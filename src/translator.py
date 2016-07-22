# coding=utf-8

import silv_parser


def walk_expr_tree(node):
    # type: (silv_parser.Node) -> str
    s = ''
    if node.value:
        s += node.value
        if node.type[0] == 'call':
            s += '('
            s += walk_expr_tree(node.rchild)
            s += ')'
    else:
        if node.type != ',':
            s += '('
        if node.lchild:
            s += walk_expr_tree(node.lchild)
            s += ' '
        s += node.type
        if node.lchild:
            s += ' '
        if node.rchild:
            s += walk_expr_tree(node.rchild)
        if node.type != ',':
            s += ')'
    return s


def t_def(node, const=False):
    # type: (silv_parser.Node) -> str
    s = ''
    if const:
        s += 'const '
    s += node.type[1]
    s += ' '
    s += node.value
    s += ' = '
    s += walk_expr_tree(node.rchild)
    s += ';'
    return s


def t_var(node):
    # type: (silv_parser.Node) -> str
    return t_def(node)


def t_const(node):
    # type: (silv_parser.Node) -> str
    return t_def(node, True)


def t_let(node):
    # type: (silv_parser.Node) -> str
    s = ''
    s += node.value
    s += ' = '
    s += walk_expr_tree(node.rchild)
    s += ';'
    return s


def t_print(node):
    # type: (silv_parser.Node) -> str
    s = ''
    mod = ''
    if node.type[1] == 'int':
        mod = '%d'
    elif node.type[1] == 'double':
        mod = '%f'
    s += 'printf("'
    s += mod
    s += '", '
    s += walk_expr_tree(node.rchild)
    s += ');'
    return s


def t_printline(node):
    # type: (silv_parser.Node) -> str
    s = ''
    mod = ''
    if node.type[1] == 'int':
        mod = '%d\\n'
    elif node.type[1] == 'double':
        mod = '%f\\n'
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
    # type: (silv_parser.Node) -> str
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
    # type: (silv_parser.Node) -> str
    s = 'while (1)\n{\n'
    ltmp = nlist_walk(node.rchild)
    for line in ltmp:
        s += line
        s += '\n'
    s += '}'
    return s


def t_do(node):
    # type: (silv_parser.Node) -> str
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
    # type: (silv_parser.Node) -> str
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
    # type: (silv_parser.Node) -> str
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
    # type: (silv_parser.Node) -> str
    s = node.type[0]
    s += ';'
    return s


def t_continue(node):
    # type: (silv_parser.Node) -> str
    s = node.type[0]
    s += ';'
    return s


def t_if(node):
    # type: (silv_parser.Node) -> str
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
    # type: (silv_parser.Node) -> str
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
    # type: (silv_parser.Node) -> str
    s = 'else\n{\n'
    ltmp = nlist_walk(node.rchild)
    for line in ltmp:
        s += line
        s += '\n'
    s += '}'
    return s


def t_func(node):
    # type: (silv_parser.Node) -> str
    s = node.type[1]
    s += ' '
    s += node.value
    s += ' ('
    for token in node.lchild:
        s += token
        s += ' '
    s += ')\n{\n'
    ltmp = nlist_walk(node.rchild)
    for line in ltmp:
        s += line
        s += '\n'
    s += '}'
    return s


def t_return(node):
    # type: (silv_parser.Node) -> str
    s = 'return '
    s += walk_expr_tree(node.rchild)
    s += ';'
    return s


def translating(code):
    # type: (list) -> list
    nodes_list = silv_parser.parsing(code)
    return nlist_walk(nodes_list)


def nlist_walk(nlist):
    # type: (list) -> list
    slist = []
    for node in nlist:
        assert isinstance(node, silv_parser.Node)
        func = 't_' + node.type[0] + '(node)'
        slist.append(eval(func))
    return slist
