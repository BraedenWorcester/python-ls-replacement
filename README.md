# Usage:

Intended to be used in conjuction with the linux 'alias' command, so as to allow for on-demand execution:
  
    # this will set an alias such that when you type "lss" into the console, it will execute 'ls.py'
    
    alias lss="python3 'your_path_here/ls.py'"
  
Arguments:
  
    -v: # sets verbose mode - if not set: all but the base file names will be excluded from output
    -f: # excludes directories from output, leaving only regular files
    -d: # excludes regular files from output, leaving only directories - if both -d and -f are set, the script will terminate without any output
    -h: # will order output horizontally, rather than vertically
    
# Output:  
    
verbose mode unset

    $ lss 

    ----DIRECTORIES----

    .         testDir3  testDir7
    ..        testDir4  testDir8
    testDir1  testDir5
    testDir2  testDir6


    ----FILES----

    testFile1      testFile4.gfx  testFile7.c
    testFile2.txt  testFile5.pdf  testFile8.py
    testFile3.jpg  testFile6.png


verbose mode set

    $ lss -v
    
    ----DIRECTORIES----

    drwxr-xr-x 1 braeden braeden 512 Jun 18 16:56 .
    drwxr-x--x 1 braeden braeden 512 Jun 19 21:19 ..
    drwxr-xr-x 1 braeden braeden 512 Jun 18 16:54 testDir1
    drwxr-xr-x 1 braeden braeden 512 Jun 18 16:54 testDir2
    drwxr-xr-x 1 braeden braeden 512 Jun 18 16:54 testDir3
    drwxr-xr-x 1 braeden braeden 512 Jun 18 16:54 testDir4
    drwxr-xr-x 1 braeden braeden 512 Jun 18 16:54 testDir5
    drwxr-xr-x 1 braeden braeden 512 Jun 18 16:54 testDir6
    drwxr-xr-x 1 braeden braeden 512 Jun 18 16:54 testDir7
    drwxr-xr-x 1 braeden braeden 512 Jun 18 16:54 testDir8


    ----FILES----

    -rw-r--r-- 1 braeden braeden 0 Jun 18 16:56 testFile1
    -rw-r--r-- 1 braeden braeden 0 Jun 18 16:56 testFile2.txt
    -rw-r--r-- 1 braeden braeden 0 Jun 18 16:56 testFile3.jpg
    -rw-r--r-- 1 braeden braeden 0 Jun 18 16:56 testFile4.gfx
    -rw-r--r-- 1 braeden braeden 0 Jun 18 16:56 testFile5.pdf
    -rw-r--r-- 1 braeden braeden 0 Jun 18 16:56 testFile6.png
    -rw-r--r-- 1 braeden braeden 0 Jun 18 16:56 testFile7.c
    -rw-r--r-- 1 braeden braeden 0 Jun 18 16:56 testFile8.py
    

do not print directories; only print files

    $ lss -f
    
    ----FILES----

    testFile1      testFile4.gfx  testFile7.c
    testFile2.txt  testFile5.pdf  testFile8.py
    testFile3.jpg  testFile6.png


only print directories, verbose mode set

    $ lss -d -v
    
    ----DIRECTORIES----

    drwxr-xr-x 1 braeden braeden 512 Jun 18 16:56 .
    drwxr-x--x 1 braeden braeden 512 Jun 19 21:19 ..
    drwxr-xr-x 1 braeden braeden 512 Jun 18 16:54 testDir1
    drwxr-xr-x 1 braeden braeden 512 Jun 18 16:54 testDir2
    drwxr-xr-x 1 braeden braeden 512 Jun 18 16:54 testDir3
    drwxr-xr-x 1 braeden braeden 512 Jun 18 16:54 testDir4
    drwxr-xr-x 1 braeden braeden 512 Jun 18 16:54 testDir5
    drwxr-xr-x 1 braeden braeden 512 Jun 18 16:54 testDir6
    drwxr-xr-x 1 braeden braeden 512 Jun 18 16:54 testDir7
    drwxr-xr-x 1 braeden braeden 512 Jun 18 16:54 testDir8


order output by row

    $ lss -h

    ----DIRECTORIES----

    .         ..        testDir1
    testDir2  testDir3  testDir4
    testDir5  testDir6  testDir7
    testDir8


    ----FILES----

    testFile1      testFile2.txt  testFile3.jpg
    testFile4.gfx  testFile5.pdf  testFile6.png
    testFile7.c    testFile8.py

# Requirements:

This script requires the numpy library installed: https://numpy.org/install/

This script was written for Python 3.10.4, and may possibly not function with earlier versions.