import subprocess
import sys

lines = subprocess.check_output(['ls', '-al']).splitlines()

directs = []
files = []

i = 0
for line in lines:
    if (i > 2):
        tokenized = line.split()
        name = b' '.join(tokenized[8:len(tokenized)]).decode(sys.stdout.encoding)
        if (chr(line[0]) == 'd'):
            directs.append(name)
        else:
            files.append(name)
    i += 1

print("\n----DIRECTORIES----")
for name in directs:
    print(name)

print("\n----FILES----")
for name in files:
    print(name)

print("")