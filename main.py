from fastapi import FastAPI

from Item import Item

app = FastAPI()

@app.get("/")
async def root():
    return {
        "message": "Hello World",
        "Swagger": "http://127.0.0.1:8000/docs",
        "redoc": "http://127.0.0.1:8000/redoc",
    }


@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}
