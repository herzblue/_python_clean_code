from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError

"""DB connector vs SQLAlchemy 
- SQLAlchemy: 커넥터를 사용하여 connection URL만 변경하고, 코드는 그대로 사용할 수 있음.
"""

# 1. database connection URL: "<db이름>+<db커넥터>://<사용자이름>:<비밀번호>@<호스트>:<포트>/<db이름>"
DATABASE_CONN = "mysql+mysqlconnector://root:root1234@localhost:3306/blog_db"

"""linux / root password 변경
sudo mysql -u root -p mysql
UPDATE user SET plugin='caching_sha2_password' WHERE User='root';
ALTER USER 'root'@'localhost' IDENTIFIED BY 'root1234';
FLUSH PRIVILEGES;
"""

# 2. Engine 생성
engine = create_engine(url=DATABASE_CONN
                       , poolclass=QueuePool, pool_size=10, max_overflow=0)

# 3. conn open & close: try - except - finally
try:
    # 3-1. Connection: connection 생성
    conn = engine.connect()
    # 4. Query: SQL 선언 및 text로 감싸기
    query = "SELECT id, title from blog"
    stmt = text(query)
    # 5. CursorResult: SQL 호출하여 CursorResult 반환.
    result = conn.execute(stmt)
    
    rows = result.fetchall()
    print(rows)
    
    print(type(rows[0])) # 6-1: tuple로 출력됨. <class 'sqlalchemy.engine.row.Row'>
    # 6-2. _key_to_index로 문의 후 index를 찾으나 cython으로 작성되어 큰 차이 없음
    print(rows[0].id, rows[0].title) 
    print(rows[0][0], rows[0][1])
    print(rows[0]._key_to_index)
    result.close()
except SQLAlchemyError as e:
    # 3-2. Error 처리
    print(e)
finally: 
    conn.close()
    print("closed connection")
    # 3-3. connection 반환: close() 메소드 호출