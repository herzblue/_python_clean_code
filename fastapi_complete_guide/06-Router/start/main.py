from fastapi import FastAPI
from routes import item, user

app = FastAPI()

# 1. item 모듈의 router를 app에 추가
app.include_router(item.router)

# 2. user 모듈의 router를 app에 추가
app.include_router(user.router)