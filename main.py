from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle
import os

app = FastAPI(
    title="Functions drive",
    description="Esta api contiene las funcionalidades para el Google drive",
    version="1.0.0",
    docs_url="/docs",  # Cambia la URL de Swagger si lo necesitas
    redoc_url="/redoc",  # Cambia la URL de ReDoc si lo necesitas
)

# Alcances necesarios para el acceso a Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/auth")
async def auth():
    """Genera la URL de autorización y redirige al usuario"""
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_4836.json", SCOPES
    )
    
    # Genera la URL de autorización
    auth_url, _ = flow.authorization_url(prompt="consent")
    
    # Redirige al usuario a la URL de autorización
    return RedirectResponse(auth_url)

@app.get("/callback")
async def callback(request: Request):
    """Recibe el código de autorización y maneja el intercambio por un token"""
    code = request.query_params.get('code')
    
    if not code:
        return {"error": "El parámetro 'code' es necesario en la URL."}

    try:
        # Inicia el flujo de autorización con el código recibido
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_4836.json", SCOPES
        )

        # Intercambia el código por un token de acceso
        creds = flow.fetch_token(authorization_response=str(request.url))

        # Guarda las credenciales en un archivo pickle
        token_path = "token.pickle"
        os.makedirs(os.path.dirname(token_path), exist_ok=True)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

        # Crear el servicio de Google Drive
        service = build("drive", "v3", credentials=creds)

        # Realiza una llamada a la API de Google Drive (ejemplo: listar archivos)
        results = service.files().list(pageSize=10).execute()
        items = results.get('files', [])
        
        if not items:
            return {"message": "No se encontraron archivos."}
        else:
            return {"files": items}

    except Exception as e:
        return {"error": f"Error durante la autenticación: {e}"}



# @app.get("/test_video")
# def autenticate():


    # service = get_auth_url()
    # return service
    # if service:
    #     download_files = download_folder(service, "videos")
    #     compress_video(service, download_files[0], download_files[1])
    #     return {"message":"success"}
    # else:
    #     return {"error":"error al autenticar"}
        
# @app.get("/callback/")
# def autenticate(code:str):
  
  
    # service = auth_callback(code)
    # print(service)
    # return service
    # if service:
    #     download_files = download_folder(service, "videos")
    #     compress_video(service, download_files[0], download_files[1])
    #     return {"message":"success"}
    # else:
    #     return {"error":"error al autenticar"}

# @app.get("/optimize_images")	
# def read_clear_drive():
#     service = authenticate()
#     if service:
#        dowloaded_files = download_folder(service, "images")
#        optimize_image(dowloaded_files[0], dowloaded_files[1])

#     else:
#         return {"error":"error al autenticar"}
       

# @app.get("/delete_duplicates")
# def read_clear_drive():
#     service = authenticate()
#     if service:
#         dowloaded_files = download_folder(service, "all")
#         remove_duplicates_local(service)
#     else:
#         return {"error":"error al autenticar"}
    
# @app.get("/orderer_files")
# def read_clear_drive():
#     service = authenticate()
#     if service:
#         dowloaded_files = download_folder(service, "all")
#     else:
#         return {"error":"error al autenticar"}
 
                