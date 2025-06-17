import os
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.routers import users, condominios
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI(
    title="Condominio API",
    description="API para gerenciamento de condomínio",
    version="1.0.0",
)

# Incluir routers
app.include_router(users.router)
app.include_router(condominios.router)


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
