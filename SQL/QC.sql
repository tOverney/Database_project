-- compute the min, max and average career duration

SELECT avg(duration), MAX(duration), MIN(duration)
FROM ( SELECT (1+(MAX(prod.production_year)-MIN(prod.production_year ))) as duration
    FROM casting c, production prod
    WHERE c.prodid = prod.uid
    GROUP BY c.perid) as career_duration

