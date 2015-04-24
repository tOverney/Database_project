CREATE INDEX CONCURRENTLY person_lastname_index ON person(last_name);
CREATE INDEX CONCURRENTLY person_gender_index ON person(gender);

CREATE INDEX CONCURRENTLY altname_pid_index ON alternative_name(pid);

CREATE INDEX CONCURRENTLY production_years_index ON production(production_year);
CREATE INDEX CONCURRENTLY production_genre_index ON production(genre);
CREATE INDEX CONCURRENTLY production_kind_index ON production(kind);

CREATE INDEX CONCURRENTLY casting_cid_index ON casting(cid);
CREATE INDEX CONCURRENTLY casting_perid_index ON casting(perid);
CREATE INDEX CONCURRENTLY casting_prodid_index ON casting(prodid);
CREATE INDEX CONCURRENTLY casting_role_index ON casting(role);