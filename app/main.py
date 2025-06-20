import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.routers import auth, users

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI(
    title="CRUD OAuth API",
    description="API para templates de CRUD com autenticação OAuth2",
    version="1.0.0",
)

# Incluir routers
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/", tags=["Root"])
def read_root():
    """
    Rota de boas-vindas da API.

    Returns:
        dict: Mensagem de confirmação que a API está funcionando
    """
    return {"message": "API rodando com sucesso!"}


@app.get("/health", tags=["Health Check"])
def health_check(db: Session = Depends(get_db)):
    """
    Verifica o status de saúde da aplicação e conexão com o banco de dados.

    Args:
        db (Session): Sessão do banco de dados injetada via dependency injection

    Returns:
        dict: Status da aplicação - "healthy" se tudo estiver funcionando,
              "unhealthy" com detalhes do erro se houver problemas

    Raises:
        Não levanta exceções, retorna status de erro no JSON
    """
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "health": True}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
