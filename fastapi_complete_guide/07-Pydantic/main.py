from fastapi import FastAPI, Path, Query, Form, Depends
from pydantic import BaseModel, Field, model_validator
from typing import Annotated
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError

app = FastAPI()

# pydantic 적용하기
# 1. class에서 validation 적용
# 1-1. 속성 validation
class Item(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    description: str = Field(None, max_length=500)
    price: float = Field(..., ge=0)
    tax: float = None
    
    # 1-2. decorator 변수 없으면 모든 변수 가져오기.
    @model_validator(mode='after')
    def tax_must_be_less_than_price(cls, values):
        # 1-3. price, tax 값 가져오기 -> tax > price
        price = values.price
        tax = values.tax
        if tax > price:
            raise ValueError("Tax must be less then price")

        return values
    
# 2. 명확히 Path, Query 파라미터 지정 가능
@app.put("/items/{item_id}")
async def update_item(item_id: int, q: str, item: Item=None):
# async def update_item(item_id: int = Path(...), q: str = Query(...), item: Item=None):
    return {"item_id": item_id, "q": q, "item": item}

# 3. Path, Query, Request Body(json)
@app.put("/items_json/{item_id}")
async def update_item_json(
    # 3-1. Form 형식과 동일 -> Path(... -> 필수 or None -> 없어도 가능, 검증 조건)
    item_id: int = Path(..., gt=0),
    # 3-2. Query는 하나당 하나의 값만 가능
    q1: str = Query(None, max_length=50),
    #q1: Annotated[str, Query(max_length=50)] = None,
    q2: str = Query(None, min_length=3),
    #q2: Annotated[str, Query(min_length=3)] = None,
    item: Item = None
):
    return {"item_id": item_id, "q1": q1, "q2": q2, "item": item}

# 4. Path, Query, Form - Form 검증 적용
@app.post("/items_form/{item_id}")
async def update_item_form(
    item_id: int = Path(..., gt=0, title="The ID of the item to get"),
    q: str = Query(None, max_length=50),
    # 4-0. Form 검증 적용
    name: str = Form(..., min_length=2, max_length=50),
    description: Annotated[str, Form(max_length=500)] = None,
    #description: str = Form(None, max_length=500),
    price: float = Form(..., ge=0), 
    tax: Annotated[float, Form()] = None
    #tax: float = Form(None)
):
    return {"item_id": item_id, "q": q, "name": name, 
            "description": description, "price": price, "tax": tax}

# 4-1. Form validation 1 - try except 구문: Item객체에서 에러 발생하면 ValidationError에서 잡도록 하기
@app.post("/items_form_01/{item_id}")
async def update_item_form_01(
    item_id: int = Path(..., gt=0, title="The ID of the item to get"),
    q: str = Query(None, max_length=50),
    name: str = Form(..., min_length=2, max_length=50),
    description: Annotated[str, Form(max_length=500)] = None,
    #description: str = Form(None, max_length=500),
    price: float = Form(..., ge=0), 
    tax: Annotated[float, Form()] = None
    #tax: float = Form(None)
):
    try: 
        item = Item(name=name, description=description, price=price, tax=tax)
        return item
    except ValidationError as e:
        # RequestValidationError: ValidationError는 FASTAPI 기본 핸들러가 처리 못하기 때문에 RequestValidationError로 변경
        raise RequestValidationError(e.errors())


# 4-2. Form validation 2 - 의존성 주입: Depends(함수) 사용
# parse_user_form을 schemas/item_schema.py에 분리하고 import해서 사용 / 반복되는 코드를 사용
def parse_user_form(
    name: str = Form(..., min_length=2, max_length=50),
    description: Annotated[str, Form(max_length=500)] = None,
    price: float = Form(..., ge=0),
    tax: Annotated[float, Form()] = None, 
) -> Item:
    try: 
        item = Item(
            name = name,
            description = description,
            price = price, 
            tax = tax
        )

        return item
    except ValidationError as e:
        raise RequestValidationError(e.errors()) 

@app.post("/items_form_02/{item_id}")
async def update_item_form_02(
    item_id: int = Path(..., gt=0, title="The ID of the item to get"),
    q: str = Query(None, max_length=50),
    # Depends는 사실 Form
    item: Item = Depends(parse_user_form)
):
    return {"item_id": item_id, "q": q, "item": item}