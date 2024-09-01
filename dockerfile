# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV AIRFLOW_HOME=/opt/airflow

# Install dependencies from requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the DAGs directory and scripts
COPY dags/ $AIRFLOW_HOME/dags/

# Set the working directory
WORKDIR $AIRFLOW_HOME

# Set the default command to run Airflow
CMD ["airflow", "standalone"]




