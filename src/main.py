# coding=utf-8

"""
var x = 5;
"""

source = open("example.txt")
lines_of_code = []
for line in source:
    lines_of_code.append(line)
source.close()

c_source = translator(parser(lexer(lines_of_code)))  # импортировать транслятор, остальные пойдут по цепочке

result = open("result.c", "w")
for line in c_source:
    result.write(line + '\n')
result.close()
