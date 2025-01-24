import os

import googleapiclient.http
from googleapiclient.errors import HttpError


def get_account_email(service):
    """
    Obtiene la dirección de correo electrónico de la cuenta autenticada.
    """
    try:
        user_info = service.about().get(fields="user/emailAddress").execute()
        return user_info.get('user').get('emailAddress')
    except HttpError as error:
        print(f"No se pudo obtener el email de la cuenta: {error}")
        return "Cuenta Desconocida"

# Función para descargar archivos de diferentes tipos por cliente
def download_files(service, client_name):
    """
    Descarga archivos de diferentes tipos desde Google Drive y los organiza
    en carpetas por cliente.
    """
    folder_id = 'root'  
    query = f"'{folder_id}' in parents"
    base_folder = "descargarportipo\descargas"  # Cambiar al usar el servidor

    # Crear carpeta del cliente
    client_folder = os.path.join(base_folder, client_name)
    if not os.path.exists(client_folder):
        os.makedirs(client_folder)

    # Diccionario para asociar tipos MIME con extensiones
    mime_to_extension = {
        'audio/': 'audio',
        'image/': 'imagen',
        'application/': 'texto',
        'video/': 'video'
    }

    # Crear las subcarpetas dentro de la carpeta del cliente
    for subfolder in list(mime_to_extension.values()) + ['desconocido']:
        subfolder_path = os.path.join(client_folder, subfolder)
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)

    try:
        results = service.files().list(
            q=query,
            spaces='drive',
            fields="files(id, name, mimeType)"
        ).execute()

        files = results.get('files', [])

        if not files:
            print(f"No se encontraron archivos para el cliente {client_name}.")
            return

        # Descarga
        downloaded_types = set()

        for file in files:
            file_name = file['name']
            file_id = file['id']
            mime_type = file['mimeType']

            # Determinar la categoría del archivo
            category = 'desconocido' 
            for mime_prefix, cat in mime_to_extension.items():
                if mime_type.startswith(mime_prefix):
                    category = cat
                    break

            # Definir la ruta de descarga en la subcarpeta que le corresponda
            category_folder = os.path.join(client_folder, category)
            file_path = os.path.join(category_folder, file_name)

            try:
                request = service.files().get_media(fileId=file_id)
                with open(file_path, 'wb') as f:
                    downloader = googleapiclient.http.MediaIoBaseDownload(f, request)
                    done = False
                    while not done:
                        status, done = downloader.next_chunk()
                        print(f"Descargando: {file_name} -> Categoría: {category} ({int(status.progress() * 100)}%)")

                downloaded_types.add(category)
                print(f"Archivo descargado en {category_folder}: {file_name}")
                # os.remove("data/authentication/token.pickle")  # Eliminar el token de autenticación
            except HttpError as error:
                print(f"No se pudo descargar {file_name}: {error}")
                # os.remove("data/authentication/token.pickle")  # Eliminar el token de autenticación
    except HttpError as error:
        print(f"Ocurrió un error al procesar al cliente {client_name}: {error}")


