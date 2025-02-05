import os
import requests

import googleapiclient.http
from googleapiclient.errors import HttpError

from authentication import authenticate


def download_media_item(request, callback):
    """
    Descarga un archivo (foto o video) desde Google Photos.
    
    :param media_item: Un diccionario que representa un mediaItem de la API de Google Photos.
    :param download_dir: Directorio donde se guardarán los archivos descargados.
    :return: Ruta del archivo descargado.
    """

    download_dir="downloads"

    media_item = authenticate(request, callback)
    return media_item

    # try:
    #     # Crear el directorio de descargas si no existe
    #     os.makedirs(download_dir, exist_ok=True)
        
    #     # Obtener la URL base y el nombre del archivo
    #     base_url = media_item.get("baseUrl")
    #     filename = media_item.get("filename")
        
    #     if not base_url or not filename:
    #         raise ValueError("El mediaItem no contiene baseUrl o filename.")
        
    #     # Construir la URL de descarga (agregar parámetro para máxima resolución)
    #     download_url = f"{base_url}=d"  # "=d" descarga el archivo en su resolución original
        
    #     # Ruta completa del archivo descargado
    #     file_path = os.path.join(download_dir, filename)
        
    #     # Descargar el archivo
    #     response = requests.get(download_url)
    #     response.raise_for_status()  # Lanza una excepción si la descarga falla
        
    #     # Guardar el archivo en el directorio de descargas
    #     with open(file_path, "wb") as file:
    #         file.write(response.content)
        
    #     return file_path
    
    # except Exception as e:
    #     print(f"Error al descargar el archivo {filename}: {str(e)}")
    #     return None

