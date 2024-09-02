import requests
from etl_modulos.exceptions import APIError

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
