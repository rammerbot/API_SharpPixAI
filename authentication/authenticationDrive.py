import os
import sys

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport import Request
from googleapiclient.discovery import build







SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/docs',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.metadata.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]


BASE_PATH = os.path.abspath(os.path.dirname(__file__))
SECRET_CLIENT = os.path.join(BASE_PATH, "client_secret_483676039355-935r0fq0itqhvrs59m0j02q93ga0krmv.apps.googleusercontent.com.json")
TOKEN = os.path.join(BASE_PATH, 'data', 'token.pickle')


def request_creds():
    creds = None
    if os.path.exists(SECRET_CLIENT):
        flow = InstalledAppFlow.from_client_secrets_file(SECRET_CLIENT, SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        return Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        print('credentials not present')
        sys.exit(1)

def get_creds():
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        return creds
    return request_creds()


def search_file():
    creds = get_creds()
    try:
        service = build('drive', 'v3',credentials=creds)
        if service:
            return {'message': f'objeto creado: {service}'}
    
    except Exception as e:
        return {'error' : f'error al crear servicio: {e}'}


# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# import os
# import pickle

# # Alcances necesarios para el acceso a Google Drive
# SCOPES = [
#     'https://www.googleapis.com/auth/drive',
#     'https://www.googleapis.com/auth/drive.file',
#     'https://www.googleapis.com/auth/drive.readonly',
#     'https://www.googleapis.com/auth/drive.metadata.readonly'
# ]

# def authenticate():
#     """Autentica con Google Drive y devuelve el servicio autenticado."""
#     creds = None
#     try:
#         # Base relativa al script
#         base_path = os.path.abspath(os.path.dirname(__file__))
#         token_path = os.path.join(base_path, "data", "token.pickle")
#         client_secret_path = os.path.join(base_path, "client_secret_483676039355-935r0fq0itqhvrs59m0j02q93ga0krmv.apps.googleusercontent.com.json")

#         # Verificar si existe un token almacenado previamente
#         if os.path.exists(token_path):
#             print("Cargando token existente...")
#             with open(token_path, 'rb') as token:
#                 creds = pickle.load(token)

#         # Si no hay credenciales válidas, iniciar autenticación
#         if not creds or not creds.valid:
#             if creds and creds.expired and creds.refresh_token:
#                 print("Actualizando token existente...")
#                 creds.refresh(Request())
#             else:
#                 if not os.path.exists(client_secret_path):
#                     raise FileNotFoundError(f"El archivo client_secret.json no se encuentra en: {client_secret_path}")
#                 print("Iniciando flujo de autenticación...")

#                 flow = InstalledAppFlow.from_client_secrets_file(
#                     client_secret_path,
#                     SCOPES
#                 )
#                 # Capturar la URL de autenticación
#                 auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')

#                 print(f"Por favor, ve a este enlace para autorizar la aplicación: {auth_url}")
#                 # Si deseas capturar el código manualmente, puedes agregar un paso adicional aquí

#                 # Nota: El siguiente paso es manual; el usuario debe ingresar el código de autorización
#                 code = input("Introduce el código de autorización: ")
#                 creds = flow.fetch_token(authorization_response=code)

#             # Guardar el token en un archivo para futuras ejecuciones
#             print("Guardando token...")
#             os.makedirs(os.path.dirname(token_path), exist_ok=True)  # Crear carpeta si no existe
#             with open(token_path, 'wb') as token:
#                 pickle.dump(creds, token)
#             print(f"Token guardado exitosamente en: {token_path}")

#         else:
#             print("Token válido cargado.")

#         # Construir el servicio de Google Drive
#         service = build('drive', 'v3', credentials=creds)
#         return service

#     except Exception as e:
#         print(f"Error durante el proceso de autenticación o guardado: {e}")
#         return None



# # def authenticate():
# #     """Autentica con Google Drive y devuelve el servicio autenticado."""
# #     creds = None
# #     try:
# #         # Base relativa al script
# #         base_path = os.path.abspath(os.path.dirname(__file__))
# #         token_path = os.path.join(base_path, "data", "token.pickle")
# #         client_secret_path = os.path.join(base_path, "client_secret_483676039355-ig9cahphvluaq6eqocvi9lv6o9h2dq0i.apps.googleusercontent.com.json")

# #         # Verificar si existe un token almacenado previamente
# #         if os.path.exists(token_path):
# #             print("Cargando token existente...")
# #             with open(token_path, 'rb') as token:
# #                 creds = pickle.load(token)

# #         # Si no hay credenciales válidas, iniciar autenticación
# #         if not creds or not creds.valid:
# #             if creds and creds.expired and creds.refresh_token:
# #                 print("Actualizando token existente...")
# #                 creds.refresh(Request())
# #             else:
# #                 if not os.path.exists(client_secret_path):
# #                     raise FileNotFoundError(f"El archivo client_secret.json no se encuentra en: {client_secret_path}")
# #                 print("Iniciando flujo de autenticación...")
# #                 flow = InstalledAppFlow.from_client_secrets_file(
# #                     client_secret_path,
# #                     SCOPES
# #                 )
# #                 creds = flow.run_local_server(port=0)

# #             # Guardar el token en un archivo para futuras ejecuciones
# #             print("Guardando token...")
# #             os.makedirs(os.path.dirname(token_path), exist_ok=True)  # Crear carpeta si no existe
# #             with open(token_path, 'wb') as token:
# #                 pickle.dump(creds, token)
# #             print(f"Token guardado exitosamente en: {token_path}")

# #         else:
# #             print("Token válido cargado.")

# #         # Construir el servicio de Google Drive
# #         service = build('drive', 'v3', credentials=creds)
# #         return service

# #     except Exception as e:
# #         print(f"Error durante el proceso de autenticación o guardado: {e}")
# #         return None