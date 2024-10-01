from pydantic import BaseModel, Field, ValidationError
from typing import Optional



# 1. Field 기본 사용법
# 속성: 타입 = Field(default=기본값, description=설명, example=예시)
class User(BaseModel):
    username: str = Field(..., description="The user's username", example="john_doe")
    email: str = Field(..., description="The user's email address", example="john.doe@example.com")
    password: str = Field(..., min_length=8, description="The user's password")
    age: Optional[int] = Field(None, ge=0, le=120, description="The user's age, must be between 0 and 120", example=30)
    is_active: bool = Field(default=True, description="Is the user currently active?", example=True)

# Example usage
try:
    user = User(username="john_doe", email="john.doe@example.com", password="Secret123", is_active=0)
    print(user)
except ValidationError as e:
    print(e.json())



'''2. 숫자 validation 방법
https://docs.pydantic.dev/2.8/concepts/fields/

gt - greater than >
lt - less than <
ge - greater than or equal to / >=
le - less than or equal to / <=
multiple_of - a multiple of the given number / 2의 배수, 3의 배수 등
allow_inf_nan - allow 'inf', '-inf', 'nan' values
'''

class Foo(BaseModel):
    positive: int = Field(gt=0)
    non_negative: int = Field(ge=0)
    negative: int = Field(lt=0)
    non_positive: int = Field(le=0)
    even: int = Field(multiple_of=2)
    love_for_pydantic: float = Field(allow_inf_nan=True)


foo = Foo(
    positive=1,
    non_negative=0,
    negative=-1,
    non_positive=0,
    even=4,
    love_for_pydantic=float('inf'),
)
print(foo)



'''3. 문자열 validation 방법
https://docs.pydantic.dev/2.8/concepts/fields/

- min_length: 문자열 최소 길이
- max_length: 문자열 최대 길이
- pattern: 문자열 정규 표현식 
    - \d: 숫자
    - \w: 문자
    - \s: 공백
    - ^: 시작
    - $: 끝
    - *: 0회 이상 반복
    - +: 1회 이상 반복
    - ?: 0회 또는 1회 반복
    - {n}: n회 반복
    - {n,}: n회 이상 반복
    - {n,m}: n회 이상 m회 이하 반복
    - [abc]: a, b, c 중 하나
    - [a-z]: a부터 z까지 중 하나
    - [^abc]: a, b, c를 제외한 문자
    - [a-zA-Z]: 대소문자 알파벳 중 하나
    - [0-9]: 숫자 중 하나
    - [가-힣]: 한글 중 하나
    - [^0-9]: 숫자를 제외한 문자
    - [0-9a-zA-Z]: 숫자 또는 대소문자 알파벳 중 하나
    - [0-9a-zA-Z_]: 숫자, 대소문자 알파벳, 밑줄 중 하나
'''

class Foo(BaseModel):
    short: str = Field(min_length=3)
    long: str = Field(max_length=10)
    regex: str = Field(pattern=r'^\d*$')  


foo = Foo(short='foo', long='foobarbaz', regex='123')
print(foo)
#> short='foo' long='foobarbaz' regex='123'



'''4. Decimal validation 방법
- max_digits: Decimal 최대 숫자수. 소수점 앞에 0만 있는 경우나, 소수점값의 맨 마지막 0는 포함하지 않음. 
- decimal_places: 소수점 자리수 . 소수점값의 맨 마지막 0는 포함하지 않음
'''

from decimal import Decimal

class Foo(BaseModel):
    precise: Decimal = Field(max_digits=5, decimal_places=2)

foo = Foo(precise=Decimal('123.45'))
print(foo)
#> precise=Decimal('123.45')