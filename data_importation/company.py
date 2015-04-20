#!/usr/bin/env python
from sys import argv

import psycopg2

# hard coded, yes it's bad but I'm lazy
FILE_PATH = "../Movies/COMPANY.CSV"

username = ""
password = ""

# we actually don't need to format that csv,
# it's already in the correct format (uid, name)
data = open(FILE_PATH, "r")


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

    # mass copy of the CSV to the desired table
    try:
        cur.copy_from(data, 'company', columns=('uid', 'country_code', 'name'))
        conn.commit()
    except psycopg2.Error as e:
        print e.pgerror
        quit()

    # closing connection correctly
    print "Import successful! Back to you human!"
    cur.close()
    conn.close()


if __name__ == "__main__":

    # we get the db login infos from the command line.
    username = argv[1]
    password = argv[2]

    execute_sql()
    
    data.close()
