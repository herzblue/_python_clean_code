from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool, NullPool

# case 1. with구문: conn.close() 자동 호출 -> 동일한 con id로 20번 수행
# 

# database connection URL
DATABASE_CONN = "mysql+mysqlconnector://root:root1234@localhost:3306/blog_db"

engine = create_engine(DATABASE_CONN,
                       echo=True, # True: SQL 출력, False: SQL 출력 x 
                    # -> 2. INFO sqlalchemy.engine.Engine ROLLBACK으로 conn 반환 확인
                       poolclass=QueuePool,
                       #poolclass=NullPool,
                       pool_size=10, max_overflow=0)

def context_execute_sleep():
    # 1. with 구문: 사용하면 자동으로 conn.close()를 호출.
    with engine.connect() as conn:
        query = "select sleep(5)"
        result = conn.execute(text(query))
        result.close()
        #conn.close()

for ind in range(20):
    print("loop index:", ind)
    context_execute_sleep()

print("end of loop")