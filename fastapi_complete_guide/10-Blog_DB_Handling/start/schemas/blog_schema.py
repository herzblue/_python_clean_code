from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from pydantic.dataclasses import dataclass

# 1. DB에 데이터를 넣기 위한 schema
class BlogInput(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    author: str = Field(..., max_length=100)
    content: str = Field(..., min_length=2, max_length=4000)
    image_loc: Optional[str] = Field(None, max_length=400) # db 연결 기본값 None -> 
    # Input should be a valid string [type=string_type, input_value=None, input_type=NoneType]

# 2-1. BlogInput을 상속 / 자동으로 추가되는 부분 (id, modified_dt 추가)
class Blog(BlogInput):
    id: int
    modified_dt: datetime

# 2-2. DB 데이터를 가져올 때 검증안하기 -> DB 내부에 검증조건이 있음. 
# BaseModel or @dataclass -> @dataclass는 기본 None값이 마지막에 와야함. (python 객체는 기본값이 마지막에 와야함)
class BlogData(BaseModel):
# @dataclass
# class BlogData:
    id: int
    title: str | None = None
    author: str | None = None
    content: str | None = None
    modified_dt: datetime | None = None
    image_loc: str | None = None