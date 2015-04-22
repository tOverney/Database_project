-- Compute the min, max and average height of female persons

SELECT DISTINCT MIN(height) as min_height, MAX(height) as max_height, AVG(height) as avg_height
FROM person
WHERE gender = 'f'