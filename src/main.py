# coding=utf-8

"""
var x = 5;
"""
import translator

source = open("J:\Nicolas\GitHub\Silver-PL\examples\\fib.silver")
lines_of_code = []
for line in source:
    lines_of_code.append(line)
source.close()

c_source = translator.translating(lines_of_code)

result = open("J:\Nicolas\GitHub\Silver-PL\examples\\result.c", "w")
for line in c_source:
    result.write(line + '\n')
result.close()
