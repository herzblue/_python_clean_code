from pydantic import BaseModel,  ValidationError, field_validator, model_validator
from typing import Optional

# 커스텀 검증로직 -> 복잡한 검증 ex) 비밀번호 2번 확인

# 1. custom validator: @field_validator
class User(BaseModel):
    username: str
    password: str
    confirm_password: str
    
    # strip 공백 제거 후 빈값 확인
    # 1-1. @field_validator('username')로 필드별 검증
    @field_validator('username')
    # 1-2. cls 클래스 함수로 설정
    # 1-3. value = username 값 -> return value
    def username_must_not_be_empty(cls, value: str):
        if not value.strip():
            raise ValueError("Username must not be empty")
        return value

    # 2. password 검증
    @field_validator('password')
    def password_must_be_strong(cls, value: str):
        # 2-1. 길이
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        # 2-2. 숫자, 문자 포함 -> not any 하나라도 아니면 false, 0
        if not any(char.isdigit() for char in value):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isalpha() for char in value):
            raise ValueError('Password must contain at least one letter')
        return value
    
    # 3. 마지막 순서 validation: 데코레이터 mode='after'
    @model_validator(mode='after')
    def check_passwords_match(cls, values):
        password = values.password
        confirm_password = values.confirm_password
        if password != confirm_password:
            raise ValueError("Password do not match")
        return values
 
    
# 검증 테스트    
try:
    user = User(username="john_doe", password="Secret123", confirm_password="Secret123")
    print(user)
except ValidationError as e:
    print(e)