-- Nb of movies per production year.
SELECT production_year, COUNT(*) FROM production
    WHERE (kind = 'movie'
        OR kind = 'tv movie'
        OR kind = 'video movie')
        AND production_year IS NOT NULL
    GROUP BY production_year
    ORDER BY production_year ASC;


-- Top 10 countries with the most production companies
SELECT c.country_code, COUNT(DISTINCT c.uid) AS count FROM company c
    LEFT JOIN participate par ON c.uid = par.cid
    WHERE par.type = 'production companies'
        AND c.country_code IS NOT NULL
    GROUP BY c.country_code
    ORDER BY count DESC
    LIMIT 10;


-- compute the min, max and average career duration
SELECT avg(duration) AS avg_duration, MAX(duration) AS max_duration,
    MIN(duration) AS min_duration
FROM (
    SELECT (1+(MAX(prod.production_year)-MIN(prod.production_year ))) AS duration
    FROM casting c, production prod
    WHERE c.prodid = prod.uid
    GROUP BY c.perid) AS career_duration;


-- Compute the min, max and average number of actors in a production
SELECT avg(numb) AS avg_nb_act, MAX(numb) AS max_nb_act, MIN(numb) AS min_nb_act
FROM (  SELECT count(*) AS numb
    FROM casting
    WHERE role = 'actor'
    GROUP BY prodid) AS number;


-- Min, Max, Avg height of female persons
SELECT MIN(height) AS min_height, MAX(height) AS max_height,
    AVG(height) AS avg_height FROM person
    WHERE gender = 'f';


-- List all pairs of persons and movies where the person has both directed
-- the movie and acted in the movie. Do not include tv and videos movies
SELECT per.first_name, per.last_name, p.title
    FROM casting c, person per, production p
    WHERE per.uid = c.perid AND p.uid = c.prodid AND c.role = 'director' 
    AND c.prodid IN (SELECT prod.uid
             FROM production prod
             WHERE prod.kind = 'movie') -- to take only movies
    AND c.perid IN (SELECT c1.perid
            FROM casting c1
            WHERE c.prodid = c1.prodid AND role = 'actor') 
    AND c.perid < 2000


-- My version
SELECT p2.uid, p1.uid, person.first_name, person.last_name, prod.title, p1.role, p2.role FROM casting p1
    LEFT JOIN casting p2
        ON p1.prodid = p2.prodid AND p1.perid = p2.perid
    LEFT JOIN person
        ON p1.perid = person.uid
    LEFT JOIN production prod
        ON p1.prodid = prod.uid
    WHERE p1.role='director' AND p2.role='actor';


-- List the three most popular character names
SELECT name, COUNT(*) AS amount
    FROM character
    GROUP BY name
    ORDER BY amount DESC LIMIT 3;