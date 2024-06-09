# Как запустить

## Запускаем сервисы и подготавилваем данные
1. `cd docker`
2. При необходимости меняем в docker-compose порты, нак оторые прокидывается airflow, postgres и mongo из докера на локальную машину. По умаолчанию они: 8080, 5460, 27017
3. `docker-compose up -d`
4. Настраиваем и заполняем PostgreSQL
   1. Подключаемся к postgres по адресу `localhost:5460` в БД postgres логин/пароль: postgres/postgres
   2. Переходим в дирикторию `lab1-pg-rows` из корня проекта
   3. Выполняем скрипты из дириктории source: ddl.sql, а затем data.sql
   4. При желании можно добавить еще данные, помиом тех что уже в data.sql
5. Настраиваем и заполняем MongoDB
   1. Подключаемся к mongo по адресу `localhost:27017` логин/пароль: admin/admin
   2. Создаем в mongo схему с именмем `etl`
   3. Кладем в схему все файлы из дириктории `lab1-mongo-collections` корня проекта
   4. При желании можно доабвить еще данные в уже представленные коллекции
6. (Опционально) Добавляем новыен данные для API
   1. Переходим в дирикторию `lab1-api-service -> src -> main -> resources`
   2. Меняем файлы delivery.json и deliveryman.json
   3. Пересобираем и перезапускаем API сервис с помощью команды `docker-compose up -d --no-deps --build api-service`. Команду надо выполнять в дириктории `docker`
7. Входим в airflow по адресу `localhost:8080` логин/пароль: airflow/airflow
8. Переходим в `admin -> connections`
9. Создаем коннекшин с id `postgres-etl`.
   1. conn-id: postgres-etl
   2. host: postgres-etl
   3. database: postgres
   4. user: postgres
   5. password: postgres
   6. port: 5432
10. Создаем connection с id `mongo-etl`
    1. conn-id: mongo-etl
    2. host: mongo-etl
    3. schema: admin
    4. user: admin
    5. password: admin
    6. port: 27017

## Запускаем DAG
Все DAGи без расписания, чтобы было удобнее разрабатывать и теситровать, а также чтобы не грузить систему. 
В ыполняем DAGи в следующем порядке: 
1. `pg_ddl_executor` -- сделает все схемы и таблицы в БД
2. `mongo_loader` -- загрузит данные из Mongo в STG
3. `pg_loader` -- загрузит данные из Postgres в STG
4. `api_loader` -- загрузит данные из API в STG
5. `stg_to_dds_loader` -- перельет данные из STG в DDS
6. `cdm_deliveryman_income_builder` -- построит витрину, путем переливания данных из DDS в CDM

После этого проверяем результат: `SELECT * from cdm.deliveryman_income;`
