--h) Compute the top ten tv-series (number of seasons)- compute time 17.326 secondes (on LASIG computer)


SELECT p.title, COUNT( DISTINCT e.season ) AS nb_seasons
FROM episode AS e, production AS p
WHERE p.uid = e.sid AND p.kind = 'tv series'
GROUP BY p.uid
ORDER BY nb_seasons DESC
LIMIT 10 ;

--i) Compute the top ten tv-series (number of episodes per season) 20.416 secondes (ssh connection)
SELECT p.title, 
(count(e.episode) / 
	CASE COUNT( DISTINCT e.season ) WHEN 0 THEN 1 ELSE COUNT( DISTINCT e.season ) END) AS nb_episode_p_season
FROM episode AS e
INNER JOIN production AS p ON p.uid = e.sid AND p.kind = 'tv series'
GROUP BY p.uid
ORDER BY nb_episode_p_season DESC
LIMIT 10 ;


--j) Find actors, actresses and directors who have movies (including tv movies and video movies) released after their death : 111.231 secondes (ssh)

SELECT per.first_name, per.last_name, per.death 
FROM person As per
LEFT OUTER JOIN casting AS c ON (per.uid = c.perid AND per.death IS NOT NULL)
LEFT OUTER JOIN production AS prod ON (prod.uid = c.prodid)
WHERE (prod.production_year > EXTRACT( YEAR FROM per.death) AND c.role = 'actor' ) OR
	(prod.production_year > EXTRACT( YEAR FROM per.death) AND c.role = 'actress' ) OR
(prod.production_year > EXTRACT( YEAR FROM per.death) AND c.role = 'director');

-- k) Elle n'est jamais arrivée à la fin (lancée en commande à distance, ssh) et je n'ais pas encore trouvé mieu qu'un self-join bien dégueux...


SELECT relA.*
FROM
(
	SELECT production_year, name, count(prod.uid) AS nb_release
	FROM company AS comp 
	LEFT JOIN participate AS part ON comp.uid=part.cid
	LEFT JOIN production AS prod ON part.pid = prod.uid AND prod.kind = 'movie' AND prod.production_year IS NOT NULL
	GROUP BY production_year,comp.uid
) AS relA,
(
	SELECT production_year, name, count(prod.uid) AS nb_release
	FROM company AS comp 
	LEFT JOIN participate AS part ON comp.uid=part.cid
	LEFT JOIN production AS prod ON part.pid = prod.uid AND prod.kind = 'movie' AND prod.production_year IS NOT NULL
	GROUP BY production_year,comp.uid
) AS relB
WHERE relB.nb_release>=relA.nb_release AND relB.production_year = relA.production_year
GROUP BY relA.production_year, relA.name, relA.nb_release
HAVING count(relB.*)<= 3
ORDER BY relA.production_year DESC, nb_release DESC ;


-- l) Give every person how have 'opera singer' in their biography (only place where it appears) order from the younger to the older : 7.277 secondes (ssh)

SELECT first_name, last_name, DATE_PART('year',NOW())-DATE_PART('year', birth) AS age
FROM person
WHERE (biography LIKE '% opera singer %' AND death IS NULL) OR
(trivia LIKE '% opera singer %' AND death IS NULL)
ORDER BY age ASC ;


-- m) List of the 10 most ambiguous credits : 648.08 secondes (ssh)
SELECT prod.title, prod.production_year, per.first_name, per.last_name, prod.nb_alias * per.nb_alias AS deg_ambig
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
LIMIT 10 ;

--n) Same problem as j)

SELECT DISTINCT comp.country_code, char.name, count(char.name) as nb_char
FROM company as comp,
(
	SELECT comp.country_code, char.name
	FROM company as comp
	INNER JOIN participate as part ON part.cid=comp.uid AND part.type= 'production company'
	INNER JOIN production as prod ON prod.uid = part.pid
	INNER JOIN casting AS cas ON prod.uid = cas.prodid
	INNER JOIN character AS char ON char.uid = cas.cid
) AS char
WHERE comp.country_code = char.country_code
GROUP BY comp.country_code, char.name
ORDER BY nb_char DESC;

SELECT DISTINCT comp1.country_code, char2.name, char2.nb_char
FROM( SELECT char.name, count(*) as nb_char FROM company as comp
	INNER JOIN participate as part ON part.cid=comp.uid AND part.type= 'production company' AND comp.country_code = comp1.country_code
	INNER JOIN production as prod ON prod.uid = part.pid
	INNER JOIN casting AS cas ON prod.uid = cas.prodid
	INNER JOIN character AS char ON char.uid = cas.cid
	GROUP BY char.name
	ORDER BY nb_char DESC
	LIMIT 1) as char2,
company as comp1;

