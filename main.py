from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse


import aiofiles
from typing import List

from mongoengine import connect, disconnect

from Item import Item
import PostAPI
from Routers import api
from User.oauth2 import *

app = FastAPI()
# connect('test', host='0.0.0.0', port=27107)
connect('test')

origins = ["http://localhost:5000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "Hello World",
        "Swagger": "http://127.0.0.1:5000/docs",
        "redoc": "http://127.0.0.1:5000/redoc",
    }


@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    if authenticate(username, password):
        access_token = create_access_token(
            data={"sub": username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")


@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}


@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}


@app.get("/download-file")
def download_file():
    file_path = "/Users/ed/Downloads/YoutubeDownloas/FFMpeg.py"
    return FileResponse(path=file_path, filename=file_path)

# api.router.include_router(PostAPI.router)
app.include_router(api.router)
app.include_router(PostAPI.router)
