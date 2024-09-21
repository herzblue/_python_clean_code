from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional, Annotated
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#1. Pydantic Model 클래스는 BaseModel 상속 -> defalut값 지정 시 주의
# -> POST body에 json key가 class 속성과 같음.
class Item(BaseModel):
    name: str
    price: float #무조건 입력 되어야 함.
    description: str | None = None #1 3.10 이상에서만 사용 가능
    #description: Optional[str] = None 
    tax: float | None =  None 
    # tax: Optional[float] = None #2 3.9 이하는 Optional 사용
    
    #3 tax를 body에 포함 안하면 None이지만, 리턴 값은 "tax": null
    # {
    # "name": "Foo",
    # "price": 45.2,
    # "description": "An optional description",
    # "tax": null
    # }

#2. 함수 변수에 Pydantic model (Item)이 입력되면 Json으로 Request Body 처리
@app.post("/items")
async def create_item(item: Item):
    print("###### item type:", type(item)) ###### item type: <class '03_main_rbody.Item'>
    print("###### item:", item) ###### item: name='Foo' description='An optional description' price=45.2 tax=3.5
    return item

#3. Request Body의 Pydantic model 값 Access 후 로직 처리
@app.post("/items_tax/")
async def create_item_tax(item: Item):
    item_dict = item.model_dump() #3-1. .model_dump(): 딕셔너리로 변경 # item.dict()가 deprecated됨.
    print("#### item_dict:", item_dict) 
    # 3-2. tax가 존재 -> price + tax 계산 / item_dict에 추가
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

#4. 함수 변수 ->Path, Request Body, Query 모두 함께 적용.
#4-1. Path = item_id, Request Body = item, Query = q
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    #4-2. result 딕셔너리에 **<딕셔너리>로 키-값 풀어서 추가
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result

class User(BaseModel):
    username: str
    full_name: str | None = None
    #full_name: Optional[str] = None

#5. 다수 request body parameter 처리. 
# ex) json 데이터의 이름 값과 함수의 인자 명 동일.  
# {
#     "item": {
#         "name": "Foo",
#         "description": "The pretender",
#         "price": 42.0,
#         "tax": 3.2
#     },
#     "user": {
#         "username": "dave",
#         "full_name": "Dave Grohl"
#     }
# }
#5-1. 변수: item, user 두 개의 클래스 변수 받음.
@app.put("/items_mt/{item_id}")
async def update_item_mt(item_id: int, item: Item, user: User = None):
    results = {"item_id": item_id, "item": item, "user": user}
    return results

#6. 개별 json 값을 포함한 경우, Body() 사용
#6-1. 클래스 없이 body json 추가 -> "importance": 5
#6-2. 변수 -> importance: int = Body()
#6-3. 변수 + default -> importance: Annotated[int, Body] = None
@app.put("/items_sn/{item_id}")
async def update_item_sn(item_id: int, item: Item, user: User, importance: int = Body()):
#async def update_item_sn(item_id: int, item: Item, user: User, importance: Annotated[int, Body] = None):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results

"""
# request body json
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    },
    "importance": 5
}
	
# Response body
{
  "item_id": 1,
  "item": {
    "name": "Foo",
    "price": 42,
    "description": "The pretender",
    "tax": 3.2
  },
  "user": {
    "username": "dave",
    "full_name": "Dave Grohl"
  },
  "importance": 5
}
"""