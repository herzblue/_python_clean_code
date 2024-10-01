from pydantic import BaseModel, ValidationError, ConfigDict, Field, Strict
from typing import List, Annotated

# 1. Pydantic Model
class Address(BaseModel):
    street: str
    city: str
    country: str

# 2. Nested Pydantic Model
class User(BaseModel):
    # 2-1. 문자열->숫자값 자동 파싱을 허용하지 않을 경우 Strict 모드로 설정. 
    # 2-1-1. 모든 속성 Strict 모드: ConfigDict(strict=True)
    # model_config = ConfigDict(strict=True)

    id: int
    name: str
    email: str
    # 2-2. Nested는 typing의 List[클래스]로 명시
    addresses: List[Address]
    age: int | None = None # Optional[int] = None
    # 2-1-2. 개별 속성에 Strict 모드 설정: Field(strict=True)나 Annotated[int, Strict()] 이용. None 적용 시 Optional
    # age: int = Field(None, strict=True) #1
    # age: int = Field(..., strict=True) # 2-1-3. None이 아닌 값 필수 설정
    # age: Annotated[int, Strict()] = None #2

# 3. try - except로 ValidationError
# Pydantic Model 객체화 시 자동으로 검증 수행 수행하고, 검증 오류 시 ValidationError raise 
try:
    user = User(
        id=123,
        name="John Doe",
        email="john.doe@example.com",
        addresses=[{"street": "123 Main St", "city": "Hometown", "country": "USA"}],
        age="29" # 3-1. strict 없이하면, 문자열 값을 자동으로 int 로 파싱함. 
    )
    print(user)
except ValidationError as e:
    print("validation error happened")
    print(e)

# 4. try - except 없이 자동 검증 수행하지만, Traceback (most recent call last) 되어 오류
# user = User(
#     id="abc",
#     name="John Doe",
#     email="john.doe@example.com",
#     addresses=[{"street": "123 Main St", "city": "Hometown", "country": "USA"}],
#     age="29" # 문자열 값을 자동으로 int 로 파싱함.
# )
# print(user)