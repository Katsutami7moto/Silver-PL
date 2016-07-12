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

    def get_type(self):
        if self.rchild and not self.lchild:
            return self.rchild.get_type()
        elif self.lchild and self.rchild:
            if self.type in {'+', '-', '*', '/', '%'}:
                if self.lchild.get_type() == 'double' or self.rchild.get_type() == 'double':
                    return 'double'
                elif self.lchild.get_type() == self.rchild.get_type():
                    return self.rchild.get_type()
            elif self.type in {'<', '>', '<=', '>=', '!=', '==', '!', '||', '&&'}:
                return 'int'
        else:
            if self.type == 'ident':
                return symbol_table['names'][self.value][0]
            else:
                return self.type


nodes = []
instructions_current = 0
expr_current = 0
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
    "string",
    "ident"
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


def build_expr_tree(tokens):
    """
    :rtype: Node
    :type tokens: list
    """
    binary = {'mul': '*', 'div': '/', 'mod': '%', 'plus': '+', 'minus': '-', 'and': '&&', 'or': '||'}
    unary = {'not': '!', '-u': '-'}
    global expr_current
    while expr_current < len(tokens):
        if tokens[expr_current].type in binary:
            nd = Node(binary[tokens[expr_current].type])
            expr_current += 1
            nd.setr(build_expr_tree(tokens))
            nd.setl(build_expr_tree(tokens))
            return nd
        elif tokens[expr_current].type in {'<', '>', '<=', '>=', '!='}:
            nd = Node(tokens[expr_current].type)
            expr_current += 1
            nd.setr(build_expr_tree(tokens))
            nd.setl(build_expr_tree(tokens))
            return nd
        elif tokens[expr_current].type == '=':
            nd = Node('==')
            expr_current += 1
            nd.setr(build_expr_tree(tokens))
            nd.setl(build_expr_tree(tokens))
            return nd
        elif tokens[expr_current].type in unary:
            nd = Node(unary[tokens[expr_current].type])
            expr_current += 1
            nd.setr(build_expr_tree(tokens))
            return nd
        else:
            tmp = tokens[expr_current]
            expr_current += 1
            return p_atom(tmp)


def p_expr(tokens):
    """
    :rtype: list
    :type tokens: list
    """

    op_stack = []
    rpn = []  # обратная польская нотация (постфиксная)

    prec = {
        'not': 7,
        '-u': 7,
        'mul': 6,
        'div': 6,
        'mod': 6,
        'plus': 5,
        'minus': 5,
        '<': 4,
        '>': 4,
        '<=': 4,
        '>=': 4,
        '=': 3,
        '!=': 3,
        'and': 2,
        'or': 1,
        'left-paren': 0,
        '': 99
    }
    right = {'-u', 'not'}
    isdouble = False

    def getprec(op):
        return prec.get(op, -1)

    last = ''
    for token in tokens:
        assert isinstance(token, lexer.Token)

        if not token:
            continue

        if token.type == 'minus' and getprec(last) >= 0:
            token.type = '-u'
        if token.type in {'int', 'double', 'ident'}:
            if last in {'int', 'double', 'ident', 'right-paren'}:
                raise Exception, "Отсутствует оператор между значениями"
            if token.type == 'double' and not isdouble:
                isdouble = True
            rpn.append(token)
        elif token.type == 'left-paren':
            op_stack.append(token)
        elif token.type == 'right-paren':
            while op_stack[-1].type != 'left-paren':
                tmp = op_stack.pop()
                rpn.append(tmp)
            if op_stack.pop().type != 'left-paren':
                raise Exception, "Не хватает '('"
        elif getprec(token.type) > 0:
            prc = getprec(token.type)
            if token.type in right:
                while op_stack and prc < getprec(op_stack[-1].type):
                    rpn.append(op_stack.pop())
            else:
                while op_stack and prc <= getprec(op_stack[-1].type):
                    rpn.append(op_stack.pop())
            op_stack.append(token)
        else:
            raise Exception, "Неизвестный токен: \"%s\"" % token.type
        last = token.type
    while op_stack:
        rpn.append(op_stack.pop())
    rpn.reverse()

    return rpn


def p_def(term, t):
    assert isinstance(term, list)
    global expr_current
    if term[0].type == 'ident' and term[1].type == '=':
        nd = Node([t, ''], term[0].value)
        if nd.value not in symbol_table['names']:
            ndr = term[2:]
            if len(ndr) == 0:
                raise Exception, "Отсутствует параметр"
            else:
                if len(ndr) == 1:
                    par = p_atom(ndr[0])
                else:
                    par = build_expr_tree(p_expr(ndr))
                    expr_current = 0
                symbol_table['names'][nd.value] = [par.get_type(), t]
                nd.setr(par)
                nd.type[1] = nd.get_type()
                return nd
        else:
            raise Exception, "Попытка определения уже определённой переменной"
    else:
        raise Exception, "Некорректное использование оператора " + t


def p_var(term):
    return p_def(term, 'var')


def p_const(term):
    return p_def(term, 'const')


def p_sem(kot):
    assert isinstance(kot, lexer.Token)
    global instructions_current
    if kot.type in sems:
        term = []
        instructions_current += 1
        while tokens_list[instructions_current].type != 'semicolon':
            term.append(tokens_list[instructions_current])
            instructions_current += 1
        instructions_current += 1
        func = 'p_' + kot.type + '(term)'
        nodes.append(eval(func))


def p_instructions():
    p_sem(tokens_list[instructions_current])
    # p_curl(tokens_list[current])
    # p_curl_sem(tokens_list[current])
    # p_curl_plus(tokens_list[current])


def p_block():
    while instructions_current < len(tokens_list) and tokens_list[instructions_current].type != 'right-curl':
        p_instructions()


def parsing(code):
    assert isinstance(code, list)
    global tokens_list
    tokens_list = lexer.lexing(code)
    if tokens_list:
        p_block()
    return nodes
