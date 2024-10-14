from sqlalchemy import create_engine, Connection
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool, NullPool
from contextlib import contextmanager
from fastapi import status
from fastapi.exceptions import HTTPException
from dotenv import load_dotenv
import os

# 1. 기본 DB CONN URL 구성
# database connection URL
DATABASE_CONN = "mysql+mysqlconnector://root:root1234@localhost:3306/blog_db1"

engine = create_engine(DATABASE_CONN, #echo=True,
                       poolclass=QueuePool,
                       #poolclass=NullPool, # Connection Pool 사용하지 않음. 
                       pool_size=10, max_overflow=0,
                       pool_recycle=300)

# 2. 직접 DB Connection을 가져오는 함수 -> routes에서 db 정보를 가져오기 위해 사용
def direct_get_conn():
    # conn 변수 선언
    conn = None
    try: 
        conn = engine.connect()
        return conn
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="요청하신 서비스가 일시적으로 문제가 발생했습니다.")
    
# 3. contextmanager를 통해 DB 연결
# 3-1. contextmanager는 안함. Depends에서 이미 contextmanager를 사용함.
def context_get_conn():
    conn = None
    try:
        conn = engine.connect()
        # 3-2. yield를 통해 conn을 선 반환 -> finally로 이어지도록 함.
        yield conn
    except SQLAlchemyError as e:
        print(e)
        # 6 예외처리
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="요청하신 서비스가 일시적으로 문제가 발생했습니다.")
    finally:
        if conn: conn.close()