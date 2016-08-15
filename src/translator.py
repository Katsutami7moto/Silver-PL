from src import silv_parser


def walk_expr_tree(node):
    # type: (silv_parser.Node) -> str
    if node.value:
        if node.type[0] == 'call':
            return '%s(%s)' % (node.value, walk_expr_tree(node.rchild))
        else:
            return node.value
    else:
        if node.type == ',':
            return '{0:s}, {1:s}'.format(walk_expr_tree(node.lchild), walk_expr_tree(node.rchild))
        elif node.lchild and node.rchild:
            return '({0:s} {1:s} {2:s})'.format(walk_expr_tree(node.lchild), node.type, walk_expr_tree(node.rchild))
        elif node.lchild:
            return '({0:s} {1:s} )'.format(walk_expr_tree(node.lchild), node.type)
        elif node.rchild:
            return '({0:s}{1:s})'.format(node.type, walk_expr_tree(node.rchild))
        else:
            return '({0:s})'.format(node.type)


def t_var(node):
    # type: (silv_parser.Node) -> str
    return '{0:s} {1:s} = {2:s};'.format(node.type[1], node.value, walk_expr_tree(node.rchild))


def t_let(node):
    # type: (silv_parser.Node) -> str
    return 'const {0:s} {1:s} = {2:s};'.format(node.type[1], node.value, walk_expr_tree(node.rchild))


def t_mod(node):
    # type: (silv_parser.Node) -> str
    return '{0:s} {1:s} {2:s};'.format(node.value, node.type[1], walk_expr_tree(node.rchild))


def t_loop(node):
    # type: (silv_parser.Node) -> str
    return 'while (1)\n{{\n{0:s}\n}}'.format('\n'.join(nlist_walk(node.rchild)))


def t_do(node):
    # type: (silv_parser.Node) -> str
    return 'do\n{{\n{0:s}\n}} while {1:s};'.format('\n'.join(nlist_walk(node.rchild)), walk_expr_tree(node.lchild))


def t_while(node):
    # type: (silv_parser.Node) -> str
    return 'while {0:s}\n{{\n{1:s}\n}}'.format(walk_expr_tree(node.lchild), '\n'.join(nlist_walk(node.rchild)))


def t_until(node):
    # type: (silv_parser.Node) -> str
    return 'while (!{0:s})\n{{\n{1:s}\n}}'.format(walk_expr_tree(node.lchild), '\n'.join(nlist_walk(node.rchild)))


def t_break(node):
    # type: (silv_parser.Node) -> str
    return '{0:s};'.format(node.type[0])


def t_continue(node):
    # type: (silv_parser.Node) -> str
    return '{0:s};'.format(node.type[0])


def t_if(node):
    # type: (silv_parser.Node) -> str
    return 'if {0:s}\n{{\n{1:s}\n}}'.format(walk_expr_tree(node.lchild), '\n'.join(nlist_walk(node.rchild)))


def t_elif(node):
    # type: (silv_parser.Node) -> str
    return 'else if {0:s}\n{{\n{1:s}\n}}'.format(walk_expr_tree(node.lchild), '\n'.join(nlist_walk(node.rchild)))


def t_else(node):
    # type: (silv_parser.Node) -> str
    return 'else\n{{\n{0:s}\n}}'.format('\n'.join(nlist_walk(node.rchild)))


def t_func(node):
    # type: (silv_parser.Node) -> str
    return '{0:s} {1:s}({2:s})\n{{\n{3:s}\n}}'.format(node.type[1], node.value,
                                                      ' '.join(node.lchild), '\n'.join(nlist_walk(node.rchild)))


def t_return(node):
    # type: (silv_parser.Node) -> str
    return 'return {0:s};'.format(walk_expr_tree(node.rchild))


def translating(code: list) -> list:
    return nlist_walk(silv_parser.parsing(code))


def nlist_walk(nlist: list) -> list:
    return [eval('t_{0:s}(node)'.format(node.type[0])) for node in nlist]
