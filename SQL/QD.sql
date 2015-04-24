-- Compute the min, max and average number of actors in a production

SELECT avg(numb) AS avg_nb_act, MAX(numb) AS max_nb_act, MIN(numb) AS min_nb_act
FROM (	SELECT count(*) as numb
	FROM casting
	WHERE role = 'actor'
	GROUP BY prodid) as number