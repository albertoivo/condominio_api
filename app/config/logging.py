import logging
import os
import sys
from datetime import datetime
from pathlib import Path


def setup_logging():
    # Cria o diretório logs se não existir
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Define o nível de log baseado na variável de ambiente
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    # Configura o formato do log
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Configura o logging
    logging.basicConfig(
        level=getattr(logging, log_level),
        format=log_format,
        handlers=[
            logging.FileHandler(
                f"logs/app_{datetime.now().strftime('%Y%m%d')}.log", encoding="utf-8"
            ),
            logging.StreamHandler(sys.stdout),
        ],
        # Evita logs duplicados
        force=True,
    )

    # Silencia logs muito verbosos de bibliotecas externas
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)
    logger.info("Sistema de logging configurado com sucesso")
    return logger
