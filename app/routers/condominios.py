from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.condominio_service import CondominioService
from app.schemas.condominio import Condominio, CondominioCreate
from typing import List

router = APIRouter(
    prefix="/condominios",
    tags=["Condominios"],
    responses={
        404: {"description": "Não encontrado"},
        500: {"description": "Erro interno do servidor"},
        400: {"description": "Erro de validação"},
        422: {"description": "Erro de validação de dados"},
    },
)


@router.get(
    "/",
    response_model=List[Condominio],
    tags=["Condominios"],
    summary="Listar Condomínios",
)
def get_condominios(db: Session = Depends(get_db)):
    """
    Retorna a lista de todos os condomínios cadastrados.

    Args:
        db (Session): Sessão do banco de dados injetada via dependency injection

    Returns:
        List: Lista com todos os condomínios encontrados no banco de dados
    """
    condominio_service = CondominioService(db)
    return condominio_service.get_condominios()


@router.post(
    "/",
    status_code=201,
    response_model=Condominio,
    tags=["Condominios"],
    summary="Criar Condomínio",
)
def create_condominio(condominio_data: CondominioCreate, db: Session = Depends(get_db)):
    """
    Cria um novo condomínio no sistema.

    Args:
        db (Session): Sessão do banco de dados injetada via dependency injection

    Returns:
        dict: Dados do condomínio criado
    """
    condominio_service = CondominioService(db)
    try:
        return condominio_service.create_condominio(condominio_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{condominio_id}",
    response_model=Condominio,
    tags=["Condominios"],
    summary="Buscar Condomínio por ID",
)
def get_condominio(condominio_id: int, db: Session = Depends(get_db)):
    """
    Busca um condomínio específico pelo ID.

    Args:
        condominio_id (int): ID único do condomínio
        db (Session): Sessão do banco de dados injetada via dependency injection

    Returns:
        dict: Dados do condomínio encontrado
    """
    condominio_service = CondominioService(db)
    condominio = condominio_service.get_condominio_by_id(condominio_id)
    if not condominio:
        raise HTTPException(status_code=404, detail="Condomínio não encontrado")
    return condominio


@router.delete(
    "/{condominio_id}",
    status_code=204,
    tags=["Condominios"],
    summary="Remover Condomínio",
)
def delete_condominio(condominio_id: int, db: Session = Depends(get_db)):
    """
    Remove um condomínio específico pelo ID.

    Args:
        condominio_id (int): ID único do condomínio a ser deletado
        db (Session): Sessão do banco de dados injetada via dependency injection

    Returns:
        None: Se o condomínio for removido com sucesso
    """
    condominio_service = CondominioService(db)
    if not condominio_service.delete_condominio(condominio_id):
        raise HTTPException(status_code=404, detail="Condomínio não encontrado")
    return {"detail": "Condomínio removido com sucesso"}


@router.put(
    "/{condominio_id}",
    response_model=Condominio,
    tags=["Condominios"],
    summary="Atualizar Condomínio",
)
def update_condominio(
    condominio_id: int, condominio_data: CondominioCreate, db: Session = Depends(get_db)
):
    """
    Atualiza os dados de um condomínio existente.

    Args:
        condominio_id (int): ID único do condomínio a ser atualizado
        condominio_data (CondominioCreate): Dados atualizados do condomínio
        db (Session): Sessão do banco de dados injetada via dependency injection

    Returns:
        dict: Dados do condomínio atualizado
    """
    condominio_service = CondominioService(db)
    condominio = condominio_service.get_condominio_by_id(condominio_id)
    if not condominio:
        raise HTTPException(status_code=404, detail="Condomínio não encontrado")

    updated_condominio = condominio_service.update_condominio(
        condominio_id, condominio_data
    )
    return updated_condominio
