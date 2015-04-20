#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv

import os
import sh
import StringIO
import psycopg2

# hard coded, yes it's bad but I'm lazy
FILE_PATH = "../Movies/PERSON.CSV"
TEMP_FILE = ".temp.csv"
FOOT_TO_CM = 30.48
INCH_TO_CM = 2.54 

fractions =    {'1/2': 0.5 * INCH_TO_CM,
                '1/4': 0.25 * INCH_TO_CM,
                '3/4': 0.75 * INCH_TO_CM,
                '5/8': 0.625 * INCH_TO_CM,
                '7/8': 0.875 * INCH_TO_CM}

months =   {'January': '01',
            'February': '02',
            'March': '03',
            'April': '04',
            'May': '05',
            'June': '06',
            'July': '07',
            'August': '08',
            'September': '09',
            'October': '10',
            'November': '11',
            'December': '12'
            }

username = ""
password = ""

# this will be the csv that we want to bulk import to our db!
sh.touch(TEMP_FILE)

def format_date(raw_date):
    raw_date = raw_date.split(" ")[0:3]

    if not len(raw_date) == 1 :
            year = raw_date[2][0:4]
            year = year.rstrip("BC")
            if len(year) == 2 :
                year = "00" + year
            raw_date = year + "-" + months[raw_date[1]] + "-" + raw_date[0] 
    else :
        raw_date = raw_date[0]
    
    return raw_date


def parse_height(height) :
    height_in_cm = ""
    height_no_space = height.replace(" ", "").split("(")[0]
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
        height_value = 0.5
    height_value = float(height_no_comma)
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

    return str(height_value % 0.01)


def prepare_data_file():

    #load the csv given by the course staff
    data = open(FILE_PATH, "r")
    formatted_csv = open(TEMP_FILE, "w+")

    for line in data :
        (uid, fname_lname, gender, trivia, quotes,
            birth_d, death_d, b_name, bio, spouse, height) = line.rstrip("\n").split("\t")
        
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
