from fastapi import FastAPI, Request, Response, Depends
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

import secrets

app = FastAPI()

# Configuración del flujo OAuth
CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPES = ["https://www.googleapis.com/auth/drive.file"]
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
    
    # Generar un state único y guardarlo
    state = secrets.token_urlsafe(16)
    oauth_states[state] = None  # Puedes almacenar datos del usuario aquí
    
    authorization_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        state=state  # Pasamos el state a Google
    )
    
    return {'message':authorization_url}

@app.get("/callback")
async def callback(request: Request, state: str, code: str = None):
    # Verificar el state (previene CSRF)
    if state not in oauth_states:
        return {"error": "State inválido"}
    
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    
    # Obtener el token
    flow.fetch_token(code=code)
    credentials = flow.credentials
    
    # Guardar credenciales (ejemplo: en base de datos)
    # ...
    
    return {"message": "Autenticación exitosa", "token": credentials.token}