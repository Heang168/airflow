import json
from datetime import datetime,timedelta
from textwrap import dedent

from venv import create
import os
from airflow import DAG, task
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook

import pandas as pd

import psycopg2
# from transform import cleaning_spark_cbre
from sqlalchemy import create_engine


# print_py.sumadd()

# @task()
# def transform():
#     conn = PostgresHook.get_connection('postgres')
#     engine = create_engine(f'postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}')
#     conn = psycopg2.connect(host='localhost', database='postgres', user ='admin',password='root')
    
    # cleaning_spark_cbre
    # print_py'
    
default_args = {
        "owner": 'airflow',
        "retries": 1,
        "retry_delay": timedelta(minutes=2)
}

with DAG(
    dag_id = 'table_postgres',
    default_args = default_args,    
    start_date= datetime(2022,4,1),
    schedule_interval=None,

) as dag: 
    task1 = PostgresOperator(
        task_id = 'create_postgres_table',
        postgres_conn_id = 'postgre_sql',
        sql = """ 
        DROP TABLE IF EXISTS new_scrapping;
        CREATE TABLE new_scrapping(
            db_id SERIAL PRIMARY KEY,
            Property_ID VARCHAR(255),
            Original_ID VARCHAR(255),
            Record_Type VARCHAR(255),
            Property_Type VARCHAR(255),
            Site_Improvement VARCHAR(255),
            Agricultural_Type VARCHAR(255),
            Current_Use VARCHAR(255),
            Purpose VARCHAR(255),
            Latitude DECIMAL(12,9),
            Longitude DECIMAL(12,9),
            Geolocation_Link TEXT,
            Provice_City VARCHAR(255),
            District_Khan VARCHAR(255),
            Commune_Sangkat VARCHAR(255),
            Village_Phum VARCHAR(255),
            Street_No_Name VARCHAR(255),
            House_No VARCHAR(255),
            Title_Address TEXT,
            Neighbor_Location VARCHAR(255),
            Access_Road VARCHAR(255),
            Land_Width DECIMAL(12,2),
            Land_Length DECIMAL(12,2),
            Land_Area_By_Title_Deed DECIMAL(12,2),
            Topography VARCHAR(255),
            Shape VARCHAR(255),
            Site_Position VARCHAR(255),
            Building_Type VARCHAR(255),
            Unit_Type VARCHAR(255),
            Building_Name VARCHAR(255),
            Project_Name VARCHAR(255),
            Width DECIMAL(12,2),
            Length DECIMAL(12,2),
            No_of_Storey INT,
            Floor_Number INT,
            Total_Bedroom INT,
            Total_Other_Room INT,
            Total_Bathroom INT,
            Total_Living_Room INT,
            Total_Kitchen INT,
            Total_Dinning_Room INT,
            Garage_Capacity_front_house INT,
            Swimming_Pool DECIMAL(5,2),
            Gross_Floor_Area_GFA DECIMAL(12,2),
            Net_Floor_Area_NFA DECIMAL(12,2),
            View_ VARCHAR(255),
            Orientation VARCHAR(255),
            Year_Started_Construction INT,
            Year_Finished_Construction INT,
            Physical_Condition VARCHAR(255),
            Furnishing VARCHAR(255),
            Pet_Friendly VARCHAR(255),
            Maintenance_Fee DECIMAL(12,2),
            Guaranteed_Rental_Return DECIMAL(5,2),
            Expected_Rental_Return DECIMAL(5,2),
            Downpayment_Ratio DECIMAL(5,2),
            Occupancy_Rate DECIMAL(5,2),
            Lease_Term_Month VARCHAR(255),
            Management_Fee DECIMAL(5,2),
            Pct_Of_Construction DECIMAL(5,2),
            Photo_Inside TEXT,
            Photo_Left_Side TEXT,
            Photo_Right_Side TEXT,
            Photo_Opposite TEXT,
            Gallery TEXT,
            Title_Deed_Type VARCHAR(255),
            Title_Deed_No VARCHAR(255),
            Issued_Year INT,
            Parcel_No VARCHAR(255),
            Total_Size_By_Title_Deed DECIMAL(12,2),
            Title_Deed_Cover_Photo TEXT,
            Title_Deed_Back_Side_Photo TEXT,
            Title_Deed_Other_Photo TEXT,
            Stamp_Date DATE,
            Additional_Information TEXT,
            Property_Owner VARCHAR(255),
            Contact_Owner VARCHAR(255),
            Email VARCHAR(255),
            Wechat VARCHAR(255),
            Price_Status VARCHAR(255),
            Total DECIMAL(12,2),
            Rent DECIMAL(12,2),
            Per_sqm DECIMAL(12,2),
            Sold_Rate DECIMAL(5,2),
            Price_increase DECIMAL(5,2),
            Tran_Date DATE,
            Source_ VARCHAR(255),
            Last_Sync_Modify DATE,
            Updated_Sync_Modify DATE,
            Title TEXT,
            Link_Website TEXT
        )
    """
    )

    # transform_task = PythonOperator(
    #     task_id='transform',
    #     python_callable = transform,
        
    # )

    # task2 = PythonOperator(
    #     task_id = 'read_csv'
        

    # ) 

    # task1 >> transform_task
    
