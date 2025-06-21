from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address


def get_identifier(request):
    """
    Função para identificar requests únicos.
    Para desenvolvimento, use uma função simples.
    """
    return get_remote_address(request)


limiter = Limiter(key_func=get_identifier)

# Exporta o handler para ser usado no main.py
__all__ = ["limiter", "_rate_limit_exceeded_handler"]
