from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool, NullPool


# case 1. Pool 없이 close하여 20번 수행
# case 2. Pool 없이 20번 수행 -> 커넥션이 계속 열림
# case 3. Pool 사용하여 20번 수행 -> 커넥션을 최대로 만들고, close()시 pool에 반환
# case 4. Pool 사용하지 않고 20번 수행 -> 커넥션이 계속 열림

# 0. 모니터링 Query
# select * from sys.session where db='blog_db' order by conn_id;

# 1. database connection URL
DATABASE_CONN = "mysql+mysqlconnector://root:root1234@localhost:3306/blog_db"

# case 1, 2
engine = create_engine(DATABASE_CONN)
# case 3, 4
# pool_size까지 connection을 생성하고, + max_overflow까지 생성 가능 -> 반환을 30초 기다리다가 TimeoutError 발생
# sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 2 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
engine = create_engine(DATABASE_CONN, 
                    #    poolclass=QueuePool, # case3: Connection Pool 사용 - 기본값 / conn.close()
                    #    pool_size=10, max_overflow=2 # case3: pool_size: 생성, max_overflow: + 최대 개수
                       poolclass=NullPool, # case4: Connection Pool 사용하지 않음. - 명시 / conn.close() x
                       )
print("#### engine created")

# 2. 쿼리를 20번 수행
# 2-1. 함수 정의
def direct_execute_sleep(is_close: bool = False):
    conn = engine.connect()
    query = "select sleep(5)"
    result = conn.execute(text(query))
    # rows = result.fetchall()
    # print(rows)
    result.close()

    # 2-2. 인자로 is_close가 True일 때만 connection close()
    if is_close:
        conn.close()
        print("conn closed")

# 2-3. 함수 20번 수행
for ind in range(20):
    print("loop index:", ind)
    direct_execute_sleep(is_close=True) # True: close(), False: close()하지 않음

print("end of loop")