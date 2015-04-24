-- List the three most popular character names

SELECT name, COUNT(*) AS amount
FROM character
GROUP BY name
ORDER BY amount DESC LIMIT 3