# coder61890
Proyecto del curso Data Engineering

Frankfurter es una API de código abierto para tipos de cambio actuales e históricos publicados por el Banco Central Europeo.

# ETL para Tasas de Cambio de Divisas

Este proyecto es un script ETL (Extract, Transform, Load) que extrae tasas de cambio de divisas desde la API de Frankfurter, transforma los datos y los carga en una base de datos Amazon Redshift.

## Descripción

Este script realiza los siguientes pasos:
1. **Extracción**: Obtiene datos de tasas de cambio de divisas desde la API de Frankfurter.
2. **Transformación**: Transforma los datos extraídos en un formato adecuado para la base de datos.
3. **Carga**: Inserta los datos transformados en una tabla en Amazon Redshift.


##Estructura del Proyecto

coder61890/
 
    ├── dags/
       ├── currency_exchange_etl.py
       ├── main.py
       └── etl_modulos/
          ├── __init__.py
          ├── extract.py
          ├── transform.py
          └── load.py
    ├── raw_data/
       ├── data.csv
       ├── load_csv_rawdata.py
       └── raw_data.py
    ├── main.py
    ├── .gitignore
    ├── docker-compose.yml
    ├── README.md
    └── requirements.txt


**dags/:** Contiene los archivos de definición del DAG para Apache Airflow.

   **currency_exchange_etl.py:** Archivo del DAG para el proceso ETL.

   **main.py:** Script principal para ejecutar el proceso ETL.

   **etl_modulos/:** Módulos de ETL.
   
     **init.py:** Inicialización del módulo.
     **extract.py:** Código para la extracción de datos.
     **transform.py:** Código para la transformación de datos.
     **load.py:** Código para la carga de datos en Redshift.

**raw_data/:** Contiene datos cargados de manera manual.

   **data.csv:** Archivo del DAG para el proceso ETL.

   **load_csv_rawdata.py:** Script para cargar de manera manual datos desde un archivo csv

   **raw_data.py:** script para lectura de csv

**.gitignore:** Archivos y carpetas que Git debe ignorar.

**docker-compose.yml:** Configuración para desplegar el entorno de Airflow y otras dependencias.

**README.md:** Este archivo, con detalles del proyecto y uso.

**requirements.txt:** Dependencias necesarias para el proyecto.

## Instrucciones de Uso


1. **Configura el Archivo de Configuración:**
    Edita config/config.ini con las credenciales de tu base de datos Redshift.

2. **Ejecuta el DAG de Airflow:**
   
    Asegúrate de que Docker y Docker Compose estén instalados.
   
    Construye la imagen Docker y levanta los contenedores con:
   
        docker-compose up --build

    Accede a la interfaz web de Airflow para ejecutar el DAG daily_etl_dag.

4. **Carga de Datos desde CSV:**(Opcional) en el caso de querer cargar datos en la tabla desde un archivo csv
    
       python raw_data/load_csv_rawdata.py

## Verifica los Datos:

Accede a tu base de datos Redshift y revisa la tabla tasa_divisas para confirmar que los datos se han cargado y actualizado correctamente.

    select *
    from veraramirez12_coderhouse.tasa_divisas td 
