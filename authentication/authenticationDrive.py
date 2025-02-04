import os
import sys
from typing import Optional, List, Dict
import secrets
import requests

from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from fastapi import Request


# Configuración del flujo OAuth
CLIENT_SECRETS_FILE = "client_secrets.json"

SCOPES = [
    "https://www.googleapis.com/auth/photoslibrary.appendonly",
    "https://www.googleapis.com/auth/photoslibrary.edit.appcreateddata",
    "https://www.googleapis.com/auth/photoslibrary.readonly",
    "https://www.googleapis.com/auth/photoslibrary.sharing"
]

REDIRECT_URI = "https://etl-machine-learning-api-movie.onrender.com/callback/"

# Almacenar estados temporalmente (usar Redis en producción)
oauth_states = {}

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
SECRET_CLIENT = os.path.join(BASE_PATH, "client_secret_483676039355-935r0fq0itqhvrs59m0j02q93ga0krmv.apps.googleusercontent.com.json")
TOKEN = os.path.join(BASE_PATH, 'data', 'token.pickle')

def request_creds():

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    
    state = secrets.token_urlsafe(16)
    oauth_states[state] = None
    
    # Quita include_granted_scopes o establece en "false"
    authorization_url, _ = flow.authorization_url(
        access_type="offline",
        state=state
    )
    
    return {'message': authorization_url}

def authenticate(request):
    
    # Obtener el código de autorización desde la URL
    code = request.query_params.get("code")
    
    if not code:
        return {"error": "No authorization code found"}

    try:
        # Cargar la configuración OAuth2
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI  # Asegúrate de usar el mismo redirect_uri que en Google Cloud
        )

        # Obtener el token de acceso
        flow.fetch_token(code=code, include_client_id=True, scope=SCOPES)

        credentials = flow.credentials  # Obtenemos las credenciales

        # Construir el servicio de Google Photos
        service = build('photoslibrary', 'v1', credentials=credentials, static_discovery=False)
        
        # Listar medios (fotos y videos)
        media_items = []
        next_page_token = None
        
        while True:
            # Hacer la solicitud a la API de Google Photos
            response = service.mediaItems().list(
                pageSize=100,  # Máximo de 100 elementos por página
                pageToken=next_page_token
            ).execute()
            
            # Agregar los medios a la lista
            media_items.extend(response.get('mediaItems', []))
            
            # Verificar si hay más páginas
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
        
        # Devolver la lista de medios
        return {
            "access_token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "expires_in": credentials.expiry,
            "token_type": credentials.token_uri,
            "media_items": media_items  # Lista de medios
        }
    
    except Exception as e:
        return {"error": f"Error obtaining access token or listing media items: {str(e)}"}
