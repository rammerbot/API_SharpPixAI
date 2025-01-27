from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
import os
import pickle

# Alcances necesarios para el acceso a Google Drive
SCOPES = [
    
    'https://www.googleapis.com/auth/drive.file',
  
  
]

def get_auth_url():
    """Generates the authorization URL."""
    try:
        base_path = os.path.abspath(os.path.dirname(__file__))
        client_secret_path = os.path.join(base_path, "client_4836.json")

        # Initiate the flow of authentication
        flow = Flow.from_client_secrets_file(
            client_secret_path,
            SCOPES,
            redirect_uri="https://etl-machine-learning-api-movie.onrender.com/callback/"
        )
        auth_url, _ = flow.authorization_url(prompt='consent')

        return {"auth_url": auth_url}

    except Exception as e:
        return {"error": f"Error generating the authorization URL: {e}"}
    
def auth_callback(code):
    """Handles the authorization callback and creates the Drive service."""
    try:
        base_path = os.path.abspath(os.path.dirname(__file__))
        flow = Flow.from_client_secrets_file(
            os.path.join(base_path, "client_4836.json"),
            SCOPES,
            redirect_uri="https://etl-machine-learning-api-movie.onrender.com/callback/"
        )
    
        # Obtain credentials using the authorization code
        creds = flow.fetch_token(authorization_response=f"https://etl-machine-learning-api-movie.onrender.com/callback/?code={code}")
      
        # Save credentials to a pickle file (optional)
        
        token_path = os.path.join(base_path, "data", "client_4836.json")
        
        os.makedirs(os.path.dirname(token_path), exist_ok=True)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)  # Save credentials for future use (optional)
        
        # Create the Drive service
        service = build('drive', 'v3', credentials=flow.credentials)
        return {"message": "Autenticación exitosa", "service": service}
    except Exception as e:
        return {"error": f"Error during authentication: {e}"}




# def authenticate():
#     creds = None
#     try:
#         base_path = os.path.abspath(os.path.dirname(__file__))
#         token_path = os.path.join(base_path, "data", "token.pickle")
#         client_secret_path = os.path.join(base_path, "client_secret_4836.json")

#         if os.path.exists(token_path):
#             print("Cargando token existente...")
#             with open(token_path, 'rb') as token:
#                 creds = pickle.load(token)

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
#                     SCOPES,
#                     redirect_uri="http://localhost:8000/callback/"
#                 )
#                 # Usa run_local_server() pero sin abrir una ventana del navegador
#                 auth_url, _ = flow.authorization_url(prompt='consent')  # Obtener la URL de autorización
#                 print(f"Por favor, abre la siguiente URL en tu navegador y autoriza el acceso:\n{auth_url}")
#                 code = input("Introduce el código de autorización: ")  # Pide el código de autorización al usuario
#                 creds = flow.fetch_token(authorization_response=code)

#             print("Guardando token...")
#             os.makedirs(os.path.dirname(token_path), exist_ok=True)
#             with open(token_path, 'wb') as token:
#                 pickle.dump(creds, token)
#             print(f"Token guardado exitosamente en: {token_path}")

#         else:
#             print("Token válido cargado.")

#         service = build('drive', 'v3', credentials=creds)
#         return service

#     except Exception as e:
#         print(f"Error durante el proceso de autenticación o guardado: {e}")
#         return None