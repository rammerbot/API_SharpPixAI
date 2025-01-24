import io
import os
import mimetypes
import uuid
import shutil

from googleapiclient.http import MediaIoBaseDownload

def get_unique_filename(directory, filename):
    base, extension = os.path.splitext(filename)
    counter = 1
    new_filename = filename

    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base}_{counter}{extension}"
        counter += 1

    return new_filename
# Función para descargar listar archivos y subcarpetas
def list_files_in_folder(service):
    """
    Lista todos los archivos en una carpeta de Google Drive, eliminando el límite de 1000 archivos mediante paginado.
    """
    query = f"'root' in parents and trashed = false"
    all_files = []  # Lista para almacenar todos los archivos
    page_token = None  # Inicialmente no hay token de paginado

    while True:
        # Solicita una página de resultados
        results = service.files().list(
            q=query,
            pageSize=1000,  # Tamaño máximo permitido por la API
            fields="nextPageToken, files(id, name, mimeType)",
            pageToken=page_token  # Token para obtener la siguiente página
        ).execute()

        # Agregar los archivos de la página actual a la lista total
        files = results.get('files', [])
        all_files.extend(files)

        # Obtener el siguiente token de página (si existe)
        page_token = results.get('nextPageToken', None)
        if not page_token:
            # Si no hay más páginas, salir del bucle
            break

    return all_files

# Función para descargar un archivo
def download_file(file_id, file_name, service):
    request = service.files().get_media(fileId=file_id)
    with io.FileIO(file_name, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Descargando {file_name}... {int(status.progress() * 100)}%")

def download_folder(service, folder_name_):
    """
    Descarga todos los archivos y carpetas de forma recursiva de Google Drive, eliminando el límite de 1000 archivos.
    """

    unique_folder = str(uuid.uuid4()) # UUID en formato str
    folder_name = os.path.join(folder_name_+ unique_folder) # Crear la ruta del nombre
    
    # Crear la carpeta local si no existe
    os.makedirs(folder_name, exist_ok=True)
    os.makedirs(f"{folder_name}2", exist_ok=True)
    
    # Para archivos de videos
    if folder_name_ == "videos":

        # Obtener todos los archivos de la carpeta actual (con manejo de paginado)
        files = list_files_in_folder(service)
        downloaded_files = {}
        for file in files:
            file_id = file['id']
            file_name = file['name']
            
            # Si el archivo es una carpeta, descargar recursivamente
            if file['mimeType'] == 'application/vnd.google-apps.folder':
                download_folder(file_id, f"{folder_name}/{file_name}")

            else:
                # Verifica que el archivo sea un video
                mime_types, _ = mimetypes.guess_type(file_name)
                if mime_types and mime_types.startswith("video"):
                    # Si es un archivo, descargarlo
                    download_file(file_id, f"{folder_name}/{file_name}", service)
                    unique_file_name = get_unique_filename(f"{folder_name}2",file_name)
                    shutil.move(f"{folder_name}/{file_name}",f"{folder_name}2/{unique_file_name}")
                    # Guardar en diccionario
                    downloaded_files[file_id] = file_name
                else:
                    continue
        return (f"{folder_name}2", downloaded_files)
    

    # para imagenes
    if folder_name_ == "images":

        # Obtener todos los archivos de la carpeta actual (con manejo de paginado)
        files = list_files_in_folder(service)

        for file in files:
            file_id = file['id']
            file_name = file['name']

            # Si el archivo es una carpeta, descargar recursivamente
            if file['mimeType'] == 'application/vnd.google-apps.folder':
                download_folder(file_id, f"{folder_name}/{file_name}")
            else:
                # Verifica que el archivo sea un video
                mime_types, _ = mimetypes.guess_type(file_name)
                if mime_types and mime_types.startswith("image"):
                 # Si es un archivo, descargarlo
                    download_file(file_id, f"{folder_name}/{file_name}", service)
                    unique_file_name = get_unique_filename(f"{folder_name}2",file_name)
                    shutil.move(f"{folder_name}/{file_name}",f"{folder_name}2/{unique_file_name}")
                    # Guardar en diccionario
                    downloaded_files[file_id] = file_name
                else:
                    continue
        return (f"{folder_name}2", downloaded_files)
    
    # Para todos los formatos
    if folder_name_ == "all":

        # Obtener todos los archivos de la carpeta actual (con manejo de paginado)
        files = list_files_in_folder(service)

        for file in files:
            file_id = file['id']
            file_name = file['name']

            # Si el archivo es una carpeta, descargar recursivamente
            if file['mimeType'] == 'application/vnd.google-apps.folder':
                download_folder(file_id, f"{folder_name}/{file_name}")
            else:
                 # Si es un archivo, descargarlo
                    download_file(file_id, f"{folder_name}/{file_name}", service)
                    unique_file_name = get_unique_filename(f"{folder_name}2",file_name)
                    shutil.move(f"{folder_name}/{file_name}",f"{folder_name}2/{unique_file_name}")
                    # Guardar en diccionario
                    downloaded_files[file_id] = file_name
        return (f"{folder_name}2", downloaded_files)
