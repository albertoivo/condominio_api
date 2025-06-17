from pydantic import BaseModel, ConfigDict
from typing import Optional


class CondominioBase(BaseModel):
    name: str


class CondominioCreate(CondominioBase):
    pass


class CondominioUpdate(BaseModel):
    name: Optional[str] = None


class Condominio(CondominioBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
