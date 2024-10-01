from fastapi import FastAPI, APIRouter
from pydantic import BaseModel

# 1. item
# 1-1. APIRouter 객체 - prefix=경로, tags=리스트(태그)
router = APIRouter(prefix="/item", tags=["item"])

# 1-2. pydantic 모델은 똑같음.
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

# 1-2. @app 대신 @router 사용
@router.get("/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@router.post("/")
async def create_item(item: Item):
    return item

@router.put("/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "item": item}