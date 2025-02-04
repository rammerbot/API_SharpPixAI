from fastapi import FastAPI, Request, Response, Depends, status
from fastapi.responses import RedirectResponse, JSONResponse
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from typing import Optional, List, Dict
import os
import secrets

import requests

app = FastAPI()

# Configuración del flujo OAuth
CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPES = [
    "https://www.googleapis.com/auth/photoslibrary.readonly",
    "https://www.googleapis.com/auth/photoslibrary.appendonly",
    "https://www.googleapis.com/auth/photoslibrary.edit.appcreateddata",
    "https://www.googleapis.com/auth/photoslibrary.sharing"
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
    token = credentials.token  # Obtiene el token de acceso

    # Usar requests para llamar a la API de Google Photos
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        "https://photoslibrary.googleapis.com/v1/mediaItems?pageSize=10",
        headers=headers
    )

    if response.status_code == 200:
        items = response.json().get("mediaItems", [])
        return JSONResponse(content=items)
    else:
        return JSONResponse(content={"error": "Error al obtener fotos", "details": response.text}, status_code=response.status_code)
