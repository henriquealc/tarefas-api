import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app

engine_teste = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SessionTeste = sessionmaker(bind=engine_teste, autoflush=False, autocommit=False)


def get_db_teste():
    db = SessionTeste()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client():
    Base.metadata.create_all(bind=engine_teste)
    app.dependency_overrides[get_db] = get_db_teste
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine_teste)


@pytest.fixture()
def auth(client):
    client.post("/auth/registro", json={"username": "aluno", "senha": "senha123"})
    resposta = client.post("/auth/login", data={"username": "aluno", "password": "senha123"})
    token = resposta.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_raiz_responde_200(client):
    assert client.get("/").status_code == 200


def test_registro_cria_usuario_sem_expor_senha(client):
    r = client.post("/auth/registro", json={"username": "novo", "senha": "senha123"})
    assert r.status_code == 201
    assert "senha" not in r.json()
    assert "senha_hash" not in r.json()


def test_registro_duplicado_retorna_409(client, auth):
    r = client.post("/auth/registro", json={"username": "aluno", "senha": "senha123"})
    assert r.status_code == 409


def test_registro_com_senha_curta_retorna_422(client):
    r = client.post("/auth/registro", json={"username": "novo", "senha": "123"})
    assert r.status_code == 422


def test_login_com_senha_errada_retorna_401(client, auth):
    r = client.post("/auth/login", data={"username": "aluno", "password": "errada"})
    assert r.status_code == 401


def test_criar_categoria_sem_token_retorna_401(client):
    r = client.post("/categorias", json={"nome": "Faculdade"})
    assert r.status_code == 401


def test_criar_e_listar_categoria(client, auth):
    r = client.post("/categorias", json={"nome": "Faculdade"}, headers=auth)
    assert r.status_code == 201
    assert r.json()["nome"] == "Faculdade"
    lista = client.get("/categorias")
    assert lista.status_code == 200
    assert len(lista.json()) == 1


def test_categoria_duplicada_retorna_409(client, auth):
    client.post("/categorias", json={"nome": "Faculdade"}, headers=auth)
    r = client.post("/categorias", json={"nome": "Faculdade"}, headers=auth)
    assert r.status_code == 409


def test_categoria_com_nome_vazio_retorna_422(client, auth):
    r = client.post("/categorias", json={"nome": ""}, headers=auth)
    assert r.status_code == 422


def test_tarefa_com_categoria_inexistente_retorna_400(client, auth):
    r = client.post("/tarefas", json={"titulo": "Teste", "categoria_id": 999}, headers=auth)
    assert r.status_code == 400


def test_crud_completo_de_tarefa(client, auth):
    categoria_id = client.post("/categorias", json={"nome": "Faculdade"}, headers=auth).json()["id"]

    criada = client.post(
        "/tarefas",
        json={"titulo": "Entregar trabalho", "categoria_id": categoria_id},
        headers=auth,
    )
    assert criada.status_code == 201
    tarefa_id = criada.json()["id"]

    assert client.get(f"/tarefas/{tarefa_id}").status_code == 200

    atualizada = client.patch(f"/tarefas/{tarefa_id}", json={"concluida": True}, headers=auth)
    assert atualizada.status_code == 200
    assert atualizada.json()["concluida"] is True
    assert atualizada.json()["titulo"] == "Entregar trabalho"

    concluidas = client.get("/tarefas", params={"concluida": True})
    assert len(concluidas.json()) == 1

    assert client.delete(f"/tarefas/{tarefa_id}", headers=auth).status_code == 204
    assert client.get(f"/tarefas/{tarefa_id}").status_code == 404


def test_tarefa_inexistente_retorna_404(client):
    assert client.get("/tarefas/999").status_code == 404


def test_atualizar_sem_token_retorna_401(client):
    r = client.patch("/tarefas/1", json={"concluida": True})
    assert r.status_code == 401


def test_cors_origem_permitida(client):
    r = client.options(
        "/tarefas",
        headers={"Origin": "http://localhost:3000", "Access-Control-Request-Method": "POST"},
    )
    assert r.status_code == 200
    assert r.headers["access-control-allow-origin"] == "http://localhost:3000"


def test_cors_origem_bloqueada(client):
    r = client.options(
        "/tarefas",
        headers={"Origin": "http://site-malicioso.com", "Access-Control-Request-Method": "POST"},
    )
    assert r.status_code == 400
    assert "access-control-allow-origin" not in r.headers