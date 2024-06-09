from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.utils.dates import days_ago

with DAG(
        'pg_ddl_executor',
        schedule_interval=None,
        start_date=days_ago(2),
) as dag:
    execute_stg_ddl = SQLExecuteQueryOperator(
        task_id="execute_stg_ddl",
        conn_id="postgres-etl",
        sql="sql/ddl/stg.sql",
    )
    execute_dds_ddl = SQLExecuteQueryOperator(
        task_id="execute_dds_ddl",
        conn_id="postgres-etl",
        sql="sql/ddl/dds.sql",
    )
    execute_cdm_ddl = SQLExecuteQueryOperator(
        task_id="execute_cdm_ddl",
        conn_id="postgres-etl",
        sql="sql/ddl/cdm.sql",
    )

    execute_stg_ddl
    execute_dds_ddl
    execute_cdm_ddl
