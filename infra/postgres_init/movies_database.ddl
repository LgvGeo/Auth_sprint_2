BEGIN;
CREATE SCHEMA IF NOT EXISTS content;
SET LOCAL search_path to content;

CREATE TABLE IF NOT EXISTS film_work (
    id UUID,
    title VARCHAR NOT NULL,
    description VARCHAR,
    creation_date DATE,
    rating FLOAT,
    type VARCHAR NOT NULL,
    created TIMESTAMP WITH TIME ZONE,
    modified TIMESTAMP WITH TIME ZONE,

    PRIMARY KEY (id)
); 

CREATE TABLE IF NOT EXISTS person (
    id UUID,
    full_name VARCHAR NOT NULL,
    created TIMESTAMP WITH TIME ZONE,
    modified TIMESTAMP WITH TIME ZONE,

    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS genre (
    id UUID,
    name VARCHAR NOT NULL,
    description VARCHAR,
    created TIMESTAMP WITH TIME ZONE,
    modified TIMESTAMP WITH TIME ZONE,

    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS genre_film_work (
    id UUID,
    genre_id UUID NOT NULL,
    film_work_id UUID NOT NULL,
    created TIMESTAMP WITH TIME ZONE,

    PRIMARY KEY(id),
    FOREIGN KEY (genre_id) REFERENCES genre (id) ON DELETE CASCADE,
    FOREIGN KEY (film_work_id) REFERENCES film_work (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS person_film_work (
    id UUID,
    person_id UUID NOT NULL,
    film_work_id UUID NOT NULL,
    role VARCHAR NOT NULL,
    created TIMESTAMP WITH TIME ZONE,

    PRIMARY KEY(id),
    FOREIGN KEY (person_id) REFERENCES person (id) ON DELETE CASCADE,
    FOREIGN KEY (film_work_id) REFERENCES film_work (id) ON DELETE CASCADE
);

CREATE UNIQUE INDEX IF NOT EXISTS genre_film_work_idx ON genre_film_work (genre_id, film_work_id);
CREATE UNIQUE INDEX IF NOT EXISTS genre_name_idx ON genre (name);
CREATE UNIQUE INDEX IF NOT EXISTS person_film_work_idx ON person_film_work (film_work_id, person_id, role);

COMMIT;
