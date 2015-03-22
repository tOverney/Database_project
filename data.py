#!/usr/bin/python
from sys import argv

def read_file(data_file, column):
    data = open(data_file, "r")
    result = []

    for line in data:
        line_elem = line.rstrip("\n").split("\t")
        elem = line_elem[int(column)]
        if elem not in result :
            print "%s" % elem
            result.append(elem)

    print "\nfound %s different values in the column" %len(result)

if __name__ == "__main__":
    read_file(argv[1], argv[2])