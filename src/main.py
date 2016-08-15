from src import translator

silver_file = open("C:\\Users\\napan\\Documents\\github\\Silver-PL\\examples\\example.silver")
c_file = open("C:\\Users\\napan\\Documents\\github\\Silver-PL\\examples\\result.c", "w")
c_file.write('\n\n'.join(translator.translating(list(silver_file))))
silver_file.close()
c_file.close()
