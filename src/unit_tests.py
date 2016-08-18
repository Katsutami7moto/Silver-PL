lexer_wrong_int = "332hsdhsk222d22"

lexer_right_int = "7436328728"

lexer_wrong_float = "26757783.323ksdis333"

lexer_right_float = "74363.28728"

# In future - tests for string, list, other containers

lexer_wrong_ident = "dhd6$8_@fj^j"

lexer_right_ident = "cool_guy___87"

lexer_wrong_signs = "+\n-\n>___<"

lexer_right_signs = "//=\n=>\n|>\n**=\n+\n"

# All lexer tests won't pass parsing

parser_wrong_modules = "module a\n{ module b\n{ let x = 5; }\n}"

parser_right_modules = "module a\n{ let x = 5; }\nmodule b\n{ let y = 3; }"

parser_wrong_imports = "module a\n{ import a;\nlet x = 9; }\nmodule b\n{ import c;\nlet y = 0; }\n"

parser_right_imports = "module a\n{ import b;\nlet x = 9; }\nmodule b\n{ import a;\nlet y = 0; }\n"

parser_wrong_types = ""

parser_right_types = ""

# Generic

parser_wrong_typedefs = ""

parser_right_typedefs = ""

parser_wrong_extends = ""

parser_right_extends = ""

parser_wrong_varblocks = ""

parser_right_varblocks = ""

parser_wrong_letblocks = ""

parser_right_letblocks = ""

# 'new'

parser_wrong_defs = ""

parser_right_defs = ""

# expr | IfExpr | PipeExpr

parser_wrong_main = ""

parser_right_main = ""

# All parser tests won't pass dealing with statements inside functions

inside_wrong_vars = ""

inside_right_vars = ""

inside_wrong_lets = ""

inside_right_lets = ""

inside_wrong_mods = ""

inside_right_mods = ""

inside_wrong_loops = ""

inside_right_loops = ""

inside_wrong_whiles = ""

inside_right_whiles = ""

inside_wrong_untils = ""

inside_right_untils = ""

inside_wrong_dowhiles = ""

inside_right_dowhiles = ""

inside_wrong_dountils = ""

inside_right_dountils = ""

inside_wrong_fors = ""

inside_right_fors = ""

inside_wrong_ifs = ""

inside_right_ifs = ""

inside_wrong_calls = ""

inside_right_calls = ""

inside_wrong_returns = ""

inside_right_returns = ""


def run_test(source_code: str):
    from src import translator
    print('\n\n'.join(translator.translating(source_code.split('\n'))))

run_test(lexer_wrong_int)
