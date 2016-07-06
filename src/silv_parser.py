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
current = 0
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
    assert isinstance(token, lexer.Token)
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
    return [tmp, tmp.type]


def p_param(tokens):
    assert isinstance(tokens, list)
    if len(tokens) == 1:
        return p_atom(tokens[0])
    # else:
    #     return p_expr(tokens)


def p_def(term, t):
    assert isinstance(term, list)
    if term[0].type == 'ident' and term[1].type == 'equal':
        nd = Node([t, ''], term[0].value)
        if nd.value not in symbol_table['names']:
            ndr = term[2:]
            if len(ndr) == 0:
                raise NameError, "Отсутствует параметр"
            else:
                par = p_param(ndr)
                symbol_table['names'][nd.value] = [par[1], t]
                nd.setr(par[0])
                nd.type[1] = par[1]
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
