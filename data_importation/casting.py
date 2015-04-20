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

# this will be the csv that we want to bulk import to our db!
sh.touch(TEMP_FILE)

def prepare_data_file():

    #load the csv given by the course staff
    data = open(FILE_PATH, "r")
    formatted_csv = open(TEMP_FILE, "w+")

    for line in data :
        (prod_id, person_id, char_id, role) = line.rstrip("\n").split("\t")
        
        (lname, fname) = ("", "")
        if ", " in fname_lname:
            (lname, fname) = fname_lname.split(", ")
        else :
            (lname, fname) = (fname_lname, "\N")

        birth_d = format_date(birth_d)
        death_d = format_date(death_d)

        height = parse_height(height)

        tuple_str = (uid, fname, lname, gender, trivia, quotes, birth_d,
            death_d, bio, spouse, height, b_name)
        correct_line = "\t".join(tuple_str)
        correct_line += "\n"
        #print line
        formatted_csv.write(correct_line)
    
    print "[-] Parsing successful"
    formatted_csv.flush()
    os.fsync(formatted_csv.fileno())
    formatted_csv.close()
    data.close()

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

    formatted_csv = open(TEMP_FILE, "r")
    # mass copy of the CSV to the desired table
    try:
        cur.copy_from(formatted_csv, 'person', sep='\t',
            columns=('uid', 'first_name', 'last_name', 'gender', 'trivia',
                'quotes', 'birth', 'death', 'biography', 'spouse', 'height',
                'birth_name'))
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

    prepare_data_file()
    # fileo = open(TEMP_FILE, "r")
    # print fileo.readline() + fileo.readline()
    # fileo.close()
    execute_sql()
    sh.rm(TEMP_FILE)
