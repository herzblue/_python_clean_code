from fastapi import FastAPI, Request

app = FastAPI()

# 1. request 객체 사용
@app.get("/items")
async def read_item(request: Request):
    client_host = request.client.host #1. client host
    headers = request.headers #2. headers
    query_params = request.query_params #3. query parameters
    url = request.url #4. url
    path_params = request.path_params #5. path parameters
    http_method = request.method #6. http method
    
    return {
            "client_host": client_host,
            "headers": headers,
            "query_params": query_params,
            "path_params": path_params,
            "url": str(url),
            "http_method":  http_method
        }

# 2. request 객체 사용 + path parameter
# 2-1. decorator에 {item_group}, function에 item_group: str
@app.get("/items/{item_group}")
async def read_item_p(request: Request, item_group: str):
    client_host = request.client.host
    headers = request.headers 
    query_params = request.query_params
    url = request.url
    path_params = request.path_params
    http_method = request.method

    return {
        "client_host": client_host,
        "headers": headers,
        "query_params": query_params,
        "path_params": path_params,
        "url": str(url),
        "http_method":  http_method
    }

# postman or thunder client로 실습
# 3. request 객체 사용 + request.json()
@app.post("/items_json/")
async def create_item_json(request: Request):
    data =  await request.json()  # Parse JSON body
    print("received_data:", data)
    return {"received_data": data}

# 4. request 객체 사용 + request.form()
@app.post("/items_form/")
async def create_item_form(request: Request):
    data = await request.form() # Parse Form body
    print("received_data:", data)
    return {"received_data": data}