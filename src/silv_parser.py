# coding=utf-8

import lexer


class Node:
    def __init__(self, t, v=None):
        self.type = t
        self.value = v

        self.lchild = None
        self.rchild = None

    def setl(self, obj):
        assert isinstance(obj, Node)
        self.lchild = obj

    def setr(self, obj):
        assert isinstance(obj, Node)
        self.rchild = obj


nodes = []
level1 = True
math = False
def_type = ''
current = 0
curr = 0
tokens_list = []
sems = {
    "var",
    "const",
    "let",
    "del",
    "print",
    "input",
    "return"
}
datas = {
    "int",
    "double",
    "string"
}
symbol_table = dict(names=dict())


def p_atom(token):
    """
    :rtype: Node
    :type token: lexer.Token
    """
    if token.type in datas:
        tmp = Node(token.type, token.value)
    elif token.type == "True":
        tmp = Node("int", "1")
    elif token.type == "False":
        tmp = Node("int", "0")
    elif token.type == 'ident':
        if token.value in symbol_table['names']:
            tmp = Node(symbol_table['names'][token.value][0], token.value)
        else:
            raise NameError, "Попытка определения через неопределённую переменную"
    else:
        raise NameError, "Некорректный параметр"
    return tmp


def build_tree(tokens):
    """
    :rtype: Node
    :type tokens: list
    """
    nd = None
    if len(tokens) == 3:
        nd = Node(tokens[1])
        nd.setl(build_tree(tokens[0]))
        nd.setr(build_tree(tokens[2]))
    elif len(tokens) == 2:
        nd = Node(tokens[0])
        nd.setr(build_tree(tokens[1]))
    elif len(tokens) == 1:
        nd = p_atom(tokens[0])
    return nd


def p_operand(tokens):
    """
    :rtype: list
    :type tokens: list
    """
    t = []
    if len(tokens) == 1:
        if isinstance(tokens[0], list):
            return p_or(tokens[0])
        elif isinstance(tokens[0], lexer.Token):
            return tokens
    elif len(tokens) == 2:
        if tokens[0].type == 'minus':
            t.append('-')
        elif tokens[0].type == 'not':
            t.append('!')
        t.append(tokens[1])
        return t


def p_mult(tokens):
    """
    :rtype: list
    :type tokens: list
    """
    ts = []
    t = []
    met = False
    global level1, math
    for token in tokens:
        if isinstance(token, lexer.Token):
            if not met:
                if token.type == 'mul':
                    met = True
                    ts.append(t)
                    ts.append('*')
                    t = []
                    if level1:
                        math = True
                        level1 = False
                    continue
                elif token.type == 'div':
                    met = True
                    ts.append(t)
                    ts.append('/')
                    t = []
                    if level1:
                        math = True
                        level1 = False
                    continue
                elif token.type == 'mod':
                    met = True
                    ts.append(t)
                    ts.append('%')
                    t = []
                    if level1:
                        math = True
                        level1 = False
                    continue
            else:
                t.append(token)
        else:
            t.append(token)
    if not met:
        return p_operand(tokens)
    else:
        ts.append(t)
        ts[0] = p_or(ts[0])
        ts[-1] = p_or(ts[-1])
        return ts


def p_addit(tokens):
    """
    :rtype: list
    :type tokens: list
    """
    ts = []
    t = []
    met = False
    global level1, math
    for token in tokens:
        if isinstance(token, lexer.Token):
            if not met:
                if token.type == 'plus':
                    met = True
                    ts.append(t)
                    ts.append('+')
                    t = []
                    if level1:
                        math = True
                        level1 = False
                    continue
                elif token.type == 'minus':
                    if len(t) == 0:
                        t.append(token)
                    else:
                        met = True
                        ts.append(t)
                        ts.append('-')
                        t = []
                        if level1:
                            math = True
                            level1 = False
                    continue
            else:
                t.append(token)
        else:
            t.append(token)
    if not met:
        return p_mult(tokens)
    else:
        ts.append(t)
        ts[0] = p_or(ts[0])
        ts[-1] = p_or(ts[-1])
        return ts


def p_comp(tokens):
    """
    :rtype: list
    :type tokens: list
    """
    ts = []
    t = []
    met = False
    global level1, def_type
    for token in tokens:
        if isinstance(token, lexer.Token):
            if not met:
                if token.type == '<' or token.type == '>' or token.type == '<=' or token.type == '>=':
                    met = True
                    ts.append(t)
                    ts.append(token.type)
                    t = []
                    if level1:
                        def_type = 'int'
                        level1 = False
                    continue
            else:
                t.append(token)
        else:
            t.append(token)
    if not met:
        return p_addit(tokens)
    else:
        ts.append(t)
        ts[0] = p_or(ts[0])
        ts[-1] = p_or(ts[-1])
        return ts


def p_equal(tokens):
    """
    :rtype: list
    :type tokens: list
    """
    ts = []
    t = []
    met = False
    global level1, def_type
    for token in tokens:
        if isinstance(token, lexer.Token):
            if not met:
                if token.type == '=' or token.type == '!=':
                    met = True
                    ts.append(t)
                    if token.type == '=':
                        ts.append('==')
                    else:
                        ts.append(token.type)
                    t = []
                    if level1:
                        def_type = 'int'
                        level1 = False
                    continue
            else:
                t.append(token)
        else:
            t.append(token)
    if not met:
        return p_comp(tokens)
    else:
        ts.append(t)
        ts[0] = p_or(ts[0])
        ts[-1] = p_or(ts[-1])
        return ts


def p_and(tokens):
    """
    :rtype: list
    :type tokens: list
    """
    ts = []
    t = []
    met = False
    global level1, def_type
    for token in tokens:
        if isinstance(token, lexer.Token):
            if token.type == 'and' and not met:
                met = True
                ts.append(t)
                ts.append('&&')
                t = []
                if level1:
                    def_type = 'int'
                    level1 = False
            else:
                t.append(token)
        else:
            t.append(token)
    if not met:
        return p_equal(tokens)
    else:
        ts.append(t)
        ts[0] = p_or(ts[0])
        ts[-1] = p_or(ts[-1])
        return ts


def p_or(tokens):
    """
    :rtype: list
    :type tokens: list
    """
    ts = []
    t = []
    met = False
    global level1, def_type
    for token in tokens:
        if isinstance(token, lexer.Token):
            if token.type == 'or' and not met:
                met = True
                ts.append(t)
                ts.append('||')
                t = []
                if level1:
                    def_type = 'int'
                    level1 = False
            else:
                t.append(token)
        else:
            t.append(token)
    if not met:
        return p_and(tokens)
    else:
        ts.append(t)
        ts[0] = p_or(ts[0])
        ts[-1] = p_or(ts[-1])
        return ts


def p_expr(tokens):
    """
    :rtype: list
    :type tokens: list
    """
    t = []
    global curr
    while curr < len(tokens) and tokens[curr].type != 'right-paren':
        if tokens[curr].type == 'left-paren':
            curr += 1
            t.append(p_expr(tokens))
        else:
            t.append(tokens[curr])
        curr += 1
    return t


def p_def(term, t):
    assert isinstance(term, list)
    global def_type
    if term[0].type == 'ident' and term[1].type == '=':
        nd = Node([t, ''], term[0].value)
        if nd.value not in symbol_table['names']:
            ndr = term[2:]
            if len(ndr) == 0:
                raise NameError, "Отсутствует параметр"
            else:
                if len(ndr) == 1:
                    par = p_atom(ndr[0])
                else:
                    par = build_tree(p_or(p_expr(ndr)))
                symbol_table['names'][nd.value] = [par, t]
                nd.setr(par)
                nd.type[1] = def_type
                def_type = ''
                return nd
        else:
            raise NameError, "Попытка определения уже определённой переменной"
    else:
        raise NameError, "Некорректное использование оператора " + t


def p_var(term):
    return p_def(term, 'var')


def p_const(term):
    return p_def(term, 'const')


def p_sem(kot):
    assert isinstance(kot, lexer.Token)
    global current
    if kot.type in sems:
        term = []
        current += 1
        while tokens_list[current].type != 'semicolon':
            term.append(tokens_list[current])
            current += 1
        current += 1
        func = 'p_' + kot.type + '(term)'
        nodes.append(eval(func))


def p_instructions():
    p_sem(tokens_list[current])
    # p_curl(tokens_list[current])
    # p_curl_sem(tokens_list[current])
    # p_curl_plus(tokens_list[current])


def p_block():
    while current < len(tokens_list) and tokens_list[current].type != 'right-curl':
        p_instructions()


def parsing(code):
    assert isinstance(code, list)
    global tokens_list
    tokens_list = lexer.lexing(code)
    if tokens_list:
        p_block()
    return nodes
