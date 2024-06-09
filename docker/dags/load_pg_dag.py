from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
from psycopg2.extras import NamedTupleCursor

# все по 1, чтобы эмулировать батчи на малом количестве данных
CLIENTS_BATCH_SIZE = 1
CATEGORIES_BATCH_SIZE = 1
DISHES_BATCH_SIZE = 1
PAYMENT_BATCH_SIZE = 1

def load_clients(**kwargs):
    pg_hook = PostgresHook(postgres_conn_id='postgres-etl')
    pg_conn = pg_hook.get_conn()
    pg_cursor = pg_conn.cursor(cursor_factory=NamedTupleCursor)
    pg_insert_cursor = pg_conn.cursor()

    pg_cursor.execute('SELECT * FROM src.client')

    while True:
        src_clients = pg_cursor.fetchmany(CLIENTS_BATCH_SIZE)
        if not src_clients:
            break

        for src_client in src_clients:
            pg_insert_cursor.execute(
                "INSERT INTO stg.postgres_client(original_id, bonus_balance, category_id) VALUES (%s, %s, %s) "
                "ON CONFLICT(original_id) DO UPDATE "
                "SET bonus_balance = excluded.bonus_balance, category_id = excluded.category_id",
                (src_client.client_id, src_client.bonus_balance, src_client.category_id)
            )
            pass

    pg_conn.commit()
    pg_conn.close()


def load_categories(**kwargs):
    pg_hook = PostgresHook(postgres_conn_id='postgres-etl')
    pg_conn = pg_hook.get_conn()
    pg_cursor = pg_conn.cursor(cursor_factory=NamedTupleCursor)
    pg_insert_cursor = pg_conn.cursor()

    pg_cursor.execute('SELECT * FROM src.category')

    while True:
        src_categories = pg_cursor.fetchmany(CATEGORIES_BATCH_SIZE)
        if not src_categories:
            break

        for src_category in src_categories:
            pg_insert_cursor.execute(
                "INSERT INTO stg.postgres_category(original_id, name, percent, min_payment) VALUES (%s, %s, %s, %s) "
                "ON CONFLICT(original_id) DO UPDATE "
                "SET name = excluded.name, percent = excluded.percent, min_payment = excluded.min_payment",
                (src_category.category_id, src_category.name, src_category.percent, src_category.min_payment)
            )
            pass

    pg_conn.commit()
    pg_conn.close()


def load_dishes(**kwargs):
    pg_hook = PostgresHook(postgres_conn_id='postgres-etl')
    pg_conn = pg_hook.get_conn()
    pg_cursor = pg_conn.cursor(cursor_factory=NamedTupleCursor)
    pg_insert_cursor = pg_conn.cursor()

    pg_cursor.execute('SELECT * FROM src.dish')

    while True:
        src_dishes = pg_cursor.fetchmany(DISHES_BATCH_SIZE)
        if not src_dishes:
            break

        for src_dish in src_dishes:
            pg_insert_cursor.execute(
                "INSERT INTO stg.postgres_dish(original_id, name, price) VALUES (%s, %s, %s) "
                "ON CONFLICT(original_id) DO UPDATE "
                "SET name = excluded.name, price = excluded.price",
                (src_dish.dish_id, src_dish.name, src_dish.price)
            )
            pass

    pg_conn.commit()
    pg_conn.close()


def load_payments(**kwargs):
    pg_hook = PostgresHook(postgres_conn_id='postgres-etl')
    pg_conn = pg_hook.get_conn()
    pg_cursor = pg_conn.cursor(cursor_factory=NamedTupleCursor)
    pg_insert_cursor = pg_conn.cursor()

    pg_cursor.execute('SELECT * FROM src.payment')

    while True:
        src_payments = pg_cursor.fetchmany(PAYMENT_BATCH_SIZE)
        if not src_payments:
            break

        for src_payment in src_payments:
            pg_insert_cursor.execute(
                "INSERT INTO stg.postgres_payment(original_id, client_id, dish_id, dish_amount, order_id, order_time, order_sum, tips) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s) "
                "ON CONFLICT(original_id) DO UPDATE "
                "SET client_id = excluded.client_id,"
                " dish_id = excluded.dish_id, "
                " dish_amount = excluded.dish_amount,"
                " order_id = excluded.order_id,"
                " order_time = excluded.order_time,"
                " order_sum = excluded.order_sum,"
                " tips = excluded.tips",
                (src_payment.payment_id,
                 src_payment.client_id,
                 src_payment.dish_id,
                 src_payment.dish_amount,
                 src_payment.order_id,
                 src_payment.order_time,
                 src_payment.order_sum,
                 src_payment.tips)
            )
            pass

    pg_conn.commit()
    pg_conn.close()


with DAG(
        'pg_loader',
        schedule_interval=None,
        start_date=days_ago(2),
) as dag:
    load_clients = PythonOperator(
        task_id='load_clients',
        python_callable=load_clients,
    )
    load_categories = PythonOperator(
        task_id='load_categories',
        python_callable=load_categories,
    )
    load_dishes = PythonOperator(
        task_id='load_dishes',
        python_callable=load_dishes,
    )
    load_payments = PythonOperator(
        task_id='load_payments',
        python_callable=load_payments,
    )

    load_clients
    load_categories
    load_dishes
    load_payments
