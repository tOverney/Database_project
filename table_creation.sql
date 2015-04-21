CREATE TABLE person
   (uid INTEGER NOT NULL,
    first_name TEXT,
    last_name TEXT NOT NULL,
    gender CHAR(1),
    trivia TEXT,
    quotes TEXT,
    birth DATE,
    death DATE,
    biography TEXT,
    spouse TEXT,
    height DOUBLE PRECISION,
    birth_name TEXT,
    primary key (uid));

CREATE TABLE alternative_name
   (uid INTEGER NOT NULL,
    pid INTEGER NOT NULL,
    name TEXT NOT NULL,
    primary key (uid),
    foreign key (pid) references person(uid)
    ON DELETE CASCADE);

CREATE TABLE character
   (uid INTEGER NOT NULL,
    name TEXT NOT NULL,
    primary key (uid));

CREATE TYPE CAST_ROLE AS
    ENUM ('actor', 'actress', 'producer', 'writer', 'cinematographer',
    'composer', 'costume designer', 'director', 'editor', 'miscellaneous crew',
    'production designer');

CREATE TYPE PRODUCTION_KIND AS
    ENUM ('tv series', 'episode', 'movie', 'video movie',
    'tv movie', 'video game');

CREATE TABLE production
   (uid INTEGER NOT NULL,
    title TEXT NOT NULL,
    production_year INT,
    kind PRODUCTION_KIND,
    genre CHAR(20),
    primary key (uid));

CREATE TABLE casting
   (uid SERIAL,
    cid INTEGER,
    perid INTEGER NOT NULL,
    prodid INTEGER NOT NULL,
    role CAST_ROLE NOT NULL,
    primary key (uid),
    foreign key (cid) references character (uid),
    foreign key (perid) references person (uid),
    foreign key (prodid) references production (uid));


CREATE TABLE tv_series
   (uid INTEGER NOT NULL,
    series_years CHAR(10),
    primary key (uid),
    foreign key (uid) references production (uid));

CREATE TABLE episode
   (uid INTEGER NOT NULL,
    sid INTEGER NOT NULL,
    season SMALLINT,
    episode INTEGER,
    primary key (uid),
    foreign key (uid) references production (uid),
    foreign key (sid) references tv_serie (uid)
    ON DELETE CASCADE);

CREATE TYPE COMPANY_TYPE AS ENUM ('distributors', 'production companies');

CREATE TABLE company
   (uid INTEGER NOT NULL,
    country_code CHAR(6),
    name TEXT NOT NULL,
    primary key (uid));

CREATE TABLE participate
   (uid INTEGER NOT NULL,
    pid INTEGER NOT NULL,
    cid INTEGER NOT NULL,
    type COMPANY_TYPE NOT NULL,
    primary key (uid),
    foreign key (pid) references production(uid),
    foreign key (cid) references company(uid));

CREATE TABLE alternative_title
   (uid INTEGER NOT NULL,
    pid INTEGER NOT NULL,
    title TEXT NOT NULL,
    primary key (uid),
    foreign key (pid) references production (uid)
    ON DELETE CASCADE);