# coding=utf-8

import lexer


class Node:
    def __init__(self, t, v=None):
        self.type = t
        self.value = v

        self.lchild = None
        self.rchild = None

    def setl(self, obj):
        self.lchild = obj

    def setr(self, obj):
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
    "printline",
    "input",
    "return"
}
curls = {
    "loop",
    "do",
    "else"
}
d_curls = {
    "while",
    "if",
    "elif"
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
            raise NameError, "Попытка обращения к неопределённой переменной"
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
                rpn.append(op_stack.pop())
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
    if len(term) > 2:
        if term[0].type == 'ident' and term[1].type == '=':
            if term[0].value not in symbol_table['names']:
                ndr = term[2:]
                if len(ndr) == 1:
                    par = p_atom(ndr[0])
                else:
                    par = build_expr_tree(p_expr(ndr))
                    expr_current = 0
                symbol_table['names'][term[0].value] = [par.get_type(), t]
                nd = Node([t, par.get_type()], term[0].value)
                nd.setr(par)
                return nd
            else:
                raise Exception, "Попытка определения уже определённой переменной"
        else:
            raise Exception, "Некорректное использование оператора " + t
    else:
        raise Exception, "Отсутствует параметр"


def p_var(term):
    return p_def(term, 'var')


def p_const(term):
    return p_def(term, 'const')


def p_let(term):
    assert isinstance(term, list)
    global expr_current
    if len(term) > 2:
        if term[0].type == 'ident' and term[1].type == '=':
            namae = term[0].value
            if namae in symbol_table['names']:
                if symbol_table['names'][namae][1] == 'var':
                    ndr = term[2:]
                    if len(ndr) == 1:
                        par = p_atom(ndr[0])
                    else:
                        par = build_expr_tree(p_expr(ndr))
                        expr_current = 0
                    if par.get_type() == symbol_table['names'][namae][0]\
                            or (par.get_type() == 'int' and symbol_table['names'][namae][0] == 'double'):
                        nd = Node(['let', par.get_type()], namae)
                        nd.setr(par)
                        return nd
                    else:
                        raise Exception, "Попытка присвоения значения некорректного типа"
                elif symbol_table['names'][namae][1] == 'const':
                    raise Exception, "Попытка изменить значение константы"
                else:
                    raise Exception, "Error"
            else:
                raise Exception, "Попытка изменения значения не определявшейся переменной"
        else:
            raise Exception, "Некорректное использование оператора присваивания"
    else:
        raise Exception, "Отсутствует параметр"


def p_print(term):
    assert isinstance(term, list)
    global expr_current
    if len(term) > 0:
        if len(term) == 1:
            par = p_atom(term[0])
        else:
            par = build_expr_tree(p_expr(term))
            expr_current = 0
        nd = Node(['print', par.get_type()])
        nd.setr(par)
        return nd
    else:
        raise Exception, "Отсутствует параметр"


def p_printline(term):
    assert isinstance(term, list)
    global expr_current
    if len(term) > 0:
        if len(term) == 1:
            par = p_atom(term[0])
        else:
            par = build_expr_tree(p_expr(term))
            expr_current = 0
        nd = Node(['printline', par.get_type()])
        nd.setr(par)
        return nd
    else:
        nd = Node(['printline', 'line'])
        return nd


def p_input(term):
    assert isinstance(term, list)
    if len(term) == 2:
        if term[0].value in {'int', 'double'} and term[1].type == 'ident':
            if term[1].value not in symbol_table['names']:
                symbol_table['names'][term[1].value] = [term[0].value, 'var']
                nd = Node(['input', term[0].value, 'new'], term[1].value)
                return nd
            else:
                if symbol_table['names'][term[1].value][0] != term[0].value:
                    raise Exception, "Неверно указан тип вводимого значения"
                nd = Node(['input', term[0].value], term[1].value)
                return nd
        else:
            raise Exception, "Некорректное использование оператора ввода"
    else:
        raise Exception, "Некорректное использование оператора ввода"


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


def p_loop():
    return Node(['loop'])


def p_curl(kot):
    assert isinstance(kot, lexer.Token)
    global instructions_current
    if kot.type in curls:
        instructions_current += 1
        if tokens_list[instructions_current].type == 'left-curl':
            instructions_current += 1
            tmp = len(nodes)
            p_block()
            instructions_current += 1
            ltmp = []
            while len(nodes) != tmp:
                ltmp.append(nodes.pop())
            ltmp.reverse()

            func = 'p_' + kot.type + '()'
            nd = eval(func)
            nd.setr(ltmp)
            nodes.append(nd)
        else:
            raise Exception, "Отсутствует открывающая фигурная скобка"


def p_while(term):
    assert isinstance(term, list)
    global expr_current
    if len(term) > 0:
        if len(term) == 1:
            par = p_atom(term[0])
        else:
            par = build_expr_tree(p_expr(term))
            expr_current = 0
        nd = Node(['while'])
        nd.setl(par)
        return nd
    else:
        raise Exception, "Отсутствует параметр"


def p_d_curl(kot):
    assert isinstance(kot, lexer.Token)
    global instructions_current
    if kot.type in d_curls or kot.type == 'type':
        instructions_current += 1
        term = []
        while tokens_list[instructions_current].type != 'left-curl':
            term.append(tokens_list[instructions_current])
            instructions_current += 1

        instructions_current += 1
        tmp = len(nodes)
        p_block()
        instructions_current += 1
        ltmp = []
        while len(nodes) != tmp:
            ltmp.append(nodes.pop())
        ltmp.reverse()

        func = 'p_' + kot.type + '(term)'
        nd = eval(func)
        nd.setr(ltmp)
        nodes.append(nd)


def p_instructions():
    if tokens_list[instructions_current].type in sems:
        p_sem(tokens_list[instructions_current])
    elif tokens_list[instructions_current].type in curls:
        p_curl(tokens_list[instructions_current])
    elif tokens_list[instructions_current].type in d_curls or tokens_list[instructions_current].type == 'type':
        p_d_curl(tokens_list[instructions_current])


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
