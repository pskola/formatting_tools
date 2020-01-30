import fileinput, sys
filename = sys.argv[1]

with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
    for line in file:
        print(line.replace(';', ','), end='')