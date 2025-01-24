import os
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# Autenticación con la API de Google Drive
def authenticate_google_drive():
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    creds = None
    # Lee las credenciales almacenadas
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('client_secret_483676039355-ig9cahphvluaq6eqocvi9lv6o9h2dq0i.apps.googleusercontent.com.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise RuntimeError("Necesitas autenticación manual.")
    return build('drive', 'v3', credentials=creds)

# Función para crear un nombre único para el archivo destino
def get_unique_filename(filename):
    base, extension = os.path.splitext(filename)
    counter = 1
    unique_filename = filename
    while os.path.exists(unique_filename):
        unique_filename = f"{base}_{counter}{extension}"
        counter += 1
    return unique_filename

# Función para descargar el archivo
def download_file(file_id, destination):
    service = authenticate_google_drive()

    # Genera un nombre único si el archivo ya existe
    unique_destination = get_unique_filename(destination)

    # Solicita la descarga del archivo
    request = service.files().get_media(fileId=file_id)
    with io.FileIO(unique_destination, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Descargando {int(status.progress() * 100)}%")
    print(f"Archivo descargado como: {unique_destination}")

# ID del archivo en Google Drive
file_id = 'ID_DEL_ARCHIVO'  # Reemplaza con el ID real del archivo

# Ruta donde deseas guardar el archivo
destination = 'archivo_descargado.txt'

# Llama a la función para descargar el archivo
download_file(file_id, destination)
