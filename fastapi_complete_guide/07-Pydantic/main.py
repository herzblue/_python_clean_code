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
    
@app.put("/items/{item_id}")
async def update_item(item_id: int, q: str, item: Item=None):
# 2. 명확히 Path, Query 파라미터 지정 가능
#async def update_item(item_id: int = Path(...), q: str = Query(...), item: Item=None):
    return {"item_id": item_id, "q": q, "item": item}

# 3. Path, Query, Request Body(json)
@app.put("/items_json/{item_id}")
async def update_item_json(
    # 3-1. Form 형식과 동일 -> Path(... or None, 검증 조건)
    item_id: int = Path(..., gt=0),
    q1: str = Query(None, max_length=50),
    #q1: Annotated[str, Query(max_length=50)] = None
    q2: str = Query(None, min_length=3),
    #q2: Annotated[str, Query(min_length=50)] = None
    item: Item = None
):
    return {"item_id": item_id, "q1": q1, "q2": q2, "item": item}

# Path, Query, Form
@app.post("/items_form/{item_id}")
async def update_item_form(
    item_id: int = Path(..., gt=0, title="The ID of the item to get"),
    q: str = Query(None, max_length=50),
    name: str = Form(..., min_length=2, max_length=50),
    description: Annotated[str, Form(max_length=500)] = None,
    #description: str = Form(None, max_length=500),
    price: float = Form(..., ge=0), 
    tax: Annotated[float, Form()] = None
    #tax: float = Form(None)
):
    return {"item_id": item_id, "q": q, "name": name, 
            "description": description, "price": price, "tax": tax}

# Path, Query, Form을 @model_validator 적용. 
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
        raise RequestValidationError(e.errors())
   
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
    item: Item = Depends(parse_user_form)
):
    return {"item_id": item_id, "q": q, "item": item}