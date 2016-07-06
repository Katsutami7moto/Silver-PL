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


def create_bi_node(operation, left, right):
    nd = Node(operation)
    nd.setl(left)
    nd.setr(right)
    return nd


def p_operand(term):
    assert isinstance(term, list)
    curr = 1
    ts = []
    t = []
    op = ''
    met = False
    if term[0].type == 'minus':
        op += '-'
    elif term[0].type == 'not':
        op += '!'
    if term[1].type == 'left-paren' and term[-1].type == 'right-paren':
        tmp = p_expr(term[2:-1])
        return [create_bi_node(op, None, tmp[0]), tmp[1]]
    else:
        tmp = p_expr(term[1:])
        return [create_bi_node(op, None, tmp[0]), tmp[1]]


def make_mult_node(terms, operation):
    if len(terms) == 1:
        return p_operand(terms[0])
    elif len(terms) == 2:
        return [create_bi_node(operation, p_operand(terms[0]), p_operand(terms[1])), '']
    # TODO: внимательно !


def p_mult(term):
    assert isinstance(term, list)
    curr = 0
    ts = []
    t = []
    op = ''
    met = False
    while curr < len(term) and term[curr].type != 'right-paren':
        if not met:
            if term[curr].type == 'left-paren':
                curr += 1
                t.append(p_expr(term))
            elif term[curr].type == 'mul':
                op += '*'
                ts.append(t)
                t = []
                met = True
            elif term[curr].type == 'div':
                op += '/'
                ts.append(t)
                t = []
                met = True
            elif term[curr].type == 'mod':
                op += '%'
                ts.append(t)
                t = []
                met = True
            else:
                t.append(term[curr])
        else:
            t.append(term[curr])
        curr += 1
    ts.append(t)
    return make_mult_node(ts, op)


def make_addit_node(terms, operation):
    if len(terms) == 1:
        return p_mult(terms[0])
    elif len(terms) == 2:
        return [create_bi_node(operation, p_mult(terms[0]), p_mult(terms[1])), '']
    # TODO: внимательно !


def p_addit(term):
    assert isinstance(term, list)
    curr = 0
    ts = []
    t = []
    op = ''
    met = False
    while curr < len(term) and term[curr].type != 'right-paren':
        if not met:
            if term[curr].type == 'left-paren':
                curr += 1
                t.append(p_expr(term))
            elif term[curr].type == 'plus' and curr != 0:
                op += '+'
                ts.append(t)
                t = []
                met = True
            elif term[curr].type == 'minus' and curr != 0:
                op += '-'
                ts.append(t)
                t = []
                met = True
            else:
                t.append(term[curr])
        else:
            t.append(term[curr])
        curr += 1
    ts.append(t)
    return make_addit_node(ts, op)


def make_comp_node(terms, operation):
    assert isinstance(terms, list)
    if len(terms) == 1:
        return p_addit(terms[0])
    elif len(terms) == 2:
        return [create_bi_node(operation, p_addit(terms[0]), p_addit(terms[1])), 'int']


def p_comp(term):
    assert isinstance(term, list)
    curr = 0
    ts = []
    t = []
    op = ''
    met = False
    while curr < len(term) and term[curr].type != 'right-paren':
        if not met:
            if term[curr].type == 'left-paren':
                curr += 1
                t.append(p_expr(term))
            elif term[curr].type == 'left-chev':
                op += '<'
                if term[curr + 1].type == 'equal':
                    op += '='
                    curr += 1
                ts.append(t)
                t = []
                met = True
            elif term[curr].type == 'right-chev':
                op += '>'
                if term[curr + 1].type == 'equal':
                    op += '='
                    curr += 1
                ts.append(t)
                t = []
                met = True
            else:
                t.append(term[curr])
        else:
            t.append(term[curr])
        curr += 1
    ts.append(t)
    return make_comp_node(ts, op)


def make_equal_node(terms, operation):
    assert isinstance(terms, list)
    if len(terms) == 1:
        return p_comp(terms[0])
    elif len(terms) == 2:
        return [create_bi_node(operation, p_comp(terms[0]), p_comp(terms[1])), 'int']


def p_equal(term):
    assert isinstance(term, list)
    curr = 0
    ts = []
    t = []
    op = ''
    met = False
    while curr < len(term) and term[curr].type != 'right-paren':
        if not met:
            if term[curr].type == 'left-paren':
                curr += 1
                t.append(p_expr(term))
            elif term[curr].type == 'exclam':
                if term[curr + 1].type == 'equal':
                    op += '!='
                    curr += 1
                    ts.append(t)
                    t = []
                    met = True
                else:
                    pass  # некорректный оператор
            elif term[curr].type == 'equal':
                op += '=='
                ts.append(t)
                t = []
                met = True
            else:
                t.append(term[curr])
        else:
            t.append(term[curr])
        curr += 1
    ts.append(t)
    return make_equal_node(ts, op)


def make_and_node(terms):
    assert isinstance(terms, list)
    if len(terms) == 1:
        return p_equal(terms[0])
    elif len(terms) == 2:
        return [create_bi_node('&&', p_equal(terms[0]), p_equal(terms[1])), 'int']


def p_and(term):
    assert isinstance(term, list)
    curr = 0
    ts = []
    t = []
    met = False
    while curr < len(term) and term[curr].type != 'right-paren':
        if not met:
            if term[curr].type == 'left-paren':
                curr += 1
                t.append(p_expr(term))
            elif term[curr].type == 'and':
                ts.append(t)
                t = []
                met = True
            else:
                t.append(term[curr])
        else:
            t.append(term[curr])
        curr += 1
    ts.append(t)
    return make_and_node(ts)


def make_or_node(terms):
    assert isinstance(terms, list)
    if len(terms) == 1:
        return p_and(terms[0])
    elif len(terms) == 2:
        return [create_bi_node('||', p_and(terms[0]), p_and(terms[1])), 'int']


def p_or(tokens):
    assert isinstance(tokens, list)
    curr = 0
    ts = []
    t = []
    met = False
    while curr < len(tokens) and tokens[curr].type != 'right-paren':
        if not met:
            if tokens[curr].type == 'left-paren':
                curr += 1
                t.append(p_expr(tokens))
            elif tokens[curr].type == 'or':
                ts.append(t)
                t = []
                met = True
            else:
                t.append(tokens[curr])
        else:
            t.append(tokens[curr])
        curr += 1
    ts.append(t)
    return make_or_node(ts)


def p_expr(tokens):
    """
    Возвращает список из узла и типа (на случай, если нужно установить тип параметра)
    :param tokens:
    :return: list
    """
    assert isinstance(tokens, list)
    if len(tokens) == 1:
        return p_atom(tokens[0])
    else:
        return p_or(tokens)


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
