# coding=utf-8

"""
Ожидает переделки !!!
"""

# Данная программа:
# - парсит регэксп в дерево
# - строит по дереву ДКА без построения НКА
# - по получившемуся ДКА парсит входной текст
# Регэксп записывать в виде: "(регэксп)#", как в примерах ниже.
# Входной текст записывать в кавычках.


TAB = '\t'
# regexp = "((ac|bc)*ad+)#"
# regexp = "((a(b|c))*c)#"
# regexp = "(1+|1*01(11|01)+)#"
# regexp = "((a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)" \
#           "(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|0|1|2|3|4|5|6|7|8|9)*)#"
# regexp = "(a*b|b*(ab+|bc))#"
# regexp = "((1?1?0)*1?)#"  # Лаба 1, задание 2
# regexp = "(2\\*2\\=1\\+1\\+1\\+1)#"
# regexp = "(\".+\")#"
regexp = "(n..b)#"
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

    def setp(self):  # этот метод только для подкласса Leaf !!!
        if self.screened or\
                (self.data != "|" and self.data != "." and self.data != "*" and self.data != "+" and self.data != "?"):
            global curposnum, followpostable, anykeytable
            self.position = curposnum
            followpostable[curposnum] = [self.data, set()]
            if self.anykey:
                assert isinstance(anykeytable, set)
                anykeytable.add(self.position)
            curposnum += 1

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
            self.f = {self.position}  # должен быть update() !!!

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
            self.l = {self.position}  # должен быть update() !!!

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


class UnaryNode(Node):
    def setc(self, obj):
        self.child = obj

    def printtree(self, h):
        print TAB * h + self.getdata()
        if self.child:
            self.child.printtree(h + 1)

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
            self.setp()

    def postorderwalk_w(self):
        if self:
            self.child.postorderwalk_w()
            self.followpos()


class Leaf(Node):
    def printtree(self, h):
        print TAB * h + self.getdata()

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


class BinaryNode(Node):
    def setl(self, obj):
        self.lchild = obj

    def setr(self, obj):
        self.rchild = obj

    def printtree(self, h):
        if self.rchild:
            self.rchild.printtree(h + 1)

        print TAB * h + self.getdata()

        if self.lchild:
            self.lchild.printtree(h + 1)

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
            self.setp()

    def postorderwalk_w(self):
        if self:
            self.lchild.postorderwalk_w()
            self.rchild.postorderwalk_w()
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


def parse():
    global regexp, current
    terms = []
    term = []
    while current < len(regexp) and regexp[current] != ')':
        if regexp[current] == '(':
            current += 1
            term.append(parse())
        elif regexp[current] == '|':
            terms.append(term)
            term = []
        elif regexp[current] == '*' or regexp[current] == '+' or regexp[current] == '?':
            term.append(createunode(regexp[current], term.pop()))
        elif regexp[current] == '\\':
            current += 1
            term.append(createleaf(regexp[current], True, False))
        elif regexp[current] == '.':
            term.append(createleaf("<@>", False, True))
        else:
            term.append(createleaf(regexp[current], False, False))
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
        if symbol != '#':  # то же, что 'one != hashposnum'
            symstate = set().union(followpostable[one][1])
            if symbol not in dfa[posset] and symbol != '<@>':
                dfa[posset][symbol] = symstate
            elif symbol == '<@>':
                temp = anykeytable & posset
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


def unittest():
    test = parse()
    calc(test)
    test.printtree(0)
    print "Hash is at position ", hashposnum
    print followpostable

    global dfa
    ffs = frozenset().union(test.f)
    dfabuild(ffs)

    print "========================"
    print dfa.keys()
    for one in dfa:
        print "========================"
        print dfa[one]

    print "========================"
    print
    w = input("Enter a word: ")
    dfareader(dfa, ffs, w)


unittest()
