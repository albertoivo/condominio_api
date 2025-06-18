from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.auth_service import AuthService


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.auth_service = AuthService(db)

    def get_users(self) -> List[User]:
        return self.db.query(User).all()

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def create_user(self, user_data: UserCreate) -> User:
        hashed_password = self.auth_service.get_password_hash(user_data.password)
        db_user = User(
            nome=user_data.name,
            email=user_data.email,
            hashed_password=hashed_password,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False

    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        user = self.get_user_by_id(user_id)
        if not user:
            return None

        update_data = user_data.dict(exclude_unset=True)
        if "name" in update_data:
            user.nome = update_data["name"]
        if "email" in update_data:
            user.email = update_data["email"]
        if "password" in update_data:
            user.hashed_password = self.auth_service.get_password_hash(
                update_data["password"]
            )

        self.db.commit()
        self.db.refresh(user)
        return user
