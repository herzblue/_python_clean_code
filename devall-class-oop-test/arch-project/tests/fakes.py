from app.application.interfaces.user_repository import AbstractRepository
from app.domain.entity import User

class FakeUserRepository(AbstractRepository):
    def __init__(self):
        self.users = []
    
    def create(self, model: User):
        # domain에서 User 객체를 받아서 fake DB인 users 리스트에 저장
        self.users.append(model)
        return model
    
    def find_one(self, model: User):
        # fake DB인 users 리스트에서 
        for _user in self.users:
            if _user.name == model.name:
                return model
        return None