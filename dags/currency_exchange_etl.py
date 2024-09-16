from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from etl_modulos.extract import extract_data
from etl_modulos.transform import transform_data
from etl_modulos.load import load_data
from etl_modulos.mail_send import send_email  
import configparser
import requests

# Definir api_url dentro del DAG
def get_api_url():
    base_currency = "USD"
    quote_currency = "EUR"
    date = datetime.now().strftime("%Y-%m-%d")
    return f"https://api.frankfurter.app/{date}?from={base_currency}&to={quote_currency}"

# Configurar argumentos por defecto
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'daily_etl_dag',
    default_args=default_args,
    description='A simple daily ETL DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime.now() - timedelta(days=1),  
)

def extract_and_return(**kwargs):
    api_url = get_api_url()
    data = extract_data(api_url)
    return data

def transform_and_return(**kwargs):
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='extract_task')
    transformed_data = transform_data(data)
    return transformed_data

def load_data_from_transformed(**kwargs):
    ti = kwargs['ti']
    transformed_data = ti.xcom_pull(task_ids='transform_task')
    config_path = '/opt/airflow/config/config.ini'
    
    config = configparser.ConfigParser()
    try:
        config.read(config_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"El archivo de configuración no se encontró en la ruta: {config_path}")

    load_data(transformed_data, config)

# Definir las tareas del DAG
extract_task = PythonOperator(
    task_id='extract_task',
    python_callable=extract_and_return,
    provide_context=True,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_task',
    python_callable=transform_and_return,
    provide_context=True,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_task',
    python_callable=load_data_from_transformed,
    provide_context=True,
    dag=dag,
)

email_alert_task = PythonOperator(
    task_id='email_alert_task',
    python_callable=send_email,
    provide_context=True,
    dag=dag,
)

# flujo de tareas
extract_task >> transform_task >> load_task >> email_alert_task

