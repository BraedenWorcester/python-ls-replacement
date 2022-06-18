# Usage:

  Intended to be used in conjuction with the linux 'alias' command, so as to allow for on-demand execution:
  
    # this will set an alias such that when you type "lsr" into the console, it will execute 'ls.py'
    
    alias lsr="python3 'your_path_here/ls.py'"
    
# Output:

  The script strips all but the file names from the 'ls -al' output, and prints them as either "DIRECTORIES" or "FILES":
  
    ----DIRECTORIES----
    exampleDirectory1
    exampleDirectory2
    exampleDirectory3
    exampleDirectory4
    exampleDirectory5

    ----FILES----
    exampleFile1.txt
    exampleFile2
    exampleFile3.pdf
    exampleFile4.jpg
    exampleFile5.gfx
