# coding=utf-8


# Данная программа:
# - парсит регэксп в дерево
# - строит по дереву ДКА без построения НКА
# - по получившемуся ДКА парсит входной текст
# Регэксп записывать в виде: "(регэксп)#", как в примерах ниже.
# Входной текст записывать в кавычках.
# ? - 0 или 1, * - 0 или много, + - 1 или много
# . - любой символ (можно итерировать), \\ - экранирование
#
# Работает с ограниченным набором регулярок (специально для транслятора) !!!


r_ident = "((a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)" \
          "(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|0|1|2|3|4|5|6|7|8|9|\\_)*)#"
r_int = "(0|(1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*)#"
r_float = "(0|(1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*\\.(0|1|2|3|4|5|6|7|8|9)+)#"
r_string = "(\".+\")#"

current = 0
curposnum = 1
hashposnum = 0
followpostable = {}
anykeytable = set()
dfa = {}


def relaunch():
    global current, curposnum, hashposnum, followpostable, anykeytable, dfa
    current = 0
    curposnum = 1
    hashposnum = 0
    followpostable = {}
    anykeytable = set()
    dfa = {}


def closing():
    global current, curposnum, hashposnum, followpostable, anykeytable, dfa
    del current
    del curposnum
    del hashposnum
    del followpostable
    del anykeytable
    del dfa


class Node:
    def __init__(self, symbol, scr=None, ak=None):
        if isinstance(self, BinaryNode):
            self.lchild = None
            self.rchild = None
        elif isinstance(self, UnaryNode):
            self.child = None
        elif isinstance(self, Leaf):
            pass
        self.screened = scr
        self.anykey = ak
        self.data = symbol
        self.position = None
        self.n = False
        self.f = set()
        self.l = set()

    def nullable(self):
        if self.data == "|" and not self.screened:
            self.n = self.lchild.n or self.rchild.n
        elif self.data == "." and not self.screened:
            self.n = self.lchild.n and self.rchild.n
        elif (self.data == "*" or self.data == "?") and not self.screened:
            self.n = True
        elif self.data == "+" and not self.screened:
            self.n = False
        else:
            self.n = False

    def firstpos(self):
        if self.data == "|" and not self.screened:
            self.f.update(self.lchild.f, self.rchild.f)
        elif self.data == "." and not self.screened:
            if self.lchild.n:
                self.f.update(self.lchild.f, self.rchild.f)
            else:
                self.f.update(self.lchild.f)
        elif (self.data == "*" or self.data == "+" or self.data == "?") and not self.screened:
            self.f.update(self.child.f)
        else:
            self.f.update({self.position})

    def lastpos(self):
        if self.data == "|" and not self.screened:
            self.l.update(self.lchild.l | self.rchild.l)
        elif self.data == "." and not self.screened:
            if self.rchild.n:
                self.l.update(self.lchild.l | self.rchild.l)
            else:
                self.l.update(self.rchild.l)
        elif (self.data == "*" or self.data == "+" or self.data == "?") and not self.screened:
            self.l.update(self.child.l)
        else:
            self.l.update({self.position})

    def followpos(self):
        global followpostable
        if self.getdata() == '.' and not self.screened:
            for one in self.lchild.l:
                assert isinstance(followpostable, dict)
                followpostable[one][1].update(self.rchild.f)
        elif (self.getdata() == '*' or self.getdata() == '+') and not self.screened:
            for one in self.child.l:
                assert isinstance(followpostable, dict)
                followpostable[one][1].update(self.child.f)

    def getdata(self):
        return self.data


class BinaryNode(Node):
    def setl(self, obj):
        self.lchild = obj

    def setr(self, obj):
        self.rchild = obj

    def postorderwalk_n(self):
        self.lchild.postorderwalk_n()
        self.rchild.postorderwalk_n()
        self.nullable()

    def postorderwalk_f(self):
        self.lchild.postorderwalk_f()
        self.rchild.postorderwalk_f()
        self.firstpos()

    def postorderwalk_l(self):
        self.lchild.postorderwalk_l()
        self.rchild.postorderwalk_l()
        self.lastpos()

    def postorderwalk_p(self):
        self.lchild.postorderwalk_p()
        self.rchild.postorderwalk_p()

    def postorderwalk_w(self):
        self.lchild.postorderwalk_w()
        self.rchild.postorderwalk_w()
        self.followpos()


class UnaryNode(Node):
    def setc(self, obj):
        self.child = obj

    def postorderwalk_n(self):
        self.child.postorderwalk_n()
        self.nullable()

    def postorderwalk_f(self):
        self.child.postorderwalk_f()
        self.firstpos()

    def postorderwalk_l(self):
        self.child.postorderwalk_l()
        self.lastpos()

    def postorderwalk_p(self):
        self.child.postorderwalk_p()

    def postorderwalk_w(self):
        self.child.postorderwalk_w()
        self.followpos()


class Leaf(Node):
    def setp(self):
        global curposnum, followpostable, anykeytable
        self.position = curposnum
        followpostable[curposnum] = [self.data, set()]
        if self.anykey:
            assert isinstance(anykeytable, set)
            anykeytable.add(self.position)
        curposnum += 1

    def postorderwalk_n(self):
        self.nullable()

    def postorderwalk_f(self):
        self.firstpos()

    def postorderwalk_l(self):
        self.lastpos()

    def postorderwalk_p(self):
        self.setp()

    def postorderwalk_w(self):
        self.followpos()


def createbinode(symbol, leftnode, rightnode):
    nd = BinaryNode(symbol)
    nd.setl(leftnode)
    nd.setr(rightnode)
    return nd


def createunode(symbol, node):
    nd = UnaryNode(symbol)
    nd.setc(node)
    return nd


def createleaf(symbol, scrnd, ak):
    return Leaf(symbol, scrnd, ak)


def makeor(terms):
    result = makeand(terms[0])
    for one in range(1, len(terms)):
        result = createbinode('|', result, makeand(terms[one]))
    return result


def makeand(term):
    result = term[0]
    for one in range(1, len(term)):
        result = createbinode('.', result, term[one])
    return result


def parse(regular):
    global current
    terms = []
    term = []
    while current < len(regular) and regular[current] != ')':
        if regular[current] == '(':
            current += 1
            term.append(parse(regular))
        elif regular[current] == '|':
            terms.append(term)
            term = []
        elif regular[current] == '*' or regular[current] == '+' or regular[current] == '?':
            term.append(createunode(regular[current], term.pop()))
        elif regular[current] == '\\':
            current += 1
            term.append(createleaf(regular[current], True, False))
        elif regular[current] == '.':
            term.append(createleaf('', False, True))
        else:
            term.append(createleaf(regular[current], False, False))
        current += 1
    terms.append(term)
    return makeor(terms)


def calc(root):
    root.postorderwalk_p()
    global curposnum, hashposnum
    hashposnum = curposnum - 1
    root.postorderwalk_n()
    root.postorderwalk_f()
    root.postorderwalk_l()
    root.postorderwalk_w()


def dfabuild(posset):
    global dfa, followpostable, hashposnum
    if posset not in dfa:
        dfa[posset] = dict()
    for one in posset:
        if one != hashposnum:
            symbol = followpostable[one][0]
            symstate = set().union(followpostable[one][1])
            if symbol not in dfa[posset] and symstate:
                dfa[posset][symbol] = symstate
            elif not symstate:
                temp1 = anykeytable & posset  # intersection
                if any(temp1):
                    dfa[posset][1] = symstate
                del temp1
            else:
                dfa[posset][symbol].update(symstate)
    for one in dfa[posset]:
        if one != 0:
            if dfa[posset][one]:
                temp2 = frozenset().union(dfa[posset][one])
                if temp2 not in dfa:
                    dfabuild(temp2)
                del temp2


def dfareturner(stt, state, word):
    # type: (dict, set, str) -> bool
    for symbol in word:
        if symbol in stt[state]:
            state = frozenset().union(stt[state][symbol])
        elif 1 in stt[state] and stt[state][1]:
            state = frozenset().union(stt[state][1])
        else:
            return False
    return True


id_tree = parse(r_ident)
calc(id_tree)
id_state = frozenset().union(id_tree.f)
del id_tree
dfabuild(id_state)
id_dfa = dfa
relaunch()

int_tree = parse(r_int)
calc(int_tree)
int_state = frozenset().union(int_tree.f)
del int_tree
dfabuild(int_state)
int_dfa = dfa
relaunch()

float_tree = parse(r_float)
calc(float_tree)
float_state = frozenset().union(float_tree.f)
del float_tree
dfabuild(float_state)
float_dfa = dfa
relaunch()

string_tree = parse(r_string)
calc(string_tree)
string_state = frozenset().union(string_tree.f)
del string_tree
dfabuild(string_state)
string_dfa = dfa

closing()


def returner(regular, word):
    if regular == 'id':
        result = dfareturner(id_dfa, id_state, word)
    elif regular == 'i':
        result = dfareturner(int_dfa, int_state, word)
    elif regular == 'f':
        result = dfareturner(float_dfa, float_state, word)
    elif regular == 's':
        result = dfareturner(string_dfa, string_state, word)
    else:
        raise Exception, "Некорректный тип регулярного выражения"

    return result
