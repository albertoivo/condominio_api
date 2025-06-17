from sqlalchemy import Column, Integer, String
from .base import Base
from pydantic import BaseModel, ConfigDict


class Condominio(Base):
    __tablename__ = "condominios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)


class CondominioSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome: str
