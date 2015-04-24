-- List the three most popular character names

SELECT DISTINCT "name", COUNT(*) as numb
FROM "character"
GROUP BY "name"
ORDER BY numb DESC LIMIT 3