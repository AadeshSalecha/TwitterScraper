Explanation of what each file does/should contain: 
a) api_keys: this is a file that contains close to 100 keys (out of which only about 7 work as of 1/17/23) - but you don't need to remove the non-working keys as the other scripts will only utilize the working keys - no changes needed here

b) inputs: this is a file that should contain a list of filenames that need to be rehydrated (note: the filenames need to be the absolute/relative path to the file, not just the name)

c) hydration.py: this file is used by multi_terminal_hydration.py as a subroutine to hydrate a single file. The only thing you might want to change in this file is the target variable on line 175 (this governs the target percentage to hydrate, since Ferrera datasets are large, I usually end up setting this to something small around <5%)

d) multi_terminal_hydration.py: this is the file you will be running. This script will spin up 6 terminal instances (one for each working api key), and hydrate 6 files at once. It gets the keys from the api_keys file (and line 27 dictates which keys are working). It gets the files to hydrate from the inputs file. 
Command usage: python3 multi_terminal.py api_keys inputs hydration.py 

TL;DR: you need to download all these files in one folder -> populate the inputs file with the filepaths to hydrate -> run the above command