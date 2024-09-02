# Usa una imagen oficial de Python como base
FROM python:3.9-slim

# Establece variables de entorno
ENV AIRFLOW_HOME=/opt/airflow
ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow/dags:/opt/airflow/etl_modulos"

# Instala dependencias desde requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el directorio de DAGs, scripts y módulos ETL
COPY dags/ $AIRFLOW_HOME/dags/
COPY etl_modulos/ $AIRFLOW_HOME/etl_modulos/
COPY config/ $AIRFLOW_HOME/config/

# Establece el directorio de trabajo
WORKDIR $AIRFLOW_HOME

# Establece el comando predeterminado para ejecutar Airflow
CMD ["airflow", "standalone"]