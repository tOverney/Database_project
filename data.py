#!/usr/bin/env python
from sys import argv

mode = 0

def read_file(data_file, column):
    data = open(data_file, "r")
    result = []
    entry = ""
    longest = 0

    for line in data:
        line_elem = line.rstrip("\n").split("\t")
        elem = line_elem[int(column)]
        if mode == 1:
            if elem not in result :
                print "%s" % elem
            result.append(elem)

        temp = max(len(elem), longest)
        if temp != longest:
            print temp
            longest = temp

    if mode == 1:
        print "\nfound %s different values in the column" %len(result)
    else:
        print "\nlongest entry was %s characters long" %longest

if __name__ == "__main__":
    if len(argv) == 4 :
        mode = int(argv[3])

    read_file(argv[1], argv[2])