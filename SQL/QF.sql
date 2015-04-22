-- List all pairs of persons and movies where the person has both directed
-- the movie and acted in the movie. Do not include tv and videos movies

SELECT per.first_name, per.last_name, p.title
FROM casting c, person per, production p
WHERE per.uid = c.perid AND p.uid = c.prodid AND c."role" = 'director' 
AND c.prodid IN (SELECT prod.uid
		 FROM production prod
		 WHERE prod.kind = 'movie') -- to take only movies
AND c.perid IN (SELECT c1.perid
		FROM casting c1
		WHERE c.prodid = c1.prodid AND "role" = 'actor') 
AND c.perid < 2000		

