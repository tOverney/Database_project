from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

import psycopg2

# Create your views here.
required_queries = {
    'Number of movies per year (includes tv and video movies)' :
    (0, """SELECT production_year, COUNT(*) FROM production
    WHERE (kind = 'movie'
        OR kind = 'tv movie'
        OR kind = 'video movie')
        AND production_year IS NOT NULL
    GROUP BY production_year
    ORDER BY production_year ASC"""),
    'Ten countries with the most production companies' :
    (1, """SELECT c.country_code, COUNT(DISTINCT c.uid) AS count FROM company c
    LEFT JOIN participate par ON c.uid = par.cid
    WHERE par.type = 'production companies'
        AND c.country_code IS NOT NULL
    GROUP BY c.country_code
    ORDER BY count DESC
    LIMIT 10"""),
    'Min, max and average career duration' :
    (2, """SELECT avg(duration) AS avg_duration, MAX(duration) AS max_duration,
    MIN(duration) AS min_duration
    FROM (
    SELECT (1+(MAX(prod.production_year)-MIN(prod.production_year ))) AS duration
    FROM casting c, production prod
    WHERE c.prodid = prod.uid
    GROUP BY c.perid) AS career_duration""")
}

def index(request):
    template = loader.get_template('index.html')
    context = RequestContext(request, {
            'queries' : required_queries,})

    return HttpResponse("Hello, world. This is live from a python" +
        " script through django, throught uwsgi")
