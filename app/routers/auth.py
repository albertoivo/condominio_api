from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import LoginRequest, Token
from app.schemas.user import User
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


@router.post("/logout", summary="Realizar logout do usuário")
def logout(current_user: User = Depends(AuthService.get_current_user)):
    """
    Realiza o logout do usuário.

    Em uma implementação stateless com JWT, o logout é primariamente uma
    operação do lado do cliente, que consiste em descartar o token.

    Este endpoint serve como um ponto de finalização formal da sessão no lado do
    servidor, embora não invalide o token diretamente. Para invalidar o token, seria
    necessário implementar uma blocklist.
    """
    return {"detail": "Logout realizado com sucesso."}


@router.get("/me", response_model=User, summary="Obter informações do usuário autenticado")
def get_current_user(current_user: User = Depends(AuthService.get_current_user)):
    """
    Obtém as informações do usuário autenticado.

    Este endpoint retorna os detalhes do usuário que está atualmente autenticado,
    utilizando o token JWT fornecido no cabeçalho da requisição.
    """
    return current_user
