"""
Testes parametrizados adicionais para validação de cadastro de usuários,
cobrindo diferentes combinações de campos faltando.
"""
import pytest
import requests

pytestmark = pytest.mark.usuarios


@pytest.mark.parametrize(
    "campo_removido, mensagem_esperada",
    [
        ("nome", "nome é obrigatório"),
        ("email", "email é obrigatório"),
        ("password", "password é obrigatório"),
        ("administrador", "administrador é obrigatório"),
    ],
)
def test_cadastro_sem_campo_obrigatorio_retorna_erro_especifico(
    base_url, usuario_valido, campo_removido, mensagem_esperada
):
    """
    Para cada campo obrigatório ausente, a API deve retornar 400
    com a mensagem de validação específica daquele campo.
    """
    payload = dict(usuario_valido)
    del payload[campo_removido]

    response = requests.post(f"{base_url}/usuarios", json=payload)

    assert response.status_code == 400
    body = response.json()
    assert body[campo_removido] == mensagem_esperada