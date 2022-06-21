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

def _processing_user(ti):
    users = ti.xcom_pull(task_ids = ['extracting_user'])
    if not len(users) or 'results' not in users[0]:
        raise ValueError('User is empty')
    user = users[0]['results'][0]
    processed_user = json_normalize({
        'firstname':user['name']['first'],
        'lastname':user['name']['last'],
        'country':user['location']['country'],
        'username':user['login']['username'],
        'password':user['login']['password'],
        'email':user['email']
    })
    processed_user.to_csv('processed_user.csv', index=None, header=False)

with DAG(
    dag_id='dags_new_version',
    default_args=default_args,
    start_date = datetime(2022,6,17),
    schedule_interval='@daily'
    
) as dag:
    task1 = PostgresOperator(
        task_id = 'create_table',
        postgres_conn_id = 'postgre_sql',
        sql = """
        DROP TABLE IF EXISTS z1_user;
        CREATE TABLE z1_user(
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
    
    task2 = HttpSensor(
        task_id = 'is_api_available',
        http_conn_id = 'user_api',
        endpoint = 'api/',
        method = 'GET'
    )
    
    task3 = SimpleHttpOperator(
        task_id = 'extracting_user',
        http_conn_id='user_api',
        endpoint='api/',
        method = 'GET',
        response_filter=lambda response : json.loads(response.text),
        log_response=True
    )
    
    task4 = PythonOperator(
        task_id = 'processing_user',
        python_callable=_processing_user   
    )
    
    # task5 = BashOperator(
    #     task_id = 'storing_user',
    #     bash_command='echo -e ".sparator ","\n.import /processed_user.csv users"'
        
    # )
    
    
    task1 >> task2 >> task3 >> task4