#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv

import os
import sh
import StringIO
import psycopg2

# hard coded, yes it's bad but I'm lazy
FILE_PATH = "../Movies/PRODUCTION_CAST.CSV"
TEMP_FILE = ".temp.csv"

username = ""
password = ""

def execute_sql():

    # opening connection to the database
    try:
        conn = psycopg2.connect(
            "dbname='postgres' user=%s host='91.121.194.141' password=%s"
            % (username, password))
    except psycopg2.Error as e:
        print e.pgerror
        quit()
    cur = conn.cursor()

    formatted_csv = open(FILE_PATH, "r")
    # mass copy of the CSV to the desired table
    try:
        cur.copy_from(formatted_csv, 'casting', sep='\t',
            columns=('prodid', 'perid', 'cid', 'role'))
        conn.commit()
    except psycopg2.Error as e:
        print e.pgerror
        quit()

    # closing connection correctly
    print "[-] Import successful! Back to you human!"

    formatted_csv.close()
    cur.close()
    conn.close()


if __name__ == "__main__":

    # we get the db login infos from the command line.
    username = argv[1]
    password = argv[2]

    execute_sql()
