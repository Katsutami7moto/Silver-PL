from src import translator

spath = ""
silver_file = open(spath)
sfile = list(silver_file)
silver_file.close()

cpath = ""
c_file = open(cpath, "w")
c_file.write('\n\n'.join(translator.translating(sfile)))
c_file.close()
