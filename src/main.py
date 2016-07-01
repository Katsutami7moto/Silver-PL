# coding=utf-8

from lexer import lexer

"""
var x = 5;
"""

source = open("example.txt")
lines_of_code = []
for line in source:
    lines_of_code.append(line)
source.close()

c_source = translator(parser(lexer(lines_of_code)))

result = open("result.c", "w")
for line in c_source:
    result.write(line + '\n')
result.close()
