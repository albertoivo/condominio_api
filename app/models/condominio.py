from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Condominio(Base):
    __tablename__ = "condominios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
