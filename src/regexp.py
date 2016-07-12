# coding=utf-8


# Данная программа:
# - парсит регэксп в дерево
# - строит по дереву ДКА без построения НКА
# - по получившемуся ДКА парсит входной текст
# Регэксп записывать в виде: "(регэксп)#", как в примерах ниже.
# Входной текст записывать в кавычках.


# regexp = "((ac|bc)*ad+)#"
# regexp = "((a(b|c))*c)#"
# regexp = "(1+|1*01(11|01)+)#"
# regexp = "((a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)" \
#           "(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|0|1|2|3|4|5|6|7|8|9)*)#"
# regexp = "(a*b|b*(ab+|bc))#"
# regexp = "((1?1?0)*1?)#"  # Лаба 1, задание 2
# regexp = "(2\\*2\\=1\\+1\\+1\\+1)#"
# regexp = "(\".+\")#"
# regexp = "(n..b)#"
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
        if self:
            self.lchild.postorderwalk_n()
            self.rchild.postorderwalk_n()
            self.nullable()

    def postorderwalk_f(self):
        if self:
            self.lchild.postorderwalk_f()
            self.rchild.postorderwalk_f()
            self.firstpos()

    def postorderwalk_l(self):
        if self:
            self.lchild.postorderwalk_l()
            self.rchild.postorderwalk_l()
            self.lastpos()

    def postorderwalk_p(self):
        if self:
            self.lchild.postorderwalk_p()
            self.rchild.postorderwalk_p()

    def postorderwalk_w(self):
        if self:
            self.lchild.postorderwalk_w()
            self.rchild.postorderwalk_w()
            self.followpos()


class UnaryNode(Node):
    def setc(self, obj):
        self.child = obj

    def postorderwalk_n(self):
        if self:
            self.child.postorderwalk_n()
            self.nullable()

    def postorderwalk_f(self):
        if self:
            self.child.postorderwalk_f()
            self.firstpos()

    def postorderwalk_l(self):
        if self:
            self.child.postorderwalk_l()
            self.lastpos()

    def postorderwalk_p(self):
        if self:
            self.child.postorderwalk_p()

    def postorderwalk_w(self):
        if self:
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
        if self:
            self.nullable()

    def postorderwalk_f(self):
        if self:
            self.firstpos()

    def postorderwalk_l(self):
        if self:
            self.lastpos()

    def postorderwalk_p(self):
        if self:
            self.setp()

    def postorderwalk_w(self):
        if self:
            self.followpos()


def createunode(symbol, node):
    nd = UnaryNode(symbol)
    nd.setc(node)
    return nd


def createleaf(symbol, scrnd, ak):
    nd = Leaf(symbol, scrnd, ak)
    return nd


def createbinode(symbol, leftnode, rightnode):
    nd = BinaryNode(symbol)
    nd.setl(leftnode)
    nd.setr(rightnode)
    return nd


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
            term.append(createleaf("<@>", False, True))
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
        symbol = followpostable[one][0]
        if one != hashposnum:
            symstate = set().union(followpostable[one][1])
            if symbol not in dfa[posset] and symbol != '<@>':
                dfa[posset][symbol] = symstate
            elif symbol == '<@>':
                temp = anykeytable & posset  # intersection
                if any(temp):
                    dfa[posset][1] = symstate
            else:
                dfa[posset][symbol].update(symstate)
    if hashposnum in posset:
        dfa[posset][0] = True
    else:
        dfa[posset][0] = False
    for one in dfa[posset]:
        if one != 0:
            if dfa[posset][one]:
                temp = frozenset().union(dfa[posset][one])
                if temp not in dfa:
                    dfabuild(temp)


def dfareader(stt, state, word):
    assert isinstance(word, str)
    for symbol in word:
        if symbol in stt[state]:
            state = frozenset().union(stt[state][symbol])
        elif 1 in stt[state] and stt[state][1]:
            state = frozenset().union(stt[state][1])
        else:
            print "Invalid word/expression!"
            return
    if stt[state][0]:
        print "The word fits."
        return
    else:
        print "Last terminal isn't finite!"
        return


def dfareturner(stt, state, word):
    assert isinstance(word, str)
    for symbol in word:
        if symbol in stt[state]:
            state = frozenset().union(stt[state][symbol])
        elif 1 in stt[state] and stt[state][1]:
            state = frozenset().union(stt[state][1])
        else:
            return False
    if stt[state][0]:
        return True
    else:
        return False


def returner(regular, word):
    global dfa
    tree = parse(regular)
    calc(tree)
    begin_state = frozenset().union(tree.f)
    dfabuild(begin_state)
    result = dfareturner(dfa, begin_state, word)
    relaunch()
    return result

# def unittest():
#     test = parse(regexp)
#     calc(test)
#     test.printtree(0)
#     print "Hash is at position ", hashposnum
#     print followpostable
#
#     global dfa
#     ffs = frozenset().union(test.f)
#     dfabuild(ffs)
#
#     print "========================"
#     print dfa.keys()
#     for one in dfa:
#         print "========================"
#         print dfa[one]
#
#     print "========================"
#     print
#     w = input("Enter a word: ")
#     dfareader(dfa, ffs, w)
#
#
# unittest()
