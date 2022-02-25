from fastapi import APIRouter

from Product import Router as product
from User import Router as user
from User import oauth2

router = APIRouter()
router.include_router(product.router)
router.include_router(user.router)
router.include_router(oauth2.router)