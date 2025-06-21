from slowapi import Limiter
from slowapi.util import get_remote_address


def get_identifier(request):
    """
    Função para identificar requests únicos.
    Para desenvolvimento, use uma função simples.
    """
    return get_remote_address(request)


limiter = Limiter(key_func=get_identifier)
