from sqlalchemy import text, Connection
from sqlalchemy.exc import SQLAlchemyError
from database import direct_get_conn

try:
    # Connection 얻기
    conn = direct_get_conn()

    # SQL 선언 및 text로 감싸기
    query = "select id, title from blog"
    stmt = text(query)

    # SQL 호출하여 CursorResult 반환. 
    result = conn.execute(stmt)
    # 1. fetchall(): row Set을 개별 원소인 <class 'list'>로 반환
    # [(1, '테스트 title 1'), (2, '테스트 title 2'), (3, '테스트 title 3'), (4, '테스트 title 4')]
    rows = result.fetchall() 
    
    # 2. fetchone(): 1개 row Set 반환
    # rows = result.fetchone() # row Set 단일 원소 반환: <class 'sqlalchemy.engine.row.Row'>
    
    # 3. fetchmany(size): size만큼 row Set 반환
    # rows = result.fetchmany(2) # row Set을 개별 원소로 가지는 <class 'list'>로 반환.
    
    # 4. List Comprehension = fetchall()과 동일한 결과
    # rows = [row for row in result] # List Comprehension으로 row Set을 개별 원소로 가지는 List로 반환
    
    print(rows)
    print(type(rows))

    row = rows[0]
    print(f"""
    - row: {row}
    - row[0]: {row[0]}
    - row[1]: {row[1]}
    - rows[0][0]: {rows[0][0]}
    - rows[0][1]: {rows[0][1]}
    """)

    # 5. 개별 row에 key(컬럼명) 으로 dict 반환 -> key(컬럼명) 중복으로 메모리 낭비
    # row_dict = result.mappings().fetchall()
    # print(row_dict)

    # 6. 코드레벨에서 컬럼명 명시화 -> row._key_to_index로 접근해서 호출이 늘어남
    # row = result.fetchone()
    # print(row._key_to_index)
    # rows = [(row.id, row.title) for row in result]
    # print(rows)

    result.close()
except SQLAlchemyError as e:
    print("############# ", e)
    #raise e
finally:
    # close() 메소드 호출하여 connection 반환.
    conn.close()