from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.condominio import Condominio
from app.schemas.condominio import CondominioCreate, CondominioUpdate


class CondominioService:
    def __init__(self, db: Session):
        self.db = db

    def get_condominios(self) -> List[Condominio]:
        return self.db.query(Condominio).all()

    def get_condominio_by_id(self, condominio_id: int) -> Optional[Condominio]:
        return self.db.query(Condominio).filter(Condominio.id == condominio_id).first()

    def create_condominio(self, condominio_data: CondominioCreate) -> Condominio:
        db_condominio = Condominio(**condominio_data.dict())
        self.db.add(db_condominio)
        self.db.commit()
        self.db.refresh(db_condominio)
        return db_condominio

    def delete_condominio(self, condominio_id: int) -> bool:
        condominio = self.get_condominio_by_id(condominio_id)
        if condominio:
            self.db.delete(condominio)
            self.db.commit()
            return True
        return False

    def update_condominio(
        self, condominio_id: int, condominio_data: CondominioUpdate
    ) -> Optional[Condominio]:
        condominio = self.get_condominio_by_id(condominio_id)
        if not condominio:
            return None

        for key, value in condominio_data.dict(exclude_unset=True).items():
            setattr(condominio, key, value)

        self.db.commit()
        self.db.refresh(condominio)
        return condominio
