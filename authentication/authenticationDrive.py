from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

# Alcances necesarios para el acceso a Google Drive
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/drive.metadata.readonly'
]

def authenticate():
    """Autentica con Google Drive y devuelve el servicio autenticado."""
    creds = None
    try:
        # Base relativa al script
        base_path = os.path.abspath(os.path.dirname(__file__))
        token_path = os.path.join(base_path, "data", "token.pickle")
        client_secret_path = os.path.join(base_path, "client_secret_483676039355-ig9cahphvluaq6eqocvi9lv6o9h2dq0i.apps.googleusercontent.com.json")

        # Verificar si existe un token almacenado previamente
        if os.path.exists(token_path):
            print("Cargando token existente...")
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)

        # Si no hay credenciales válidas, iniciar autenticación
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("Actualizando token existente...")
                creds.refresh(Request())
            else:
                if not os.path.exists(client_secret_path):
                    raise FileNotFoundError(f"El archivo client_secret.json no se encuentra en: {client_secret_path}")
                print("Iniciando flujo de autenticación...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    client_secret_path,
                    SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Guardar el token en un archivo para futuras ejecuciones
            print("Guardando token...")
            os.makedirs(os.path.dirname(token_path), exist_ok=True)  # Crear carpeta si no existe
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
            print(f"Token guardado exitosamente en: {token_path}")

        else:
            print("Token válido cargado.")

        # Construir el servicio de Google Drive
        service = build('drive', 'v3', credentials=creds)
        return service

    except Exception as e:
        print(f"Error durante el proceso de autenticación o guardado: {e}")
        return None