from fastapi import FastAPI
from enum import Enum

app = FastAPI()


# http://localhost:8081/items/3
# 1. path parameter: decorator 변수 문자열 format string { }로 지정된 변수 
@app.get("/items/{item_id}")
# 2. path parameter 변수 타입: async def 함수 인자의 타입
async def read_item(item_id: int):
    return {"item_id": item_id}

# 3. path parameter: 특정 지정 Path와 Path parameter값이 충돌되지 않도록 endpoint 작성 코드 위치가 특정지정 path가 위에 위치해야 함.
@app.get("/items/all")
# 수행 함수 인자로 path parameter가 입력됨. 함수 인자의 타입을 지정하여 path parameter 타입 지정.  
async def read_all_items():
    return {"message": "all items"}

# 4. Path parameter: 지정 값들을 그룹으로 묶어 지정 - 아래와 같이 Enum Class로 Path유형을 지정. 
# 4-1. Enum class -> mixin class: enum + str
class ItemType(str, Enum):
    small = "small"
    medium = "medium"
    large = "large"

# 4-2. item_type.value로 small/medium/large만 가능. 
# @app.get("/items/type/{item_type}")
# async def get_item_type(item_type: ItemType):
#     # print(f"item_type: {item_type.value}")
#     return {"message": f"item type is {item_type.value}"}

# 4-3. 분기처리
@app.get("/items/type/{item_type}")
async def get_item_type(item_type: ItemType):
    if item_type is ItemType.small:
         return {"message": f"small item type should be very {item_type.value}"}
    return {"message": f"item type is {item_type.value}"}

