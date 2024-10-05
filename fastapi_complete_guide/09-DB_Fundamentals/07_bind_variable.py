from sqlalchemy import text, Connection
from sqlalchemy.exc import SQLAlchemyError
from database import direct_get_conn
from datetime import datetime

"""bind variable: SQL 쿼리문에 변수를 바인딩하여 사용하는 방법
- DB 서버 메모리: 공유 메모리(쿼리 동작에 필요한 작업) + 전용 메모리(세션)
- 사용 이유: 공유 메모리에서 같은 쿼리가 변수만 바껴도 같은 작업 수행 -> 메모리 낭비
"""

try:
    # 1. Connection 얻기
    conn = direct_get_conn()

    # 2. SQL 선언 및 text로 감싸기
    # 바뀌는 부분: ex) 1, 2, 3, 4 | '둘리', '길동'
    
    # 2-1. 바인딩 변수-> :id, :author, :modified_dt / 바인딩 변수는 ''사용하지 않음
    query = "select id, title, author from blog where id = :id and author = :author \
             and modified_dt < :modified_dt"
    stmt = text(query)
    # 2-2. bindparams() 변수 바인딩
    bind_stmt = stmt.bindparams(id=1, author='둘리', modified_dt=datetime.now())

    # SQL 호출하여 CursorResult 반환. 
    result = conn.execute(bind_stmt)
    rows = result.fetchall() # row Set을 개별 원소로 가지는 List로 반환. 
    print(rows)
    result.close()
except SQLAlchemyError as e:
    print("############# ", e)
    #raise e
finally:
    # close() 메소드 호출하여 connection 반환.
    conn.close()