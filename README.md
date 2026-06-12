# Testes Automatizados - ServeRest Usuários
 
Projeto de automação de testes para o endpoint de **Usuários** da API ServeRest, utilizando **Python**, **Requests** e **Pytest**.
 
API utilizada:
 
```text
https://compassuol.serverest.dev
```
 
Endpoint testado:
 
```text
/usuarios
```
 
---
 
## Tecnologias utilizadas
 
* Python
* Pytest
* Requests
* Faker
---
 
## Estrutura do projeto
 
```text
desafio-bootcamp/
│
├── tests/
│   ├── test_usuarios.py
│   └── test_usuarios_validacoes.py
│
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```
 
---
 
## Como instalar
 
Clone o repositório:
 
```bash
git clone <url-do-seu-repositorio>
```
 
Acesse a pasta do projeto:
 
```bash
cd desafio-bootcamp
```
 
Crie o ambiente virtual:
 
```bash
python -m venv .venv
```
 
Ative o ambiente virtual no Windows:
 
```bash
.venv\Scripts\activate
```
 
Instale as dependências:
 
```bash
pip install -r requirements.txt
```
 
---
 
## Como executar os testes
 
Executar todos os testes:
 
```bash
pytest
```
 
Executar com mais detalhes:
 
```bash
pytest -v
```
 
ou:
 
```bash
pytest -vv
```
 
Executar apenas o arquivo de testes principal:
 
```bash
pytest tests/test_usuarios.py
```
 
Executar testes pelo marcador `usuarios`:
 
```bash
pytest -m usuarios
```
 
Executar um teste específico:
 
```bash
pytest tests/test_usuarios.py::test_listar_usuarios_retorna_200_e_lista -vv
```
 
Executar testes filtrando pelo nome:
 
```bash
pytest -k "cadastrar" -vv
```
 
Exibir prints durante a execução:
 
```bash
pytest -s
```
 
---
 
## Cenários mínimos solicitados
 
| Cenário mínimo                        | Teste implementado                                               | Método HTTP | Endpoint         |
| -------------------------------------- | ----------------------------------------------------------------- | ----------- | ---------------- |
| Listar usuários                        | `test_listar_usuarios_retorna_200_e_lista`                         | GET         | `/usuarios`      |
| Cadastrar usuário válido               | `test_cadastrar_usuario_valido_retorna_201`                        | POST        | `/usuarios`      |
| Cadastrar usuário com email duplicado  | `test_cadastrar_usuario_com_email_duplicado_retorna_400`           | POST        | `/usuarios`      |
| Cadastrar usuário com campos faltando  | `test_cadastrar_usuario_com_campos_faltando_retorna_400`           | POST        | `/usuarios`      |
| Cadastrar usuário sem cada campo (parametrizado) | `test_cadastro_sem_campo_obrigatorio_retorna_erro_especifico` | POST        | `/usuarios`      |
| Buscar usuário por ID                  | `test_buscar_usuario_por_id_existente_retorna_200`                 | GET         | `/usuarios/{id}` |
| Atualizar usuário                      | `test_atualizar_usuario_existente_retorna_200`                     | PUT         | `/usuarios/{id}` |
| Excluir usuário                        | `test_excluir_usuario_existente_retorna_200`                       | DELETE      | `/usuarios/{id}` |
 
---
 
## Cenários adicionais
 
| Cenário adicional                                  | Teste implementado                                                       | Método HTTP | Endpoint         |
| ---------------------------------------------------- | --------------------------------------------------------------------------- | ----------- | ---------------- |
| Listar usuários filtrando por email                  | `test_listar_usuarios_aceita_filtro_por_email`                               | GET         | `/usuarios`      |
| Buscar usuário com ID inexistente (formato válido)   | `test_buscar_usuario_por_id_inexistente_retorna_400`                         | GET         | `/usuarios/{id}` |
| Atualizar usuário com email de outro usuário         | `test_atualizar_usuario_com_email_de_outro_usuario_retorna_400`              | PUT         | `/usuarios/{id}` |
| Excluir usuário inexistente                          | `test_excluir_usuario_inexistente_retorna_200_com_mensagem_de_nao_encontrado` | DELETE      | `/usuarios/{id}` |
 
---
 
## Total de testes
 
Foram implementados **15 testes automatizados** para o endpoint `/usuarios`.
 
Os testes utilizam emails dinâmicos (gerados via Faker) para evitar conflitos e foram estruturados para serem independentes entre si, com criação e limpeza dos próprios dados quando necessário.