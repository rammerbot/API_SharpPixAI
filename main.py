from fastapi import FastAPI, Request, Response, Depends, status
from fastapi.responses import RedirectResponse, JSONResponse

from authentication import request_creds, authenticate
app = FastAPI()


@app.get("/auth/video")
async def auth_google_video(request: Request):
    return request_creds(request, 'video')

@app.get("/auth/image")
async def auth_google_image(request: Request):
    return request_creds(request, 'image')

@app.get("/auth/duplicate")
async def auth_google_duplicate(request: Request):
    return request_creds(request, 'duplicate')

@app.get("/callback_video")
async def callback_video(request: Request):
    return authenticate(request, 'video')

@app.get("/callback_image")
async def callback_image(request: Request):
    return authenticate(request, 'image')

@app.get("/callback_duplicate")
async def callback_duplicate(request: Request):
    return authenticate(request, 'duplicate')