from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.mongo.hooks.mongo import MongoHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
from bson import json_util


# указывать размер батча не нужно, так как pymongo под капотом сама грузит данные кусочками с сервера, если верить документации на find()

def load_clients(**kwargs):
    mongo_hook = MongoHook(mongo_conn_id='mongo-etl')
    mongo_conn = mongo_hook.get_conn()
    mongo_db = mongo_conn.etl
    mongo_clients_collection = mongo_db.clients

    mongo_clients_cursor = mongo_clients_collection.find()

    pg_hook = PostgresHook(postgres_conn_id='postgres-etl')
    pg_conn = pg_hook.get_conn()
    pg_insert_cursor = pg_conn.cursor()

    for mongo_client in mongo_clients_cursor:
        client_id = str(mongo_client['_id'])
        client_json = json_util.dumps(mongo_client)
        pg_insert_cursor.execute(
            "INSERT INTO stg.mongo_clients(original_id, json_value) VALUES (%s, %s) "
            "ON CONFLICT(original_id) DO UPDATE "
            "SET json_value = excluded.json_value",
            (client_id, client_json)
        )
        pass

    pg_conn.commit()
    pg_conn.close()


def load_orders(**kwargs):
    mongo_hook = MongoHook(mongo_conn_id='mongo-etl')
    mongo_conn = mongo_hook.get_conn()
    mongo_db = mongo_conn.etl
    mongo_orders_collection = mongo_db.orders
    mongo_orders_cursor = mongo_orders_collection.find()

    pg_hook = PostgresHook(postgres_conn_id='postgres-etl')
    pg_conn = pg_hook.get_conn()
    pg_insert_cursor = pg_conn.cursor()

    for mongo_order in mongo_orders_cursor:
        order_id = str(mongo_order['_id'])
        order_json = json_util.dumps(mongo_order)
        pg_insert_cursor.execute(
            "INSERT INTO stg.mongo_orders(original_id, json_value) VALUES (%s, %s) "
            "ON CONFLICT(original_id) DO UPDATE "
            "SET json_value = excluded.json_value",
            (order_id, order_json)
        )
        pass

    pg_conn.commit()
    pg_conn.close()


def load_restaurants(**kwargs):
    mongo_hook = MongoHook(mongo_conn_id='mongo-etl')
    mongo_conn = mongo_hook.get_conn()
    mongo_db = mongo_conn.etl
    mongo_restaurants_collection = mongo_db.restaurant
    mongo_restaurants_cursor = mongo_restaurants_collection.find()

    pg_hook = PostgresHook(postgres_conn_id='postgres-etl')
    pg_conn = pg_hook.get_conn()
    pg_insert_cursor = pg_conn.cursor()

    for mongo_restaurant in mongo_restaurants_cursor:
        restaurant_id = str(mongo_restaurant['_id'])
        restaurant_json = json_util.dumps(mongo_restaurant)
        pg_insert_cursor.execute(
            "INSERT INTO stg.mongo_restaurants(original_id, json_value) VALUES (%s, %s) "
            "ON CONFLICT(original_id) DO UPDATE "
            "SET json_value = excluded.json_value",
            (restaurant_id, restaurant_json)
        )
        pass

    pg_conn.commit()
    pg_conn.close()


with DAG(
        'mongo_loader',
        schedule_interval=None,
        start_date=days_ago(2),
) as dag:
    load_clients = PythonOperator(
        task_id='load_clients',
        python_callable=load_clients,
    )

    load_orders = PythonOperator(
        task_id='load_orders',
        python_callable=load_orders,
    )

    load_restaurants = PythonOperator(
        task_id='load_restaurants',
        python_callable=load_restaurants,
    )

    load_clients
    load_orders
    load_restaurants
