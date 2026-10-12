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

    git clone https://github.com/henriquealc/tarefas-api.git
    cd tarefas-api

Crie e ative o ambiente virtual.

No Windows (PowerShell):

    python -m venv .venv
    ./.venv/Scripts/Activate.ps1

Se o PowerShell informar que a execução de scripts está desabilitada, rode uma vez o comando abaixo e repita a ativação:

    Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

No Linux ou macOS:

    python -m venv .venv
    source .venv/bin/activate

Com o ambiente ativo (o nome `(.venv)` aparece no início da linha), instale as dependências:

    python -m pip install -r requirements.txt

Observação: `python -m pip` equivale ao comando `pip` e evita o bloqueio de executáveis que ocorre em alguns computadores Windows com Controle de Aplicativo ativado.

## Configuração

O projeto usa uma chave secreta para assinar os tokens JWT. Ela fica em um arquivo `.env`, que não é versionado (o arquivo `.env.example` mostra o formato esperado).

Crie o arquivo `.env` com uma chave aleatória gerada na hora:

    python -c "import secrets; open('.env','w').write('SECRET_KEY=' + secrets.token_hex(32))"

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

Listar as tarefas ainda não concluídas.

No Windows (PowerShell):

    curl.exe "http://127.0.0.1:8000/tarefas?concluida=false"

No Linux ou macOS:

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