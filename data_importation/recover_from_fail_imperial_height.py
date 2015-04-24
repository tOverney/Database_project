#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv

import os
import sh
import StringIO
import psycopg2

# hard coded, yes it's bad but I'm lazy
FILE_PATH = "../Movies/PERSON.CSV"
FOOT_TO_CM = 30.48
INCH_TO_CM = 2.54 

fractions =    {'1/2': 0.5 * INCH_TO_CM,
                '1/4': 0.25 * INCH_TO_CM,
                '3/4': 0.75 * INCH_TO_CM,
                '5/8': 0.625 * INCH_TO_CM,
                '7/8': 0.875 * INCH_TO_CM}

values = []

username = ""
password = ""

def parse_height(height) :
    height_in_cm = ""
    height_no_space = height.replace(" ", "").split("(")[0]
    has_unit_chars = False
    for unit in ('cm', '\'', '\"') :
        if unit in height_no_space :
            has_unit_chars = True
    if not has_unit_chars and len(height_no_space) > 2:
        height_no_space = height_no_space + "cm"
    try :
        if "cm" in height_no_space :
            height_in_cm = parse_metric(height_no_space)
        else :
           height_in_cm = parse_imperial(height_no_space)
    except Exception as e:
        print height_no_space
        print e
        quit()

    return height_in_cm

def parse_metric(height) :
    height_no_unit = height.replace("cm", "")
    height_no_comma = height_no_unit.replace(",",".")
    height_value = 0.0
    if '½' in height_no_comma :
        height_no_comma = height_no_comma.rstrip('½')
        height_value += 0.5
    height_value += float(height_no_comma)
    if height_value < 10 :
        height_value *= 100
    return str(height_value)

def parse_imperial(height) :
    height_value = 0.0
    height_cleaned = height.replace(",", "").split("\'")

    if "\N" == height_cleaned[0] :
        return "\N"
    elif len(height_cleaned) > 1 and not height_cleaned[1] == "":
        inches = height_cleaned[1].split("\"")[0]
        for fract in fractions :
            if fract in inches :
                height_value += fractions[fract]
                inches = inches.replace(fract, "")
                inches = "0" + inches

        height_value += float(inches) * INCH_TO_CM

    if "\"" in height_cleaned[0] :
        height_cleaned = height_cleaned[0].split("\"")
        height_value += float(height_cleaned[1]) * INCH_TO_CM

    height_value += float(height_cleaned[0]) * FOOT_TO_CM

    list_parts = str(height_value).split(".")
    list_parts[1] = list_parts[1][0:3]
    string_height = ".".join(list_parts)
    return string_height


def prepare_data_file():

    #load the csv given by the course staff
    data = open(FILE_PATH, "r")

    for line in data :
        line_elems = line.rstrip("\n").split("\t")
        
        height = parse_height(line_elems[10])

        if "\N" not in height :
            values.append((float(height), line_elems[0]))
    
    print "[-] Parsing successful"
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

    try:
        cur.executemany("""UPDATE person SET height = %s WHERE uid = %s""", values)
        conn.commit()
    except psycopg2.Error as e:
        print e.pgerror
        quit()

    # closing connection correctly
    print "[-] Update successful! Back to you human!"

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
