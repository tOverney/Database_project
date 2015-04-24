-- Compute the number of movies per year. Make sur to include tv and video movies

SELECT DISTINCT production_year, count(*)
FROM production
GROUP BY production_year 
ORDER BY production_year