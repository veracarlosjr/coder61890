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

  -- config/
  
    └── config.ini
  -- scripts/
  
    script.py
    raw_data/
      ├── load_csv_rawdata.py
      ├── raw_data.py
      
  -- README.md

## Instrucciones de Uso


1. **Configura el Archivo de Configuración:**
    Edita config/config.ini con las credenciales de tu base de datos Redshift.

2. **Ejecuta el Script:**
    Asegúrate de tener las dependencias instaladas (requests, psycopg2, pandas).
    Ejecuta el script con el siguiente comando:
   
        python scripts/script.py

4. **Carga de Datos desde CSV:**
    Para cargar datos desde un archivo CSV y realizar pruebas de ETL, ejecuta el script:
   
       python scripts/load_csv_rawdata.py

## Verifica los Datos:

Accede a tu base de datos Redshift y revisa la tabla tasa_divisas para confirmar que los datos se han cargado y actualizado correctamente.

    select *
    from veraramirez12_coderhouse.tasa_divisas td 
