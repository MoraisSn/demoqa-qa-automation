"""Operações da API de contas do DemoQA."""

import requests

BASE_URL_ACCOUNT = "https://demoqa.com/Account/v1/"

class AccountClient:
    """Cliente para criar usuários, gerar tokens e consultar contas.

    `session` permite compartilhar a mesma conexão entre as chamadas.
    As URLs ficam nos atributos `user_route`, `generate_token_route`
    e `authorized_route`.
    """

    def __init__(self, session: requests.Session | None = None) -> None:
        self.session = session or requests.Session()

        self.user_route = f"{BASE_URL_ACCOUNT}User"
        self.generate_token_route = f"{BASE_URL_ACCOUNT}GenerateToken"
        self.authorized_route = f"{BASE_URL_ACCOUNT}Authorized"

    def create_user(self, username: str, password: str) -> requests.Response:
        """Cria um usuário; a resposta da API contém o ID gerado."""
        return self.session.post(
            self.user_route,
            json={"userName": username, "password": password},
            timeout=15
        )
    
    def generate_token(self, username: str, password: str) -> requests.Response:
        """Gera um token usando as credenciais do usuário."""
        return self.session.post(
            self.generate_token_route,
            json={"userName": username, "password": password},
            timeout=15
        )
    def user_is_authorized(self, username: str, password: str) -> requests.Response:
        """Verifica se o usuário está autorizado."""
        return self.session.post(
            self.authorized_route,
            json={"userName": username, "password": password},
            timeout=15
        )

    def get_user(self, user_id: str, token: str) -> requests.Response:
        """Busca o usuário pelo ID; o token autoriza a consulta."""
        return self.session.get(
            f"{self.user_route}/{user_id}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=15,
        )

