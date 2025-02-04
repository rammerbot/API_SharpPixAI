from fastapi import FastAPI, Request, Response, Depends, status
from fastapi.responses import RedirectResponse, JSONResponse
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
    'https://www.googleapis.com/auth/drive.readonly',
    "https://www.googleapis.com/auth/photoslibrary.readonly"
]
REDIRECT_URI = "https://etl-machine-learning-api-movie.onrender.com/callback/"

# Almacenar estados temporalmente (usar Redis en producción)
oauth_states = {}

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
    
    # Construir el servicio de Google photos
    drive_service = build("photoslibrary", "v1", credentials=credentials)
    
    # Construir el servicio de Google photos
    photo_service = build("photoslibrary", "v1", credentials=credentials)
    
    results = photo_service.mediaItems().list(pageSize=10).execute()
    items = results.get("mediaItems", [])

    if not items:
        print("No se encontraron fotos.")
        return []

    for item in items:
        print(f"Nombre: {item['filename']} - URL: {item['baseUrl']}")
    return JSONResponse(content=items)
