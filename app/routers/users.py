from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import User, UserCreate, UserUpdate
from app.services.auth_service import AuthService
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=User, tags=["Users"], summary="Usuário Logado")
def logged_user(
    db: Session = Depends(get_db),
    current_user: dict = Depends(AuthService.get_current_user),
):
    """
    Dependency to get the currently logged-in user.
    """
    return current_user


@router.get("/", response_model=List[User], tags=["Users"], summary="Listar Usuários")
def get_users(
    db: Session = Depends(get_db),
    current_user: dict = Depends(AuthService.verify_admin),
):
    """
    Retorna a lista de todos os usuários cadastrados.

    Args:
        db (Session): Sessão do banco de dados injetada via dependency injection
        current_user (dict): Dados do usuário atual (injetado automaticamente)

    Returns:
        List[User]: Lista com todos os usuários encontrados no banco de dados

    Raises:
        HTTPException: Em caso de erro interno do servidor
    """
    user_service = UserService(db)
    return user_service.get_users()


@router.post(
    "/", response_model=User, status_code=201, tags=["Users"], summary="Criar Usuário"
)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Cria um novo usuário no sistema.

    Args:
        user_data (UserCreate): Dados do usuário a ser criado (nome, email, etc.)
        db (Session): Sessão do banco de dados injetada via dependency injection

    Returns:
        User: Dados do usuário criado, incluindo o ID gerado

    Raises:
        HTTPException: 400 - Se houver erro na validação dos dados ou
                            se o email já estiver em uso
    """
    user_service = UserService(db)
    try:
        return user_service.create_user(user_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{user_id}", response_model=User, tags=["Users"], summary="Buscar Usuário por ID"
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Busca um usuário específico pelo ID.

    Args:
        user_id (int): ID único do usuário
        db (Session): Sessão do banco de dados injetada via dependency injection

    Returns:
        User: Dados do usuário encontrado

    Raises:
        HTTPException: 404 - Se o usuário não for encontrado
    """
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Remove um usuário do sistema pelo ID.

    Args:
        user_id (int): ID único do usuário a ser removido
        db (Session): Sessão do banco de dados injetada via dependency injection

    Returns:
        dict: Mensagem de confirmação se o usuário foi removido com sucesso

    Raises:
        HTTPException: 404 - Se o usuário com o ID fornecido não for encontrado
    """
    user_service = UserService(db)
    if user_service.delete_user(user_id):
        return {"message": "Usuário removido com sucesso"}
    else:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")


@router.put(
    "/{user_id}", response_model=User, tags=["Users"], summary="Atualizar Usuário"
)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    """
    Atualiza os dados de um usuário existente.

    Args:
        user_id (int): ID único do usuário a ser atualizado
        user_data (UserUpdate): Dados atualizados do usuário
        db (Session): Sessão do banco de dados injetada via dependency injection

    Returns:
        User: Dados do usuário atualizado

    Raises:
        HTTPException: 404 - Se o usuário não for encontrado
                       400 - Se houver erro na validação dos dados
    """
    user_service = UserService(db)
    updated_user = user_service.update_user(user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return updated_user
