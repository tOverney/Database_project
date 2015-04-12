#!/usr/bin/env python
from sys import argv

import psycopg2

FILE_PATH = "../Movies/CHARACTER.CSV"

username = "";
password = "";
query_parameters = []
 
def fill_array():
    data = open(FILE_PATH, "r")

    for line in data:
        query_line = line.rstrip("\n").split("\t")
        query_parameters.append(query_line)


def execute_sql():
    try:
        conn = psycopg2.connect(
            "dbname='postgres' user=%s host='91.121.194.141' password=%s"
            % (username, password))
    except psycopg2.Error as e:
        print e.pgerror
        quit()

    cur = conn.cursor()
    try:
        cur.executemany("""INSERT INTO character(uid, name) VALUES (%s, %s)""", query_parameters)
    except psycopg2.Error as e:
        print e.pgerror
        quit()

    print "Import successful! Back to you human!"
    cur.close()
    conn.close()

if __name__ == "__main__":

    username = argv[1]
    password = argv[2]
    fill_array()
    execute_sql()
