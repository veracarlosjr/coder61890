from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def run_etl():
    subprocess.run(["python", "/app/scripts/main.py"])

dag = DAG(
    'daily_etl_dag',
    default_args=default_args,
    description='A simple daily ETL DAG',
    schedule_interval=timedelta(days=1),
)

run_etl_task = PythonOperator(
    task_id='run_etl',
    python_callable=run_etl,
    dag=dag,
)



