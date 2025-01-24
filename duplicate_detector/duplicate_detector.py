import os
import hashlib
from googleapiclient.errors import HttpError

from download_files import download_folder


def generate_file_hash(file_path):
    """
    Genera el hash de un archivo utilizando el algoritmo SHA-256.

    :param file_path: Ruta del archivo.
    :return: Hash del archivo como una cadena hexadecimal.
    """
    hash_func = hashlib.new("sha256")
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def detect_duplicates(file_paths):
    """
    Detecta archivos duplicados basándose en sus hashes.

    :param file_paths: Lista de rutas de archivos.
    :return: Lista de archivos duplicados.
    """
    hashes = {}
    duplicates = []

    for file_path in file_paths:
        file_hash = generate_file_hash(file_path)
        if file_hash in hashes:
            duplicates.append(file_path)
        else:
            hashes[file_hash] = file_path
    return duplicates

def remove_duplicates_local(service):
    """
    Detecta y elimina archivos duplicados en un directorio local.

    :param directory: Ruta del directorio que contiene los archivos.
    """
    # descarga de archivos desde el drive
    directory = download_folder(service)

    file_paths = [os.path.join(directory, file_name) for file_name in os.listdir(directory) if os.path.isfile(os.path.join(directory, file_name))]
    duplicates = detect_duplicates(file_paths)
    for duplicate in duplicates:
        os.remove(duplicate)
        print(f"Archivo duplicado eliminado: {duplicate}")

def clear_drive(service):
    """
    Elimina todos los archivos de Google Drive.

    :param service: Servicio autenticado de Google Drive.
    """

    remove_duplicates_local("images")

    try:
        # Listar todos los archivos en Google Drive
        files = []
        page_token = None

        while True:
            response = service.files().list(
                q="trashed=false",
                spaces="drive",
                fields="nextPageToken, files(id, name)",
                pageToken=page_token
            ).execute()

            files.extend(response.get('files', []))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

        # Eliminar todos los archivos encontrados
        for file in files:
            file_id = file['id']
            file_name = file['name']
            service.files().delete(fileId=file_id).execute()
            print(f"Archivo eliminado en Drive: {file_name} (ID: {file_id})")

    except HttpError as error:
        print(f"Error al limpiar Google Drive: {error}")





