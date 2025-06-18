from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    nome: str
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
