-- Compute the ten countries with most production companies

SELECT DISTINCT country_code, count(*) as numb
FROM company
WHERE country_code IS NOT NULL
GROUP BY country_code
ORDER BY numb DESC LIMIT 10