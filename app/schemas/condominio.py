from pydantic import BaseModel
from typing import Optional


class CondominioBase(BaseModel):
    name: str


class CondominioCreate(CondominioBase):
    pass


class CondominioUpdate(BaseModel):
    name: Optional[str] = None


class Condominio(CondominioBase):
    id: int

    class Config:
        from_attributes = True
