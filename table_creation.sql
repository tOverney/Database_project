CREATE TABLE Person
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

CREATE TABLE AlternativeName
   (uid INTEGER NOT NULL,
    pid INTEGER NOT NULL,
    name CHAR(60) NOT NULL,
    primary key (uid)
    foreign key (pid) references Person(uid),
    ON DELETE CASCADE);

CREATE TABLE Character
   (uid INTEGER NOT NULL,
    name CHAR(60) NOT NULL,
    primary key (uid),
    );

CREATE TYPE CAST_ROLE AS
    ENUM ('actor', 'actress', 'producer', 'writer', 'cinematographer',
    'composer', 'costume designer', 'director', 'editor', 'miscellaneous crew',
    'production designer');

CREATE TABLE Cast
   (cid INTEGER,
    perid INTEGER NOT NULL,
    prodid INTEGER NOT NULL,
    rid CAST_ROLE NOT NULL,
    primary key (cid, perid, prodid, role),
    foreign key (cid) references Character (uid),
    foreign key (perid) references Person (uid),
    foreign key (prodid) references Production (uid)
    foreign key (rid) references Role (uid));

CREATE TABLE Production
   (uid INTEGER NOT NULL,
    title CHAR(80) NOT NULL,
    production_year DATE,
    series_years CHAR (11),
    genre CHAR(20),
    primary key (uid));

CREATE TABLE Episode
   (sid INTEGER NOT NULL,
    season SMALLINT NOT NULL,
    episode SMALLINT NOT NULL,
    foreign key (sid) references TvSerie (uid);
    primary key (uid)) INHERITS (Production);

CREATE TABLE TvSerie
    (primary key (uid)) INHERITS (Production);

CREATE TABLE TvMovie
    (primary key (uid)) INHERITS (Production);

CREATE TABLE Movie
    (primary key (uid)) INHERITS (Production);

CREATE TABLE VideoMovie
    (primary key (uid)) INHERITS (Production);

CREATE TABLE VideoGame
    (primary key (uid)) INHERITS (Production);

CREATE TYPE COMPANY_TYPE AS ENUM ('distributors', 'production company');

CREATE TABLE Participate
   (pid INTEGER NOT NULL,
    cid INTEGER NOT NULL,
    type COMPANY_TYPE NOT NULL,
    primary key (pid, cid)
    foreign key (pid) references Production(uid),
    foreign key (cid) references Company(uid));

CREATE TABLE Company
   (uid INTEGER NOT NULL,
    name CHAR(80) NOT NULL,
    country_code CHAR(6),
    primary key (uid));

CREATE TABLE AlternativeTitle
   (uid INTEGER NOT NULL,
    pid INTEGER NOT NULL,
    title CHAR (80) NOT NULL,
    primary key (uid, pid)
    foreign key (pid) references Production (uid),
    ON DELETE CASCADE);