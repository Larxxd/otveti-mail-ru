from pydantic import BaseModel, ConfigDict
from typing import Union

class UserCreate(BaseModel):
    name: str
    password: str

class UserRead(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    name: Union[str, None] = None