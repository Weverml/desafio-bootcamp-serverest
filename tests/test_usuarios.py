"""
Testes automatizados para o endpoint /usuarios da API ServeRest.

Cobertura:
- Listar usuários
- Cadastrar usuário (válido, email duplicado, campos faltando)
- Buscar usuário por ID (existente e inexistente)
- Atualizar usuário
- Excluir usuário (existente e inexistente)
"""
import pytest
import requests

pytestmark = pytest.mark.usuarios


# ---------------------------------------------------------------------------
# LISTAR USUÁRIOS
# ---------------------------------------------------------------------------

def test_listar_usuarios_retorna_200_e_lista(base_url):
    """GET /usuarios deve retornar status 200 e uma estrutura com 'usuarios' (lista)."""
    response = requests.get(f"{base_url}/usuarios")

    assert response.status_code == 200
    body = response.json()
    assert "usuarios" in body
    assert isinstance(body["usuarios"], list)
    assert "quantidade" in body


def test_listar_usuarios_aceita_filtro_por_email(base_url, usuario_cadastrado):
    """
    GET /usuarios?email=... deve retornar apenas o usuário com o email informado,
    validando que o filtro de busca funciona.
    """
    email = usuario_cadastrado["email"]

    response = requests.get(f"{base_url}/usuarios", params={"email": email})

    assert response.status_code == 200
    body = response.json()
    assert body["quantidade"] == 1
    assert body["usuarios"][0]["email"] == email


# ---------------------------------------------------------------------------
# CADASTRAR USUÁRIO
# ---------------------------------------------------------------------------

def test_cadastrar_usuario_valido_retorna_201(base_url, usuario_valido):
    """POST /usuarios com payload válido deve criar o usuário e retornar 201 + _id."""
    response = requests.post(f"{base_url}/usuarios", json=usuario_valido)

    assert response.status_code == 201
    body = response.json()
    assert body["message"] == "Cadastro realizado com sucesso"
    assert "_id" in body
    assert isinstance(body["_id"], str) and len(body["_id"]) > 0

    # limpeza para não deixar dado residual
    requests.delete(f"{base_url}/usuarios/{body['_id']}")


def test_cadastrar_usuario_com_email_duplicado_retorna_400(base_url, usuario_cadastrado, usuario_valido):
    """
    POST /usuarios com um email que já existe deve retornar 400
    e mensagem indicando que o email já está em uso.
    """
    payload_duplicado = {**usuario_valido, "email": usuario_cadastrado["email"]}

    response = requests.post(f"{base_url}/usuarios", json=payload_duplicado)

    assert response.status_code == 400
    body = response.json()
    assert body["message"] == "Este email já está sendo usado"


def test_cadastrar_usuario_com_campos_faltando_retorna_400(base_url):
    """
    POST /usuarios sem os campos obrigatórios deve retornar 400
    com as mensagens de validação correspondentes.
    """
    payload_incompleto = {"nome": "Usuário Sem Dados Obrigatórios"}

    response = requests.post(f"{base_url}/usuarios", json=payload_incompleto)

    assert response.status_code == 400
    body = response.json()
    assert body["email"] == "email é obrigatório"
    assert body["password"] == "password é obrigatório"
    assert body["administrador"] == "administrador é obrigatório"


# ---------------------------------------------------------------------------
# BUSCAR USUÁRIO POR ID
# ---------------------------------------------------------------------------

def test_buscar_usuario_por_id_existente_retorna_200(base_url, usuario_cadastrado):
    """GET /usuarios/{_id} de um usuário existente deve retornar 200 com os dados corretos."""
    user_id = usuario_cadastrado["_id"]

    response = requests.get(f"{base_url}/usuarios/{user_id}")

    assert response.status_code == 200
    body = response.json()
    assert body["_id"] == user_id
    assert body["email"] == usuario_cadastrado["email"]
    assert body["nome"] == usuario_cadastrado["nome"]


def test_buscar_usuario_por_id_inexistente_retorna_400(base_url):
    """
    GET /usuarios/{_id} com um ID de formato válido (16 caracteres) mas
    que não existe deve retornar 400 indicando 'Usuário não encontrado'.
    """
    id_invalido = "ABCDEF0123456789"[:16]

    response = requests.get(f"{base_url}/usuarios/{id_invalido}")

    assert response.status_code == 400
    body = response.json()
    assert body["message"] == "Usuário não encontrado"


# ---------------------------------------------------------------------------
# ATUALIZAR USUÁRIO
# ---------------------------------------------------------------------------

def test_atualizar_usuario_existente_retorna_200(base_url, usuario_cadastrado):
    """
    PUT /usuarios/{_id} com payload válido deve atualizar os dados do usuário
    e retornar 200 com mensagem de sucesso.
    """
    user_id = usuario_cadastrado["_id"]
    payload_atualizado = {
        "nome": "Nome Atualizado pelo Teste",
        "email": usuario_cadastrado["email"],
        "password": usuario_cadastrado["password"],
        "administrador": "true",
    }

    response = requests.put(f"{base_url}/usuarios/{user_id}", json=payload_atualizado)

    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Registro alterado com sucesso"

    # valida que o nome foi realmente persistido
    verificacao = requests.get(f"{base_url}/usuarios/{user_id}")
    assert verificacao.json()["nome"] == "Nome Atualizado pelo Teste"


def test_atualizar_usuario_com_email_de_outro_usuario_retorna_400(base_url, usuario_cadastrado):
    """
    PUT /usuarios/{_id} usando um email que já pertence a outro usuário
    deve retornar 400, indicando conflito de email.
    """
    from faker import Faker
    fake = Faker("pt_BR")

    segundo_payload = {
        "nome": fake.name(),
        "email": f"{fake.user_name()}_{fake.unique.random_number(digits=6)}@teste.com",
        "password": "Senha123!",
        "administrador": "true",
    }

    # cria um segundo usuário só para este teste
    resp_segundo = requests.post(f"{base_url}/usuarios", json=segundo_payload)
    assert resp_segundo.status_code == 201
    segundo_id = resp_segundo.json()["_id"]

    try:
        payload = {**segundo_payload, "email": usuario_cadastrado["email"]}

        response = requests.put(f"{base_url}/usuarios/{segundo_id}", json=payload)

        assert response.status_code == 400
        body = response.json()
        assert body["message"] == "Este email já está sendo usado"
    finally:
        requests.delete(f"{base_url}/usuarios/{segundo_id}")

# ---------------------------------------------------------------------------
# EXCLUIR USUÁRIO
# ---------------------------------------------------------------------------

def test_excluir_usuario_existente_retorna_200(base_url, usuario_valido):
    """
    DELETE /usuarios/{_id} de um usuário existente deve retornar 200
    com mensagem de sucesso, e o usuário não deve mais existir após isso.
    """
    cadastro = requests.post(f"{base_url}/usuarios", json=usuario_valido)
    user_id = cadastro.json()["_id"]

    response = requests.delete(f"{base_url}/usuarios/{user_id}")

    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Registro excluído com sucesso"

    # confirma que o usuário não é mais encontrado
    verificacao = requests.get(f"{base_url}/usuarios/{user_id}")
    assert verificacao.status_code == 400


def test_excluir_usuario_inexistente_retorna_200_com_mensagem_de_nao_encontrado(base_url):
    """
    DELETE /usuarios/{_id} com um ID inexistente retorna 200,
    mas com mensagem indicando que nenhum registro foi excluído.
    """
    id_invalido = "idQueNaoExiste123456"

    response = requests.delete(f"{base_url}/usuarios/{id_invalido}")

    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Nenhum registro excluído"