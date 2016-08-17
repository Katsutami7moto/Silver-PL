from src import translator


lexer_error_wrong_int = "332hsdhsk222d22"

lexer_error_wrong_float = "26757783.323ksdis333"

lexer_error_wrong_ident = "_dhd678_hfjfj"

lexer_error_wrong_signs = ">___<"

lexer_error_right_int = "7436328728"

lexer_error_right_float = "74363.28728"

lexer_error_right_ident = "cool_guy_87"

lexer_error_right_signs = "//=\n=>\n|>\n**="


def run_test(source_code: str):
    print('\n\n'.join(translator.translating(source_code.split('\n'))))

run_test(lexer_error_wrong_int)
