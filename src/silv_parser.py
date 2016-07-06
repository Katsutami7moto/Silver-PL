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
    'string'
}
symbol_table = dict(vars=dict())


def p_var(term):
    assert isinstance(term, list)
    if term[0].type == 'ident' and term[1].type == 'equal':
        nd = Node('var', term[0].value)
        ndr = term[2:]
        if len(ndr) == 1:
            subj = ndr[0]
            assert isinstance(subj, lexer.Token)
            if subj.type in datas:
                tmp = Node(subj.type, subj.value)
                symbol_table['vars'][nd.value] = tmp.type
                nd.setr(tmp)
            elif subj.type in {"True", "False"}:
                tmp = Node(subj.type)
                symbol_table['vars'][nd.value] = tmp.type
                nd.setr(tmp)
            elif subj.type == 'ident':
                try:
                    find = symbol_table['vars'][subj.value]
                except KeyError:
                    raise NameError, "Попытка определения через неопределённую переменную"
                else:
                    tmp = Node(find, subj.value)
                    symbol_table['vars'][nd.value] = tmp.type
                    nd.setr(tmp)
            else:
                raise NameError, "Некорректный параметр"
        else:
            pass  # для сложных параметров

        return nd


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
