import subprocess
import sys

# number of files on a single output line in non-verbose mode
itemsPerRow = 3

# number of files on a single output line in verbose mode
itemsPerRowVerbose = 1

# what we want to put in between distinct files on the same output line; I personally prefer nothing
itemDeliminator = ""

# maximum amount of displayed characters per file in non-verbose mode
itemMaxCharacters = 40

# distance between files on same line; number here doesn't matter, is calculated w/ DeterminePadding()
itemOffset = -1

def GetBaseName(fileString):
    return ' '.join(fileString.split()[8:len(fileString)]).lower()


# remember DeterminePadding() returns so we save time not reworking indentical calls
determinePaddingResults = dict()
# get the size of the longest nth word from all strings in arr, n = -1 looks for longest length of all words combined; return sum of longest and 2 for a nice padding amount
def DeterminePadding(arr, n = -1, offset = 0):

    global determinePaddingResults
    key = hash(str(n)+ "narr" + str(arr) + str(offset))
    if not key in determinePaddingResults:

        longest = 0
        for string in arr:
            if not n == -1:
                try:
                    tokenized = string.split()
                except AttributeError:
                    tokenized = string
                length = len(tokenized[n])
            else:
                length = len(string)
            if length > longest:
                longest = length

        if longest > itemMaxCharacters and not verbose:
            longest = itemMaxCharacters + 3 # + 3 accounts for the '...' at the end of cut off file names
        determinePaddingResults[key] = longest + offset

    return determinePaddingResults[key]


# convert list of lists of words into list of formatted strings
def Reformat(arr):

    newarr = []
    for subarr in arr:
        if not verbose:
            newarr.append(' '.join(subarr[8:]))
        else:
            newsubarr = subarr.copy()
            newsubarr[0] = subarr[0].ljust(DeterminePadding(arr, 0))
            newsubarr[1] = subarr[1].ljust(DeterminePadding(arr, 1))
            newsubarr[2] = subarr[2].ljust(DeterminePadding(arr, 2))
            newsubarr[3] = subarr[3].ljust(DeterminePadding(arr, 3))
            newsubarr[4] = subarr[4].zfill(DeterminePadding(arr, 4))
            newsubarr[5] = subarr[5].rjust(DeterminePadding(arr, 5))
            newsubarr[6] = subarr[6].zfill(2).rjust(DeterminePadding(arr, 6))
            newsubarr[7] = subarr[7].rjust(DeterminePadding(arr, 7))
            newarr.append(' '.join(newsubarr))

    return newarr
        


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

        out = tokenized
        if (chr(line[0]) == 'd'):
            directs.append(out)
        elif (chr(line[0]) == '-'):
            files.append(out)

directs = Reformat(directs)
files = Reformat(files)

# sort output alphabetically
if verbose:
    directs = sorted(directs, key=GetBaseName)
    files = sorted(files, key=GetBaseName)
else:
    directs = sorted(directs, key=str.lower)
    files = sorted(files, key=str.lower)


itemOffset = DeterminePadding(directs, offset=2)
itemsInRow = 0
print("")
print("\n----DIRECTORIES----\n")
for out in directs:
    if not verbose and len(out) > itemMaxCharacters:
        out = out[:itemMaxCharacters] + "..."
    if (not verbose and itemsInRow < itemsPerRow-1) or (verbose and itemsInRow < itemsPerRowVerbose-1):
        itemsInRow += 1
        print(out.ljust(itemOffset), end=itemDeliminator)
    else:
        itemsInRow = 0
        print(out)

itemOffset = DeterminePadding(files, offset=2)
itemsInRow = 0
print("")
print("\n----FILES----\n")
for out in files:
    if not verbose and len(out) > itemMaxCharacters:
        out = out[:itemMaxCharacters] + "..."
    if (not verbose and itemsInRow < itemsPerRow-1) or (verbose and itemsInRow < itemsPerRowVerbose-1):
        itemsInRow += 1
        print(out.ljust(itemOffset), end=itemDeliminator)
    else:
        itemsInRow = 0
        print(out)
print("\n")