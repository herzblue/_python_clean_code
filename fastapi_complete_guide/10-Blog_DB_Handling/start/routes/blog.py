
from fastapi import APIRouter, Request, Depends, status, Form
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy import text, Connection
from db.database import direct_get_conn, context_get_conn
from sqlalchemy.exc import SQLAlchemyError
from schemas.blog_schema import Blog, BlogData
from utils import util

"""
순서: 
1. router 생성 후 main에서 연결
2. database 연결 함수 생성
3. 쿼리 작성
4. schema 작성 - pydantic Model 사용
5. schema에 작성한 pydantic Model객체에 db 데이터 저장
6. database 연결 - Depends 사용
7. jinja2 template 사용
8. CRUD 작업
9. Error Handling
"""

# router 생성
router = APIRouter(prefix="/blogs", tags=["blogs"])

# 3. jinja2 Template 
# 3-1. 엔진 생성
templates = Jinja2Templates(directory="templates")

# 1. bd에서 blog의 모든 데이터를 가져오는 API
@router.get("/")
async def get_all_blogs(request: Request): # 1-1. HTTP template 사용 위해 Request 객체 추가
    conn = None
    try:
        # 1-2. database 연결 및 쿼리 작성
        conn = direct_get_conn()
        query = """
        SELECT id, title, author, content, image_loc, modified_dt
        FROM blog
        """
        result = conn.execute(text(text=query))
        
        # 1-3. schema에 작성한 pydantic Model객체에 db 데이터 저장
        # rows = result.fatchall()
        all_blogs = [BlogData(id = row.id,
                     title=row.title,
                     author=row.author,
                     content=util.truncate_text(row.content),
                     image_loc=row.image_loc, # 1-5. DB NULL -> 객체 None 처리
                     modified_dt=row.modified_dt) 
                for row in result]
        result.close()
        # 1-4. return json rows
        # return rows 
        
        # 3-2. jinja2 template 사용
        return templates.TemplateResponse(
            request = request,
            name = "index.html",
            context = {"all_blogs": all_blogs} # 3-3. key -> index.html / value -> all_blogs 변수
        )

        """ 6. 예외처리 -> 4xx, 5xx 에러 구분
        6-1. raise SQLAlchemyError 기본
        INFO:     127.0.0.1:42636 - "GET /blogs/ HTTP/1.1" 500 Internal Server Error
        ERROR:    Exception in ASGI application
        Traceback (most recent call last): ...
        
        6-2. raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
        6-3. raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        6-4. DB conn 연결 문제 -> database.py에 HTTP_503_SERVICE_UNAVAILABLE 처리
        """

    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="요청하신 서비스가 일시적으로 문제가 발생했습니다.")
    finally:
        # 1-4. db 연결 종료 - 연결이 생기지 않을 수 있으니 if conn
        if conn: conn.close()

# 2. Depends를 통해 DB 연결, close 수행
# 2-1. Connection객체, Depends로 DB 연결
# 2-2. contextmanager 포함 -> database에서 close (finally database에서 수행)
@router.get("/show/{id}")
async def get_blog_by_id(reqeust: Request, id: int,
                         conn: Connection = Depends(context_get_conn)):
    try:
        query = f"""
        SELECT id, title, author, content, image_loc, modified_dt
        FROM blog
        -- WHERE id = {id} -- 1. f-string 사용
        WHERE id = :id -- 2. bind params 사용
        """
        stmt = text(query)
        # result = conn.execute(stmt) # 1. f-string 사용
        bind_stmt = stmt.bindparams(id=id) # 2. bind params 사용
        result = conn.execute(bind_stmt) # 2. bind params 사용
        
        # 2-4. 오류 발생 시 예외처리 / result.rowcount == 0 으로 인식: 한 건도 없어도 None이 아님
        if result.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"해당 id {id}에 대한 데이터가 없습니다.")
        
        row = result.fetchone()
        blog = BlogData(id=row.id,
                 title=row.title,
                 author=row.author,
                 content=util.newline_to_br(row.content),
                 image_loc=row.image_loc,
                 modified_dt=row.modified_dt)
        result.close()
        # 2-3. return blog
        # return blog 
        return templates.TemplateResponse(
            request = reqeust,
            name = "show_blog.html",
            context = {"blog": blog}
        )
    
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="요청하신 서비스가 일시적으로 문제가 발생했습니다.")

# 4. 블로그 포스트 생성
# 4-1. 블로그 포스트 UI 작성
@router.get("/new")
async def new_blog(request: Request):
    return templates.TemplateResponse(
        request = request,
        name = "new_blog.html",
        context = {} # context 무조건 필요
        )

# 4-2. 블로그 포스트 데이터 저장
@router.post("/new")
async def create_blog(request: Request, 
                        title = Form(min_length=2, max_length=200),
                        author = Form(max_length=100),
                        content = Form(min_length=2, max_length=4000),
                        conn: Connection = Depends(context_get_conn)): # 1. Depends 사용해서 db 연결
    try:
        query = f"""
        INSERT INTO blog (title, author, content, modified_dt)
        values (:title, :author, :content, NOW())
        """
        stmt = text(query)
        bind_stmt = stmt.bindparams(title = title, author = author, content = content) # 2. bind params 사용
        
        conn.execute(bind_stmt)
        conn.commit() # 3. create 작업이므로 commit 필요
        
        return RedirectResponse("/blogs", status_code = status.HTTP_303_SEE_OTHER)
    except SQLAlchemyError as e:
        print(e)
        conn.rollback() # db에서 rollback 수행, close되면서 자동으로 rollback 수행되지만 명시
        raise e

# 4. 블로그 포스트 수정
# 4-1. 블로그 포스트 수정 UI
@router.get("/modify/{id}")
def update_blog_ui(request: Request,
                   id: int,
                   conn: Connection = Depends(context_get_conn)):
    try:
        query = f"""
        SELECT id, title, author, content 
        FROM blog
        WHERE id = :id
        """
        stmt = text(query)
        bind_stmt = stmt.bindparams(id=id)
        result = conn.execute(bind_stmt)
        
        if result.rowcount == 0: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"해당 id {id}에 대한 데이터가 없습니다.")
        row = result.fetchone()
        # blog = BlogData(id=row.id,
        #          title=row.title,
        #          author=row.author,
        #          content=row.content)
        
        return templates.TemplateResponse(
            request = request,
            name = "modify_blog.html",
            context = {"id": row.id, "title": row.title, "author": row.author, "content": row.content}
        )
    except SQLAlchemyError as e:
        print(e)
        raise e
    
# 4-2. 블로그 포스트 수정 데이터 저장
@router.post("/modify/{id}")
def update_blog(request: Request, id: int,
                title = Form(min_length=2, max_length=200),
                author = Form(max_length=100),
                content = Form(min_length=2, max_length=4000),
                conn: Connection = Depends(context_get_conn)): # 1. Depends 사용해서 db 연결
    try: 
        query = f"""
        UPDATE blog
        SET title = :title, author = :author, content = :content, modified_dt = NOW()
        WHERE id = :id
        """
        stmt = text(query)
        # 2. bind params 사용
        bind_stmt = stmt.bindparams(id = id, title = title, author = author, content = content) #
        result = conn.execute(bind_stmt)
        # 3. 예외처리
        if result.rowcount == 0:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                                detail=f"해당 id {id}에 대한 데이터가 없습니다.")
        conn.commit() # 3. update 작업이므로 commit 필요
        return RedirectResponse(f"/blogs/show/{id}", status_code = status.HTTP_302_FOUND)
    except SQLAlchemyError as e:
        print(e)
        conn.rollback()
        raise e

# 5. 블로그 포스트 삭제
@router.post("/delete/{id}")
def delete_blog(request: Request, id: int,
                conn: Connection = Depends(context_get_conn)):
    try:
        query = f"""
        DELETE FROM blog
        WHERE id = :id
        """
        stmt = text(query)
        bind_stmt = stmt.bindparams(id=id)
        result = conn.execute(bind_stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                                detail=f"해당 id {id}에 대한 데이터가 없습니다.")
        conn.commit()
        return RedirectResponse("/blogs", status_code = status.HTTP_303_SEE_OTHER)
    except SQLAlchemyError as e:
        print(e)
        conn.rollback()
        raise e