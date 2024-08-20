import pandas as pd

def read_csv(file_path):
    try:
        # Leer el archivo CSV
        df = pd.read_csv(file_path)
        
        # Imprimir las primeras filas para verificar el contenido
        print("Datos del archivo CSV:")
        print(df.head())
        
        # Imprimir información del DataFrame
        print("\nInformación del DataFrame:")
        print(df.info())
        
        # Verificar si hay valores nulos
        print("\nValores nulos en el DataFrame:")
        print(df.isnull().sum())
        
        # Verificar duplicados
        print("\nDuplicados en el DataFrame:")
        print(df.duplicated().sum())
        
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")

# Ruta al archivo CSV
file_path = 'raw_data/data.csv'
read_csv(file_path)