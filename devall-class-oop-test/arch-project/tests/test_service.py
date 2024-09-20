
import pytest
from app.application.service.user import UserService
from tests.fakes import FakeUserRepository

@pytest.fixture
def user_service():
    # 테스트에 공통으로 사용하는 코드
    repository = FakeUserRepository()
    
    user_service = UserService(repository=repository)
    return user_service

def test_create_user_well(user_serivce):
    # fixture로 생성한 user_service를 사용
    # fake 객체 사용: service의 create_user를 호출하면 실제 DB에 접근하게 되는 문제가 있음.
    
    user_name = "grab"
    
    user = user_service.create_user(user_name=user_name)
    
    assert user == User(name=user_name)