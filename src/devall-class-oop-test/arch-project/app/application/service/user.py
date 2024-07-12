from app.domain.entity import User

# 접근방식: 앱이 클라이언트에 무엇을 해줄지 생각 - 엔티티, 유즈케이스 / 프레임워크 생각안함
def create_user(user_name: str):
    user = User(name=user_name)
    return user