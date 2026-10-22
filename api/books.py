"""Operações da API de livros do DemoQA."""

import requests

BASE_URL_BOOKS = "https://demoqa.com/BookStore/v1/"

class BookStoreClient:
    """Cliente para consultar livros e associá-los a um usuário.

    `session` permite compartilhar a conexão. `books_route` é a URL
    usada para listar e adicionar livros.
    """

    def __init__(self, session: requests.Session | None = None) -> None:
        self.session = session or requests.Session()
        
        self.books_route = f"{BASE_URL_BOOKS}Books"

    def list_books(self) -> requests.Response:
        """Busca o catálogo de livros disponíveis."""
        return self.session.get(
            self.books_route,
            timeout=15,
        )

    def rent_books(self, user_id: str, books_isbn: list[str], token: str) -> requests.Response:
        """Adiciona os livros identificados por `books_isbn` ao usuário.

        Recebe uma lista de códigos ISBN e monta o corpo exigido pela API.
        `user_id` identifica o usuário e `token` autoriza a operação.
        """
        return self.session.post(
            self.books_route,
            headers={"Authorization": f"Bearer {token}"},
            json={
                "userId": user_id,
                "collectionOfIsbns": [{"isbn": isbn} for isbn in books_isbn],
            },
            timeout=15,
        )
