from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
import requests
import json

# все по 1, чтобы эмулировать батчи на малом количестве данных
DELIVERYMAN_BATCH_SIZE = 1
DELIVERY_BATCH_SIZE = 1

DELIVERY_TIME_SETTING_NAME = "api_delivery_time"

DELIVERY_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


# счиатем, что доставщиков мало, плюс у них нет даты обновления,
# а значит не надо загружать инкрементально и каждый раз перегружаем всех
def load_deliveryman(**kwargs):
    pg_hook = PostgresHook(postgres_conn_id='postgres-etl')
    pg_conn = pg_hook.get_conn()
    pg_insert_cursor = pg_conn.cursor()

    offset = 0
    while True:
        query_params = {
            'limit': DELIVERYMAN_BATCH_SIZE,
            'offset': offset,
        }
        response = requests.get("http://api-service:8080/api/deliveryman", params=query_params)
        deliveryman_json = json.loads(response.content)
        if len(deliveryman_json) == 0:
            break

        offset += DELIVERYMAN_BATCH_SIZE
        for deliveryman_obj in deliveryman_json:
            deliveryman_str = json.dumps(deliveryman_obj)
            deliveryman_id = deliveryman_obj['_id']
            pg_insert_cursor.execute(
                "INSERT INTO stg.api_deliveryman(original_id, json_value) VALUES (%s, %s) "
                "ON CONFLICT(original_id) DO UPDATE "
                "SET json_value = excluded.json_value",
                (deliveryman_id, deliveryman_str)
            )
            pass

    pg_conn.commit()
    pg_conn.close()


def load_delivery(**kwargs):
    pg_hook = PostgresHook(postgres_conn_id='postgres-etl')
    pg_conn = pg_hook.get_conn()
    pg_select_cursor = pg_conn.cursor()
    pg_insert_cursor = pg_conn.cursor()

    pg_select_cursor.execute("SELECT * FROM stg.settings WHERE key = %s", (DELIVERY_TIME_SETTING_NAME,))
    latest_delivery_time_fetched = pg_select_cursor.fetchone()

    offset = 0
    timestamp_setting_to_save = None;
    while True:
        if latest_delivery_time_fetched is None:
            query_params = {
                'limit': DELIVERY_BATCH_SIZE,
                'offset': offset,
            }
        else:
            query_params = {
                'limit': DELIVERY_BATCH_SIZE,
                'offset': offset,
                'delivery_time_gt': latest_delivery_time_fetched,
            }

        response = requests.get("http://api-service:8080/api/delivery", params=query_params)
        delivery_json = json.loads(response.content)
        print(delivery_json)
        if len(delivery_json) == 0:
            break

        offset += DELIVERY_BATCH_SIZE
        for delivery_obj in delivery_json:
            delivery_str = json.dumps(delivery_obj)
            delivery_id = delivery_obj['delivery_id']

            pg_insert_cursor.execute(
                "INSERT INTO stg.api_delivery(original_id, json_value) VALUES (%s, %s) "
                "ON CONFLICT(original_id) DO UPDATE "
                "SET json_value = excluded.json_value",
                (delivery_id, delivery_str)
            )

            delivery_time = delivery_obj['delivery_time']
            if timestamp_setting_to_save is None:
                timestamp_setting_to_save = delivery_time

            formatted_delivery_time = datetime.strptime(delivery_time, DELIVERY_TIME_FORMAT)
            formatted_timestamp_to_save = datetime.strptime(timestamp_setting_to_save, DELIVERY_TIME_FORMAT)
            if formatted_delivery_time > formatted_timestamp_to_save:
                timestamp_setting_to_save = delivery_time
            pass

    if timestamp_setting_to_save is not None:
        pg_insert_cursor.execute(
            "INSERT INTO stg.settings(key, value) VALUES (%s, %s) "
            "ON CONFLICT(key) DO UPDATE "
            "SET value = excluded.value",
            (DELIVERY_TIME_SETTING_NAME, timestamp_setting_to_save)
        )

    pg_conn.commit()
    pg_conn.close()


with DAG(
        'api_loader',
        schedule_interval=None,
        start_date=days_ago(2),
) as dag:
    load_deliveryman = PythonOperator(
        task_id='load_deliveryman',
        python_callable=load_deliveryman,
    )

    load_delivery = PythonOperator(
        task_id='load_delivery',
        python_callable=load_delivery,
    )

    load_deliveryman
    load_delivery
