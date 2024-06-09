CREATE SCHEMA IF NOT EXISTS cdm;
SET SEARCH_PATH TO cdm;

CREATE TABLE IF NOT EXISTS deliveryman_income
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

CREATE OR REPLACE FUNCTION deliveryman_order_income_acc(double precision, double precision, smallint)
   returns double precision
   language plpgsql
  as
$$
declare
   temp_income numeric;
begin
   if $3 <= 3 then
       temp_income = $2 * 0.05;
       if temp_income < 400 then
           return $1 + 400;
       end if;
       return $1 + temp_income;
   end if;

   temp_income = $2 * 0.1;
   if temp_income < 400 then
       return $1 + 400;
   end if;
   if temp_income > 1000 then
       return $1 + 1000;
   end if;
   return $1 + temp_income;
end;
$$;

CREATE OR REPLACE AGGREGATE deliveryman_order_income (double precision, smallint)
(
    sfunc = deliveryman_order_income_acc,
    stype = double precision,
    initcond = '0.0'
);