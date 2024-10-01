# 1. FastAPI import
from fastapi import FastAPI

# 2. FastAPI instance 생성
app = FastAPI()

# 3. Path 오퍼레이션 생성. 
# 3-1. Path: 도메인명을 제외 /로 시작하는 URL, url이 https://example.com/items/foo 라면 path는 /items/foo
# 3-2. Operation은 GET, POST, PUT/PATCH, DELETE등의 HTTP 메소드
# 3-3. async def
@app.get("/", summary="간단한 API", tags=["Simple"])
async def root():
    """ 
    이것은 간단한 API 입니다. 아래는 인자값입니다. 
    - 인자값1
    - 인자값2
    """
    return {"message": "Hello World"}

# 4. app 동작하기
# uvicorn <파일명>:<FastAPI 객체의 인스턴스 이름> --port=<포트이름> --reload
# uvicorn main:app --port=8081 --reload