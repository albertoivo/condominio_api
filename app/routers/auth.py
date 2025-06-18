from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import LoginRequest, Token
from app.services.auth_service import AuthService

router = APIRouter(tags=["Auth"])


@router.post("/login", response_model=Token, summary="Realizar login")
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    token = service.authenticate_user(credentials.email, credentials.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas"
        )
    return {"access_token": token, "token_type": "bearer"}
