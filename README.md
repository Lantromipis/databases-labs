# Как запустить

1. `cd doceker`
2. `docker-compose up`
3. Настраиваем и заполняем PostgreSQL
   1. Подключаемся к postgres по адресу `localhost:5460` в БД postgres логин/пароль: postgres/postgres
   2. Переходим в дирикторию `scripts -> postgres` из корня проекта
   3. Выполняем скрипты из дириктории source: ddl.sql, а затем data.sql
   4. Выполняем все скрипты из директории postgres в любом порядке: cdm.sql, dds.sql, stg.sql
4. Настраиваем и заполняем MongoDB
   1. Подключаемся к mongo по адресу `localhost:27017` логин/пароль: admin/admin
   2. Создаем в mongo схему с именмем `etl`
   3. Кладем в схему все файлы из дириктории `scripts -> mongo` корня проекта
5. Входим в airflow по адресу `localhost:8080` логин/пароль: airflow/airflow
6. Переходим в `admin -> connections`
7. Создаем коннекшин с id `postgres-etl`.
   1. conn-id: postgres-etl
   2. host: postgres-etl
   3. database: postgres
   4. user: postgres
   5. password: postgres
   6. port: 5432
8. Создаем connection с id `mongo-etl`
   1. conn-id: mongo-etl
   2. host: mongo-etl
   3. schema: admin
   4. user: admin
   5. password: admin
   6. port: 27017
9. docker-compose up -d --no-deps --build api-service
