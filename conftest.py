"""
Fixtures compartilhadas para os testes da API ServeRest.
"""
import pytest
import requests
from faker import Faker

BASE_URL = "https://compassuol.serverest.dev"

fake = Faker("pt_BR")


@pytest.fixture(scope="session")
def base_url():
    """URL base da API sob teste."""
    return BASE_URL


@pytest.fixture
def usuario_valido():
    """
    Gera um payload de usuário válido com email dinâmico
    (evita conflito de 'email já cadastrado' entre execuções/testes).
    """
    return {
        "nome": fake.name(),
        "email": f"{fake.user_name()}_{fake.unique.random_number(digits=6)}@teste.com",
        "password": "Senha123!",
        "administrador": "true",
    }


@pytest.fixture
def usuario_cadastrado(base_url, usuario_valido):
    """
    Cadastra um usuário via API e retorna seus dados (incluindo o _id).
    Faz a limpeza (delete) ao final do teste, garantindo independência
    entre os testes.
    """
    resp = requests.post(f"{base_url}/usuarios", json=usuario_valido)
    assert resp.status_code == 201, (
        f"Falha ao criar usuário de apoio para o teste: {resp.text}"
    )
    dados = resp.json()
    usuario = {**usuario_valido, "_id": dados["_id"]}

    yield usuario

    # Teardown: remove o usuário criado, se ainda existir
    requests.delete(f"{base_url}/usuarios/{usuario['_id']}")