from src import lexer
from collections import namedtuple


Module = namedtuple('Module', 'name imports declarations definitions')
Declaration = namedtuple('Declaration', 'subject name type args')
Definition = namedtuple('Definition', 'subject name type statements args')
Statement = namedtuple('Statement', 'subject name type rvalue args statements')
symbol_table = dict()
module_kwords = {
    "import",
    "type",
    "typedef",
    "fields",
    "extend",
    "def"
}


def p_def_type(tokens: list) -> Definition:
    pass


def p_def_typedef(tokens: list) -> Definition:
    pass


def p_def_fields(tokens: list) -> list:
    pass


def p_def_extend(tokens: list) -> Definition:
    pass


def p_def_def(tokens: list) -> Definition:
    pass


def p_definitions(statements: list) -> list:
    defs = []
    kwords = (module_kwords - {"import"})
    for x in statements:
        if x[0] in kwords:
            defs.append(eval('p_def_{0:s}(x[1])'.format(x[0])))
    return defs


def p_decl_type(tokens: list) -> Declaration:
    pass


def p_decl_typedef(tokens: list) -> Declaration:
    pass


def p_decl_fields(tokens: list) -> list:
    pass


def p_decl_extend(tokens: list) -> Declaration:
    pass


def p_decl_def(tokens: list) -> Declaration:
    pass


def p_declarations(statements: list) -> list:
    decls = []
    kwords = (module_kwords - {"import"})
    for x in statements:
        if x[0] in kwords:
            decls.append(eval('p_decl_{0:s}(x[1])'.format(x[0])))
    return decls


def p_imports(statements: list) -> set:
    imps = set()
    for x in statements:
        if x[0] == 'import':
            if x[1][0].type == 'ident':
                imps.add(x[1][0].value)
            else:
                pass
    return imps


def make_module(module_info: tuple) -> Module:
    module_name, tokens = module_info
    module_statements = []
    i = 0
    while i < len(tokens):
        s = []
        kw = ''
        if tokens[i].type in module_kwords:
            kw = tokens[i].type
            i += 1
        else:
            pass
        while tokens[i].type not in module_kwords:
            s.append(tokens[i])
            i += 1
        module_statements.append((kw, s))
    imports = p_imports(module_statements)  # TODO: к этим импортам и имени нельзя обратиться - исправить !!!
    declarations = p_declarations(module_statements)
    definitions = p_definitions(module_statements)


def p_start(tokens: list) -> list:
    modules_infos = []
    i = 0
    while i < len(tokens):
        m = []
        n = ''
        if tokens[i].type == 'module':
            i += 1
        else:
            pass
        if tokens[i].type == 'ident':
            n = tokens[i].value
            i += 1
        else:
            pass
        if tokens[i].type == 'left-curl':
            i += 1
        else:
            pass
        while tokens[i].type != 'right-curl':
            m.append(tokens[i])
            i += 1
        modules_infos.append((n, m))
        symbol_table[n] = dict()
        i += 1
    return map(make_module, modules_infos)


def m_rearrange(mods: list) -> list:
    nodes = []
    for m in mods:
        nodes.extend(m.declarations)
    for m in mods:
        nodes.extend(m.definitions)
    return nodes


def parsing(code: list) -> list:
    return m_rearrange(p_start(lexer.lexing(code)))
