import os
#ignore = ['.py', '.md', '.pdf', '.git', '.rpt']
workedDirectory = 'PDF'

os.chdir(workedDirectory)
full_dir = []
for root, dirs, files in os.walk('.', topdown = False):
    #dirs[:] = [d for d in dirs if d not in ignore]
    dirs[:] = [d for d in dirs]
    #print(dirs)
    tup = (root,files)
    #print(tup)
    full_dir.append(tup)

del full_dir[-1]

print(full_dir)
print(len(full_dir))