from fastapi import FastAPI, APIRouter
from pydantic import BaseModel

# 2. item
# 1-1. APIRouter 객체 - prefix=경로, tags=리스트(태그)
router = APIRouter(prefix="/user", tags=["user"])

# 1-2. app 대신 router 사용
@router.get("/")
async def read_users():
    return [{"username": "Rickie"}, {"username": "Martin"}]


@router.get("/me")
async def read_user_me():
    return {"username": "currentuser"}


@router.get("/{username}")
async def read_user(username: str):
    return {"username": username}