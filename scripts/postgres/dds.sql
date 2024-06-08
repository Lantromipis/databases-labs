CREATE SCHEMA dds;
SET SEARCH_PATH TO dds;

CREATE TABLE dm_deliveryman
(
    id   BIGINT PRIMARY KEY,
    name TEXT
);

CREATE TABLE dm_order
(
    id BIGINT PRIMARY KEY,
    final_status TEXT,
    cost DOUBLE PRECISION,
    order_date TIMESTAMP
);

CREATE TABLE dm_delivery
(
    id BIGINT PRIMARY KEY,
    deliveryman_id BIGINT REFERENCES dm_deliveryman (id),
    order_id BIGINT REFERENCES dm_order (id),
    rating SMALLINT,
    tips DOUBLE PRECISION
);