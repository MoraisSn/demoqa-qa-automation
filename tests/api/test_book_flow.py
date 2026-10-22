"""Fluxo completo: criar usuário, autenticar e associar dois livros."""

import requests
import secrets
import sys
from pathlib import Path
from uuid import uuid4

# Ao depurar este arquivo diretamente, inclui a raiz do projeto nos imports.
project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from api.account_client import AccountClient
from api.books import BookStoreClient


def test_user_can_add_two_books():
    username = f"qa_{uuid4().hex[:12]}"
    password = f"Aa1@{secrets.token_hex(12)}"

    with requests.Session() as session:
        account = AccountClient(session)
        bookstore = BookStoreClient(session)

        print("[1/6] Criando usuario...", flush=True)
        created = account.create_user(username, password)
        assert created.status_code == 201, created.text

        created_user = created.json()
        assert created_user["username"] == username

        user_id = created_user["userID"]
        assert user_id
        print(f"      OK: {username} ({user_id})", flush=True)

        print("[2/6] Gerando token...", flush=True)
        generated = account.generate_token(username, password)
        assert generated.status_code == 200, generated.text

        token = generated.json()["token"]
        assert token
        print("      OK: token recebido", flush=True)

        print("[3/6] Confirmando autorizacao...", flush=True)
        authorized = account.user_is_authorized(username, password)
        assert authorized.status_code == 200, authorized.text
        assert authorized.json() is True
        print("      OK: usuario autorizado", flush=True)

        print("[4/6] Listando livros...", flush=True)
        catalog_response = bookstore.list_books()
        assert catalog_response.status_code == 200, catalog_response.text
        available_isbns = [book["isbn"] for book in catalog_response.json()["books"]]
        selected_isbns = list(dict.fromkeys(available_isbns))[:2]
        assert len(selected_isbns) == 2, "O catálogo precisa conter dois livros distintos"
        print(f"      OK: ISBNs escolhidos {selected_isbns}", flush=True)

        print("[5/6] Adicionando os dois livros...", flush=True)
        added = bookstore.rent_books(user_id, selected_isbns, token)
        assert added.status_code == 201, added.text
        print("      OK: livros adicionados", flush=True)

        print("[6/6] Consultando usuario e conferindo os livros...", flush=True)
        user_response = account.get_user(user_id, token)
        assert user_response.status_code == 200, user_response.text
        user = user_response.json()
        assert user["userId"] == user_id
        assert user["username"] == username
        returned_isbns = [book["isbn"] for book in user["books"]]
        assert len(returned_isbns) == 2
        assert set(returned_isbns) == set(selected_isbns)
        print("      OK: os dois ISBNs constam na conta", flush=True)


if __name__ == "__main__":
    test_user_can_add_two_books()
    print("Fluxo de API: sucesso.")

