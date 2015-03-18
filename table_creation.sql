CREATE TABLE Person
   (uid INTEGER NOT NULL,
    first_name CHAR(75),
    last_name CHAR(75),
    gender CHAR(1),
    trivia VARCHAR,
    quotes VARCHAR,
    birth DATE,
    death DATE,
    biography VARCHAR,
    spouse CHAR(100),
    primary key (uid));

CREATE TABLE AlternativeName
   (uid INTEGER,
    pid INTEGER,
    name CHAR(60),
    primary key (uid)
    foreign key (pid) references Person(uid),
    ON DELETE CASCADE);

CREATE TABLE Character
   (uid INTEGER,
    name CHAR(60),
    primary key (uid),
    );

CREATE TABLE Cast
   (cid INTEGER,
    perid INTEGER NOT NULL,
    prodid INTEGER NOT NULL,
    role CHAR(20) NOT NULL,
    primary key (cid, perid, prodid, role),
    foreign key (cid) references Character (uid),
    foreign key (perid) references Person (uid),
    foreign key (prodid) references Production (uid));

CREATE TABLE Production
   (uid INTEGER NOT NULL,
    title CHAR(80) NOT NULL,
    currency CHAR(3),
    budget INTEGER,
    primary key (uid));

CREATE TABLE Participate
   (pid INTEGER NOT NULL,
    cid INTEGER NOT NULL,
    type CHAR(20) NOT NULL,
    primary key (pid, cid)
    foreign key (pid) references Production(uid),
    foreign key (pid) references Company(uid));

CREATE TABLE Company
   (uid INTEGER NOT NULL,
    name CHAR(20) NOT NULL,
    country_code CHAR(6),
    primary key (uid));

CREATE TABLE AlternativeTitle
   (uid INTEGER NOT NULL,
    pid INTEGER,
    title CHAR (30),
    primary key (uid, pid)
    foreign key (pid) references Production (uid),
    ON DELETE CASCADE);