import psycopg2
from etl_modulos.exceptions import DatabaseError

def load_data(data, config, table_name='tasa_divisas'):
    try:
        conn = psycopg2.connect(
            dbname=config['redshift']['dbname'],
            user=config['redshift']['user'],
            password=config['redshift']['password'],
            host=config['redshift']['host'],
            port=config['redshift']['port']
        )
        cursor = conn.cursor()
        
        # Crear la tabla si no existe
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
        
        # Eliminar filas existentes con la misma clave compuesta
        delete_query = f"""
        DELETE FROM {table_name}
        WHERE divisa_base = %s AND divisa_cambio = %s AND fecha_tasa = %s
        """
        
        # Insertar los datos
        insert_query = f"""
        INSERT INTO {table_name} (divisa_base, divisa_cambio, tasa, fecha_tasa)
        VALUES (%s, %s, %s, %s)
        """
        
        for record in data:
            cursor.execute(delete_query, (record[0], record[1], record[3]))
            cursor.execute(insert_query, record)
        
        conn.commit()
        cursor.close()
        conn.close()
    except psycopg2.OperationalError as op_err:
        raise DatabaseError(f"Operational error: {op_err}") from op_err
    except psycopg2.ProgrammingError as prog_err:
        raise DatabaseError(f"Programming error: {prog_err}") from prog_err
    except psycopg2.DatabaseError as db_err:
        raise DatabaseError(f"Database error: {db_err}") from db_err