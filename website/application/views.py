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
    ("Average # actors", "Max # actors", "Min # actors")],

    ["Min, max and average height of female persons",
    """SELECT MIN(height) AS min_height, MAX(height) AS max_height,
    AVG(height) AS avg_height FROM person
    WHERE gender = 'f';""",
    ("Minimal height", "Maximal height", "Average Height")],

    ["Movies that had the same person as actor and director",
    """SELECT p2.uid, p1.uid, person.first_name, person.last_name, prod.title, p1.role, p2.role FROM casting p1
    LEFT JOIN casting p2
        ON p1.prodid = p2.prodid AND p1.perid = p2.perid
    LEFT JOIN person
        ON p1.perid = person.uid
    LEFT JOIN production prod
        ON p1.prodid = prod.uid
    WHERE p1.role='director' AND p2.role='actor';""",
    ("First name", "Last name", "Production Title")],

    ["The three most popular character names",
    """SELECT name, COUNT(*) AS amount
    FROM character
    GROUP BY name
    ORDER BY amount DESC LIMIT 3;""",
    ("Character name", "# of occurences")],

    ["Actors age difference greater than 55 years",
    """SELECT DISTINCT p1.uid as person_id, c1.prodid as production_id
FROM person p1
LEFT JOIN casting c1 ON p1.uid = c1.perid
LEFT JOIN casting c2 ON c1.prodid = c2.prodid
LEFT JOIN person p2 ON c2.perid = p2.uid
WHERE p1.birth IS NOT NULL AND p2.birth IS NOT NULL AND p1.uid <> p2.uid AND p1.birth >= p2.birth + 55 * interval '1 year';""",
    ("Eldest person's id", "Production's id")],

    ["Bradley Cooper's most productive year",
    """SELECT production_year
FROM (
    SELECT production_year, COUNT(*) AS count
    FROM ( SELECT production_year
        FROM person
        LEFT JOIN casting ON person.uid = casting.perid 
        LEFT JOIN production ON casting.prodid = production.uid
        WHERE last_name = 'Cooper' AND first_name = 'Bradley'
        ) AS prod_year
    GROUP BY production_year
    ORDER BY count DESC LIMIT 1
    ) AS year;""",
    ("Year of production", "# of production that year")],

    ["Year 2000's most prolific companies, per genre",
    """(SELECT genre, name, count(*) as nombre_de_prod
FROM participate pa
LEFT JOIN production p ON pa.pid = p.uid
LEFT JOIN company c ON pa.cid = c.uid
WHERE production_year = 2000 AND p.genre = 'Action'  
GROUP BY name, genre
ORDER BY nombre_de_prod DESC LIMIT 1)
UNION 
(SELECT genre, name, count(*) as nombre_de_prod
FROM participate pa
LEFT JOIN production p ON pa.pid = p.uid
LEFT JOIN company c ON pa.cid = c.uid
WHERE production_year = 2000 AND p.genre = 'Adventure'  
GROUP BY name, genre
ORDER BY nombre_de_prod DESC LIMIT 1)
UNION
(SELECT genre, name, count(*) as nombre_de_prod
FROM participate pa
LEFT JOIN production p ON pa.pid = p.uid
LEFT JOIN company c ON pa.cid = c.uid
WHERE production_year = 2000 AND p.genre = 'Animation'  
GROUP BY name, genre
ORDER BY nombre_de_prod DESC LIMIT 1)
UNION
(SELECT genre, name, count(*) as nombre_de_prod
FROM participate pa
LEFT JOIN production p ON pa.pid = p.uid
LEFT JOIN company c ON pa.cid = c.uid
WHERE production_year = 2000 AND p.genre = 'Biography'  
GROUP BY name, genre
ORDER BY nombre_de_prod DESC LIMIT 1)
UNION 
(SELECT genre, name, count(*) as nombre_de_prod
FROM participate pa
LEFT JOIN production p ON pa.pid = p.uid
LEFT JOIN company c ON pa.cid = c.uid
WHERE production_year = 2000 AND p.genre = 'Comedy'  
GROUP BY name, genre
ORDER BY nombre_de_prod DESC LIMIT 1)
UNION
(SELECT genre, name, count(*) as nombre_de_prod
FROM participate pa
LEFT JOIN production p ON pa.pid = p.uid
LEFT JOIN company c ON pa.cid = c.uid
WHERE production_year = 2000 AND p.genre = 'Crime'  
GROUP BY name, genre
ORDER BY nombre_de_prod DESC LIMIT 1)
UNION
(SELECT genre, name, count(*) as nombre_de_prod
FROM participate pa
LEFT JOIN production p ON pa.pid = p.uid
LEFT JOIN company c ON pa.cid = c.uid
WHERE production_year = 2000 AND p.genre = 'Documentary'  
GROUP BY name, genre
ORDER BY nombre_de_prod DESC LIMIT 1)
UNION 
(SELECT genre, name, count(*) as nombre_de_prod
FROM participate pa
LEFT JOIN production p ON pa.pid = p.uid
LEFT JOIN company c ON pa.cid = c.uid
WHERE production_year = 2000 AND p.genre = 'Drama'  
GROUP BY name, genre
ORDER BY nombre_de_prod DESC LIMIT 1)
UNION
(SELECT genre, name, count(*) as nombre_de_prod
FROM participate pa
LEFT JOIN production p ON pa.pid = p.uid
LEFT JOIN company c ON pa.cid = c.uid
WHERE production_year = 2000 AND p.genre = 'Family'  
GROUP BY name, genre
ORDER BY nombre_de_prod DESC LIMIT 1)
UNION
(SELECT genre, name, count(*) as nombre_de_prod
FROM participate pa
LEFT JOIN production p ON pa.pid = p.uid
LEFT JOIN company c ON pa.cid = c.uid
WHERE production_year = 2000 AND p.genre = 'Fantasy'  
GROUP BY name, genre
ORDER BY nombre_de_prod DESC LIMIT 1)
UNION 
(SELECT genre, name, count(*) as nombre_de_prod
FROM participate pa
LEFT JOIN production p ON pa.pid = p.uid
LEFT JOIN company c ON pa.cid = c.uid
WHERE production_year = 2000 AND p.genre = 'Film-Noir'  
GROUP BY name, genre
ORDER BY nombre_de_prod DESC LIMIT 1)
UNION
(SELECT genre, name, count(*) as nombre_de_prod
FROM participate pa
LEFT JOIN production p ON pa.pid = p.uid
LEFT JOIN company c ON pa.cid = c.uid
WHERE production_year = 2000 AND p.genre = 'Game-Show'  
GROUP BY name, genre
ORDER BY nombre_de_prod DESC LIMIT 1)
UNION
(SELECT genre, name, count(*) as nombre_de_prod
FROM participate pa
LEFT JOIN production p ON pa.pid = p.uid
LEFT JOIN company c ON pa.cid = c.uid
WHERE production_year = 2000 AND p.genre = 'History'  
GROUP BY name, genre
ORDER BY nombre_de_prod DESC LIMIT 1)
UNION 
(SELECT genre, name, count(*) as nombre_de_prod
FROM participate pa
LEFT JOIN production p ON pa.pid = p.uid
LEFT JOIN company c ON pa.cid = c.uid
WHERE production_year = 2000 AND p.genre = 'Horror'  
GROUP BY name, genre
ORDER BY nombre_de_prod DESC LIMIT 1)
UNION
(SELECT genre, name, count(*) as nombre_de_prod
FROM participate pa
LEFT JOIN production p ON pa.pid = p.uid
LEFT JOIN company c ON pa.cid = c.uid
WHERE production_year = 2000 AND p.genre = 'Music'  
GROUP BY name, genre
ORDER BY nombre_de_prod DESC LIMIT 1)
UNION
(SELECT genre, name, count(*) as nombre_de_prod
FROM participate pa
LEFT JOIN production p ON pa.pid = p.uid
LEFT JOIN company c ON pa.cid = c.uid
WHERE production_year = 2000 AND p.genre = 'Musical'  
GROUP BY name, genre
ORDER BY nombre_de_prod DESC LIMIT 1)
UNION 
(SELECT genre, name, count(*) as nombre_de_prod
FROM participate pa
LEFT JOIN production p ON pa.pid = p.uid
LEFT JOIN company c ON pa.cid = c.uid
WHERE production_year = 2000 AND p.genre = 'Mystery'  
GROUP BY name, genre
ORDER BY nombre_de_prod DESC LIMIT 1)
UNION
(SELECT genre, name, count(*) as nombre_de_prod
FROM participate pa
LEFT JOIN production p ON pa.pid = p.uid
LEFT JOIN company c ON pa.cid = c.uid
WHERE production_year = 2000 AND p.genre = 'News'  
GROUP BY name, genre
ORDER BY nombre_de_prod DESC LIMIT 1)
UNION
(SELECT genre, name, count(*) as nombre_de_prod
FROM participate pa
LEFT JOIN production p ON pa.pid = p.uid
LEFT JOIN company c ON pa.cid = c.uid
WHERE production_year = 2000 AND p.genre = 'Reality-TV'  
GROUP BY name, genre
ORDER BY nombre_de_prod DESC LIMIT 1)
UNION 
(SELECT genre, name, count(*) as nombre_de_prod
FROM participate pa
LEFT JOIN production p ON pa.pid = p.uid
LEFT JOIN company c ON pa.cid = c.uid
WHERE production_year = 2000 AND p.genre = 'Romance'  
GROUP BY name, genre
ORDER BY nombre_de_prod DESC LIMIT 1)
UNION
(SELECT genre, name, count(*) as nombre_de_prod
FROM participate pa
LEFT JOIN production p ON pa.pid = p.uid
LEFT JOIN company c ON pa.cid = c.uid
WHERE production_year = 2000 AND p.genre = 'Sci-Fi'  
GROUP BY name, genre
ORDER BY nombre_de_prod DESC LIMIT 1)
UNION
(SELECT genre, name, count(*) as nombre_de_prod
FROM participate pa
LEFT JOIN production p ON pa.pid = p.uid
LEFT JOIN company c ON pa.cid = c.uid
WHERE production_year = 2000 AND p.genre = 'Short'  
GROUP BY name, genre
ORDER BY nombre_de_prod DESC LIMIT 1)
UNION 
(SELECT genre, name, count(*) as nombre_de_prod
FROM participate pa
LEFT JOIN production p ON pa.pid = p.uid
LEFT JOIN company c ON pa.cid = c.uid
WHERE production_year = 2000 AND p.genre = 'Sport'  
GROUP BY name, genre
ORDER BY nombre_de_prod DESC LIMIT 1)
UNION
(SELECT genre, name, count(*) as nombre_de_prod
FROM participate pa
LEFT JOIN production p ON pa.pid = p.uid
LEFT JOIN company c ON pa.cid = c.uid
WHERE production_year = 2000 AND p.genre = 'Talk-Show'  
GROUP BY name, genre
ORDER BY nombre_de_prod DESC LIMIT 1)
UNION
(SELECT genre, name, count(*) as nombre_de_prod
FROM participate pa
LEFT JOIN production p ON pa.pid = p.uid
LEFT JOIN company c ON pa.cid = c.uid
WHERE production_year = 2000 AND p.genre = 'Thriller'  
GROUP BY name, genre
ORDER BY nombre_de_prod DESC LIMIT 1)
UNION 
(SELECT genre, name, count(*) as nombre_de_prod
FROM participate pa
LEFT JOIN production p ON pa.pid = p.uid
LEFT JOIN company c ON pa.cid = c.uid
WHERE production_year = 2000 AND p.genre = 'War'  
GROUP BY name, genre
ORDER BY nombre_de_prod DESC LIMIT 1)
UNION
(SELECT genre, name, count(*) as nombre_de_prod
FROM participate pa
LEFT JOIN production p ON pa.pid = p.uid
LEFT JOIN company c ON pa.cid = c.uid
WHERE production_year = 2000 AND p.genre = 'Western'  
GROUP BY name, genre
ORDER BY nombre_de_prod DESC LIMIT 1);""",
    ("Production genre", "Company name", "# of productions")],

    ["People who worked with relatives on a production",
    """SELECT c1.prodid, p1.last_name, p1.first_name, p2.last_name, p2.first_name
FROM casting c1
LEFT JOIN person p1 ON c1.perid = p1.uid
LEFT JOIN casting c2 ON c1.prodid = c2.prodid
LEFT JOIN person p2 ON c2.perid = p2.uid
WHERE p1.uid <> p2.uid AND p1.last_name = p2.last_name ;""",
    ("Production id", "Person's first name", "Person's last name",
        "Relative's first name", "Relative's last name")],

    ["Average number of actors per production per year",
    """SELECT p.production_year, COUNT(*) / COUNT(DISTINCT p.uid)
FROM casting c
LEFT JOIN production p ON c.prodid = p.uid
WHERE c.role = 'actor' OR c.role = 'actress' 
GROUP BY p.production_year
ORDER BY p.production_year;""",
    ("Year of production", "Average number of actors")],

    ["Average number of episodes per season",
    """SELECT AVG(num) 
FROM (  SELECT COUNT(*) AS num
    FROM episode
    GROUP BY sid, season
    ) AS nb_episode;""",
    ("Average number of episodes",)],

    ["Average number of seasons per tv show",
    """SELECT AVG (numb) 
FROM    (SELECT count(DISTINCT season) AS numb
    FROM episode
    GROUP BY sid
    ) AS count;""",
    ("Average number of seasons",)],

    ["Top 10 tv shows in number of seasons",
    """SELECT p.title, COUNT( DISTINCT e.season ) AS nb_seasons
FROM episode AS e, production AS p
WHERE p.uid = e.sid AND p.kind = 'tv series'
GROUP BY p.uid
ORDER BY nb_seasons DESC
LIMIT 10 ;""",
    ("Production title", "# of seasons")],

    ["Top 10 tv shows in number of episodes per season",
    """SELECT p.title, 
(count(e.episode) / 
    CASE COUNT( DISTINCT e.season ) WHEN 0 THEN 1 ELSE COUNT( DISTINCT e.season ) END) AS nb_episode_p_season
FROM episode AS e
INNER JOIN production AS p ON p.uid = e.sid AND p.kind = 'tv series'
GROUP BY p.uid
ORDER BY nb_episode_p_season DESC
LIMIT 10 ;""",
    ("Production title", "# of episodes")],

    ["Persons having a movie released after their death",
    """SELECT per.first_name, per.last_name, per.death 
FROM person As per
LEFT OUTER JOIN casting AS c ON (per.uid = c.perid AND per.death IS NOT NULL)
LEFT OUTER JOIN production AS prod ON (prod.uid = c.prodid)
WHERE (prod.production_year > EXTRACT( YEAR FROM per.death) AND c.role = 'actor' ) OR
    (prod.production_year > EXTRACT( YEAR FROM per.death) AND c.role = 'actress' ) OR
(prod.production_year > EXTRACT( YEAR FROM per.death) AND c.role = 'director');""",
    ("First name", "Last name", "Death date")],

    ["Top 3 companies per year in number of movies released",
    """SELECT DISTINCT production_year AS year, comp.name, num_movie, Rank
FROM(
    SELECT DISTINCT *, RANK() OVER (PARTITION BY production_year ORDER BY num_movie DESC) AS Rank
    FROM (
        SELECT part.cid, prod.production_year, COUNT(*) AS num_movie
        FROM production AS prod
        JOIN participate AS part ON prod.uid = part.pid
        WHERE prod.production_year IS NOT NULL
        GROUP BY part.cid, prod.production_year
    ) AS MoviesPerCompanyInAYear
) AS MoviesPerCompanyInAYearWithRank
JOIN company AS comp ON comp.uid = cid
WHERE Rank <= 3
ORDER BY production_year, num_movie DESC;""",
    ("Year of production", "Company name", "# of productions", "Ranking")],

    ["All living opera singers, ordered by age",
    """SELECT first_name, last_name, DATE_PART('year',NOW())-DATE_PART('year', birth) AS age
FROM person
WHERE (biography LIKE '% opera singer %' AND death IS NULL) OR
(trivia LIKE '% opera singer %' AND death IS NULL)
ORDER BY age ASC ;""",
    ("First name", "Last name", "Age")],

    ["Top 10 most ambiguous credits",
    """SELECT prod.title, prod.production_year, per.first_name, per.last_name, prod.nb_alias * per.nb_alias AS deg_ambig
FROM
(
    SELECT per.uid, per.first_name, per.last_name, count(*)+1 as nb_alias
    FROM person AS per
    INNER JOIN alternative_name AS a_name ON a_name.pid = per.uid
    GROUP BY per.uid
) AS per,
(
    SELECT prod.uid, prod.title, prod.production_year, count(*)+1 as nb_alias
    FROM production AS prod
    INNER JOIN alternative_title AS a_title ON prod.uid = a_title.pid
    GROUP BY prod.uid
) AS prod
WHERE EXISTS ( 
    SELECT *
    FROM casting AS cas
    WHERE cas.prodid = prod.uid AND cas.perid = per.uid
)
ORDER BY deg_ambig DESC
LIMIT 10 ;""",
    ("Production title", "Production year", "Person's first name",
        "Person's last name", "Ambiguity level")],

    ["Most frequent character name per country per prod comp",
    """SELECT  country_code, name, name_tot
FROM(
    SELECT DISTINCT *, RANK() OVER (PARTITION BY country_code ORDER BY name_tot DESC) AS rank
    FROM (
        SELECT DISTINCT comp.country_code, char.name, COUNT(*) AS name_tot
       FROM company as comp
    JOIN participate as part ON part.cid=comp.uid AND part.type= 'production company'
    JOIN production as prod ON prod.uid = part.pid
    JOIN casting AS cas ON prod.uid = cas.prodid
    JOIN character AS char ON char.uid = cas.cid
        WHERE comp.country_code IS NOT NULL
        GROUP BY comp.country_code, char.name
    ) AS NameWithNameCountPerCountry
) AS NameWithNameCountPerCountryWithRank
WHERE rank <= 1
ORDER BY country_code ASC;""",
    ("Country code", "Character name", "# of occurences")]]

search_queries = {
    'Person': """SELECT * FROM Person
    WHERE last_name LIKE 'P_PH %(keyword)s P_PH'
    OR first_name LIKE 'P_PH %(keyword)s P_PH'
    OR trivia LIKE 'P_PH %(keyword)s P_PH'
    OR quotes LIKE 'P_PH %(keyword)s P_PH'
    OR biography LIKE 'P_PH %(keyword)s P_PH'
    OR spouse LIKE 'P_PH %(keyword)s P_PH'
    LIMIT 600;""",
    'Production': """SELECT * FROM Production
    WHERE title LIKE 'P_PH %(keyword)s P_PH'
    OR kind::text = '%(keyword)s'
    OR genre LIKE 'P_PH %(keyword)s P_PH'
    LIMIT 600""",
    'Character': """SELECT * FROM Character
    WHERE name LIKE 'P_PH %(keyword)s P_PH'
    LIMIT 600;""",
    'Company': """SELECT * FROM Company
    WHERE name LIKE 'P_PH %(keyword)s P_PH'
    OR country_code LIKE 'P_PH %(keyword)s P_PH'
    LIMIT 600;"""}

keywords = ["Person", "Production", "Character", "Company"]

def index(request):

    context = {'queries': required_queries, 'range': range(len(required_queries)), 'keywords': keywords}

    return render(request, 'application/index.html', context)



def result(request, query_index):
    query_index = int(query_index)
    if query_index >= len(required_queries):
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
    context = {'queries': required_queries, 'query_name': current[0],
        'query_result': result_array,
        'col_title': current[2]}
    
    return render(request, 'application/result.html', context)

def search_result(request):

    selected_table = "Person"
    keyword = "No search keyword"
    try:
        selected_table = request.POST['kw_choice']
        keyword = request.POST['keyword']
    except KeyError:
        raise Http404("ya dun goofed") 

    filler = {'keyword': keyword}
    current = (search_queries[selected_table] % filler)
    current = current.replace("P_PH", '%')

    # opening connection to the database
    cur = connection.cursor()

    # do the selection

    cur.execute(current)
    connection.commit()


    # fetch the result 
    result_array = cur.fetchall()
    columns = [col[0] for col in cur.description]

    # we close everything db related
    cur.close()
    connection.close()

    # [["Bidon", "Bbb"],["Citron", "ccc"]]
    context = {'queries': required_queries, 'keyword': keyword,
        'selected': selected_table, 'query_result': result_array,
        'col_title': columns}
    
    return render(request, 'application/search_result.html', context)