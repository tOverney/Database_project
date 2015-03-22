CREATE TABLE person
   (uid INTEGER NOT NULL,
    first_name CHAR(75) NOT NULL,
    last_name CHAR(75) NOT NULL,
    gender CHAR(1),
    trivia TEXT,
    quotes VARCHAR(4000),
    birth DATE,
    death DATE,
    biography TEXT,
    spouse CHAR(100),
    height DOUBLE PRECISION,
    primary key (uid));

CREATE TABLE alternative_name
   (uid INTEGER NOT NULL,
    pid INTEGER NOT NULL,
    name CHAR(60) NOT NULL,
    primary key (uid),
    foreign key (pid) references person(uid)
    ON DELETE CASCADE);

CREATE TABLE character
   (uid INTEGER NOT NULL,
    name CHAR(60) NOT NULL,
    primary key (uid));

CREATE TYPE CAST_ROLE AS
    ENUM ('actor', 'actress', 'producer', 'writer', 'cinematographer',
    'composer', 'costume designer', 'director', 'editor', 'miscellaneous crew',
    'production designer');

CREATE TABLE production
   (uid INTEGER NOT NULL,
    title CHAR(80) NOT NULL,
    production_year DATE,
    series_years CHAR (11),
    genre CHAR(20),
    primary key (uid));

CREATE TABLE casting
   (cid INTEGER,
    perid INTEGER NOT NULL,
    prodid INTEGER NOT NULL,
    role CAST_ROLE NOT NULL,
    primary key (cid, perid, prodid, role),
    foreign key (cid) references character (uid),
    foreign key (perid) references person (uid),
    foreign key (prodid) references production (uid));


CREATE TABLE tv_serie
    (primary key (uid)) INHERITS (Production);

CREATE TABLE episode
   (sid INTEGER NOT NULL,
    season SMALLINT NOT NULL,
    episode SMALLINT NOT NULL,
    primary key (uid),
    foreign key (sid) references tv_serie (uid)) INHERITS (production);

CREATE TABLE tv_movie
    (primary key (uid)) INHERITS (production);

CREATE TABLE movie
    (primary key (uid)) INHERITS (production);

CREATE TABLE video_movie
    (primary key (uid)) INHERITS (production);

CREATE TABLE video_game
    (primary key (uid)) INHERITS (production);

CREATE TYPE COMPANY_TYPE AS ENUM ('distributors', 'production company');

CREATE TABLE company
   (uid INTEGER NOT NULL,
    name CHAR(80) NOT NULL,
    country_code CHAR(6),
    primary key (uid));

CREATE TABLE participate
   (pid INTEGER NOT NULL,
    cid INTEGER NOT NULL,
    type COMPANY_TYPE NOT NULL,
    primary key (pid, cid),
    foreign key (pid) references production(uid),
    foreign key (cid) references company(uid));

CREATE TABLE alternative_title
   (uid INTEGER NOT NULL,
    pid INTEGER NOT NULL,
    title CHAR (80) NOT NULL,
    primary key (uid),
    foreign key (pid) references production (uid)
    ON DELETE CASCADE);