from fastapi import FastAPI, Request, Response, Depends, status
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from typing import Optional, List, Dict
import os
import secrets

app = FastAPI()

# Configuración del flujo OAuth
CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/docs',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.metadata.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]
REDIRECT_URI = "https://etl-machine-learning-api-movie.onrender.com/callback/"

# Almacenar estados temporalmente (usar Redis en producción)
oauth_states = {}

# Función para obtener credenciales (MOVIDA AL PRINCIPIO)
async def get_credentials(request: Request):
    # Implementa lógica real para obtener credenciales
    token = request.query_params.get("token")  # Ejemplo básico, usa cookies en producción
    return Credentials(token)

@app.get("/auth/google")
async def auth_google(request: Request):
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    
    state = secrets.token_urlsafe(16)
    oauth_states[state] = None
    
    authorization_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        state=state
    )
    
    return {'message': authorization_url}

@app.get("/callback")
async def callback(request: Request, state: str, code: str = None):
    if state not in oauth_states:
        return {"error": "State inválido"}
    
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    
    flow.fetch_token(code=code)
    credentials = flow.credentials
    
    return {"message": "Autenticación exitosa", "token": credentials.token}

@app.get("/files", response_model=List[Dict[str, str]])
async def list_files(credentials: Credentials = Depends(get_credentials)):
    drive_service = build("drive", "v3", credentials=credentials)
    
    results = drive_service.files().list(
        pageSize=100,
        fields="nextPageToken, files(id, name, mimeType, createdTime)"
    ).execute()
    
    files = results.get("files", [])
    
    while "nextPageToken" in results:
        next_page_token = results["nextPageToken"]
        results = drive_service.files().list(
            pageSize=100,
            fields="nextPageToken, files(id, name, mimeType, createdTime)",
            pageToken=next_page_token
        ).execute()
        files.extend(results.get("files", []))
    
    return files