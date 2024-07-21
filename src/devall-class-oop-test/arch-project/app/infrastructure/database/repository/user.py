from app.domain.entity import User
from app.application.interfaces.user_repository import AbstractRepository
from app.infrastructure.database.orm import UserModel

class UserRepository(AbstractRepository):
    def create(self, model: User):
        UserModel.create(name=model)
        return model