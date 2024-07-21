from app.application.service.user import UserService
from app.infrastructure.database.repository.user import UserRepository

def signup():
    user_service = UserService(repository=UserRepository())
    user = user_service.create_user(user_name='qq')
    return user