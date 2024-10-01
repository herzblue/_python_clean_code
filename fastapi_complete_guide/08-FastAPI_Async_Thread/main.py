from fastapi import FastAPI
import asyncio
import time

app = FastAPI()

# 1. 기본 - async/await 키워드
# 1-1. async def 함수(비동기 함수) 호출 시, await로 함수 호출
# 1-2. await 키워드 사용할 때는 async def 함수 내부에서만 사용 가능

# 1. 비동기 함수 long-running I/O-bound 작업 시뮬레이션
async def long_running_task():
    # 특정 초동안 수행 시뮬레이션
    await asyncio.sleep(20)
    return {"status": "long_running task completed"}

# @app.get("/task")
# async def run_task():
#     result = await long_running_task()
#     return result

# 2-2. 동기 함수
@app.get("/task")
# 2-2-1. async 키워드 함수 + 동기 함수 => evnet loop가 동기 함수에 의해 block
async def run_task():
# 2-2-2. 동기 함수 + 동기 함수 => thread pool 사용해서 evnet loop block되지 않음
# def run_task(): # 별도 스레드에서 동작하기 -> 동작한 process id가 다름
    # 2-2-1. async 키워드 함수 + 동기 함수 => evnet loop가 동기 함수에 의해 block
    time.sleep(20)
    return {"status": "long_running task completed"}
    
    # 2-2-3. thread pool
    # uvicorn main:app --port 8001 --workers=3
    # process-> parent 1개, server 3개 생성됨
    
# 2-1. 동기 함수
@app.get("/quick")
async def quick_response():
    return {"status": "quick response"}