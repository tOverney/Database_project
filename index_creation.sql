CREATE INDEX CONCURRENTLY person_lastname_index ON person(last_name);
CREATE INDEX CONCURRENTLY person_gender_index ON person(gender);

CREATE INDEX CONCURRENTLY production_years_index ON production(production_year);
CREATE INDEX CONCURRENTLY production_genre_index ON production(genre);
CREATE INDEX CONCURRENTLY production_kind_index ON production(kind);