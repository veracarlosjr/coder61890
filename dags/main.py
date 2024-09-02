from etl_modulos.extract import extract_data
from etl_modulos.transform import transform_data
from etl_modulos.load import load_data
import configparser
from datetime import datetime

def main():
    base_currency = "USD"
    quote_currency = "EUR"
    date = datetime.now().strftime("%Y-%m-%d")
    
    api_url = f"https://api.frankfurter.app/{date}?from={base_currency}&to={quote_currency}"
    
    # Leer credenciales desde el archivo config.ini
    config = configparser.ConfigParser()
    config_path = '/opt/airflow/config/config.ini'  
    try:
        config.read(config_path)
    except FileNotFoundError:
        print(f"El archivo de configuración no se encontró en la ruta: {config_path}")
        return
    
    try:
        # Proceso ETL
        data = extract_data(api_url)
        transformed_data = transform_data(data)
        load_data(transformed_data, config)
    except Exception as e:
        print(f"Ocurrió un error durante el proceso ETL: {e}")

if __name__ == "__main__":
    main()
