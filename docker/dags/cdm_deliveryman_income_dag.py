from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
from psycopg2.extras import NamedTupleCursor


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


def period_start_for_date(d):
    if d.day < 21:
        if d.month == 1:
            return datetime(d.year - 1, 12, 21)
        else:
            return datetime(d.year, d.month - 1, 21)
    else:
        return datetime(d.year, d.month, 21)


def period_end_for_date(d):
    if d.day < 21:
        return datetime(d.year, d.month, 21)
    else:
        if d.month == 12:
            return datetime(d.year + 1, 1, 21)
        else:
            return datetime(d.year, d.month + 1, 21)


def fill_deliveryman_income(**kwargs):
    pg_hook = PostgresHook(postgres_conn_id='postgres-etl')
    pg_conn = pg_hook.get_conn()
    pg_cursor = pg_conn.cursor(cursor_factory=NamedTupleCursor)
    pg_insert_cursor = pg_conn.cursor()

    pg_cursor.execute("SET SEARCH_PATH TO cdm;")
    pg_insert_cursor.execute("TRUNCATE cdm.deliveryman_income")

    query_str = open('dags/sql/query/deliveryman_income_select.sql').read()
    pg_cursor.execute(query_str, ())

    calculated_records = pg_cursor.fetchall()

    for record in calculated_records:
        deliveryman_id = record.deliveryman_id
        deliveryman_name = record.deliveryman_name
        year = record.year
        month = record.month
        orders_amount = record.orders_amount
        orders_total_cost = record.orders_total_cost
        company_commission = record.company_commission
        rating = record.rating
        tips = record.tips
        deliveryman_order_income = record.deliveryman_order_income

        pg_insert_cursor.execute(
            "INSERT INTO cdm.deliveryman_income(deliveryman_id, deliveryman_name, year, "
            "month, orders_amount, orders_total_cost, rating, company_commission,"
            " deliveryman_order_income, tips)"
            " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (deliveryman_id, deliveryman_name, year, month,
             orders_amount, orders_total_cost, rating, company_commission, deliveryman_order_income, tips)
        )
        pass

    pg_conn.commit()
    pg_conn.close()
    print("Finished filling deliveryman income")


with DAG(
        'cdm_deliveryman_income_builder',
        schedule_interval=None,
        start_date=days_ago(2),
) as dag:
    fill_deliveryman_income = PythonOperator(
        task_id='fill_deliveryman_income',
        python_callable=fill_deliveryman_income,
    )

    fill_deliveryman_income
