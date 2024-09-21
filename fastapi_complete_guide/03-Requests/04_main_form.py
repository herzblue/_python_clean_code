from pydantic import BaseModel
from typing import Optional, Annotated

from fastapi import FastAPI, Form

app = FastAPI()

# 1. HTTP Form 
# 1-1. 각각의 Form data 값을 Form()으로 처리
# 1-2. Form()은 form data값 입력 필요. Form(None)과 Annotated[str, Form()] = None은 Optional
@app.post("/login/")
async def login(username: str = Form(),
                email: str = Form(),
                # country: str = Form()):
                # country: str = Form(None)): # 타입 힌트 전 옛날 방식
                country: Annotated[str, Form()] = None): # 3.10 이상 방식
    return {"username": username,
            "email": email,
            "country": country}

"""
# Curl
curl -X 'POST' \
  'http://localhost:8081/login/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=herzblue&email=herzblue%40gmail.com&country=korea'
# Response body
{
  "username": "herzblue",
  "email": "herzblue@gmail.com",
  "country": "korea"
}

# Curl
curl -X 'POST' \
  'http://localhost:8081/login/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=herzblue&email=herzblue%40gmail.com&country='
# Response body
{
  "username": "herzblue",
  "email": "herzblue@gmail.com",
  "country": null
}
"""

# 2. HTTP Form with required values
# 2-1. ellipsis(...) 을 사용하면 form data가 필수가 됨.
@app.post("/login_f/")
async def login(username: str = Form(...), 
                email: str = Form(...),
                country: Annotated[str, Form()] = None):
    return {"username": username, 
            "email": email, 
            "country": country}

# 3. HTTP Form + path, query
# path, query parameter와 함께
@app.post("/login_pq/{login_gubun}")
async def login(login_gubun: int, 
                q: str | None = None, 
                username: str = Form(), 
                email: str = Form(),
                country: Annotated[str, Form()] = None):
    return {"login_gubun": login_gubun,
            "q": q,
            "username": username, 
            "email": email, 
            "country": country}

# 4. HTTP Form + Pydantic Model
#Pydantic Model 클래스는 반드시 BaseModel을 상속받아 생성. 
class Item(BaseModel):
    name: str
    description: str | None = None
    #description: Optional[str] = None
    price: float
    tax: float | None = None
    #tax: Optional[float] = None

# 5. 분리: 5-1. json request body용 end point와 5-2. form tag용 end point
# 5-1. json request body용 end point
@app.post("/items_json/")
async def create_item_json(item: Item):
    return item

# 5-2. form tag용 end point
@app.post("/items_form/")
async def create_item_json(name: str = Form(),
                           description: Annotated[str, Form()] = None,
                           price: str = Form(),
                           tax: Annotated[int, Form()] = None
                           ):
    return {"name": name, "description": description, "price": price, "tax": tax}