--h) Compute the top ten tv-series (number of seasons)- compute time 17.326 secondes (on LASIG computer)


SELECT p.title, COUNT( DISTINCT e.season ) AS nb_seasons
FROM episode AS e, production AS p
WHERE p.uid = e.sid AND p.kind = 'tv series'
GROUP BY p.uid
ORDER BY nb_seasons DESC
LIMIT 10 ;

--i) Compute the top ten tv-series (number of episodes per season)

SELECT p.title, 
( 
	count(e.episode) / 
	CASE COUNT( DISTINCT e.season ) AS nb_seasons 
		WHEN 0 THEN 1
		ELSE nb_seasons
	END
) AS nb_episode_p_season
FROM episode AS e
INNER JOIN production AS p ON p.uid = e.sid AND p.kind = 'tv series'
GROUP BY p.uid
ORDER BY nb_episode_p_season DESC
LIMIT 10 ;


--j) Find actors, actresses and directors who have movies (including tv movies and video movies) released after their death.

-- Elle n'est jamais arrivée à la fin (lancée en commande à distance, ssh) et je n'ais pas encore trouvé mieu qu'un self-join bien dégueux...

SELECT relA.*
FROM
(
	SELECT production_year, name, count(prod.uid) AS nb_release
	FROM company AS comp 
	INNER JOIN participate AS part ON comp.uid=part.cid
	INNER JOIN production AS prod ON part.pid = prod.uid AND prod.kind = 'movie' AND prod.production_year IS NOT NULL
	GROUP BY production_year,comp.uid
) AS relA,
(
	SELECT production_year, name, count(prod.uid) AS nb_release
	FROM company AS comp 
	INNER JOIN participate AS part ON comp.uid=part.cid
	INNER JOIN production AS prod ON part.pid = prod.uid AND prod.kind = 'movie' AND prod.production_year IS NOT NULL
	GROUP BY production_year,comp.uid
) AS relB
WHERE relB.nb_release>=relA.nb_release AND relB.production_year = relA.production_year
GROUP BY relA.production_year, relA.name, relA.nb_release
HAVING count(relB.*)<= 3
ORDER BY relA.production_year DESC, nb_release DESC ;

-- l) Give every person how have 'opera singer' in their biography (only place where it appears) order from the younger to the older

SELECT first_name, last_name, DATE_PART('year',NOW())-DATE_PART('year', birth) AS age
FROM person
WHERE biography LIKE '% opera singer %' AND death IS NULL
ORDER BY age ASC ;


-- m) List of the 10 most ambiguous credits  11min 2s
SELECT prod.title, prod.production_year, per.first_name, per.last_name, prod.nb_alias * per.nb_alias AS nb_ambig
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
ORDER BY nb_ambig DESC
LIMIT 10 ;

--n) Same problem as j)
SELECT c.country_code, ch.name, COUNT(*) AS total_use FROM company c
 INNER JOIN participate pc ON pc.cid = c.uid
 INNER JOIN casting cas ON pc.pid = cas.prodid
 INNER JOIN character ch ON ch.uid = cas.cid
 WHERE cas.cid IS NOT NULL AND c.country_code IS NOT NULL
 GROUP BY c.country_code, ch.name
 ORDER BY total_use DESC;