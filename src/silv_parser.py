from src import lexer


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
            if isinstance(self.type, list):
                return self.type[1][0]
            else:
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


class Module:
    def __init__(self, n, i, decls, defs):
        # type: (str, list, list, list) -> object
        self.name = n
        self.imports = i
        self.declarations = decls
        self.definitions = defs


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
    "return",
    "break",
    "continue"
}
curls = {
    "loop",
    "do",
    "else"
}
d_curls = {
    "while",
    "until",
    "if",
    "elif"
}
types = {
    "int",
    "double"
}
symbol_table = dict(names=dict())
in_function = False  # TODO: уточнить работу и переименовать в 'in_block'
current_scope = dict()  # TODO: уточнить работу


def cur_tok(inc: int = 0) -> lexer.Token:
    return tokens_list[instructions_current + inc]


def cur_tok_is(typename: str) -> bool:
    return cur_tok().type == typename


def cur_tok_not(typename: str) -> bool:
    return cur_tok().type != typename


def token_error(msg: str, token: lexer.Token = cur_tok()):
    raise Exception(msg + " %d:%d" % (token.line, token.symbol))


def p_atom(token: lexer.Token) -> Node:
    tmp = None
    if token.type in types:
        tmp = Node(token.type, token.value)
    elif token.type == "True":
        tmp = Node("int", "1")
    elif token.type == "False":
        tmp = Node("int", "0")
    elif token.type == 'ident':
        if in_function and token.value in current_scope:
            tmp = Node(current_scope[token.value], token.value)
        else:
            if token.value in symbol_table['names']:
                tmp = Node(symbol_table['names'][token.value][0], token.value)
            else:
                token_error("Попытка обращения к неопределённой переменной", token)
    else:
        token_error("Некорректный параметр", token)
    return tmp


def build_expr_tree(tokens: list) -> Node:
    binary = {'asterisk': '*', 'slash': '/', 'percent': '%', 'plus': '+', 'minus': '-', 'and': '&&', 'or': '||',
              'comma': ',', 'left-chev': '<', 'right-chev': '>', 'less-equal': '<=', 'more-equal': '>=',
              'is-equal': '==', 'not-equal': '!='}
    unary = {'not': '!', '-u': '-'}
    global expr_current
    while expr_current < len(tokens):
        if tokens[expr_current].type[0] == 'call':
            nd = Node(tokens[expr_current].type, tokens[expr_current].value)
            expr_current += 1
            nd.setr(build_expr_tree(tokens))
            return nd
        elif tokens[expr_current].type in binary:
            nd = Node(binary[tokens[expr_current].type])
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


def p_expr(tokens: list) -> list:
    op_stack = []
    rpn = []  # обратная польская нотация (постфиксная)

    prec = {
        'call': 9,
        'not': 8,
        '-u': 8,
        'asterisk': 7,
        'slash': 7,
        'percent': 7,
        'plus': 6,
        'minus': 6,
        'left-chev': 5,
        'right-chev': 5,
        'less-equal': 5,
        'more-equal': 5,
        'is-equal': 4,
        'not-equal': 4,
        'and': 3,
        'or': 2,
        'comma': 1,
        'left-paren': 0,
        '': 99
    }
    right = {'-u', 'not'}

    def getprec(op):
        if isinstance(op, list):
            return prec.get(op[0], -1)
        else:
            return prec.get(op, -1)

    last = lexer.Token('', 0, 0, '')
    for token in tokens:
        assert isinstance(token, lexer.Token)
        if not token:
            continue
        if token.type == 'minus' and getprec(last.type) >= 0:
            token.type = '-u'
        if token.type in {'int', 'double', 'ident'}:
            if last.type in {'int', 'double', 'ident', 'right-paren'}:
                token_error("Отсутствует оператор между значениями", token)
            rpn.append(token)
        elif token.type == 'left-paren':
            if last.type == 'ident':
                op_stack.append(
                    lexer.Token(['call', symbol_table['names'][last.value]], last.line, last.symbol, last.value))
                rpn.pop()
            op_stack.append(token)
        elif token.type == 'right-paren':
            while op_stack[-1].type != 'left-paren':
                rpn.append(op_stack.pop())
            tmp = op_stack.pop()
            if tmp.type != 'left-paren':
                token_error("Не хватает '('", token)
            elif isinstance(tmp.type, list):
                rpn.append(tmp)
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
            token_error("Неизвестный токен", token)
        last = token
    while op_stack:
        rpn.append(op_stack.pop())
    rpn.reverse()
    return rpn


# def p_name(term, t):
#     # type: (list) -> Node
#     global expr_current
#     if len(term) > 2:
#         if term[0].type == 'ident' and term[1].type == 'equal':
#             if term[0].value not in symbol_table['names']:
#                 ndr = term[2:]
#                 if len(ndr) == 1:
#                     par = p_atom(ndr[0])
#                 else:
#                     par = build_expr_tree(p_expr(ndr))
#                     expr_current = 0
#                 symbol_table['names'][term[0].value] = [par.get_type(), t]
#                 nd = Node([t, par.get_type()], term[0].value)
#                 nd.setr(par)
#                 return nd
#             else:
#                 raise Exception, "Попытка определения уже определённой переменной %d:%d" % (
#                     term[0].line, term[0].symbol)
#         else:
#             raise Exception, "Некорректное использование оператора %s %d:%d" % (t, term[0].line, term[0].symbol)
#     else:
#         raise Exception, "Отсутствует параметр %d:%d" % (term[0].line, term[0].symbol)


def p_name(term, t):
    global expr_current
    if len(term) > 2:
        if term[0].type == 'ident':
            if term[0].value not in symbol_table['names']:
                if term[1].type == 'equal':
                    if len(term) == 3 and term[2].type in types:
                        par = p_atom(term[2])
                        symbol_table['names'][term[0].value] = [par.get_type(), t]
                        nd = Node([t, par.get_type()], term[0].value)
                        nd.setr(par)
                        return nd
                    else:
                        pass  # место для 'new' (заменить на elif)
                elif term[1].type == 'colon':
                    if term[2].type == 'ident':
                        if term[3].type == 'equal':
                            ndr = term[4:]
                            par = build_expr_tree(p_expr(ndr))
                            expr_current = 0
                            if par.get_type() == term[2].value:
                                symbol_table['names'][term[0].value] = [par.get_type(), t]
                                nd = Node([t, par.get_type()], term[0].value)
                                nd.setr(par)
                                return nd
                            else:
                                token_error("Несоответствие типа параметра заявленному", term[0])
                        else:
                            token_error("Отсутствует знак '='", term[0])
                    else:
                        token_error("Отсутствует имя типа", term[0])
                else:
                    token_error("Отсутствует знак '='", term[0])
            else:
                token_error("Попытка определения уже определённой переменной", term[0])
        else:
            token_error("Отсутствует идентификатор", term[0])
    else:
        token_error("Отсутствует параметр", term[0])


def p_var(term: list) -> Node:
    return p_name(term, 'var')


def p_let(term: list) -> Node:
    return p_name(term, 'let')


def p_mod(term: list) -> Node:
    global expr_current
    if len(term) > 2:
        if term[0].type == 'ident' and term[1].type in {'equal', 'self-inc', 'self-dec', 'self-mul', 'self-div',
                                                        'self-mod'}:
            namae = term[0].value
            if namae in symbol_table['names']:
                if symbol_table['names'][namae][1] == 'var':
                    ndr = term[2:]
                    if len(ndr) == 1:
                        par = p_atom(ndr[0])
                    else:
                        par = build_expr_tree(p_expr(ndr))
                        expr_current = 0
                    if par.get_type() == symbol_table['names'][namae][0] \
                            or (par.get_type() == 'int' and symbol_table['names'][namae][0] == 'double'):
                        nd = Node(['mod', term[1].type], namae)
                        nd.setr(par)
                        return nd
                    else:
                        token_error("Попытка присвоения значения некорректного типа", term[0])
                else:
                    token_error("Обращение не к переменной", term[0])
            else:
                token_error("Попытка изменения значения не определявшейся переменной", term[0])
        else:
            token_error("Некорректное использование оператора присваивания", term[0])
    else:
        token_error("Отсутствует параметр", term[0])


def p_print(term: list) -> Node:
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
        token_error("Отсутствует параметр", term[0])


def p_printline(term: list) -> Node:
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


def p_input(term: list) -> Node:
    if len(term) == 2:
        if term[0].value in {'int', 'double'} and term[1].type == 'ident':
            if term[1].value not in symbol_table['names']:
                symbol_table['names'][term[1].value] = [term[0].value, 'var']
                nd = Node(['input', term[0].value, 'new'], term[1].value)
                return nd
            else:
                if symbol_table['names'][term[1].value][0] != term[0].value:
                    token_error("Неверно указан тип вводимого значения", term[0])
                nd = Node(['input', term[0].value], term[1].value)
                return nd
        else:
            token_error("Некорректное использование оператора ввода", term[0])
    else:
        token_error("Некорректное использование оператора ввода", term[0])


def p_return(term: list) -> Node:
    global expr_current
    if len(term) >= 1:
        if len(term) == 1:
            par = p_atom(term[0])
        else:
            par = build_expr_tree(p_expr(term))
            expr_current = 0
        nd = Node(['return'])
        nd.setr(par)
        return nd
    else:
        token_error("Отсутствует возвращаемое значение", term[0])


def p_sem(kot):
    assert isinstance(kot, lexer.Token)
    global instructions_current
    term = []
    instructions_current += 1
    while cur_tok_not('semicolon'):
        term.append(cur_tok())
        instructions_current += 1
    instructions_current += 1
    if kot.type in {'break', 'continue'}:
        nodes.append(Node([kot.type]))
    else:
        func = 'p_' + kot.type + '(term)'
        nodes.append(eval(func))


def p_curl(kot):
    assert isinstance(kot, lexer.Token)
    global instructions_current, expr_current
    instructions_current += 1
    if cur_tok_is('left-curl'):
        term = []
        instructions_current += 1
        tmp = len(nodes)
        p_block()
        instructions_current += 1

        if kot.type == 'do':
            if cur_tok_is('while'):
                instructions_current += 1
                while cur_tok_not('semicolon'):
                    term.append(cur_tok())
                    instructions_current += 1
                instructions_current += 1
            elif cur_tok_is('until'):
                term.append(lexer.Token('not', 0, 0))
                term.append(lexer.Token('left-paren', 0, 0))
                instructions_current += 1
                while cur_tok_not('semicolon'):
                    term.append(cur_tok())
                    instructions_current += 1
                term.append(lexer.Token('right-paren', 0, 0))
                instructions_current += 1
            else:
                token_error("Некорректное использование оператора do (нет while или until)", kot)

        ltmp = []
        while len(nodes) != tmp:
            ltmp.append(nodes.pop())
        ltmp.reverse()

        nd = Node([kot.type])
        if kot.type == 'do':
            par = None
            if len(term) > 0:
                if len(term) == 1:
                    par = p_atom(term[0])
                else:
                    par = build_expr_tree(p_expr(term))
                    expr_current = 0
            else:
                token_error("Отсутствует параметр", kot)
            nd.setl(par)
        nd.setr(ltmp)
        nodes.append(nd)
    else:
        token_error("Отсутствует открывающая фигурная скобка", kot)


def p_while(term: list) -> Node:
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
        token_error("Отсутствует параметр", term[0])


def p_until(term: list) -> Node:
    global expr_current
    if len(term) > 0:
        if len(term) == 1:
            par = p_atom(term[0])
        else:
            par = build_expr_tree(p_expr(term))
            expr_current = 0
        nd = Node(['until'])
        nd.setl(par)
        return nd
    else:
        token_error("Отсутствует параметр", term[0])


def p_if(term: list) -> Node:
    global expr_current
    if len(term) > 0:
        if len(term) == 1:
            par = p_atom(term[0])
        else:
            par = build_expr_tree(p_expr(term))
            expr_current = 0
        nd = Node(['if'])
        nd.setl(par)
        return nd
    else:
        token_error("Отсутствует параметр", term[0])


def p_elif(term: list) -> Node:
    global expr_current
    if len(term) > 0:
        if len(term) == 1:
            par = p_atom(term[0])
        else:
            par = build_expr_tree(p_expr(term))
            expr_current = 0
        nd = Node(['elif'])
        nd.setl(par)
        return nd
    else:
        token_error("Отсутствует параметр", term[0])


def p_d_curl(kot):
    assert isinstance(kot, lexer.Token)
    global instructions_current
    instructions_current += 1
    term = []
    while cur_tok_not('left-curl'):
        term.append(cur_tok())
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


def p_func(kot):
    assert isinstance(kot, lexer.Token)
    ftype = kot.value
    term = []
    global instructions_current, symbol_table, in_function, current_scope
    start = instructions_current
    instructions_current += 1
    if cur_tok_is('ident'):
        fname = cur_tok().value
        if fname not in symbol_table['names']:
            symbol_table['names'][fname] = [ftype, 'func']
        instructions_current += 1
        if cur_tok_is('left-paren'):
            instructions_current += 1
            ltmp = []
            while cur_tok_not('right-paren'):
                if cur_tok_is('comma'):
                    term.append(',')
                    instructions_current += 1
                elif cur_tok().value in types and cur_tok(1).type == 'ident':
                    term.append(cur_tok().value)
                    term.append(cur_tok(1).value)
                    current_scope[cur_tok(1).value] = cur_tok().value
                    instructions_current += 2
                else:
                    token_error("Некорректный список формальных аргументов функции")
            instructions_current += 1
            if cur_tok_is('left-curl'):
                instructions_current += 1
                tmp = len(nodes)
                in_function = True
                p_block()
                in_function = False
                current_scope = dict()
                instructions_current += 1
                stop = instructions_current
                instructions_current = start
                del tokens_list[start:stop]
                while len(nodes) != tmp:
                    ltmp.append(nodes.pop())
                ltmp.reverse()
            else:
                token_error("Отсутствует тело функции")
            nd = Node(['func', ftype], fname)
            nd.setl(term)
            nd.setr(ltmp)
            nodes.append(nd)
        else:
            token_error("После имени функции должны быть круглые скобки")
    else:
        token_error("Некорректное объявление функции")


def p_instructions():
    if cur_tok().type in sems:
        p_sem(cur_tok())
    elif cur_tok().type in curls:
        p_curl(cur_tok())
    elif cur_tok().type in d_curls:
        p_d_curl(cur_tok())
    elif cur_tok().type == 'def':
        pass


# def p_block():
#     while instructions_current < len(tokens_list) and tokens_list[instructions_current].type != 'right-curl':
#         p_instructions()
#
#
# def p_fdefs():
#     global instructions_current
#     while instructions_current < len(tokens_list):
#         if tokens_list[instructions_current].value in types and tokens_list[instructions_current - 1].type != 'input':
#             p_func(tokens_list[instructions_current])
#         else:
#             instructions_current += 1
#     instructions_current = 0


def p_definitions():
    """
    :rtype: list
    """
    pass


def p_declarations():
    """
    :rtype: list
    """
    pass


def p_imports():
    """
    :rtype: list
    """
    pass


def p_module():
    global instructions_current
    instructions_current += 1
    if cur_tok_is('ident'):
        name = cur_tok().value
        instructions_current += 1
        if cur_tok_is('left-curl'):
            instructions_current += 1
            mstart = instructions_current
            imps = p_imports()
            declars = p_declarations()
            instructions_current = mstart
            defins = p_definitions()
            return Module(name, imps, declars, defins)


def p_start():
    modules = []
    while instructions_current < len(tokens_list):
        if cur_tok_is('module'):
            modules.append(p_module())
    return modules


def m_rearrange(mods: list) -> list:
    pass


def parsing(code: list) -> list:
    # type: (list) -> list
    global tokens_list
    tokens_list = lexer.lexing(code)
    if tokens_list:
        return m_rearrange(p_start())
