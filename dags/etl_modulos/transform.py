def transform_data(data):
    print("Datos recibidos para transformar:", data)  # Esto imprimirá los datos en los logs de Airflow
    transformed_data = []
    
    # Validar claves esperadas en el diccionario
    if not all(key in data for key in ['base', 'date', 'rates']):
        raise ValueError("Data is missing required keys")
    
    base_currency = data['base']
    date = data['date']
    rates = data['rates']
    
    for quote_currency, rate in rates.items():
        transformed_data.append((base_currency, quote_currency, rate, date))
    
    return transformed_data

