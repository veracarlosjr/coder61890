import requests
import psycopg2
from datetime import datetime
import configparser

class APIError(Exception):
    """Exception raised for errors in the API request."""
    def __init__(self, message, status_code=None):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

# Función para extraer los datos desde la API
def extract_data(api_url):
    try:
        response = requests.get(api_url, timeout=10)  # Añadir timeout de 10 segundos
        response.raise_for_status()  # Levantar excepción para códigos de estado HTTP 4xx/5xx
        return response.json()
    except requests.exceptions.Timeout as exc:
        raise APIError("Request timed out") from exc
    except requests.exceptions.HTTPError as http_err:
        raise APIError(f"HTTP error occurred: {http_err}") from http_err
    except requests.exceptions.RequestException as req_err:
        raise APIError(f"Error occurred: {req_err}") from req_err

# Función para transformar los datos en el formato adecuado
def transform_data(data):
    transformed_data = []
    base_currency = data['base']
    date = data['date']
    rates = data['rates']
    
    for quote_currency, rate in rates.items():
        transformed_data.append((base_currency, quote_currency, rate, date))
    
    return transformed_data

# Función para insertar o actualizar los datos en una base de datos Redshift
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
        print(f"Operational error: {op_err}")
    except psycopg2.ProgrammingError as prog_err:
        print(f"Programming error: {prog_err}")
    except psycopg2.DatabaseError as db_err:
        print(f"Database error: {db_err}")

# Función principal
def main():
    base_currency = "USD"
    quote_currency = "EUR"
    date = datetime.now().strftime("%Y-%m-%d")
    
    api_url = f"https://api.frankfurter.app/{date}?from={base_currency}&to={quote_currency}"
    
    # Leer credenciales desde el archivo config.ini
    config = configparser.ConfigParser()
    try:
        config.read('config/config.ini')
    except configparser.Error as cfg_err:
        print(f"Configuration file error: {cfg_err}")
        return
    
    # Proceso ETL
    try:
        data = extract_data(api_url)
        transformed_data = transform_data(data)
        load_data(transformed_data, config)
        print("ETL process completed successfully.")
    except APIError as api_err:
        print(f"API Error: {api_err}")
    except psycopg2.Error as redshift_err:
        print(f"Redshift error: {redshift_err}")

if __name__ == "__main__":
    main()