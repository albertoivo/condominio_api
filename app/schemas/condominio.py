from typing import Optional

from pydantic import BaseModel, ConfigDict


class CondominioBase(BaseModel):
    name: str


class CondominioCreate(CondominioBase):
    pass


class CondominioUpdate(BaseModel):
    name: Optional[str] = None


class Condominio(CondominioBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
