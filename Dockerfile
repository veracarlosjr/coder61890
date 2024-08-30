# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV AIRFLOW_HOME=/opt/airflow

# Install Airflow and other dependencies
RUN pip install --no-cache-dir apache-airflow==2.5.0 psycopg2-binary pandas

# Copy the DAGs directory and scripts
COPY dags/ $AIRFLOW_HOME/dags/
COPY scripts/ /app/scripts/

# Set the working directory
WORKDIR $AIRFLOW_HOME

# Set the default command to run Airflow
CMD ["airflow", "standalone"]



