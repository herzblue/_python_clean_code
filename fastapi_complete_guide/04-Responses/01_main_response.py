from fastapi import FastAPI, Form, status
from fastapi.responses import (
    JSONResponse,
    HTMLResponse,
    RedirectResponse
)

from pydantic import BaseModel

app = FastAPI()

# 1. JSON Response
# 1-1. decorator에 response_class=JSONResponse로 미리 정해줄 수 있음.
@app.get("/resp_json/{item_id}", response_class=JSONResponse)
# 1-2. 함수 return에 content: dict -> json으로 자동 변환해서 response
async def responce_json(item_id: int, q:str | None = None):
    return JSONResponse(content={"message": "Hello World",
                                 "item_id": item_id,
                                 "q": q}, status_code=status.HTTP_200_OK)
# 1-3. response_class는 default가 JSONResponse. response_class가 HTMLResponse일 경우 아래 코드는? -> 1) json으로 변환되어 response 2) swagger에서는 HTMLResponse로 표시됨.


# 2. HTML Response
@app.get("/resp_html/{item_id}", response_class=HTMLResponse)
async def response_html(item_id: int, item_name: str | None = None):
    html_str = f'''
    <html>
    <body>
        <h2>HTML Response</h2>
        <p>item_id: {item_id}</p>
        <p>item_name: {item_name}</p>
    </body>
    </html>
    '''
    return HTMLResponse(html_str, status_code=status.HTTP_200_OK)


# 3. Redirect(Get -> Get)
# status_code = 307: Get -> Get
@app.get("/redirect")
async def redirect_only(comment: str | None = None):
    print(f"redirect {comment}")
    
    return RedirectResponse(url=f"/resp_html/3?item_name={comment}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    # "GET /redirect?comment=test_comment HTTP/1.1" 307 Temporary Redirect
    # "GET /resp_html/3?item_name=test_comment HTTP/1.1" 200 OK

# 4. Redirect(Post -> Get)
# status_code = 303: Post -> Get; login 후에 home으로 redirect할 때 사용
@app.post("/redirect_post")
async def redirect_post(item_id: int = Form(), item_name: str = Form()):
    print(f"item_id: {item_id} item name: {item_name}")

    return RedirectResponse(url=f"/resp_html/{item_id}?item_name={item_name}", status_code=status.HTTP_303_SEE_OTHER)
    # Post -> Get으로 redirect할 때는 302 status code 사용: "detail": "Method Not Allowed"

@app.post("/create_redirect")
async def create_item(item_id: int = Form(), item_name: str = Form()):
    print(f"item_id: {item_id} item name: {item_name}")

    return RedirectResponse(url=f"/resp_html/{item_id}?item_name={item_name}"
                            , status_code=status.HTTP_302_FOUND)


# 5. Response Model
class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float | None = None

# Pydantic model for response data
# 5-1. response model 정의
class ItemResp(BaseModel):
    name: str
    description: str
    price_with_tax: float

# 5-2. reponse_model: return값은 무조건 response_model(ItemResp)로 반환해야 함.
@app.post("/create_item/", response_model=ItemResp, status_code=status.HTTP_200_OK)
async def create_item_model(item: Item):
    if item.tax:
        price_with_tax = item.price + item.tax
    else:
        price_with_tax = item.price

    item_resp = ItemResp(name=item.name,
             description = item.description,
             price_with_tax = price_with_tax)

    return item_resp
    # return값이 ItemResp가 아니면 fastapi.exceptions.ResponseValidationError: 1 validation errors