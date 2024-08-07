from app.application.interfaces.user_repository import AbstractRepository
from app.domain.entity import User

class UserService:
    def __init__(self, repository: AbstractRepository):
        self.repository = repository

    # 접근방식: 앱이 클라이언트에 무엇을 해줄지 생각 - 엔티티, 유즈케이스 / 프레임워크 생각안함
    def create_user(self, user_name: str):
        # 데이터베이스에 저장하는 로직 
        _user = User(name=user_name)
        # 데이터베이스에 이름이 있는지 확인, 있다면 Exception을 발생
        if self.repository.find_one(model=_user):
            raise ValueError('유저가 이미 존재합니다.')
        
        user = self.repository.create(_user)
        return user