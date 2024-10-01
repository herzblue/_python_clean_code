from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
# 1. jinja2 Template은 fastapi에 통합
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

# 2.jinja2 Template 생성: 변수로 directory 입력
templates = Jinja2Templates(directory="templates")

class Item(BaseModel):
    name: str
    price: float

# 3-1. decorator: response_class는 Output을 명확히 하는 역할
# response_class=HTMLResponse를 생략 -> application/json으로 Swagger UI 인식(별 문제는 없음)
@app.get("/items/{id}", response_class=HTMLResponse)
# 3-2. template engine을 사용 -> 반드시 Request 객체를 1변수로 입력 -> return에 Request 객체 전달
async def read_item(request: Request, id:str, q: str | None = None):
    # 3-3. 내부에서 pydantic 객체 생성. 
    item = Item(name="test_item", price=10)
    # 3-4. pydantic model값을 dict 변환. 
    item_dict = item.model_dump()

    # 3-5. templates.TemplateResponse(): 
    # context에 dict의 key가 template 변수와 일치해야 함.
    return templates.TemplateResponse(
        request=request,
        name="item.html",
        context={"id":id, "q_str":q, "item":item, "item_dict":item_dict}
    )
    
    # FastAPI 0.108 이하 버전에서는 아래와 같이 TemplateResponse() 인자 호출
    # return templates.TemplateResponse(name="item.html",
    #                                   {"request": request
    #                                    , "id": id, "q_str": q, "item": item, "item_dict": item_dict})

# 4. jinja2 조건문으로 admin, user 구분하여 html template 출력
@app.get("/item_gubun")
async def read_item_by_gubun(request: Request, gubun: str):
    item = Item(name="test_item_02", price=4.0)
    
    return templates.TemplateResponse(
        request=request, 
        name="item_gubun.html", 
        context={"gubun": gubun, "item": item}
    )


# 5. jinja2 반복문으로 list 출력
@app.get("/all_items", response_class=HTMLResponse)
async def read_all_items(request: Request):
    # 5-1. Item 객체를 5개 생성
    all_items = [Item(name="test_item_" +str(i), price=i) for i in range(5) ]
    print("all_items:", all_items)
    return templates.TemplateResponse(
        request=request, 
        name="item_all.html", 
        context={"all_items": all_items}
    )


# 6. safe read: tag가 &lt;ul&gt;로 변환되어 잘못 출력
@app.get("/read_safe", response_class=HTMLResponse)
async def read_safe(request: Request):
    html_str = '''
    <ul>
    <li>튼튼</li>
    <li>저렴</li>
    </ul>
    '''
    return templates.TemplateResponse(
        request=request, 
        name="read_safe.html", 
        context={"html_str": html_str}
    )
