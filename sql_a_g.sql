-- A
SELECT DISTINCT p1.uid as person_id, c1.prodid as production_id
FROM person p1
LEFT JOIN casting c1 ON p1.uid = c1.perid
LEFT JOIN casting c2 ON c1.prodid = c2.prodid
LEFT JOIN person p2 ON c2.perid = p2.uid
WHERE (p1.birth IS NOT NULL AND p2.birth IS NOT NULL AND p1.uid <> p2.uid AND AGE(p1.birth) >= AGE(p2.birth) + 55 * interval '1 year') 
OR (p1.birth IS NOT NULL AND p2.birth IS NOT NULL AND p1.uid <> p2.uid AND AGE(p1.birth) >= AGE(p2.birth) + 55 * interval '1 year' )
OR (p1.birth IS NOT NULL AND p2.birth IS NOT NULL AND p1.uid <> p2.uid AND AGE(p1.birth) >= AGE(p2.birth) + 55 * interval '1 year' )
OR (p1.birth IS NOT NULL AND p2.birth IS NOT NULL AND p1.uid <> p2.uid AND AGE(p1.birth) >= AGE(p2.birth) + 55 * interval '1 year');


-- B
SELECT production_year
FROM (
	SELECT production_year, COUNT(*) AS count
	FROM ( SELECT production_year
		FROM person
		LEFT JOIN casting ON person.uid = casting.perid 
		LEFT JOIN production ON casting.prodid = production.uid
		WHERE last_name = 'Damon' AND first_name = 'Matt'
		) AS prod_year
	GROUP BY production_year
	ORDER BY count DESC LIMIT 1
	) AS year;


-- C
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
WHERE production_year = 2000 AND p.genre = 'Comedy'  
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
WHERE production_year = 2000 AND p.genre = 'Adventure'  
GROUP BY name, genre
ORDER BY nombre_de_prod DESC LIMIT 1);   -- continue with each different gender (27 in total)? 

-- D 
SELECT c1.prodid, p1.last_name, p1.first_name, p2.last_name, p2.first_name
FROM casting c1
LEFT JOIN person p1 ON c1.perid = p1.uid
LEFT JOIN casting c2 ON c1.prodid = c2.prodid
LEFT JOIN person p2 ON c2.perid = p2.uid
WHERE p1.uid <> p2.uid AND p1.last_name = p2.last_name ;

-- E
SELECT production_year, AVG(count)
FROM (
	SELECT production_year, prodid, count(*) AS count
	FROM casting c
	LEFT JOIN production p ON c.prodid = p.uid
	WHERE c.role = 'actor' OR c.role = 'actress' 
	GROUP BY prodid, production_year ) AS calcul
GROUP BY production_year; 	-- pas certaine d'avoir compris ce qu'ils voulaient exactement mais ça semble  être le nombre 
				-- d'acteur moyen par production par année
-- F
SELECT AVG(num) 
FROM (	SELECT COUNT(*) AS num
	FROM episode
	GROUP BY sid, season
	) AS nb_episode;

--G
SELECT AVG (numb) 
FROM 	(SELECT count(DISTINCT season) AS numb
	FROM episode
	GROUP BY sid
	) AS count;			