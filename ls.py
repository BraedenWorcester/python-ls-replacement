import subprocess
import sys
import numpy as np

# number of files on a single output line in non-verbose mode
itemsPerRow = 3

# what we want to put in between distinct files on the same output line; I personally prefer nothing
itemDeliminator = ""

# maximum amount of displayed characters per file in non-verbose mode
itemMaxCharacters = 40



# distance between files on same line; number here doesn't matter, is calculated w/ DeterminePadding()
itemOffset = -1

printHorizontally = False
filesShouldPrint = True
directsShouldPrint = True
verbose = False
itemHasCharacterLimit = True

def ParseArgs(args):

    global printHorizontally
    global filesShouldPrint
    global directsShouldPrint
    global verbose
    global itemsPerRow
    global itemHasCharacterLimit

    for arg in args:
        if (arg == '-v'):
            verbose = True
            itemsPerRow = 1
            printHorizontally = False
        if (arg == '-f'):
            directsShouldPrint = False
        if (arg == '-d'):
            filesShouldPrint = False
        if (arg == '-h' and not verbose):
            printHorizontally = True
        if (arg == '-u'):
            itemHasCharacterLimit = False
    
    if not filesShouldPrint and not directsShouldPrint:
        exit()

def GetBaseName(fileString):
    return ' '.join(fileString.split()[8:len(fileString)]).lower()


def RoundOffArr(arr):
    while arr.size % itemsPerRow != 0:
        arr = np.append(arr, "...")
    return arr

# remember DeterminePadding() returns so we save time not reworking indentical calls
determinePaddingResults = dict()
# get the size of the longest nth word from all strings in arr, n = -1 looks for longest length of all words combined; return sum of longest and offset for a nice padding amount
def DeterminePadding(arr, n = -1, offset = 0):
    global determinePaddingResults
    key = hash(str(n)+ "narr" + str(arr) + str(offset))
    if not key in determinePaddingResults:

        longest = 0
        for row in arr:
            if not n == -1:
                try:
                    tokenized = row.split()
                except AttributeError:
                    tokenized = row
                length = len(tokenized[n])
                if length > longest:
                        longest = length
            else:
                for string in row:
                    length = len(string)
                    if length > longest:
                        longest = length

        if (longest > itemMaxCharacters) and (not verbose) and (itemHasCharacterLimit):
            longest = itemMaxCharacters + 3 # + 3 accounts for the '...' at the end of cut off file names
        determinePaddingResults[key] = longest + offset

    return determinePaddingResults[key]


# convert list of lists of words into list of formatted strings
def Reformat(arr):

    newarr = []
    for subarr in arr:
        if not verbose:
            newString = ' '.join(subarr[8:])
            if (len(newString) > itemMaxCharacters) and (itemHasCharacterLimit):
                newString = newString[:itemMaxCharacters-1] + "..."
            newarr.append(newString)
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
        

ParseArgs(sys.argv)
cmd = subprocess.Popen(['ls', '-al'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
lines = cmd.communicate()[0].splitlines()

directs = []
files = []

for line in lines:
    if (len(line.split()) > 8):
        tokenized = line.split()
        for token in tokenized:
            loc = tokenized.index(token)
            tokenized[loc] = token.decode(sys.stdout.encoding)

        out = tokenized
        if (chr(line[0]) == 'd' and directsShouldPrint):
            directs.append(out)
        elif (chr(line[0]) == '-' and filesShouldPrint):
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

# convert lists to numpy arrays
directs = np.array(directs)
files = np.array(files)

# make array sizes divisible by itemsPerRow
directs = RoundOffArr(directs)
files = RoundOffArr(files)

# convert to 2D arrays
if not printHorizontally:
    directs.shape = (itemsPerRow, -1)
    files.shape = (itemsPerRow, -1)
else:
    directs.shape = (-1, itemsPerRow)
    files.shape = (-1, itemsPerRow)

# transpose array such that values are printed by column rather than by row
if not printHorizontally:
    directs = np.transpose(directs)
    files = np.transpose(files)


if directsShouldPrint:

    itemOffset = DeterminePadding(directs, offset=2)
    print("")
    print("\n----DIRECTORIES----\n")
    i = 0
    j = 0
    while i < directs[:,0].size:
        while j < directs[0,:].size:
            if not directs[i,j] == "...":
                print(directs[i,j].ljust(itemOffset), end=itemDeliminator)
            j += 1
        print()
        j = 0
        i += 1

if filesShouldPrint:

    itemOffset = DeterminePadding(files, offset=2)
    print("")
    print("\n----FILES----\n")
    i = 0
    j = 0
    while i < files[:,0].size:
        while j < files[0,:].size:
            if not files[i,j] == "...":
                print(files[i,j].ljust(itemOffset), end=itemDeliminator)
            j += 1
        print()
        j = 0
        i += 1
            
print("\n")