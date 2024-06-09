CREATE SCHEMA IF NOT EXISTS src;
SET SEARCH_PATH TO src;

CREATE TABLE IF NOT EXISTS category
(
    category_id BIGSERIAL PRIMARY KEY,
    name        VARCHAR(256),
    percent     DOUBLE PRECISION,
    min_payment DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS client
(
    client_id     BIGSERIAL PRIMARY KEY,
    bonus_balance DOUBLE PRECISION,
    category_id   BIGINT REFERENCES category (category_id)
);

CREATE TABLE IF NOT EXISTS dish
(
    dish_id BIGSERIAL PRIMARY KEY,
    name    VARCHAR(256),
    price   DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS payment
(
    payment_id  BIGSERIAL PRIMARY KEY,
    client_id   BIGINT REFERENCES client (client_id),
    dish_id     BIGINT REFERENCES dish (dish_id),
    dish_amount INTEGER,
    order_id    BIGINT,
    order_time  TIMESTAMP,
    order_sum   DOUBLE PRECISION,
    tips        DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS logs
(
    id         BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(256),
    action     VARCHAR(32),
    time       TIMESTAMP,
    values     TEXT
);

-- category triggers
CREATE OR REPLACE FUNCTION log_category_table_update()
    RETURNS TRIGGER AS
$$
BEGIN
    INSERT INTO logs (table_name, action, time, values) VALUES ('category', 'update', NOW(), ROW_TO_JSON(new));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER category_table_update
    BEFORE UPDATE
    ON category
    FOR EACH ROW
EXECUTE FUNCTION log_category_table_update();

CREATE OR REPLACE FUNCTION log_category_table_insert()
    RETURNS TRIGGER AS
$$
BEGIN
    INSERT INTO logs (table_name, action, time, values) VALUES ('category', 'insert', NOW(), ROW_TO_JSON(new));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER category_table_insert
    AFTER INSERT
    ON category
    FOR EACH ROW
EXECUTE FUNCTION log_category_table_insert();

CREATE OR REPLACE FUNCTION log_category_table_delete()
    RETURNS TRIGGER AS
$$
BEGIN
    INSERT INTO logs (table_name, action, time, values) VALUES ('category', 'delete', NOW(), '');
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER category_table_delete
    BEFORE UPDATE
    ON category
    FOR EACH ROW
EXECUTE FUNCTION log_category_table_delete();

-- dish triggers
CREATE OR REPLACE FUNCTION log_dish_table_row_update()
    RETURNS TRIGGER AS
$$
BEGIN
    INSERT INTO logs (table_name, action, time, values) VALUES ('dish', 'update', NOW(), ROW_TO_JSON(new));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER dish_table_row_update
    BEFORE UPDATE
    ON dish
    FOR EACH ROW
EXECUTE FUNCTION log_dish_table_row_update();

CREATE OR REPLACE FUNCTION log_dish_table_row_insert()
    RETURNS TRIGGER AS
$$
BEGIN
    INSERT INTO logs (table_name, action, time, values) VALUES ('dish', 'insert', NOW(), ROW_TO_JSON(new));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER dish_table_row_insert
    AFTER INSERT
    ON dish
    FOR EACH ROW
EXECUTE FUNCTION log_dish_table_row_insert();

CREATE OR REPLACE FUNCTION log_dish_table_row_delete()
    RETURNS TRIGGER AS
$$
BEGIN
    INSERT INTO logs (table_name, action, time, values) VALUES ('dish', 'delete', NOW(), '');
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER dish_table_row_delete
    AFTER DELETE
    ON dish
    FOR EACH ROW
EXECUTE FUNCTION log_dish_table_row_delete();

-- payment triggers
CREATE OR REPLACE FUNCTION log_payment_table_row_update()
    RETURNS TRIGGER AS
$$
BEGIN
    INSERT INTO logs (table_name, action, time, values) VALUES ('payment', 'update', NOW(), ROW_TO_JSON(NEW));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER payment_table_row_update
    BEFORE UPDATE
    ON payment
    FOR EACH ROW
EXECUTE FUNCTION log_payment_table_row_update();

CREATE OR REPLACE FUNCTION log_payment_table_row_insert()
    RETURNS TRIGGER AS
$$
BEGIN
    INSERT INTO logs (table_name, action, time, values) VALUES ('payment', 'insert', NOW(), ROW_TO_JSON(NEW));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER payment_table_row_insert
    AFTER INSERT
    ON payment
    FOR EACH ROW
EXECUTE FUNCTION log_payment_table_row_insert();

CREATE OR REPLACE FUNCTION log_payment_table_row_delete()
    RETURNS TRIGGER AS
$$
BEGIN
    INSERT INTO logs (table_name, action, time, values) VALUES ('payment', 'delete', NOW(), '');
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER payment_table_row_delete
    AFTER DELETE
    ON payment
    FOR EACH ROW
EXECUTE FUNCTION log_payment_table_row_delete();
