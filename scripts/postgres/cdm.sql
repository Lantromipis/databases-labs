CREATE SCHEMA cdm;
SET SEARCH_PATH TO cdm;

CREATE TABLE deliveryman_income
(
    id                       BIGSERIAL PRIMARY KEY,
    deliveryman_id           BIGINT,
    deliveryman_name         TEXT,
    year                     INTEGER,
    month                    INTEGER,
    orders_amount            INTEGER,
    orders_total_cost        DOUBLE PRECISION,
    rating                   DOUBLE PRECISION,
    company_commission       DOUBLE PRECISION,
    deliveryman_order_income DOUBLE PRECISION,
    tips                     DOUBLE PRECISION
);

SELECT dm.id, dm.name, sum
FROM dds.dm_delivery d
         JOIN dds.dm_deliveryman dm ON dm.id = d.deliveryman_id
         JOIN dds.dm_order o on o.id = d.order_id
WHERE o.final_status = 'CLOSED'
  AND o.order_date BETWEEN '2024-05-09' AND '2024-04-09'
GROUP BY dm.id, dm.name