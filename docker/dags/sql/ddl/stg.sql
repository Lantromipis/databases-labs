CREATE SCHEMA IF NOT EXISTS stg;
SET SEARCH_PATH TO stg;

/* Mongo */
CREATE TABLE IF NOT EXISTS mongo_clients
(
    id           BIGSERIAL PRIMARY KEY,
    original_id  TEXT NOT NULL UNIQUE,
    json_value   TEXT NOT NULL,
    updated_when TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mongo_restaurants
(
    id           BIGSERIAL PRIMARY KEY,
    original_id  TEXT NOT NULL UNIQUE,
    json_value   TEXT NOT NULL,
    updated_when TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mongo_orders
(
    id           BIGSERIAL PRIMARY KEY,
    original_id  TEXT NOT NULL UNIQUE,
    json_value   TEXT NOT NULL,
    updated_when TIMESTAMP
);

/* Postgres */

CREATE TABLE IF NOT EXISTS postgres_category
(
    id          BIGSERIAL PRIMARY KEY,
    original_id BIGINT NOT NULL UNIQUE,
    name        VARCHAR(256),
    percent     DOUBLE PRECISION,
    min_payment DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS postgres_client
(
    id            BIGSERIAL PRIMARY KEY,
    original_id   BIGINT NOT NULL UNIQUE,
    bonus_balance DOUBLE PRECISION,
    category_id   BIGINT
);

CREATE TABLE IF NOT EXISTS postgres_dish
(
    id          BIGSERIAL PRIMARY KEY,
    original_id BIGINT NOT NULL UNIQUE,
    name        VARCHAR(256),
    price       DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS postgres_payment
(
    id          BIGSERIAL PRIMARY KEY,
    original_id BIGINT NOT NULL UNIQUE,
    client_id   BIGINT,
    dish_id     BIGINT,
    dish_amount INTEGER,
    order_id    BIGINT,
    order_time  TIMESTAMP,
    order_sum   DOUBLE PRECISION,
    tips        DOUBLE PRECISION
);

/* API */

CREATE TABLE IF NOT EXISTS api_deliveryman
(
    id           BIGSERIAL PRIMARY KEY,
    original_id  TEXT NOT NULL UNIQUE,
    json_value   TEXT NOT NULL,
    updated_when TIMESTAMP
);

CREATE TABLE IF NOT EXISTS api_delivery
(
    id           BIGSERIAL PRIMARY KEY,
    original_id  TEXT NOT NULL UNIQUE,
    json_value   TEXT NOT NULL,
    updated_when TIMESTAMP
);

/* settings */

CREATE TABLE IF NOT EXISTS settings
(
    key   VARCHAR(128) PRIMARY KEY,
    value TEXT
);