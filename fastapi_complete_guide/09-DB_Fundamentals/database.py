from sqlalchemy import create_engine, Connection
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool, NullPool
from contextlib import contextmanager


"""db 모듈을 사용하는 이유
1. router에서 db pool을 각각 생성해야함.
2. db를 바꾸면 router마다 DATABASE_CONN을 바꿔야함.
"""

# database connection URL
DATABASE_CONN = "mysql+mysqlconnector://root:root1234@localhost:3306/blog_db"

engine = create_engine(DATABASE_CONN,
                    #    echo=True,
                       poolclass=QueuePool,
                       #poolclass=NullPool, # Connection Pool 사용하지 않음. 
                       pool_size=10, max_overflow=0)

# case 1. try - except -> 모듈 불러오는 파일에서 finally로 close() 호출
def direct_get_conn():
    try:
        conn = engine.connect()
        return conn
    except SQLAlchemyError as e:
        print(e)
        raise e

# case2: with 절 사용시 이슈 -> yield 사용, next()로 호출
# - with 절을 사용하면 conn.close()가 자동으로 호출되어, conn이 이미 close되어 있는 상태에서 다시 close()를 호출하면 에러 발생
# def context_get_conn():
#     try:
#         with engine.connect() as conn:
#             yield conn
#     except SQLAlchemyError as e:
#         print(e)
#         raise e
#     finally:
#         conn.close()
#         print("###### connection yield is finished")

# case3: contextmanager 사용 -> 의존성 주입 시에는 contextmanager 포함되어 있어서 뺌.
@contextmanager# 3-1. contextmanager 데코레이터
def context_get_conn():
    try:
        conn = engine.connect()
        yield conn # 3-2. 호출하는 곳에서 컨트롤 가능
    except SQLAlchemyError as e:
        print(e)
        raise e
    finally: 
        conn.close() # 3-3. 호출 쪽 with 해제 -> yield 해제 -> finally, close() 호출
