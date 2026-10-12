# API de Tarefas e Categorias

API REST desenvolvida para a Atividade Prática de Arquitetura e Desenvolvimento de APIs (Uninter).

## Descrição e problema resolvido

A API permite organizar tarefas por categoria (por exemplo, a categoria "Faculdade" com as tarefas "Entregar trabalho" e "Estudar para a prova"). É possível cadastrar categorias, criar, consultar, filtrar, atualizar e excluir tarefas. As operações que alteram dados exigem autenticação por token JWT, e as consultas são abertas.

## Tecnologias utilizadas

- Python 3.12
- FastAPI (framework web, validação e documentação Swagger automática)
- SQLAlchemy 2.0 (ORM)
- SQLite (banco de dados em arquivo)
- PyJWT (tokens JWT) e PBKDF2 da biblioteca padrão do Python (hash de senhas)
- Pytest (testes automatizados)

## Pré-requisitos

- Python 3.10 ou superior
- Git

## Instalação

Clone o repositório e entre na pasta do projeto:

    git clone LINK-DO-REPOSITORIO
    cd tarefas-api

Crie e ative o ambiente virtual.

No Windows (PowerShell):

    python -m venv .venv
    .venv\Scripts\Activate.ps1

No Linux ou macOS:

    python -m venv .venv
    source .venv/bin/activate

Instale as dependências:

    pip install -r requirements.txt

## Configuração

O projeto usa uma chave secreta para assinar os tokens JWT. Ela fica em um arquivo `.env`, que não é versionado.

Copie o arquivo de exemplo:

    copy .env.example .env

(no Linux ou macOS, use `cp .env.example .env`).

Gere uma chave aleatória com o comando abaixo e cole o resultado no `.env`, no lugar do texto de exemplo, ficando `SECRET_KEY=` seguido da chave:

    python -c "import secrets; print(secrets.token_hex(32))"

Banco de dados: não é preciso instalar nem configurar nada. As tabelas (categorias, tarefas e usuarios) são criadas automaticamente no arquivo `tarefas.db` na primeira execução, a partir dos modelos definidos em `models.py`.

## Executando a API

    fastapi dev main.py

A API fica disponível em http://127.0.0.1:8000.

## Documentação (Swagger)

Com a API rodando, acesse http://127.0.0.1:8000/docs para ver e testar todos os endpoints.

## Resumo dos endpoints

| Método | Rota | Descrição | Autenticação | Respostas |
|---|---|---|---|---|
| POST | /auth/registro | Cadastra um usuário | Não | 201, 409, 422 |
| POST | /auth/login | Faz login e devolve o token | Não | 200, 401 |
| GET | /categorias | Lista as categorias | Não | 200 |
| POST | /categorias | Cria uma categoria | Sim | 201, 401, 409, 422 |
| GET | /tarefas | Lista tarefas (filtros opcionais: concluida e categoria_id) | Não | 200 |
| GET | /tarefas/{id} | Consulta uma tarefa | Não | 200, 404 |
| POST | /tarefas | Cria uma tarefa | Sim | 201, 400, 401, 422 |
| PATCH | /tarefas/{id} | Atualiza campos de uma tarefa | Sim | 200, 400, 401, 404, 422 |
| DELETE | /tarefas/{id} | Exclui uma tarefa | Sim | 204, 401, 404 |

## Exemplo de requisição

Listar as tarefas ainda não concluídas:

    curl "http://127.0.0.1:8000/tarefas?concluida=false"

## Autenticação (como testar sem expor credenciais)

Cada pessoa cria o próprio usuário, então não há senha fixa no repositório.

1. Cadastre um usuário em POST /auth/registro, com o corpo JSON: {"username": "seu_usuario", "senha": "sua_senha"} (usuário de 3 a 50 caracteres e senha de 6 a 128).
2. No Swagger, clique em Authorize (canto superior direito), informe o usuário e a senha e confirme. O Swagger passa a enviar o token nas requisições.
3. Os endpoints com cadeado (POST, PATCH e DELETE) passam a funcionar. Sem o token, eles respondem 401.

O token expira em 30 minutos. Depois disso, basta autorizar de novo.

## Testes automatizados

Os testes usam um banco temporário em memória e não alteram o `tarefas.db`:

    python -m pytest -v

## Estrutura do projeto

    main.py            aplicação, CORS e registro dos routers
    database.py        conexão com o banco e sessões
    models.py          modelos do ORM (tabelas)
    schemas.py         schemas de entrada e saída (validação)
    security.py        hash de senha e criação do token JWT
    dependencias.py    verificação do token nos endpoints protegidos
    routers/           endpoints (auth, categorias, tarefas)
    tests/             testes automatizados
    requirements.txt   dependências
    .env.example       modelo das variáveis de ambiente

## Autor

ALUIZIO HENRIQUE - RU: 5209545