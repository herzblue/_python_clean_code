from fastapi import HTTPException

from app.application.service.user import UserService
from app.infrastructure.database.repository.user import UserRepository

def signup(user_name):
    user_service = UserService(repository=UserRepository())
    try:
        user = user_service.create_user(user_name=user_name)
        return user
    # 예외처리: fastapi의 HTTPException 사용 - fastapi와 같이 중심이 되는 코드상에서 변화되지 않는 프레임워크는 의존하면서 사용하기도 함.
    except ValueError as e:
        # ValueError는 User가 존재하는데 생성하려고 할 때 발생하는 에러
        raise HTTPException(status_code=403, detail=str(e))
        # 403: 리소스에 대한 액세스가 금지
    except Exception as e:
        # 이외의 에러는 서버의 오류로 500으로 처리
        raise HTTPException(status_code=500, detail=str(e))
        # 500: 서버에 오류가 발생