from concurrent.futures import process
import json
from datetime import datetime,timedelta
from airflow import DAG, task
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.bash import BashOperator

from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from pandas import json_normalize

default_args = {
    "owner":'airflow',
    "retries":1,
    "retry_delay":timedelta(minutes=2)
}

with DAG(
    dag_id='dags_v1',
    default_args=default_args,
    start_date = datetime(2022,6,17),
    schedule_interval='@daily'
) as dag:
    task1 = PostgresOperator(
        task_id = 'create_table',
        postgres_conn_id = 'postgre_sql',
        sql = """
        DROP TABLE IF EXISTS testing;
        CREATE TABLE testing(
            user_id SERIAL PRIMARY KEY,
            firstname VARCHAR(255),
            lastname VARCHAR(255),
            country VARCHAR(255),
            username VARCHAR(255),
            password VARCHAR(255),
            email VARCHAR(255)
        )
        """
    )