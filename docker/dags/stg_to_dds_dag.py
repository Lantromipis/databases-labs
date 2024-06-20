import json

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
from psycopg2.extras import NamedTupleCursor
from datetime import datetime

STG_API_DELIVERYMAN_BATCH_SIZE = 1
STG_API_ORDER_BATCH_SIZE = 1
STG_API_DELIVERY_BATCH_SIZE = 1


def resolve_deliveryman_id(pg_cursor, original_id):
    pg_cursor.execute(
        "SELECT * FROM stg.api_deliveryman WHERE original_id = %s", (original_id,))
    deliveryman_api_stg_record = pg_cursor.fetchone()
    if deliveryman_api_stg_record is None:
        return None

    return deliveryman_api_stg_record.id


def resolve_order_id(pg_cursor, original_id):
    pg_cursor.execute(
        "SELECT * FROM stg.mongo_orders WHERE original_id = %s", (original_id,))
    order_mongo_stg_record = pg_cursor.fetchone()
    if order_mongo_stg_record is None:
        return None

    return order_mongo_stg_record.id


def fill_deliveryman_from_api(**kwargs):
    pg_hook = PostgresHook(postgres_conn_id='postgres-etl')
    pg_conn = pg_hook.get_conn()
    pg_cursor = pg_conn.cursor(cursor_factory=NamedTupleCursor)
    pg_insert_cursor = pg_conn.cursor()

    pg_cursor.execute('SELECT * FROM stg.api_deliveryman')

    while True:
        stg_api_deliverymen = pg_cursor.fetchmany(STG_API_DELIVERYMAN_BATCH_SIZE)
        if not stg_api_deliverymen:
            break

        for stg_api_deliveryman in stg_api_deliverymen:
            deliveryman_json = json.loads(stg_api_deliveryman.json_value)

            pg_insert_cursor.execute(
                "INSERT INTO dds.dm_deliveryman(id, name) VALUES (%s, %s) "
                "ON CONFLICT(id) DO UPDATE "
                "SET name = excluded.name",
                (stg_api_deliveryman.id, deliveryman_json["name"])
            )
            pass

    pg_conn.commit()
    pg_conn.close()


def fill_orders_from_mongo(**kwargs):
    pg_hook = PostgresHook(postgres_conn_id='postgres-etl')
    pg_conn = pg_hook.get_conn()
    pg_cursor = pg_conn.cursor(cursor_factory=NamedTupleCursor)
    pg_insert_cursor = pg_conn.cursor()

    pg_cursor.execute('SELECT * FROM stg.mongo_orders')

    while True:
        stg_mongo_orders = pg_cursor.fetchmany(STG_API_ORDER_BATCH_SIZE)
        if not stg_mongo_orders:
            break

        for stg_mongo_order in stg_mongo_orders:
            order_json = json.loads(stg_mongo_order.json_value)

            order_date = order_json["order_date"]["$date"]
            order_date_datetime = datetime.fromisoformat(order_date)

            pg_insert_cursor.execute(
                "INSERT INTO dds.dm_time(time_mark, year, month, day, time, date) VALUES "
                "(%s, %s, %s, %s, %s, %s) RETURNING id",
                (order_date_datetime,
                 order_date_datetime.year,
                 order_date_datetime.month,
                 order_date_datetime.day,
                 order_date_datetime.time(),
                 order_date_datetime.date()
                 )
            )

            timee_id_record = pg_insert_cursor.fetchone()
            time_id = timee_id_record[0]

            pg_insert_cursor.execute(
                "INSERT INTO dds.dm_order(id, final_status, cost, order_time_id) VALUES (%s, %s, %s, %s) "
                "ON CONFLICT(id) DO UPDATE "
                "SET final_status = excluded.final_status, cost = excluded.cost, order_time_id = excluded.order_time_id",
                (stg_mongo_order.id, order_json["final_status"], order_json["cost"], time_id)
            )
            pass

    pg_conn.commit()
    pg_conn.close()


def fill_delivery_from_api(**kwargs):
    pg_hook = PostgresHook(postgres_conn_id='postgres-etl')
    pg_conn = pg_hook.get_conn()
    pg_delivery_fetch_cursor = pg_conn.cursor(cursor_factory=NamedTupleCursor)
    pg_helper_fetch_cursor = pg_conn.cursor(cursor_factory=NamedTupleCursor)
    pg_insert_cursor = pg_conn.cursor()

    pg_delivery_fetch_cursor.execute('SELECT * FROM stg.api_delivery')

    while True:
        stg_api_deliveries = pg_delivery_fetch_cursor.fetchmany(STG_API_DELIVERY_BATCH_SIZE)
        if not stg_api_deliveries:
            break

        for stg_api_delivery in stg_api_deliveries:
            delivery_json = json.loads(stg_api_delivery.json_value)

            # важно использовать новые айдишки из stg как внешние ключи, для чего нужно сделать мапппинг на них при вставке в dds слой
            # маппинг айдишки для доставщика
            new_deliveryman_id = resolve_deliveryman_id(pg_helper_fetch_cursor, delivery_json["deliveryman_id"])

            # маппинг айдишки для заказа
            new_order_id = resolve_order_id(pg_helper_fetch_cursor, delivery_json["order_id"])

            pg_insert_cursor.execute(
                "INSERT INTO dds.dm_delivery(id, deliveryman_id, order_id, rating, tips) VALUES (%s, %s, %s, %s, %s) "
                "ON CONFLICT(id) DO UPDATE "
                "SET deliveryman_id = excluded.deliveryman_id,"
                " order_id = excluded.order_id,"
                " rating = excluded.rating,"
                " tips = excluded.tips",
                (stg_api_delivery.id, new_deliveryman_id, new_order_id,
                 delivery_json["rating"], delivery_json["tips"])
            )
            pass

    pg_conn.commit()
    pg_conn.close()


# важно исполнять по порядку, ведь на данном слое уже есть завязки на внешние ключи
with DAG(
        'stg_to_dds_loader',
        schedule_interval=None,
        start_date=days_ago(2),
) as dag:
    fill_deliveryman_from_api = PythonOperator(
        task_id='fill_deliveryman_from_api',
        python_callable=fill_deliveryman_from_api,
    )

    fill_orders_from_mongo = PythonOperator(
        task_id='fill_orders_from_mongo',
        python_callable=fill_orders_from_mongo,
    )

    fill_delivery_from_api = PythonOperator(
        task_id='fill_delivery_from_api',
        python_callable=fill_delivery_from_api,
    )

    fill_deliveryman_from_api >> fill_delivery_from_api
    fill_orders_from_mongo >> fill_delivery_from_api
