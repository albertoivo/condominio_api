from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    nome: str
    email: str


class UserCreate(UserBase):
    nome: str
    email: str
    password: str
    role: Optional[str] = "user"


class UserUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: str = "user"
