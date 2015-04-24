-- Nb of movies per production year.
SELECT production_year, COUNT(*) FROM production
    WHERE (kind = 'movie'
        OR kind = 'tv movie'
        OR kind = 'video movie')
        AND production_year IS NOT NULL
    GROUP BY production_year
    ORDER BY production_year ASC;

-- Top 10 countries with the most production companies
SELECT c.country_code, COUNT(DISTINCT c.uid) AS count FROM company c
    LEFT JOIN participate par ON c.uid = par.cid
    WHERE par.type = 'production companies'
        AND c.country_code IS NOT NULL
    GROUP BY c.country_code
    ORDER BY count DESC
    LIMIT 10;

-- Min, Max, Avg height of female persons
SELECT MIN(height) AS min_height, MAX(height) AS max_height,
    AVG(height) AS avg_height FROM person
    WHERE gender = 'f';