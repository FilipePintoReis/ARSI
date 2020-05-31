from os import listdir, getcwd, path, chdir, remove
from random import sample


directory = getcwd() + '/src/random-metadata'

filelist = [ f for f in listdir(directory) if f.endswith(".abs") ]
for f in filelist:
    remove(path.join(directory, f))

directory = getcwd() + '/src/metadata'
s = set()

for filename in listdir(directory):
    if filename.endswith(".abs"):
        s.add(filename)
    else:
        continue

for filename in listdir(directory):
    if filename.endswith(".abs"):
        file = sample(s, 1)[0]
        s.discard(file)


        chdir('src/metadata')
        contents = open(file, 'r').read()
        chdir('..')
        chdir('..')

        chdir('src/random-metadata')

        f = open(filename,"w+")
        f.write(contents)

        chdir('..')
        chdir('..')
    else:
        continue

