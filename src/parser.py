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
    "ident",
    "int",
    "double",
    "string"
}


def p_param(term):
    assert isinstance(term, list)
    if len(term) == 1:
        subj = term[0]
        assert isinstance(subj, lexer.Token)
        if subj.type in datas:
            return Node(subj.type, subj.value)
        elif subj.type in {"True", "False"}:
            return Node(subj.type)
        else:
            pass  # параметр - один токен, но не данные и не идентификатор
    else:
        pass  # для сложных параметров


def p_var(term):
    assert isinstance(term, list)
    if term[0].type == 'ident' and term[1].type == 'equal':
        nd = Node('var', term[0].value)
        nd.setr(p_param(term[2:]))
        return nd


def p_sem(check):
    global current
    if check:
        term = []
        current += 1
        while tokens_list[current] != 'semicolon':
            term.append(tokens_list[current])
            current += 1
        current += 1
        func = 'p_' + check + '(term)'
        nodes.append(eval(func))


def c_sem(kot):
    assert isinstance(kot, lexer.Token)
    if kot.type in sems:
        return kot.type
    else:
        return False


def p_instructions():
    p_sem(c_sem(tokens_list[current]))
    # p_curl(c_curl(tokens_list[current]))
    # p_curl_sem(c_curl_sem(tokens_list[current]))
    # p_curl_plus(c_curl_plus(tokens_list[current]))


def p_block():
    while current < len(tokens_list) and tokens_list[current].type != 'right-curl':
        p_instructions()


def parser(code):
    assert isinstance(code, list)
    global tokens_list
    tokens_list = lexer.lexer(code)
    if tokens_list:
        p_block()
    return nodes
