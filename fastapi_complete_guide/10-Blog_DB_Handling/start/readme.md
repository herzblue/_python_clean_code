## FastAPI 기본 가이드
1. main.py 파일을 생성합니다.
    ```bash
    touch main.py
    ```
    main.py 파일에 다음과 같이 작성합니다.
    ```python
    from fastapi import FastAPI

    app = FastAPI()
    ```

2. db, routes, schemas 폴더를 생성합니다.
    ```bash
    mkdir db routes schemas
    ```

3. routes 폴더에 blog.py 파일 구성
    ```bash
    touch routes/blog.py
    ```
    blog.py 파일에 다음과 같이 작성합니다.
    ```python
    from fastapi import APIRouter

    router = APIRouter()
    ```

    main.py 파일에 다음과 같이 blog routes를 추가
    ```python
    from fastapi import FastAPI
    from routes.blog import router as blog_router # blog routes 추가

    app = FastAPI()

    # blog routes를 추가
    app.include_router(blog_router)
    ```

4. db/database.py 구성
    ```bash
    touch db/database.py
    ```
    database.py 파일 작성
    ```python


</br>
</br>
</br>

## DBeaver - mysql - wsl2 연동 에러
1. 에러 메시지
    ```
    Access denied for user 'root'@'LAPTOP-G9IKBAQQ.mshome.net' (using password: YES)
    ```

2. 권한 부여
    ```bash
    mysql -u root -p
    ```
    ```sql
    CREATE USER 'root'@'LAPTOP-G9IKBAQQ.mshome.net' IDENTIFIED WITH mysql_native_password BY 'root1234';
    GRANT ALL ON *.* TO 'root'@'LAPTOP-G9IKBAQQ.mshome.net';
    -- user 설정 확인
    SELECT user, host, plugin FROM mysql.user;
    ```