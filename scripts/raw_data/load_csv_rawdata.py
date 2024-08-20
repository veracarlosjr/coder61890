import pandas as pd
import psycopg2
from psycopg2 import sql
import configparser

def read_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

def load_data(df, config, table_name='tasa_divisas'):
    try:
        conn = psycopg2.connect(
            dbname=config['redshift']['dbname'],
            user=config['redshift']['user'],
            password=config['redshift']['password'],
            host=config['redshift']['host'],
            port=config['redshift']['port']
        )
        cursor = conn.cursor()
        
        # Crear la tabla principal si no existe
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id BIGINT IDENTITY(1,1) PRIMARY KEY,
            divisa_base VARCHAR(5),
            divisa_cambio VARCHAR(5),
            tasa FLOAT,
            fecha_tasa DATE,
            fecha_modificacion DATE DEFAULT CURRENT_DATE
        )
        """
        cursor.execute(create_table_query)

        # Crear tabla temporal
        temp_table_name = f"{table_name}_temp"
        create_temp_table_query = f"""
        CREATE TEMP TABLE {temp_table_name} (
            divisa_base VARCHAR(5),
            divisa_cambio VARCHAR(5),
            tasa FLOAT,
            fecha_tasa DATE
        )
        """
        cursor.execute(create_temp_table_query)
        
        # Insertar los datos en la tabla temporal
        insert_temp_query = f"""
        INSERT INTO {temp_table_name} (divisa_base, divisa_cambio, tasa, fecha_tasa)
        VALUES (%s, %s, %s, %s)
        """
        cursor.executemany(insert_temp_query, df.values.tolist())
        
        # Actualizar o insertar los datos en la tabla principal desde la tabla temporal
        upsert_query = f"""
        BEGIN;
        
        DELETE FROM {table_name} USING {temp_table_name}
        WHERE {table_name}.divisa_base = {temp_table_name}.divisa_base
          AND {table_name}.divisa_cambio = {temp_table_name}.divisa_cambio
          AND {table_name}.fecha_tasa = {temp_table_name}.fecha_tasa;

        INSERT INTO {table_name} (divisa_base, divisa_cambio, tasa, fecha_tasa)
        SELECT divisa_base, divisa_cambio, tasa, fecha_tasa
        FROM {temp_table_name};

        COMMIT;
        """
        cursor.execute(upsert_query)

        conn.commit()
        cursor.close()
        conn.close()
    except psycopg2.Error as redshift_err:
        print(f"Redshift error: {redshift_err}")

def main():
    config = configparser.ConfigParser()
    config.read('config/config.ini')

    # Leer datos desde el archivo CSV
    df = read_csv('raw_data/data.csv')
    
    if df is not None:
        # Cargar datos en Redshift
        load_data(df, config)
        print("Datos cargados en Redshift con éxito.")
    else:
        print("No se pudo cargar el archivo CSV.")

if __name__ == "__main__":
    main()