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
    "https://www.googleapis.com/auth/photoslibrary.appendonly",
    "https://www.googleapis.com/auth/photoslibrary.edit.appcreateddata",
    "https://www.googleapis.com/auth/photoslibrary.readonly",
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
    
    # Quita include_granted_scopes o establece en "false"
    authorization_url, _ = flow.authorization_url(
        access_type="offline",
        state=state
    )
    
    return {'message': authorization_url}

@app.get("/callback")
async def callback(request: Request):
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

        return {
            "access_token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "expires_in": credentials.expiry,
            "token_type": credentials.token_uri
        }
    
    except Exception as e:
        return {"error": f"Error obtaining access token: {str(e)}"}