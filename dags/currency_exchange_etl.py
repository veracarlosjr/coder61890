from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Importa las funciones de tus módulos ETL
from etl_modulos.extract import extract_data
from etl_modulos.transform import transform_data
from etl_modulos.load import load_data

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'daily_etl_dag',
    default_args=default_args,
    description='A simple daily ETL DAG',
    schedule_interval=timedelta(days=1),
)

# Define las tareas del DAG
extract_task = PythonOperator(
    task_id='extract_task',
    python_callable=extract_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_task',
    python_callable=transform_data,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_task',
    python_callable=load_data,
    dag=dag,
)

# Define el flujo de tareas
extract_task >> transform_task >> load_task
