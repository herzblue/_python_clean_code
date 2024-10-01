from pydantic import BaseModel, ValidationError
from typing import List, Optional
import json

# print(pydantic.__version__): 2.9.2

# 1. Pydantic Model: = 이 아니라 :로!
class User(BaseModel):
    id: int
    name: str
    email: str
    age: int | None = None # Optional[int] = None

# vs 일반 클래스 선언
class UserClass:
    def __init__(self, id: int, name: str, email: str, age: int):
        self.id = id
        self.name = name
        self.email = email
        self.age = age

    def get_info(self):
        return f"id: {self.id}, name: {self.name}"
    
    def __str__(self):
        return f"id: {self.id}, name: {self.name}, email: {self.email}, age: {self.age}"

userobj = UserClass(10, 'test_name', 'tname@example.com', 40)
print("userobj:", userobj, userobj.id)


# 2. Pydantic Model 객체화. 
# 2-1. 중요) 객체 변수명을 명시
#User(10, 'test_name', 'tname@example.com', 40) 하지 않도록 유의
user = User(id=10, name="test_name", email="tname@example.com", age=40)
print("user:", user, user.id)

# 2-2. kwargs
# dict keyword argument(kwargs)로 Pydantic Model 객체화
user_from_dict = User(**{"id": 10, "name": "test_name", "email": "tname@example.com", "age": 40})
print("user_from_dict:", user_from_dict, user_from_dict.id)

# 2-3. json 문자열
# json.loads(json_string) -> json 문자열 기반 Pydantic Model 객체화. 
json_string = '{"id": 10, "name": "test_name", "email": "tname@example.com", "age": 40}'
json_dict = json.loads(json_string)
#print("json_dict type:", type(json_dict))
user_from_json = User(**json_dict)
print("user_from_json:", user_from_json, user_from_json.id)

# 3. Pydantic Model의 상속
# 3-1. User 속성은 상속, 추가 속성 advanced_level은 추가
class AdvancedUser(User):
    advanced_level: int

# 3-1. (중요) 변수값 무조건 추가: AdvancedUser(10, 'test_name', 'tname@example.com', 40, 10) 하지 않도록 유의
adv_user = AdvancedUser(id=10, name="test_name", email="tname@example.com", age=40, advanced_level=9)
print("adv_user:", adv_user)


# 4. Nested Json
# 4-1. 2개 클래스 -> 내포된(Nested 된 Json) 데이터 기반 Pydantic Model 생성. 
class Address(BaseModel):
    street: str
    city: str

class UserNested(BaseModel):
    name: str
    age: int
    address: Address

# 4-2. 내포된 Json 문자열에서 생성. 
json_string_nested = '{"name": "John Doe", "age": 30, "address": {"street": "123 Main St", "city": "Anytown"}}'
json_dict_nested = json.loads(json_string_nested)

user_nested_01 = UserNested(**json_dict_nested)
print("user_nested_01:", user_nested_01, user_nested_01.address, user_nested_01.address.city)

# 4-3. python dict: address = {} 형태도 가능.
# 인자로 전달 시 Nested 된 값을 dict 형태로 전달하여 생성.
user_nested_02 = UserNested(
    name="test_name", age=40, address = {"street": "123 Main St", "city": "Anytown"}
)
print("user_nested_02:", user_nested_02, user_nested_02.address, user_nested_02.address.city)

# 5. Pydantic Model의 Validation
# 5-1. python 기반, pydantic serialization
# {'id': 10, 'name': 'test_name', 'email': 'tname@example.com', 'age': 40} <class 'dict'>
user_dump_01 = user.model_dump()
print(user_dump_01, type(user_dump_01))

# 5-2. json 문자열 기반, pydantic serialization
# {"id":10,"name":"test_name","email":"tname@example.com","age":40} <class 'str'>
user_dump_02 = user.model_dump_json()
print(user_dump_02, type(user_dump_02))
