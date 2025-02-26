import os
import requests

from authentication import authenticate


import os
import requests

from authentication import authenticate

def download_media_item(request, callback):
    """
    Descarga un archivo (foto o video) desde Google Photos.
    
    :param request: Objeto de solicitud para la autenticación.
    :param callback: Tipo de archivo a descargar ("video", "image" o "duplicate").
    :return: Una tupla con la ruta del directorio y una lista de tuplas (nombre_archivo, id_archivo).
    """
    download_dir = "downloads_" + callback
    # Crear el directorio de descargas si no existe
    os.makedirs(download_dir, exist_ok=True)

    # Autenticación del usuario y obtener la metadata de los archivos
    media_items = authenticate(request, callback).get('media_items', [])

    # Lista para almacenar tuplas (nombre_archivo, id_archivo)
    file_info = []

    # Iteración sobre la lista de metadatos
    for media_item in media_items:
        # Obtener el tipo MIME del archivo
        mime_type = media_item.get('mimeType', '')

        # Filtrar según el tipo de archivo
        if callback == 'video' and not mime_type.startswith('video/'):
            continue
        elif callback == 'image' and not mime_type.startswith('image/'):
            continue
        elif callback not in ('video', 'image', 'duplicate'):
            raise ValueError("Error en el callback, llamada al archivo inadecuado")

        try:
            # Obtener la URL base, el nombre del archivo y el ID
            base_url = media_item.get("baseUrl")
            filename = media_item.get("filename")
            file_id = media_item.get("id")  # Obtener el ID del archivo
            
            if not base_url or not filename or not file_id:
                raise ValueError("El mediaItem no contiene baseUrl, filename o ID.")

            # Construir la URL de descarga (agregar parámetro para máxima resolución)
            download_url = f"{base_url}=d"  # "=d" descarga el archivo en su resolución original

            # Ruta completa del archivo descargado
            file_path = os.path.join(download_dir, filename)

            # Descargar el archivo
            response = requests.get(download_url)
            response.raise_for_status()  # Lanza una excepción si la descarga falla

            # Guardar el archivo en el directorio de descargas
            with open(file_path, "wb") as file:
                file.write(response.content)

            # Almacenar el nombre del archivo y su ID
            file_info.append((filename, file_id))

        except Exception as e:
            print(f"Error al descargar el archivo {filename}: {str(e)}")

    # Ruta absoluta del directorio de descargas
    path_dir = os.path.abspath(download_dir)

    # Devolver el directorio y la lista de tuplas (nombre_archivo, id_archivo)
    return path_dir, file_info

def delete_media_item(media_item_id, access_token):
    """
    Elimina un archivo de Google Photos usando su ID.
    """
    url = f"https://photoslibrary.googleapis.com/v1/mediaItems/{media_item_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        print(f"Archivo {media_item_id} eliminado de Google Photos.")
    else:
        print(f"Error al eliminar {media_item_id}: {response.status_code} - {response.text}")
        raise Exception(f"Error al eliminar {media_item_id}: {response.text}")

def upload_media_item(file_path, access_token):
    """
    Sube un archivo a Google Photos.
    """
    # Paso 1: Obtener la URL de subida
    upload_url = "https://photoslibrary.googleapis.com/v1/uploads"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-type": "application/octet-stream",
        "X-Goog-Upload-File-Name": os.path.basename(file_path),
        "X-Goog-Upload-Protocol": "raw",
    }
    with open(file_path, "rb") as file:
        response = requests.post(upload_url, headers=headers, data=file)
    
    if response.status_code != 200:
        print(f"Error al subir {file_path}: {response.status_code} - {response.text}")
        raise Exception(f"Error al subir {file_path}: {response.text}")

    upload_token = response.text

    # Paso 2: Crear el mediaItem en Google Photos
    create_url = "https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-type": "application/json",
    }
    payload = {
        "newMediaItems": [
            {
                "description": "Archivo comprimido",
                "simpleMediaItem": {
                    "uploadToken": upload_token,
                },
            }
        ]
    }
    response = requests.post(create_url, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"Archivo {file_path} subido a Google Photos.")
    else:
        print(f"Error al crear mediaItem para {file_path}: {response.status_code} - {response.text}")
        raise Exception(f"Error al crear mediaItem para {file_path}: {response.text}")