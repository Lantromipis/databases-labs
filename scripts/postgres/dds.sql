CREATE SCHEMA dds;
SET SEARCH_PATH TO dds;

CREATE TABLE dm_deliveryman
(
    id   BIGINT PRIMARY KEY NOT NULL,
    name TEXT
);

CREATE TABLE dm_order
(
    id BIGINT PRIMARY KEY NOT NULL,
    final_status TEXT,
    cost DOUBLE PRECISION,
    order_date TIMESTAMP
);

CREATE TABLE dm_delivery
(
    id BIGINT PRIMARY KEY NOT NULL,
    deliveryman_id BIGINT REFERENCES dm_deliveryman (id) NOT NULL,
    order_id BIGINT REFERENCES dm_order (id) NOT NULL,
    rating SMALLINT,
    tips DOUBLE PRECISION
);