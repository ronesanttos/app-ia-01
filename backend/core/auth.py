import os

from rest_framework.authentication import BaseAuthentication  # type: ignore
from rest_framework.exceptions import AuthenticationFailed  # type: ignore


class APIKeyAuthentication(BaseAuthentication):
    """
    Autenticação simples via header.
    - Envie: X-API-KEY: <sua-chave>
    - Configure: API_KEY no ambiente/.env
    """

    header_name = "HTTP_X_API_KEY"

    def authenticate(self, request):
        expected = os.environ.get("API_KEY")
        # Se não estiver configurado, não bloqueia (útil para dev).
        if not expected:
            return None

        provided = request.META.get(self.header_name)
        if not provided:
            raise AuthenticationFailed("API key ausente (header X-API-KEY).")

        if provided != expected:
            raise AuthenticationFailed("API key inválida.")

        # Não usamos usuário aqui; apenas marca como autenticado.
        return (None, provided)

