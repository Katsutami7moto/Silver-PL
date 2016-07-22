# coding=utf-8


import translator

source = open("C:\\Users\\napan\\Documents\\github\\Silver-PL\\examples\\example.silver")
lines_of_code = []
for line in source:
    lines_of_code.append(line)
source.close()

c_source = translator.translating(lines_of_code)

result = open("C:\\Users\\napan\\Documents\\github\\Silver-PL\\examples\\result.c", "w")
for line in c_source:
    assert isinstance(line, str)
    result.write(line + '\n\n')
result.close()
