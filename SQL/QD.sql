-- Compute the min, max and average number of actors in a production

SELECT avg(numb), MAX(numb), MIN(numb)
FROM (	SELECT count(*) as numb
	FROM casting
	WHERE "role" = 'actor'
	GROUP BY prodid) as number