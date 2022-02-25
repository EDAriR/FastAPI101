from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from mongoengine import connect, disconnect

from Item import Item
import PostAPI
from Routers import api

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


@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}


@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}


# api.router.include_router(PostAPI.router)
app.include_router(api.router)
app.include_router(PostAPI.router)
