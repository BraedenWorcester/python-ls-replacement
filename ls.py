import subprocess
import sys

# number of files on a single output line in non-verbose mode
itemsPerRow = 3

# number of files on a single output line in verbose mode
itemsPerRowVerbose = 1

# what we want to put in between distinct files on the same output line
itemDeliminator = ""

# amount of padding we should use when printing multiple files to a single line of output
itemOffset = 50

# maximum amount of displayed characters per file in non-verbose mode
itemMaxCharacters = 40

# amount of padding we should use between the owner and group output in verbose mode
verbosePaddingOwnerAndGroup = 8

# amount of padding we should use between the group and size output in verbose mode
verbosePaddingGroupAndSize = 8

# minimum digits our size output should have in verbose mode
verboseZFillSize = 8 

# amount of padding we should use between the size and date output in verbose mode
verbosePaddingSizeAndDate = verboseZFillSize + 1

def getBaseName(fileString, toBeLowered = True, tokenized = False):
    if not tokenized:
        fileString = fileString.split()
    try:
        stringOut =  ' '.join(fileString[8:len(fileString)])
    except TypeError:
        stringOut =  b' '.join(fileString[8:len(fileString)]).decode(sys.stdout.encoding)
    if toBeLowered:
        stringOut = stringOut.lower()
    return stringOut

cmd = subprocess.Popen(['ls', '-al'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
lines = cmd.communicate()[0].splitlines()

directs = []
files = []

try:
    if (sys.argv[1] == "-v"):
        verbose = True  
    else:
        verbose = False
except IndexError:
    verbose = False

for line in lines:
    if (len(line.split()) > 8):
        tokenized = line.split()
        for token in tokenized:
            loc = tokenized.index(token)
            tokenized[loc] = token.decode(sys.stdout.encoding)

        # if verbose mode is unset, we strip everything aside from the basename
        if not verbose:
            out = getBaseName(tokenized, False, True)

        # otherwise we pad out certain values to line up our output
        else:
            tokenized[2] = tokenized[2].ljust(verbosePaddingOwnerAndGroup)
            tokenized[3] = tokenized[3].ljust(verbosePaddingGroupAndSize)
            tokenized[4] = tokenized[4].zfill(verboseZFillSize).ljust(verbosePaddingSizeAndDate)
            tokenized[6] = tokenized[6].zfill(2)
            tokenized[7] = tokenized[7].rjust(5)
            out = ' '.join(tokenized)
        
        if (chr(line[0]) == 'd'):
            directs.append(out)
        elif (chr(line[0]) == '-'):
            files.append(out)

# sort output alphabetically
if verbose:
    directs = sorted(directs, key=getBaseName)
    files = sorted(files, key=getBaseName)
else:
    directs = sorted(directs, key=str.lower)
    files = sorted(files, key=str.lower)

itemsInRow = 0
print("")
print("\n----DIRECTORIES----\n")
for out in directs:
    if not verbose and len(out) > itemMaxCharacters:
        out = out[:itemMaxCharacters] + "..."
    if not verbose and itemsInRow < itemsPerRow-1:
        itemsInRow += 1
        print(out.ljust(itemOffset), end=itemDeliminator)
    elif verbose and itemsInRow < itemsPerRowVerbose-1:
        itemsInRow += 1
        print(out.ljust(itemOffset), end=itemDeliminator)
    else:
        itemsInRow = 0
        print(out)

itemsInRow = 0
print("")
print("\n----FILES----\n")
for out in files:
    if not verbose and len(out) > itemMaxCharacters:
        out = out[:itemMaxCharacters] + "..."
    if not verbose and itemsInRow < itemsPerRow-1:
        itemsInRow += 1
        print(out.ljust(itemOffset), end=itemDeliminator)
    elif verbose and itemsInRow < itemsPerRowVerbose-1:
        itemsInRow += 1
        print(out.ljust(itemOffset), end=itemDeliminator)
    else:
        itemsInRow = 0
        print(out)
print("\n")