#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv

import os
import sh
import StringIO
import psycopg2

# hard coded, yes it's bad but I'm lazy
FILE_PATH = "../Movies/PRODUCTION.CSV"
TEMP_FILES =   {"tv_series": (".tvseries.csv",
                ('uid', 'title', 'production_year', 'genre', 'series_years')),
                "episode": (".episode.csv",
                ('uid', 'title', 'production_year', 'genre', 'sid', 'season', 'episode')),
                "movie": (".movie.csv",
                ('uid', 'title', 'production_year', 'genre')),
                "video_movie": (".vmovie.csv",
                ('uid', 'title', 'production_year', 'genre')),
                "tv_movie": (".tmovie.csv",
                ('uid', 'title', 'production_year', 'genre')),
                "video_game": (".videogame.csv",
                ('uid', 'title', 'production_year', 'genre'))}

username = ""
password = ""

# this will be the csv that we want to bulk import to our db!
for temp_file in TEMP_FILES.viewvalues() :
    sh.touch(temp_file[0])


def prepare_data_file():

    #load the csv given by the course staff
    data = open(FILE_PATH, "r")
    csvs = {}
    for prod_kind in TEMP_FILES.viewkeys():
        csvs[prod_kind] = open(TEMP_FILES[prod_kind][0], "w+")

    for line in data :
        (uid, title, prod_year, s_id, s_num,
            e_num, series_years, kind, genre) = line.rstrip("\n").split("\t")
        

        entry_data = [uid, title, prod_year, genre]
        kind = kind.replace(" ","_")
        if kind == "tv_series" :
            entry_data.append(series_years)
        elif kind == "episode" :
            for elem in (s_id, s_num, e_num) :
                entry_data.append(elem)
        correct_line = "\t".join(entry_data)
        correct_line += "\n"

        csvs[kind].write(correct_line)
    
    print "[-] Parsing successful"
    for csv in csvs.viewvalues() :
        csv.flush()
        os.fsync(csv.fileno())
        csv.close()

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

    print "[+] Insertion started!"

    for key_name in sorted(TEMP_FILES.viewkeys(), reverse=True) :
        print " |--[-] Insertion of '%s' started ..." % key_name
        formatted_csv = open(TEMP_FILES[key_name][0], "r")
        # mass copy of the CSV to the desired table
        try:
            cur.copy_from(formatted_csv, key_name, sep='\t',
                columns=TEMP_FILES[key_name][1])
        except psycopg2.Error as e:
            print e.pgerror
            quit()

        # closing connection correctly
        print " |--[-] Insertion of '%s' successful!" % key_name

        formatted_csv.close()

    conn.commit()
    print "[-] Insertion successful! Back to you, human!"
    cur.close()
    conn.close()


if __name__ == "__main__":

    # we get the db login infos from the command line.
    username = argv[1]
    password = argv[2]

    prepare_data_file()
    execute_sql()
    for temp_file in TEMP_FILES.viewvalues() :
        sh.rm(temp_file[0])
