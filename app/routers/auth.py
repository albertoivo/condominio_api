from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import LoginRequest, Token
from app.schemas.user import User
from app.services.auth_service import AuthService, get_current_user

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


@router.post("/logout", summary="Realizar logout do usuário")
def logout(current_user: User = Depends(get_current_user)):
    """
    Realiza o logout do usuário.

    Em uma implementação stateless com JWT, o logout é primariamente uma
    operação do lado do cliente, que consiste em descartar o token.

    Este endpoint serve como um ponto de finalização formal da sessão no lado do servidor,
    embora não invalide o token diretamente. Para invalidar o token, seria
    necessário implementar uma blocklist.
    """
    return {"message": "Logout realizado com sucesso."}
