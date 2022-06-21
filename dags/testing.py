import sqlite3
from airflow.models import DAG
from datetime import datetime,timedelta
from airflow.sensors.filesystem import FileSensor
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator

default_args = {
        "owner": 'airflow',
        "retries": 1,
        "retry_delay": timedelta(minutes=2)
}

with DAG(
    dag_id = 'testing',
    default_args = default_args,    
    start_date= datetime(2022,4,1),
    schedule_interval=None,
) as dag:
    task1 = PostgresOperator(
        task_id = 'create_postgres_table',
        postgres_conn_id = 'testing',
        sql = """
        DROP TABLE IF EXISTS z1_user;
        CREATE TABLE z1_user(
            name VARCHAR(255),
            phonenumber VARCHAR(255),
            email NOT NULL VARCHAR(255) PRIMARY KEY,
            address VARCHAR(255),
            work VARCHAR(255),
            other VARCHAR(255),
        ) 
        """
    )
    