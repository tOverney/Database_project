-- A (503031 ms = 8min 23sc)
SELECT DISTINCT p1.uid as person_id, c1.prodid as production_id
FROM person p1
LEFT JOIN casting c1 ON p1.uid = c1.perid
LEFT JOIN casting c2 ON c1.prodid = c2.prodid
LEFT JOIN person p2 ON c2.perid = p2.uid
WHERE (p1.birth IS NOT NULL AND p2.birth IS NOT NULL AND p1.uid <> p2.uid AND p1.birth >= p2.birth + 55 * interval '1 year') 
OR (p1.birth IS NOT NULL AND p2.birth IS NOT NULL AND p1.uid <> p2.uid AND p1.birth >= p2.birth + 55 * interval '1 year' )
OR (p1.birth IS NOT NULL AND p2.birth IS NOT NULL AND p1.uid <> p2.uid AND p1.birth >= p2.birth + 55 * interval '1 year' )
OR (p1.birth IS NOT NULL AND p2.birth IS NOT NULL AND p1.uid <> p2.uid AND p1.birth >= p2.birth + 55 * interval '1 year');


-- B ( ex: Bradley Cooper: 1951ms = 2sc / Marion Cotillard: 551ms   )
SELECT production_year
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
	) AS year;


-- C (for year 2000 : 83054ms = 1min 23sc)
(SELECT genre, name, count(*) as nombre_de_prod
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
ORDER BY nombre_de_prod DESC LIMIT 1)

-- D (1772692ms = 29.54 min)
SELECT c1.prodid, p1.last_name, p1.first_name, p2.last_name, p2.first_name
FROM casting c1
LEFT JOIN person p1 ON c1.perid = p1.uid
LEFT JOIN casting c2 ON c1.prodid = c2.prodid
LEFT JOIN person p2 ON c2.perid = p2.uid
WHERE p1.uid <> p2.uid AND p1.last_name = p2.last_name ;

-- E ( 397676.537 ms = 6 min 37 s)
SELECT p.production_year, COUNT(*) / COUNT(DISTINCT p.uid)
FROM casting c
LEFT JOIN production p ON c.prodid = p.uid
WHERE c.role = 'actor' OR c.role = 'actress' 
GROUP BY p.production_year
ORDER BY p.production_year; 	-- pas certaine d'avoir compris ce qu'ils voulaient exactement mais ça semble  être le nombre 
				-- d'acteur moyen par production par année
-- F ( 12428.628 ms = 12.42 s )
SELECT AVG(num) 
FROM (	SELECT COUNT(*) AS num
	FROM episode
	GROUP BY sid, season
	) AS nb_episode;

--G (19411ms = 19sc )
SELECT AVG (numb) 
FROM 	(SELECT count(DISTINCT season) AS numb
	FROM episode
	GROUP BY sid
	) AS count;			