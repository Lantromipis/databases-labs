CREATE SCHEMA IF NOT EXISTS dds;
SET SEARCH_PATH TO dds;

CREATE TABLE IF NOT EXISTS dm_time
(
    id        BIGSERIAL PRIMARY KEY NOT NULL,
    time_mark TIMESTAMP,
    year      SMALLINT CHECK ( year > 2022 ),
    month     SMALLINT CHECK ( month >= 1 AND month <= 12 ),
    day       SMALLINT CHECK ( day >= 1 AND day <= 31),
    time      TIME,
    date      DATE
);

CREATE TABLE IF NOT EXISTS dm_deliveryman
(
    id   BIGINT PRIMARY KEY NOT NULL,
    name TEXT
);

CREATE TABLE IF NOT EXISTS dm_order
(
    id            BIGINT PRIMARY KEY NOT NULL,
    final_status  TEXT,
    cost          DOUBLE PRECISION,
    order_time_id BIGINT REFERENCES dm_time (id)
);

CREATE TABLE IF NOT EXISTS dm_delivery
(
    id             BIGINT PRIMARY KEY                    NOT NULL,
    deliveryman_id BIGINT REFERENCES dm_deliveryman (id) NOT NULL,
    order_id       BIGINT REFERENCES dm_order (id)       NOT NULL,
    rating         SMALLINT,
    tips           DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS settings
(
    key   VARCHAR(128) PRIMARY KEY,
    value TEXT
);