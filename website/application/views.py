from django.shortcuts import render
from django.http import HttpResponse, Http404

from django.db import connection

# Create your views here.
required_queries = [
    ["Number of movies per year (includes tv and video movies)",
    """SELECT production_year, COUNT(*) FROM production
    WHERE (kind = 'movie'
        OR kind = 'tv movie'
        OR kind = 'video movie')
        AND production_year IS NOT NULL
    GROUP BY production_year
    ORDER BY production_year ASC;""",
    ("Year of production", "# of production that year")],

    ["Ten countries with the most production companies",
    """SELECT c.country_code, COUNT(DISTINCT c.uid) AS count FROM company c
    LEFT JOIN participate par ON c.uid = par.cid
    WHERE par.type = 'production companies'
        AND c.country_code IS NOT NULL
    GROUP BY c.country_code
    ORDER BY count DESC
    LIMIT 10;""",
    ("Country code", "# production companies")],

    ["Min, max and average career duration",
    """SELECT avg(duration) AS avg_duration, MAX(duration) AS max_duration,
    MIN(duration) AS min_duration
    FROM (
    SELECT (1+(MAX(prod.production_year)-MIN(prod.production_year ))) AS duration
    FROM casting c, production prod
    WHERE c.prodid = prod.uid
    GROUP BY c.perid) AS career_duration;""",
    ("Average duration", "Max duration", "Min duration")],

    ["Min, max and average number of actors in a production",
    """SELECT avg(numb) AS avg_nb_act, MAX(numb) AS max_nb_act, MIN(numb) AS min_nb_act
    FROM (  SELECT count(*) AS numb
    FROM casting
    WHERE role = 'actor'
    GROUP BY prodid) AS number;""",
    ("Average # actors", "Max # actors", "Min # actors")]]

def index(request) :

    context = {'queries' : required_queries, 'range' : range(len(required_queries))}

    return render(request, 'application/index.html', context)



def result(request, query_index) :
    query_index = int(query_index)
    if query_index >= len(required_queries) :
        raise Http404("Question does not exist")

    current = required_queries[query_index]
    # opening connection to the database
    cur = connection.cursor()

    # do the selection

    cur.execute(current[1])
    connection.commit()


    # fetch the result 
    result_array = cur.fetchall()

    # we close everything db related
    cur.close()
    connection.close()

    if len(result_array) == 0:
        raise Http404("Empty result..")

    # [["Bidon", "Bbb"],["Citron", "ccc"]]
    context = {'query_name' : current[0],
        'query_result' : result_array,
        'col_title' : current[2]}
    
    return render(request, 'application/result.html', context)