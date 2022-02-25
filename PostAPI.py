from Item import Item
from fastapi import APIRouter

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
