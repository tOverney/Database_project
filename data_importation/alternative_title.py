#!/usr/bin/python
from sys import argv

FILE_PATH = "../Movies/ALTERNATIVE_TITLE.CSV"
username = "";
password = "";
query_parameters = []
 
def fill_array():
    data = open(FILE_PATH, "r")
    query_line = []
    i = 0

    for line in data:
        (uid, production_id, title) = line.rstrip("\n").split("\t")
        query_line.append((int(uid), int(production_id), title))
        i += 1

    print "\nfound %s %s entries" % (len(query_line), i)

def execute_sql():
    print "here psycopg enters into plays and we execute many! yay!"

if __name__ == "__main__":
    if len(argv) < 3:
        print "db login infos must be passed as argument (username password)"
        quit()

    username = argv[1]
    password = argv[2]
    fill_array()
    execute_sql()