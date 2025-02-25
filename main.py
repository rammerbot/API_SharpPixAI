from fastapi import FastAPI, Request

from authentication import request_creds, authenticate
from download_files import download_media_item
from video_optimizer import compress_video

app = FastAPI(
    title="SharpPixAI - Google Auth API",
    description="""
    Esta API permite la autenticación con Google photos para gestionar los archivos de los clientes en SharpPixAI.
    
    **Funciones principales:**
    - Autenticación para la compresion de videos o imágenes o eliminar duplicados.
    - Manejo de callbacks para recibir tokens.

    
    """,
    version="1.0.0",
    contact={
        "name": "ShapPixAI",
        "url": "https://ShapPixAI.com",
        "email": "rammer@rammerbot.com"
    },
    license_info={
        "name": "ShapPixAI - Google photos Auth",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/docs",  # Documentacion con Swagger UI
    redoc_url="/redoc"  # Documentacion con ReDoc
)

tags_metadata = [
    {
        "name": "Autenticación segun la funcionalidad",
        "description": "Endpoints para autenticar con Google.",
        "externalDocs": {
            "description": "Más información",
            "url": "https://developers.google.com/identity"
        }
    },
    {
        "name": "Callbacks",
        "description": "Manejo de respuestas desde Google y procesamiento de funcionalidades."
    }
]


@app.get("/auth/video", tags=['Autentication'])
async def auth_google_video(request: Request):
    return request_creds(request, 'video')

@app.get("/auth/image", tags=['Autentication'])
async def auth_google_image(request: Request):
    return request_creds(request, 'image')

@app.get("/auth/duplicate", tags=['Autentication'])
async def auth_google_duplicate(request: Request):
    return request_creds(request, 'duplicate')

@app.get("/callback_video", tags=['callback'])
async def callback_video(request: Request):
    return compress_video(request, 'video')

@app.get("/callback_image", tags=['callback'])
async def callback_image(request: Request):
    return download_media_item(request, 'image')

@app.get("/callback_duplicate", tags=['callback'])
async def callback_duplicate(request: Request):
    return download_media_item(request, 'duplicate')