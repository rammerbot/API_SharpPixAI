from fastapi import FastAPI, Request, Response, Depends, status
from fastapi.responses import RedirectResponse, JSONResponse

from authentication import request_creds, authenticate
app = FastAPI()


@app.get("/auth/google")
async def auth_google(request: Request):
    return request_creds(request)

@app.get("/callback")
async def callback(request: Request):
    return authenticate(request)

@app.get("/callback_video")
async def callback(request: Request):
    return authenticate(request, 'video')

@app.get("/callback_image")
async def callback(request: Request):
    return authenticate(request, 'image')

@app.get("/callback_duplicate")
async def callback(request: Request):
    return authenticate(request, 'duplicate')