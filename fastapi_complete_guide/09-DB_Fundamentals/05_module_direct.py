from sqlalchemy import text, Connection
from sqlalchemy.exc import SQLAlchemyError
from database import direct_get_conn

# case 1. try - except -> 모듈 불러오는 파일에서 finally로 close() 호출
def execute_query(conn: Connection):
    query = "select * from blog"
    stmt = text(query)
    # SQL 호출하여 CursorResult 반환. 
    result = conn.execute(stmt)

    rows = result.fetchall()
    print(rows)
    result.close()

def execute_sleep(conn: Connection):
    query = "select sleep(5)"
    result = conn.execute(text(query))
    result.close()

for ind in range(20):
    try: 
        conn = direct_get_conn()
        execute_sleep(conn)
        print("loop index:", ind)
    except SQLAlchemyError as e:
        print(e)
    finally: 
        conn.close()
        print("connection is closed inside finally")

print("end of loop")






