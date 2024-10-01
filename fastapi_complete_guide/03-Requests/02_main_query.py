from fastapi import FastAPI
from typing import Optional

app = FastAPI()
# uvicorn 02_main_query:app --port=8081 --reload

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
# URL 예시: http://localhost:8081/items?skip=0&limit=10
# 1. query parameter: 함수에 개별 인자값  path parameter가 아닌 모든 인자는 query parameter
# query parameter의 타입과 default값을 함수인자로 설정할 수 있음. 
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

@app.get("/items_nd/")
# 2. 함수 변수에 default 값이 없으면 무조건 입력 필요.  
async def read_item_nd(skip: int, limit: int):
    return fake_items_db[skip : skip + limit]

@app.get("/items_op/")
# 3. 함수 변수에 default 값 None + "Optional" 추가 또는 "| None" 타입 추가  
async def read_item_op(skip: int, limit: Optional[int] = None):
    # return fake_items_db[skip : skip + limit]
    if limit:
        return fake_items_db[skip : skip + limit]
    else:
        return {"limit is not provided"}

# 4. Path와 Query Parameter를 함께 사용.     
@app.get("/items/{item_id}")
# 4-1. decorator 변수 item_id를 Path Parameter로 인지. 
# 4-2. 함수 변수 중 item_id는 Path, 나머지는 Query Parameter
async def read_item_path_query(item_id: str, q: str = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item